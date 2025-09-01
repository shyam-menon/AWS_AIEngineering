#!/bin/bash
"""
AWS Bedrock Knowledge Base Setup Script

This script creates an ephemeral AWS infrastructure for the RAG demo:
1. S3 bucket for document storage
2. OpenSearch Serverless collection for vector storage
3. IAM role for Bedrock Knowledge Base
4. Knowledge Base with data source
5. Document ingestion

This script is designed for educational use and creates resources that
will incur AWS charges. Use teardown-kb.sh to clean up when finished.

Author: AWS AI Engineering Course
Chapter: 4 - Storage for Retrieval
"""

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
REGION=${AWS_REGION:-us-east-1}
BUCKET_SUFFIX=$(date +%s)
BUCKET_NAME="rag-demo-kb-${BUCKET_SUFFIX}"
COLLECTION_NAME="rag-demo-collection-${BUCKET_SUFFIX}"
ROLE_NAME="rag-demo-kb-role-${BUCKET_SUFFIX}"
KB_NAME="rag-demo-kb-${BUCKET_SUFFIX}"
DATA_SOURCE_NAME="s3-docs"

echo -e "${BLUE}🚀 AWS Bedrock Knowledge Base Setup${NC}"
echo "=================================="
echo -e "Region: ${GREEN}${REGION}${NC}"
echo -e "Bucket: ${GREEN}${BUCKET_NAME}${NC}"
echo -e "Collection: ${GREEN}${COLLECTION_NAME}${NC}"
echo ""

# Check prerequisites
echo -e "${BLUE}📋 Checking prerequisites...${NC}"

# Check AWS CLI
if ! command -v aws &> /dev/null; then
    echo -e "${RED}❌ AWS CLI not found. Please install AWS CLI.${NC}"
    exit 1
fi

# Check AWS credentials
if ! aws sts get-caller-identity &> /dev/null; then
    echo -e "${RED}❌ AWS credentials not configured.${NC}"
    echo "Please run: aws configure"
    exit 1
fi

# Check if documents exist
if [ ! -d "data/sample_docs" ] || [ -z "$(ls -A data/sample_docs)" ]; then
    echo -e "${RED}❌ No documents found in data/sample_docs${NC}"
    echo "Please ensure you have documents to index."
    exit 1
fi

echo -e "${GREEN}✅ Prerequisites check passed${NC}"

# Estimate costs
echo ""
echo -e "${YELLOW}💰 COST ESTIMATE:${NC}"
echo "This setup will create AWS resources that incur charges:"
echo "• S3 bucket: ~$0.023/GB/month"
echo "• OpenSearch Serverless: ~$0.24/OCU/hour (minimum 0.5 OCU)"
echo "• Bedrock embeddings: ~$0.0001/1K tokens"
echo "• Bedrock chat: ~$0.0008/1K input tokens"
echo ""
echo -e "${RED}⚠️  These resources will incur charges until deleted!${NC}"
echo "Use 'make down' or scripts/teardown-kb.sh to clean up."
echo ""

read -p "Continue with setup? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Setup cancelled."
    exit 0
fi

# Function to handle errors
handle_error() {
    echo -e "${RED}❌ Error occurred. Attempting cleanup...${NC}"
    ./scripts/teardown-kb.sh 2>/dev/null || true
    exit 1
}

trap handle_error ERR

# Step 1: Create S3 bucket
echo ""
echo -e "${BLUE}📦 Step 1: Creating S3 bucket...${NC}"

aws s3 mb s3://${BUCKET_NAME} --region ${REGION}
echo -e "${GREEN}✅ Created S3 bucket: ${BUCKET_NAME}${NC}"

# Upload documents
echo -e "${BLUE}📤 Uploading documents...${NC}"
aws s3 sync data/sample_docs s3://${BUCKET_NAME}/sample_docs/
echo -e "${GREEN}✅ Documents uploaded to s3://${BUCKET_NAME}/sample_docs/${NC}"

# Step 2: Create OpenSearch Serverless collection
echo ""
echo -e "${BLUE}🔍 Step 2: Creating OpenSearch Serverless collection...${NC}"

# Create security policy for encryption
ENCRYPTION_POLICY=$(cat <<EOF
{
    "Rules": [
        {
            "ResourceType": "collection",
            "Resource": ["collection/${COLLECTION_NAME}"]
        }
    ],
    "AWSOwnedKey": true
}
EOF
)

aws opensearchserverless create-security-policy \
    --name "${COLLECTION_NAME}-encryption" \
    --type encryption \
    --policy "${ENCRYPTION_POLICY}" \
    --region ${REGION} > /dev/null

# Create network policy
NETWORK_POLICY=$(cat <<EOF
[
    {
        "Rules": [
            {
                "ResourceType": "collection",
                "Resource": ["collection/${COLLECTION_NAME}"],
                "AllowFromPublic": true
            },
            {
                "ResourceType": "dashboard",
                "Resource": ["collection/${COLLECTION_NAME}"],
                "AllowFromPublic": true
            }
        ]
    }
]
EOF
)

aws opensearchserverless create-security-policy \
    --name "${COLLECTION_NAME}-network" \
    --type network \
    --policy "${NETWORK_POLICY}" \
    --region ${REGION} > /dev/null

# Create collection
aws opensearchserverless create-collection \
    --name ${COLLECTION_NAME} \
    --type VECTORSEARCH \
    --region ${REGION} > /dev/null

echo -e "${GREEN}✅ Created OpenSearch Serverless collection: ${COLLECTION_NAME}${NC}"

# Wait for collection to be active
echo -e "${BLUE}⏳ Waiting for collection to be active...${NC}"
while true; do
    STATUS=$(aws opensearchserverless list-collections \
        --collection-filters name=${COLLECTION_NAME} \
        --region ${REGION} \
        --query 'collectionSummaries[0].status' \
        --output text)
    
    if [ "$STATUS" = "ACTIVE" ]; then
        break
    fi
    echo "Collection status: $STATUS. Waiting..."
    sleep 10
done

# Get collection endpoint
COLLECTION_ENDPOINT=$(aws opensearchserverless list-collections \
    --collection-filters name=${COLLECTION_NAME} \
    --region ${REGION} \
    --query 'collectionSummaries[0].id' \
    --output text)

COLLECTION_ARN="arn:aws:aoss:${REGION}:$(aws sts get-caller-identity --query Account --output text):collection/${COLLECTION_ENDPOINT}"

echo -e "${GREEN}✅ Collection is active: ${COLLECTION_ARN}${NC}"

# Step 3: Create IAM role
echo ""
echo -e "${BLUE}🔐 Step 3: Creating IAM role...${NC}"

# Trust policy for Bedrock
TRUST_POLICY=$(cat <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "bedrock.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
EOF
)

# Create role
aws iam create-role \
    --role-name ${ROLE_NAME} \
    --assume-role-policy-document "${TRUST_POLICY}" > /dev/null

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ROLE_ARN="arn:aws:iam::${ACCOUNT_ID}:role/${ROLE_NAME}"

# Attach S3 policy
S3_POLICY=$(cat <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::${BUCKET_NAME}",
                "arn:aws:s3:::${BUCKET_NAME}/*"
            ]
        }
    ]
}
EOF
)

aws iam put-role-policy \
    --role-name ${ROLE_NAME} \
    --policy-name S3Access \
    --policy-document "${S3_POLICY}"

# Attach OpenSearch policy
AOSS_POLICY=$(cat <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "aoss:APIAccessAll"
            ],
            "Resource": "${COLLECTION_ARN}"
        }
    ]
}
EOF
)

aws iam put-role-policy \
    --role-name ${ROLE_NAME} \
    --policy-name AOSSAccess \
    --policy-document "${AOSS_POLICY}"

echo -e "${GREEN}✅ Created IAM role: ${ROLE_ARN}${NC}"

# Step 4: Create data access policy for OpenSearch
echo ""
echo -e "${BLUE}🔑 Step 4: Setting up OpenSearch access...${NC}"

DATA_ACCESS_POLICY=$(cat <<EOF
[
    {
        "Rules": [
            {
                "ResourceType": "index",
                "Resource": ["index/${COLLECTION_NAME}/*"],
                "Permission": [
                    "aoss:CreateIndex",
                    "aoss:DeleteIndex",
                    "aoss:UpdateIndex",
                    "aoss:DescribeIndex",
                    "aoss:ReadDocument",
                    "aoss:WriteDocument"
                ]
            },
            {
                "ResourceType": "collection",
                "Resource": ["collection/${COLLECTION_NAME}"],
                "Permission": [
                    "aoss:CreateCollectionItems",
                    "aoss:DeleteCollectionItems",
                    "aoss:UpdateCollectionItems",
                    "aoss:DescribeCollectionItems"
                ]
            }
        ],
        "Principal": ["${ROLE_ARN}"]
    }
]
EOF
)

aws opensearchserverless create-access-policy \
    --name "${COLLECTION_NAME}-access" \
    --type data \
    --policy "${DATA_ACCESS_POLICY}" \
    --region ${REGION} > /dev/null

echo -e "${GREEN}✅ Created OpenSearch data access policy${NC}"

# Wait for IAM role propagation
echo -e "${BLUE}⏳ Waiting for IAM role propagation...${NC}"
sleep 30

# Step 5: Create Knowledge Base
echo ""
echo -e "${BLUE}🧠 Step 5: Creating Bedrock Knowledge Base...${NC}"

KB_CREATE_RESPONSE=$(aws bedrock-agent create-knowledge-base \
    --name ${KB_NAME} \
    --description "RAG Demo Knowledge Base for AI Engineering Course" \
    --role-arn ${ROLE_ARN} \
    --knowledge-base-configuration '{
        "type": "VECTOR",
        "vectorKnowledgeBaseConfiguration": {
            "embeddingModelArn": "arn:aws:bedrock:'${REGION}'::foundation-model/amazon.titan-embed-text-v2:0"
        }
    }' \
    --storage-configuration '{
        "type": "OPENSEARCH_SERVERLESS",
        "opensearchServerlessConfiguration": {
            "collectionArn": "'${COLLECTION_ARN}'",
            "vectorIndexName": "rag-demo-index",
            "fieldMapping": {
                "vectorField": "vector",
                "textField": "text",
                "metadataField": "metadata"
            }
        }
    }' \
    --region ${REGION})

KB_ID=$(echo ${KB_CREATE_RESPONSE} | python3 -c "import sys, json; print(json.load(sys.stdin)['knowledgeBase']['knowledgeBaseId'])")

echo -e "${GREEN}✅ Created Knowledge Base: ${KB_ID}${NC}"

# Step 6: Create Data Source
echo ""
echo -e "${BLUE}📊 Step 6: Creating data source...${NC}"

DS_CREATE_RESPONSE=$(aws bedrock-agent create-data-source \
    --knowledge-base-id ${KB_ID} \
    --name ${DATA_SOURCE_NAME} \
    --description "S3 documents for RAG demo" \
    --data-source-configuration '{
        "type": "S3",
        "s3Configuration": {
            "bucketArn": "arn:aws:s3:::'${BUCKET_NAME}'",
            "inclusionPrefixes": ["sample_docs/"]
        }
    }' \
    --vector-ingestion-configuration '{
        "chunkingConfiguration": {
            "chunkingStrategy": "FIXED_SIZE",
            "fixedSizeChunkingConfiguration": {
                "maxTokens": 512,
                "overlapPercentage": 20
            }
        }
    }' \
    --region ${REGION})

DATA_SOURCE_ID=$(echo ${DS_CREATE_RESPONSE} | python3 -c "import sys, json; print(json.load(sys.stdin)['dataSource']['dataSourceId'])")

echo -e "${GREEN}✅ Created data source: ${DATA_SOURCE_ID}${NC}"

# Step 7: Start ingestion
echo ""
echo -e "${BLUE}📥 Step 7: Starting document ingestion...${NC}"

INGESTION_RESPONSE=$(aws bedrock-agent start-ingestion-job \
    --knowledge-base-id ${KB_ID} \
    --data-source-id ${DATA_SOURCE_ID} \
    --description "Initial ingestion of sample documents" \
    --region ${REGION})

INGESTION_JOB_ID=$(echo ${INGESTION_RESPONSE} | python3 -c "import sys, json; print(json.load(sys.stdin)['ingestionJob']['ingestionJobId'])")

echo -e "${GREEN}✅ Started ingestion job: ${INGESTION_JOB_ID}${NC}"

# Wait for ingestion to complete
echo -e "${BLUE}⏳ Waiting for document ingestion to complete...${NC}"
echo "This may take several minutes..."

while true; do
    STATUS=$(aws bedrock-agent get-ingestion-job \
        --knowledge-base-id ${KB_ID} \
        --data-source-id ${DATA_SOURCE_ID} \
        --ingestion-job-id ${INGESTION_JOB_ID} \
        --region ${REGION} \
        --query 'ingestionJob.status' \
        --output text)
    
    if [ "$STATUS" = "COMPLETE" ]; then
        break
    elif [ "$STATUS" = "FAILED" ]; then
        echo -e "${RED}❌ Ingestion failed!${NC}"
        exit 1
    fi
    
    echo "Ingestion status: $STATUS. Waiting..."
    sleep 15
done

# Step 8: Save configuration
echo ""
echo -e "${BLUE}💾 Step 8: Saving configuration...${NC}"

cat > .kb.env << EOF
# Generated by setup-kb.sh on $(date)
# These values are specific to this demo environment

KB_ID=${KB_ID}
DATA_SOURCE_ID=${DATA_SOURCE_ID}
S3_URI_FOR_KB=s3://${BUCKET_NAME}/sample_docs/
ROLE_ARN=${ROLE_ARN}
OS_COLLECTION_NAME=${COLLECTION_NAME}
OS_COLLECTION_ARN=${COLLECTION_ARN}
BUCKET_NAME=${BUCKET_NAME}
INGESTION_JOB_ID=${INGESTION_JOB_ID}

# For cleanup (used by teardown script)
CLEANUP_ROLE_NAME=${ROLE_NAME}
CLEANUP_COLLECTION_NAME=${COLLECTION_NAME}
CLEANUP_BUCKET_NAME=${BUCKET_NAME}
EOF

echo -e "${GREEN}✅ Configuration saved to .kb.env${NC}"

# Final summary
echo ""
echo -e "${GREEN}🎉 SETUP COMPLETE!${NC}"
echo "================================"
echo -e "Knowledge Base ID: ${GREEN}${KB_ID}${NC}"
echo -e "S3 Bucket: ${GREEN}s3://${BUCKET_NAME}/sample_docs/${NC}"
echo -e "OpenSearch Collection: ${GREEN}${COLLECTION_NAME}${NC}"
echo ""
echo -e "${BLUE}📋 Next steps:${NC}"
echo "1. Test with: python rag_bedrock_kb.py --question 'What is AI Engineering?'"
echo "2. Try the agent: python strands_agent.py --demo"
echo "3. When finished: make down (or scripts/teardown-kb.sh)"
echo ""
echo -e "${YELLOW}💰 Remember: Resources are now running and incurring charges!${NC}"
echo -e "${RED}🧹 Clean up with: make down${NC}"

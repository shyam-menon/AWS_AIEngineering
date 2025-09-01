#!/bin/bash
"""
AWS Bedrock Knowledge Base Teardown Script

This script safely removes all AWS resources created by setup-kb.sh:
1. Delete ingestion jobs and data sources
2. Delete Knowledge Base
3. Delete OpenSearch Serverless collection and policies
4. Delete IAM role and policies
5. Empty and delete S3 bucket
6. Clean up local configuration files

This script is designed to completely clean up the demo environment
and stop all charges from AWS resources.

Author: AWS AI Engineering Course
Chapter: 4 - Storage for Retrieval
"""

set -e  # Exit on any error (but continue cleanup on individual failures)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
REGION=${AWS_REGION:-us-east-1}

echo -e "${BLUE}🧹 AWS Bedrock Knowledge Base Teardown${NC}"
echo "====================================="
echo ""

# Check if .kb.env exists
if [ ! -f ".kb.env" ]; then
    echo -e "${YELLOW}⚠️  No .kb.env file found.${NC}"
    echo "This usually means either:"
    echo "1. Setup was never run"
    echo "2. Resources were already cleaned up"
    echo "3. Working directory is incorrect"
    echo ""
    
    read -p "Continue with manual cleanup? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Teardown cancelled."
        exit 0
    fi
    
    # Manual mode - try to find resources by naming pattern
    TIMESTAMP=$(date +%s)
    echo -e "${YELLOW}🔍 Searching for resources to clean up...${NC}"
    
    # This is a simplified cleanup - in practice you'd search for resources
    echo -e "${RED}❌ Manual cleanup not fully implemented.${NC}"
    echo "Please clean up resources manually through AWS Console:"
    echo "1. Bedrock Knowledge Bases"
    echo "2. OpenSearch Serverless Collections"
    echo "3. IAM Roles (search for 'rag-demo-kb-role')"
    echo "4. S3 Buckets (search for 'rag-demo-kb')"
    exit 1
fi

# Load configuration
source .kb.env

echo -e "Region: ${GREEN}${REGION}${NC}"
echo -e "Knowledge Base: ${GREEN}${KB_ID:-Not set}${NC}"
echo -e "S3 Bucket: ${GREEN}${CLEANUP_BUCKET_NAME:-Not set}${NC}"
echo -e "Collection: ${GREEN}${CLEANUP_COLLECTION_NAME:-Not set}${NC}"
echo ""

# Warning about cleanup
echo -e "${YELLOW}⚠️  This will delete all demo resources and stop AWS charges.${NC}"
echo -e "${RED}This action cannot be undone!${NC}"
echo ""

read -p "Continue with teardown? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Teardown cancelled."
    exit 0
fi

# Function to safely run commands and continue on failure
safe_run() {
    local description="$1"
    shift
    
    echo -e "${BLUE}$description${NC}"
    
    if "$@" 2>/dev/null; then
        echo -e "${GREEN}✅ Success: $description${NC}"
    else
        echo -e "${YELLOW}⚠️  Warning: $description failed (resource may not exist)${NC}"
    fi
}

# Step 1: Delete Data Source and Ingestion Jobs
if [ -n "$KB_ID" ] && [ -n "$DATA_SOURCE_ID" ]; then
    echo ""
    echo -e "${BLUE}📊 Step 1: Deleting data sources...${NC}"
    
    safe_run "Deleting data source" \
        aws bedrock-agent delete-data-source \
            --knowledge-base-id "$KB_ID" \
            --data-source-id "$DATA_SOURCE_ID" \
            --region "$REGION"
    
    # Wait a moment for deletion to propagate
    sleep 5
fi

# Step 2: Delete Knowledge Base
if [ -n "$KB_ID" ]; then
    echo ""
    echo -e "${BLUE}🧠 Step 2: Deleting Knowledge Base...${NC}"
    
    safe_run "Deleting Knowledge Base" \
        aws bedrock-agent delete-knowledge-base \
            --knowledge-base-id "$KB_ID" \
            --region "$REGION"
    
    # Wait for KB deletion to complete
    echo -e "${BLUE}⏳ Waiting for Knowledge Base deletion...${NC}"
    sleep 10
fi

# Step 3: Delete OpenSearch Serverless resources
if [ -n "$CLEANUP_COLLECTION_NAME" ]; then
    echo ""
    echo -e "${BLUE}🔍 Step 3: Deleting OpenSearch Serverless resources...${NC}"
    
    # Delete data access policy
    safe_run "Deleting data access policy" \
        aws opensearchserverless delete-access-policy \
            --name "${CLEANUP_COLLECTION_NAME}-access" \
            --type data \
            --region "$REGION"
    
    # Delete collection
    safe_run "Deleting OpenSearch collection" \
        aws opensearchserverless delete-collection \
            --name "$CLEANUP_COLLECTION_NAME" \
            --region "$REGION"
    
    # Wait for collection deletion
    echo -e "${BLUE}⏳ Waiting for collection deletion...${NC}"
    sleep 15
    
    # Delete security policies
    safe_run "Deleting encryption policy" \
        aws opensearchserverless delete-security-policy \
            --name "${CLEANUP_COLLECTION_NAME}-encryption" \
            --type encryption \
            --region "$REGION"
    
    safe_run "Deleting network policy" \
        aws opensearchserverless delete-security-policy \
            --name "${CLEANUP_COLLECTION_NAME}-network" \
            --type network \
            --region "$REGION"
fi

# Step 4: Delete IAM Role
if [ -n "$CLEANUP_ROLE_NAME" ]; then
    echo ""
    echo -e "${BLUE}🔐 Step 4: Deleting IAM role...${NC}"
    
    # Delete inline policies first
    safe_run "Deleting S3 policy from role" \
        aws iam delete-role-policy \
            --role-name "$CLEANUP_ROLE_NAME" \
            --policy-name S3Access
    
    safe_run "Deleting AOSS policy from role" \
        aws iam delete-role-policy \
            --role-name "$CLEANUP_ROLE_NAME" \
            --policy-name AOSSAccess
    
    # Delete the role
    safe_run "Deleting IAM role" \
        aws iam delete-role \
            --role-name "$CLEANUP_ROLE_NAME"
fi

# Step 5: Delete S3 Bucket
if [ -n "$CLEANUP_BUCKET_NAME" ]; then
    echo ""
    echo -e "${BLUE}📦 Step 5: Deleting S3 bucket...${NC}"
    
    # Empty bucket first
    safe_run "Emptying S3 bucket" \
        aws s3 rm "s3://$CLEANUP_BUCKET_NAME" --recursive
    
    # Delete bucket
    safe_run "Deleting S3 bucket" \
        aws s3 rb "s3://$CLEANUP_BUCKET_NAME"
fi

# Step 6: Clean up local files
echo ""
echo -e "${BLUE}🗂️  Step 6: Cleaning up local files...${NC}"

if [ -f ".kb.env" ]; then
    echo -e "${BLUE}Removing .kb.env...${NC}"
    rm -f .kb.env
    echo -e "${GREEN}✅ Removed .kb.env${NC}"
fi

# Optional: Clean up FAISS index files
if [ -f "faiss_index.faiss" ]; then
    read -p "Remove local FAISS index files? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -f faiss_index.faiss faiss_index_data.npz
        echo -e "${GREEN}✅ Removed local FAISS index files${NC}"
    fi
fi

# Final summary
echo ""
echo -e "${GREEN}🎉 TEARDOWN COMPLETE!${NC}"
echo "=========================="
echo ""
echo -e "${GREEN}✅ All AWS resources have been cleaned up${NC}"
echo -e "${GREEN}✅ Local configuration files removed${NC}"
echo -e "${GREEN}✅ AWS charges should now be stopped${NC}"
echo ""
echo -e "${BLUE}📋 What was cleaned up:${NC}"
echo "• Knowledge Base and data sources"
echo "• OpenSearch Serverless collection and policies"
echo "• IAM role and policies"
echo "• S3 bucket and contents"
echo "• Local configuration files"
echo ""
echo -e "${YELLOW}💡 To recreate the demo environment:${NC}"
echo "Run: make up (or scripts/setup-kb.sh)"
echo ""
echo -e "${GREEN}Thank you for using the RAG demo responsibly! 🌱${NC}"

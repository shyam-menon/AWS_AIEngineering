# AWS Bedrock Knowledge Base Setup Script (PowerShell)
# This script creates an ephemeral AWS infrastructure for the RAG demo

param(
    [string]$Region = "us-east-1"
)

# Colors for output
function Write-Success { param($Message) Write-Host $Message -ForegroundColor Green }
function Write-Info { param($Message) Write-Host $Message -ForegroundColor Cyan }
function Write-Warning { param($Message) Write-Host $Message -ForegroundColor Yellow }
function Write-Error { param($Message) Write-Host $Message -ForegroundColor Red }

# Configuration
$BucketSuffix = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
$BucketName = "rag-demo-kb-$BucketSuffix"
$CollectionName = "rag-demo-collection-$BucketSuffix"
$RoleName = "rag-demo-kb-role-$BucketSuffix"
$KBName = "rag-demo-kb-$BucketSuffix"
$DataSourceName = "s3-docs"

Write-Info "AWS Bedrock Knowledge Base Setup"
Write-Info "=================================="
Write-Info "Region: $Region"
Write-Info "Bucket: $BucketName"
Write-Info "Collection: $CollectionName"
Write-Info ""

# Check prerequisites
Write-Info "Checking prerequisites..."

# Check AWS CLI
try {
    $awsVersion = aws --version 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Error "AWS CLI not found. Please install AWS CLI."
        exit 1
    }
    Write-Success "AWS CLI found: $($awsVersion -split ' ')[0]"
} catch {
    Write-Error "AWS CLI not found. Please install AWS CLI."
    exit 1
}

# Check AWS credentials
try {
    $identity = aws sts get-caller-identity --output json | ConvertFrom-Json
    Write-Success "AWS credentials configured for: $($identity.Arn)"
} catch {
    Write-Error "AWS credentials not configured. Run 'aws configure'"
    exit 1
}

# Check if Bedrock is available in region
Write-Info "Checking Bedrock availability in $Region..."
try {
    aws bedrock list-foundation-models --region $Region --output json | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Bedrock not available in $Region"
        exit 1
    }
    Write-Success "Bedrock available in $Region"
} catch {
    Write-Error "Error checking Bedrock availability"
    exit 1
}

# Step 1: Create S3 bucket
Write-Info "Creating S3 bucket: $BucketName"
try {
    if ($Region -eq "us-east-1") {
        aws s3api create-bucket --bucket $BucketName --region $Region
    } else {
        aws s3api create-bucket --bucket $BucketName --region $Region --create-bucket-configuration LocationConstraint=$Region
    }
    
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to create bucket"
    }
    
    Write-Success "S3 bucket created: $BucketName"
} catch {
    Write-Error "Failed to create S3 bucket: $_"
    exit 1
}

# Upload sample documents
Write-Info "Uploading sample documents..."
try {
    aws s3 sync data/sample_docs s3://$BucketName/sample_docs/ --region $Region
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to upload documents"
    }
    Write-Success "Documents uploaded to s3://$BucketName/sample_docs/"
} catch {
    Write-Error "Failed to upload documents: $_"
    exit 1
}

# Step 2: Create IAM role for Knowledge Base
Write-Info "Creating IAM role: $RoleName"

# Create trust policy
$trustPolicy = @{
    Version = "2012-10-17"
    Statement = @(
        @{
            Effect = "Allow"
            Principal = @{
                Service = "bedrock.amazonaws.com"
            }
            Action = "sts:AssumeRole"
        }
    )
} | ConvertTo-Json -Depth 10

# Create the role
try {
    aws iam create-role --role-name $RoleName --assume-role-policy-document $trustPolicy --region $Region
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to create role"
    }
    Write-Success "IAM role created: $RoleName"
} catch {
    Write-Error "Failed to create IAM role: $_"
    exit 1
}

# Create and attach policy
$policyDocument = @{
    Version = "2012-10-17"
    Statement = @(
        @{
            Effect = "Allow"
            Action = @(
                "s3:GetObject",
                "s3:ListBucket"
            )
            Resource = @(
                "arn:aws:s3:::$BucketName",
                "arn:aws:s3:::$BucketName/*"
            )
        },
        @{
            Effect = "Allow"
            Action = @(
                "aoss:CreateCollection",
                "aoss:DeleteCollection",
                "aoss:CreateIndex",
                "aoss:DeleteIndex",
                "aoss:UpdateIndex",
                "aoss:DescribeIndex",
                "aoss:APIAccessAll"
            )
            Resource = "*"
        },
        @{
            Effect = "Allow"
            Action = @(
                "bedrock:InvokeModel"
            )
            Resource = "*"
        }
    )
} | ConvertTo-Json -Depth 10

try {
    $policyArn = aws iam create-policy --policy-name "$RoleName-policy" --policy-document $policyDocument --query "Policy.Arn" --output text --region $Region
    aws iam attach-role-policy --role-name $RoleName --policy-arn $policyArn --region $Region
    Write-Success "IAM policy attached to role"
} catch {
    Write-Error "Failed to create/attach policy: $_"
    exit 1
}

# Step 3: Create OpenSearch Serverless collection
Write-Info "Creating OpenSearch Serverless collection: $CollectionName"

# Get account ID for security policies
$accountId = aws sts get-caller-identity --query "Account" --output text

# Create encryption policy
$encryptionPolicy = @{
    Rules = @(
        @{
            ResourceType = "collection"
            Resource = @("collection/$CollectionName")
        }
    )
    AWSOwnedKey = $true
} | ConvertTo-Json -Depth 10

try {
    aws opensearchserverless create-security-policy --name "$CollectionName-encryption" --type "encryption" --policy $encryptionPolicy --region $Region
    Write-Success "Encryption policy created"
} catch {
    Write-Warning "Encryption policy may already exist or creation failed"
}

# Create network policy
$networkPolicy = @(
    @{
        Description = "Public access for $CollectionName"
        Rules = @(
            @{
                ResourceType = "collection"
                Resource = @("collection/$CollectionName")
            },
            @{
                ResourceType = "dashboard"
                Resource = @("collection/$CollectionName")
            }
        )
        AllowFromPublic = $true
    }
) | ConvertTo-Json -Depth 10

try {
    aws opensearchserverless create-security-policy --name "$CollectionName-network" --type "network" --policy $networkPolicy --region $Region
    Write-Success "Network policy created"
} catch {
    Write-Warning "Network policy may already exist or creation failed"
}

# Create data access policy
$dataAccessPolicy = @(
    @{
        Rules = @(
            @{
                ResourceType = "collection"
                Resource = @("collection/$CollectionName")
                Permission = @("aoss:*")
            },
            @{
                ResourceType = "index"
                Resource = @("index/$CollectionName/*")
                Permission = @("aoss:*")
            }
        )
        Principal = @("arn:aws:iam::$accountId:role/$RoleName")
    }
) | ConvertTo-Json -Depth 10

try {
    aws opensearchserverless create-access-policy --name "$CollectionName-access" --type "data" --policy $dataAccessPolicy --region $Region
    Write-Success "Data access policy created"
} catch {
    Write-Warning "Data access policy may already exist or creation failed"
}

# Create the collection
try {
    $collectionId = aws opensearchserverless create-collection --name $CollectionName --type "VECTORSEARCH" --query "createCollectionDetail.id" --output text --region $Region
    Write-Success "OpenSearch collection created: $collectionId"
    
    # Wait for collection to be active
    Write-Info "Waiting for collection to be active..."
    do {
        Start-Sleep 10
        $status = aws opensearchserverless batch-get-collection --ids $collectionId --query "collectionDetails[0].status" --output text --region $Region
        Write-Info "Collection status: $status"
    } while ($status -ne "ACTIVE")
    
    Write-Success "Collection is now active"
} catch {
    Write-Error "Failed to create OpenSearch collection: $_"
    exit 1
}

# Step 4: Create Knowledge Base
Write-Info "Creating Bedrock Knowledge Base: $KBName"

# Get role ARN
$roleArn = aws iam get-role --role-name $RoleName --query "Role.Arn" --output text --region $Region

# Get collection endpoint
$collectionEndpoint = aws opensearchserverless batch-get-collection --ids $collectionId --query "collectionDetails[0].collectionEndpoint" --output text --region $Region

# Knowledge Base configuration
$kbConfig = @{
    name = $KBName
    description = "RAG Demo Knowledge Base for AI Engineering Course"
    roleArn = $roleArn
    knowledgeBaseConfiguration = @{
        type = "VECTOR"
        vectorKnowledgeBaseConfiguration = @{
            embeddingModelArn = "arn:aws:bedrock:${Region}::foundation-model/amazon.titan-embed-text-v2:0"
            embeddingModelConfiguration = @{
                bedrockEmbeddingModelConfiguration = @{
                    dimensions = 1024
                }
            }
        }
    }
    storageConfiguration = @{
        type = "OPENSEARCH_SERVERLESS"
        opensearchServerlessConfiguration = @{
            collectionArn = "arn:aws:aoss:${Region}:${accountId}:collection/$collectionId"
            vectorIndexName = "rag-demo-index"
            fieldMapping = @{
                vectorField = "vector"
                textField = "text"
                metadataField = "metadata"
            }
        }
    }
} | ConvertTo-Json -Depth 10

try {
    $kbId = aws bedrock-agent create-knowledge-base --cli-input-json $kbConfig --query "knowledgeBase.knowledgeBaseId" --output text --region $Region
    Write-Success "Knowledge Base created: $kbId"
} catch {
    Write-Error "Failed to create Knowledge Base: $_"
    exit 1
}

# Step 5: Create Data Source
Write-Info "Creating data source..."

$dataSourceConfig = @{
    knowledgeBaseId = $kbId
    name = $DataSourceName
    description = "S3 data source for RAG demo"
    dataSourceConfiguration = @{
        type = "S3"
        s3Configuration = @{
            bucketArn = "arn:aws:s3:::$BucketName"
            inclusionPrefixes = @("sample_docs/")
        }
    }
    vectorIngestionConfiguration = @{
        chunkingConfiguration = @{
            chunkingStrategy = "FIXED_SIZE"
            fixedSizeChunkingConfiguration = @{
                maxTokens = 300
                overlapPercentage = 20
            }
        }
    }
} | ConvertTo-Json -Depth 10

try {
    $dataSourceId = aws bedrock-agent create-data-source --cli-input-json $dataSourceConfig --query "dataSource.dataSourceId" --output text --region $Region
    Write-Success "Data source created: $dataSourceId"
} catch {
    Write-Error "Failed to create data source: $_"
    exit 1
}

# Step 6: Start ingestion
Write-Info "Starting document ingestion..."
try {
    $ingestionJobId = aws bedrock-agent start-ingestion-job --knowledge-base-id $kbId --data-source-id $dataSourceId --query "ingestionJob.ingestionJobId" --output text --region $Region
    Write-Success "Ingestion job started: $ingestionJobId"
    
    Write-Info "Waiting for ingestion to complete..."
    do {
        Start-Sleep 15
        $ingestionStatus = aws bedrock-agent get-ingestion-job --knowledge-base-id $kbId --data-source-id $dataSourceId --ingestion-job-id $ingestionJobId --query "ingestionJob.status" --output text --region $Region
        Write-Info "Ingestion status: $ingestionStatus"
    } while ($ingestionStatus -eq "IN_PROGRESS")
    
    if ($ingestionStatus -eq "COMPLETE") {
        Write-Success "Document ingestion completed successfully!"
    } else {
        Write-Error "Ingestion failed with status: $ingestionStatus"
        exit 1
    }
} catch {
    Write-Error "Failed to start ingestion: $_"
    exit 1
}

# Step 7: Update .env file
Write-Info "Updating .env file..."
try {
    $envContent = Get-Content ".env" -Raw
    $envContent = $envContent -replace "KB_ID=.*", "KB_ID=$kbId"
    $envContent = $envContent -replace "S3_URI_FOR_KB=.*", "S3_URI_FOR_KB=s3://$BucketName/sample_docs/"
    Set-Content ".env" $envContent
    
    # Also create .kb.env for easy cleanup
    $kbEnvContent = @"
# Knowledge Base Configuration (generated by setup-kb.ps1)
KB_ID=$kbId
S3_BUCKET_NAME=$BucketName
COLLECTION_NAME=$CollectionName
ROLE_NAME=$RoleName
KB_NAME=$KBName
DATA_SOURCE_ID=$dataSourceId
REGION=$Region
"@
    Set-Content ".kb.env" $kbEnvContent
    
    Write-Success "Configuration saved to .env and .kb.env"
} catch {
    Write-Error "Failed to update configuration files: $_"
}

# Summary
Write-Info ""
Write-Success "AWS Knowledge Base setup complete!"
Write-Info "====================================="
Write-Info "Knowledge Base ID: $kbId"
Write-Info "S3 Bucket: $BucketName"
Write-Info "Region: $Region"
Write-Info ""
Write-Info "Next steps:"
Write-Info "1. Test the Knowledge Base: .\run-demo.ps1 demo-kb"
Write-Info "2. Run the agent demo: .\run-demo.ps1 agent"
Write-Info "3. When finished, cleanup: .\teardown-kb.ps1"
Write-Info ""
Write-Warning "This setup creates AWS resources that incur charges."
Write-Warning "Use teardown-kb.ps1 to clean up when finished."

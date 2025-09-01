# AWS Bedrock Knowledge Base Teardown Script (PowerShell)
# This script cleans up all resources created by setup-kb.ps1

param(
    [string]$Region = "us-east-1",
    [switch]$Force = $false
)

# Colors for output
function Write-Success { param($Message) Write-Host $Message -ForegroundColor Green }
function Write-Info { param($Message) Write-Host $Message -ForegroundColor Cyan }
function Write-Warning { param($Message) Write-Host $Message -ForegroundColor Yellow }
function Write-Error { param($Message) Write-Host $Message -ForegroundColor Red }

Write-Info "🧹 AWS Bedrock Knowledge Base Teardown"
Write-Info "====================================="
Write-Info ""

# Load configuration from .kb.env
if (-not (Test-Path ".kb.env")) {
    Write-Error "❌ Configuration file .kb.env not found."
    Write-Info "This file should have been created by setup-kb.ps1"
    exit 1
}

$config = @{}
Get-Content ".kb.env" | ForEach-Object {
    if ($_ -match "^([^#][^=]+)=(.*)$") {
        $config[$matches[1].Trim()] = $matches[2].Trim()
    }
}

$KBId = $config.KB_ID
$BucketName = $config.S3_BUCKET_NAME
$CollectionName = $config.COLLECTION_NAME
$RoleName = $config.ROLE_NAME

Write-Info "Configuration loaded:"
Write-Info "  Knowledge Base ID: $KBId"
Write-Info "  S3 Bucket: $BucketName"
Write-Info "  Collection: $CollectionName"
Write-Info "  Role: $RoleName"
Write-Info ""

if (-not $Force) {
    $confirmation = Read-Host "❓ Are you sure you want to delete all resources? (yes/no)"
    if ($confirmation -ne "yes") {
        Write-Info "Teardown cancelled."
        exit 0
    }
}

Write-Info "🗑️  Starting resource cleanup..."

# Step 1: Delete Knowledge Base
if ($KBId) {
    Write-Info "🧠 Deleting Knowledge Base: $KBId"
    try {
        aws bedrock-agent delete-knowledge-base --knowledge-base-id $KBId --region $Region
        Write-Success "✅ Knowledge Base deletion initiated"
        
        # Wait for deletion
        Write-Info "⏳ Waiting for Knowledge Base deletion..."
        do {
            Start-Sleep 10
            try {
                $kbStatus = aws bedrock-agent get-knowledge-base --knowledge-base-id $KBId --query "knowledgeBase.status" --output text --region $Region 2>$null
                if ($LASTEXITCODE -ne 0) {
                    # Knowledge Base not found = deleted
                    break
                }
                Write-Info "KB status: $kbStatus"
            } catch {
                break  # KB deleted
            }
        } while ($true)
        
        Write-Success "✅ Knowledge Base deleted"
    } catch {
        Write-Warning "⚠️  Knowledge Base deletion failed or already deleted: $_"
    }
}

# Step 2: Delete S3 bucket
if ($BucketName) {
    Write-Info "📦 Deleting S3 bucket: $BucketName"
    try {
        # Empty bucket first
        aws s3 rm s3://$BucketName --recursive --region $Region
        aws s3api delete-bucket --bucket $BucketName --region $Region
        Write-Success "✅ S3 bucket deleted"
    } catch {
        Write-Warning "⚠️  S3 bucket deletion failed or already deleted: $_"
    }
}

# Step 3: Delete OpenSearch Serverless collection
if ($CollectionName) {
    Write-Info "🔍 Deleting OpenSearch collection: $CollectionName"
    try {
        aws opensearchserverless delete-collection --id $CollectionName --region $Region
        Write-Success "✅ OpenSearch collection deletion initiated"
        
        # Wait for deletion
        Write-Info "⏳ Waiting for collection deletion..."
        do {
            Start-Sleep 15
            try {
                $collectionStatus = aws opensearchserverless batch-get-collection --names $CollectionName --query "collectionDetails[0].status" --output text --region $Region 2>$null
                if ($LASTEXITCODE -ne 0) {
                    break  # Collection not found = deleted
                }
                Write-Info "Collection status: $collectionStatus"
            } catch {
                break  # Collection deleted
            }
        } while ($true)
        
        Write-Success "✅ OpenSearch collection deleted"
    } catch {
        Write-Warning "⚠️  OpenSearch collection deletion failed or already deleted: $_"
    }
    
    # Delete OpenSearch policies
    try {
        aws opensearchserverless delete-security-policy --name "$CollectionName-encryption" --type "encryption" --region $Region 2>$null
        aws opensearchserverless delete-security-policy --name "$CollectionName-network" --type "network" --region $Region 2>$null
        aws opensearchserverless delete-access-policy --name "$CollectionName-access" --type "data" --region $Region 2>$null
        Write-Success "✅ OpenSearch policies deleted"
    } catch {
        Write-Warning "⚠️  Some OpenSearch policies may not have been deleted"
    }
}

# Step 4: Delete IAM role and policy
if ($RoleName) {
    Write-Info "🔐 Deleting IAM role: $RoleName"
    try {
        # Get attached policies
        $policies = aws iam list-attached-role-policies --role-name $RoleName --query "AttachedPolicies[].PolicyArn" --output text --region $Region 2>$null
        
        # Detach and delete policies
        $policies -split "`t" | ForEach-Object {
            if ($_ -and $_ -match "arn:aws:iam") {
                aws iam detach-role-policy --role-name $RoleName --policy-arn $_ --region $Region 2>$null
                if ($_ -like "*$RoleName-policy*") {
                    aws iam delete-policy --policy-arn $_ --region $Region 2>$null
                }
            }
        }
        
        # Delete role
        aws iam delete-role --role-name $RoleName --region $Region
        Write-Success "✅ IAM role and policies deleted"
    } catch {
        Write-Warning "⚠️  IAM role deletion failed or already deleted: $_"
    }
}

# Step 5: Clean up configuration files
Write-Info "📝 Cleaning up configuration files..."
try {
    if (Test-Path ".kb.env") {
        Remove-Item ".kb.env"
        Write-Success "✅ Removed .kb.env"
    }
    
    # Reset .env file
    if (Test-Path ".env") {
        $envContent = Get-Content ".env" -Raw
        $envContent = $envContent -replace "KB_ID=.*", "KB_ID="
        $envContent = $envContent -replace "S3_URI_FOR_KB=.*", "S3_URI_FOR_KB="
        Set-Content ".env" $envContent
        Write-Success "✅ Reset .env file"
    }
} catch {
    Write-Warning "⚠️  Configuration file cleanup failed: $_"
}

Write-Info ""
Write-Success "🎉 Teardown complete!"
Write-Info "==================="
Write-Info "All AWS resources have been cleaned up."
Write-Info "You can now run setup-kb.ps1 again if needed."
Write-Info ""
Write-Info "💰 Billing note: Resource deletion may take a few minutes to"
Write-Info "   reflect in your AWS billing. Charges should stop once"
Write-Info "   resources are fully deleted."

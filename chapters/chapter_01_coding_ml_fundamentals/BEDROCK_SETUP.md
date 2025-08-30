# AWS Bedrock Setup Guide for Strands Agents

This guide helps you configure AWS Bedrock to work with Strands Agents framework.

## Overview

Strands Agents uses AWS Bedrock as the default model provider with Claude 4 Sonnet. This requires:
1. AWS account with appropriate permissions
2. Bedrock model access enabled
3. Proper AWS credentials configuration

## Step 1: AWS Credentials Configuration

### Option A: Environment Variables
```bash
# Windows PowerShell
$env:AWS_ACCESS_KEY_ID="your_access_key_here"
$env:AWS_SECRET_ACCESS_KEY="your_secret_key_here"
$env:AWS_DEFAULT_REGION="us-east-1"

# Windows Command Prompt
set AWS_ACCESS_KEY_ID=your_access_key_here
set AWS_SECRET_ACCESS_KEY=your_secret_key_here
set AWS_DEFAULT_REGION=us-east-1

# Linux/macOS
export AWS_ACCESS_KEY_ID=your_access_key_here
export AWS_SECRET_ACCESS_KEY=your_secret_key_here
export AWS_DEFAULT_REGION=us-east-1
```

### Option B: AWS CLI Configuration
```bash
# Install AWS CLI (if not already installed)
pip install awscli

# Configure credentials
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key  
# Enter your default region (e.g., us-east-1)
# Enter output format (json)
```

### Option C: IAM Roles (for EC2/ECS/Lambda)
If running on AWS services, use IAM roles instead of access keys.

## Step 2: Enable Bedrock Model Access

1. **Open AWS Bedrock Console**:
   - Go to https://console.aws.amazon.com/bedrock/
   - Ensure you're in the correct region (us-east-1 recommended)

2. **Request Model Access**:
   - Click "Model access" in the left sidebar
   - Find "Claude 4 Sonnet" (us.anthropic.claude-sonnet-4-20250514-v1:0)
   - Click "Request model access" 
   - Fill out the form with use case details
   - Submit the request

3. **Wait for Approval**:
   - Model access requests are typically approved within minutes
   - You'll receive an email notification when approved
   - Refresh the page to see the updated status

4. **Verify Access**:
   - The model should show "Access granted" status
   - You can now use the model with Strands Agents

## Step 3: Required IAM Permissions

Ensure your AWS user/role has these permissions:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": [
                "arn:aws:bedrock:*::foundation-model/us.anthropic.claude-sonnet-4-20250514-v1:0"
            ]
        }
    ]
}
```

## Step 4: Test Your Setup

Run the simple test script:

```bash
cd chapters/chapter_01_coding_ml_fundamentals
python simple_strands_example.py
```

Expected output when working:
```
✅ Strands Agents library is available!
🔧 Creating a simple agent with tools...
✅ Agent created successfully!
[Agent response with tool usage]
```

## Troubleshooting

### Common Error: AccessDeniedException
```
An error occurred (AccessDeniedException) when calling the ConverseStream operation: 
Your account does not have an agreement to this model.
```

**Solution**: Complete Step 2 (Enable Bedrock Model Access) above.

### Common Error: UnauthorizedOperation
```
UnauthorizedOperation: You are not authorized to perform this operation.
```

**Solution**: 
1. Check AWS credentials are correctly configured
2. Verify IAM permissions include Bedrock access
3. Ensure you're in the correct AWS region

### Common Error: RegionNotSupportedException
```
The requested operation is not supported in this region.
```

**Solution**: Use a supported region like us-east-1, us-west-2, or eu-west-1.

### Model Not Available
If Claude 4 Sonnet is not available in your region, you can specify a different model:

```python
from strands import Agent

# Use Claude 3.5 Sonnet instead
agent = Agent(model="anthropic.claude-3-5-sonnet-20241022-v2:0")
```

## Alternative Model Providers

If you can't use AWS Bedrock, Strands supports other providers:

### OpenAI
```python
from strands import Agent
from strands.models import OpenAIModel

agent = Agent(model=OpenAIModel(
    model_id="gpt-4",
    api_key="your_openai_api_key"
))
```

### Anthropic Direct API
```python
from strands import Agent
from strands.models import AnthropicModel

agent = Agent(model=AnthropicModel(
    model_id="claude-3-5-sonnet-20241022",
    api_key="your_anthropic_api_key"
))
```

## Next Steps

Once Bedrock is configured:
1. Run the Strands examples in this chapter
2. Explore the Strands documentation: https://strandsagents.com/
3. Build your first AI agent with custom tools
4. Integrate agents with your AI engineering workflows

## Resources

- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Strands Agents Documentation](https://strandsagents.com/latest/documentation/)
- [AWS IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [Bedrock Model Access Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access-modify.html)

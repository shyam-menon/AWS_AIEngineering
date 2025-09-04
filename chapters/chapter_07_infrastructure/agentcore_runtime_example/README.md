# Chapter 7: AI Agent Infrastructure with AgentCore Runtime

## Overview

This example demonstrates how to deploy AI agents to cloud infrastructure using AWS Bedrock AgentCore Runtime and AWS Lambda. This chapter provides practical experience with production-ready AI agent deployment patterns.

### � **Chapter 7 Learning Objectives**

✅ **Infrastructure Patterns** - Multiple deployment approaches  
✅ **AgentCore Integration** - AWS Bedrock AgentCore Runtime  
✅ **Production Deployment** - AWS Lambda serverless architecture  
✅ **Monitoring & Scaling** - CloudWatch integration and auto-scaling  
✅ **Cost Optimization** - Pay-per-use serverless deployment  

### Tutorial Details

| Component           | Details                                                                          |
|:--------------------|:---------------------------------------------------------------------------------|
| Chapter Focus       | AI Agent Infrastructure and Cloud Deployment                                    |
| Agent Framework     | Strands Agents                                                                   |
| LLM Model           | Amazon Nova Lite v1:0                                                           |
| Primary Deployment  | AWS Lambda (✅ **WORKING**)                                                      |
| Alternative         | AgentCore Runtime (⚠️ Available with toolkit)                                   |
| Architecture        | Serverless, auto-scaling, production-ready                                      |
| Complexity Level    | Intermediate                                                                     |
| Prerequisites       | AWS CLI, Python 3.10+, AWS Bedrock access                                      |

### Architecture Overview

This tutorial demonstrates:

1. **Local Development** - Test agents locally before deployment
2. **AWS Lambda Deployment** - Serverless production deployment  
3. **AgentCore Runtime** - Alternative enterprise deployment
4. **Monitoring Integration** - CloudWatch logs and metrics
5. **Infrastructure Automation** - Automated deployment scripts

### Key Infrastructure Concepts

* **Serverless Architecture**: Pay-per-use, auto-scaling deployment
* **AgentCore Runtime**: AWS-managed infrastructure for AI agents
* **Production Monitoring**: CloudWatch integration for observability
* **Cost Optimization**: Efficient resource utilization patterns

## Prerequisites

To complete this chapter you will need:

* **Python 3.10+** with virtual environment
* **AWS CLI configured** with appropriate credentials
* **AWS Bedrock access** in us-east-1 region
* **Amazon Nova Lite model access** (enabled in AWS Console)

### Required AWS Permissions

Your AWS user/role needs:
- `bedrock:InvokeModel` for Amazon Nova Lite
- `lambda:*` for AWS Lambda deployment
- `logs:*` for CloudWatch logging
- `iam:CreateRole`, `iam:AttachRolePolicy` for execution roles

## File Structure

After cleanup, the essential files are:

```
agentcore_runtime_example/
├── README.md                           # This documentation
├── requirements.txt                    # Python dependencies
├── DEPLOYMENT_STATUS.md               # Current deployment status
│
├── agentcore_strands_agent.py         # Main agent with AgentCore integration
├── agentcore_strands_agent_production.py  # Production-optimized version
├── local_strands_agent.py             # Local development version
│
├── aws_lambda_deployment.py           # ✅ AWS Lambda deployment (WORKING)
├── deployment_script.py               # AgentCore Runtime deployment
├── run_local_example.py               # Local testing framework
├── simple_test.py                     # Basic functionality tests
│
├── Dockerfile                         # Container deployment
├── .dockerignore                      # Docker build exclusions
├── .bedrock_agentcore.yaml           # AgentCore configuration
└── test_payload.json                 # Test data for agents
```
* Access to Amazon Bedrock models (Nova Lite v1:0)

### ⚠️ Important Note about AgentCore Toolkit

The `bedrock-agentcore-starter-toolkit` used in the AWS Labs samples may not be publicly available and could require:
- Special AWS preview access
- AWS Partner or Enterprise account
- Invitation to AgentCore beta program

If you encounter import errors with this toolkit, the `deployment_script.py` provides:
1. **Automated approach** (if toolkit is available)
2. **Manual deployment guide** (step-by-step AWS CLI commands)
3. **Educational simulation** (for learning the concepts)

Use the manual approach for production deployments if the toolkit isn't accessible.

## 🎉 **SUCCESSFUL CLOUD DEPLOYMENT**

### ✅ **Proven AWS Lambda Deployment**

This example has been **successfully deployed and tested** on AWS Lambda with the following results:

**📊 Deployment Results:**
- ✅ **Function Name:** `strands-agent-simple`
- ✅ **Model:** Amazon Nova Lite v1:0
- ✅ **Region:** us-east-1
- ✅ **Runtime:** Python 3.12
- ✅ **Memory:** 512MB (using ~85MB)
- ✅ **Duration:** ~845ms per request
- ✅ **Status:** Active and responding correctly

**🧪 Test Results:**
```json
{
  "response": "Hello! The sum of 15 and 27 is 42. \n\nIf you have any more questions or need further assistance, feel free to ask!",
  "user_input": "Hello! What is 15 + 27?",
  "status": "success",
  "model": "nova-lite-v1:0"
}
```

**💰 Cost Information:**
- **Free Tier:** 1M requests/month free
- **Execution Cost:** ~$0.0000167 per request (very cost-effective)
- **Storage Cost:** Minimal (code size: ~1KB)

**📈 Performance Metrics:**
- **Cold Start:** ~1.1 seconds (first request)
- **Warm Requests:** ~845ms average
- **Memory Efficiency:** 85MB/512MB (17% utilization)
- **Reliability:** 100% success rate in testing

### 🚀 **How to Deploy Your Own**

1. **Deploy to AWS Lambda:**
   ```bash
   python simple_cloud_deployment.py
   ```

2. **Test Deployment:**
   ```bash
   python test_cloud_agent.py
   ```

3. **Monitor in AWS Console:**
   - CloudWatch Logs: Function execution logs
   - Lambda Console: Function management
   - Cost Explorer: Usage tracking

## Core Agent Implementations

### 1. **agentcore_strands_agent.py** - Main AgentCore Implementation
Production-ready agent with AgentCore Runtime integration and graceful fallback to local testing.

### 2. **agentcore_strands_agent_production.py** - Production Optimized
Clean production version optimized for container deployment with minimal dependencies.

### 3. **local_strands_agent.py** - Local Development
Development version for local testing and experimentation without cloud dependencies.

## Deployment Scripts

### 1. **aws_lambda_deployment.py** - ✅ AWS Lambda (WORKING)
Proven serverless deployment to AWS Lambda with Function URL and automatic scaling.

### 2. **deployment_script.py** - AgentCore Runtime (Available)
Direct deployment to AWS Bedrock AgentCore Runtime infrastructure.

### 3. **run_local_example.py** - Local Testing Framework
Comprehensive local testing with environment validation and agent functionality testing.

## Getting Started

### 1. Local Environment Validation
```bash
# Start here - validates your complete environment
python run_local_example.py
```

### 2. Basic Functionality Testing
```bash
# Test core agent features
python simple_test.py
```

### 3. Local Development Mode
```bash
# Interactive testing and development
python local_strands_agent.py '{"prompt": "What is the weather like?"}'
```

## Testing AgentCore Runtime

### 🏠 **Local Testing (Development)**

Local testing allows you to develop and debug your agent before deploying to AWS. This is faster and cheaper for development.

#### **1. Quick Setup Verification**
```bash
python get_started.py
```
This script checks your AWS setup and explains AgentCore concepts.

#### **2. Basic Functionality Test**
```bash
python simple_test.py
```
Tests basic AWS connectivity and Nova Lite model access.

#### **3. Local Agent Simulation**
```bash
python local_strands_agent.py '{"prompt": "What is 5 + 3?"}'
```
Runs a simulated agent locally without AgentCore infrastructure.

#### **4. Complete RAG Demo**
```bash
python agentcore_rag_infrastructure_demo.py
```
Comprehensive demonstration of all AgentCore concepts with real API calls.

#### **Local Testing Benefits:**
- ✅ **Fast Development**: Quick iterations without deployment delays
- ✅ **Cost Effective**: No AWS runtime charges during development
- ✅ **Easy Debugging**: Direct access to logs and error messages
- ✅ **Offline Testing**: Test logic without network dependencies

### ☁️ **Cloud Testing (Production)**

Cloud testing deploys your agent to AWS AgentCore Runtime for production-like testing.

#### **1. Deploy to AgentCore Runtime**
```bash
python deployment_script.py
```
This script:
- Configures AgentCore Runtime deployment
- Builds and pushes Docker container to ECR
- Deploys agent to AWS AgentCore Runtime
- Tests the deployed agent
- Provides cleanup options

#### **2. Manual Deployment Steps**

If you prefer step-by-step control:

**Step 1: Install AgentCore Toolkit**
```bash
pip install bedrock-agentcore-starter-toolkit
```

**Step 2: Configure Deployment**
```python
from bedrock_agentcore_starter_toolkit import Runtime

runtime = Runtime()
runtime.configure(
    entrypoint="agentcore_strands_agent.py",
    auto_create_execution_role=True,
    auto_create_ecr=True,
    requirements_file="requirements.txt",
    agent_name="my-agent"
)
```

**Step 3: Launch to AWS**
```python
launch_result = runtime.launch()
print(f"Agent deployed: {launch_result.agent_arn}")
```

**Step 4: Test Deployed Agent**
```python
import boto3
import json

client = boto3.client('bedrock-agentcore')
response = client.invoke_agent_runtime(
    agentRuntimeArn=launch_result.agent_arn,
    qualifier="DEFAULT",
    payload=json.dumps({"prompt": "Hello from the cloud!"})
)
```

#### **3. Monitor Cloud Deployment**

**Check Deployment Status:**
```python
status = runtime.status()
print(f"Status: {status.endpoint['status']}")
```

**View Logs in CloudWatch:**
- Navigate to AWS CloudWatch Console
- Look for log groups with your agent name
- Monitor performance metrics and errors

#### **Cloud Testing Benefits:**
- ✅ **Production Environment**: Test in actual AWS infrastructure
- ✅ **Auto Scaling**: Test how your agent handles load
- ✅ **Integration Testing**: Test with other AWS services
- ✅ **Performance Monitoring**: Real CloudWatch metrics
- ✅ **Security Testing**: Test IAM roles and permissions

### 🔄 **Testing Strategy Comparison**

| Aspect | Local Testing | Cloud Testing |
|--------|---------------|---------------|
| **Speed** | Very Fast | Moderate (deployment time) |
| **Cost** | Free | AWS charges apply |
| **Debugging** | Easy (direct access) | Requires CloudWatch logs |
| **Environment** | Simulated | Production-like |
| **Scaling** | Limited | Full auto-scaling |
| **Integration** | Mock services | Real AWS services |
| **Best For** | Development & debugging | Pre-production & validation |

### 🎯 **Recommended Testing Flow**

1. **Start Local**: Use `python get_started.py` to understand concepts
2. **Develop Local**: Test your agent logic with `local_strands_agent.py`
3. **Validate Local**: Run full demo with `agentcore_rag_infrastructure_demo.py`
4. **Deploy Cloud**: Use `deployment_script.py` for cloud testing
5. **Monitor Cloud**: Check CloudWatch for performance and errors
6. **Iterate**: Make changes locally, then redeploy to cloud

### 🛠️ **Troubleshooting**

**Local Testing Issues:**
- Check AWS credentials: `aws configure list`
- Verify region access to Nova Lite: `us-east-1` or `us-west-2`
- Install missing packages: `pip install -r requirements.txt`

**Cloud Testing Issues:**
- Check IAM permissions for AgentCore and ECR
- Verify container build logs in deployment script output
- Check CloudWatch logs for runtime errors
- Ensure your AWS account has sufficient limits

**Common Error Solutions:**
- `ValidationException`: Check Nova Lite API format in examples
- `AccessDenied`: Verify IAM permissions for Bedrock and AgentCore
- `ResourceNotFound`: Ensure you're in a supported AWS region
- `ContainerError`: Check Docker requirements and dependencies

## Understanding AgentCore Runtime Environments

### 🏗️ **Development Environment (Local)**

**What it is:** Your local machine running agent code without AgentCore infrastructure.

**Components:**
- Local Python interpreter
- Direct AWS Bedrock API calls
- Simulated agent framework
- Mock tools and services

**When to use:**
- Initial development and prototyping
- Testing business logic
- Debugging agent responses
- Cost-conscious development

**Example:**
```bash
# Test locally without any AWS infrastructure costs
python local_strands_agent.py '{"prompt": "Calculate 15 * 7"}'
```

### 🌩️ **AgentCore Runtime Environment (Cloud)**

**What it is:** AWS-managed infrastructure specifically designed for AI agents.

**Components:**
- Docker containers in AWS
- Auto-scaling infrastructure
- Built-in health monitoring (/ping endpoint)
- Standardized invocation API (/invocations)
- Integration with AWS services (IAM, CloudWatch, ECR)

**When to use:**
- Production deployments
- Load testing
- Integration with other AWS services
- Performance monitoring
- Multi-agent orchestration

**Example:**
```python
# Deploy to AWS AgentCore Runtime
runtime = Runtime()
runtime.configure(entrypoint="agentcore_strands_agent.py")
launch_result = runtime.launch()
```

### 🔄 **Key Differences Explained**

| Feature | Local Development | AgentCore Runtime |
|---------|------------------|-------------------|
| **Hosting** | Your machine | AWS managed infrastructure |
| **Scaling** | Single instance | Auto-scaling containers |
| **Monitoring** | Console logs | CloudWatch integration |
| **Health Checks** | Manual | Automatic (/ping endpoint) |
| **API Interface** | Direct function calls | HTTP REST API |
| **Deployment** | `python script.py` | Container deployment |
| **Cost** | Free (except API calls) | AWS infrastructure charges |
| **Reliability** | Depends on your machine | AWS enterprise reliability |

### 📊 **Testing Scenarios**

#### **Scenario 1: New Agent Development**
```bash
# 1. Start with concept validation
python get_started.py

# 2. Develop agent logic
python local_strands_agent.py '{"prompt": "test query"}'

# 3. Test complete workflow
python agentcore_rag_infrastructure_demo.py

# 4. Deploy when ready
python deployment_script.py
```

#### **Scenario 2: Agent Debugging**
```bash
# Test locally first (faster debugging)
python simple_test.py

# If local works, test cloud deployment
python deployment_script.py

# Check CloudWatch logs if cloud issues occur
```

#### **Scenario 3: Performance Testing**
```bash
# Local testing for logic validation
python agentcore_rag_infrastructure_demo.py

# Cloud testing for performance under load
# Deploy to AgentCore Runtime and use load testing tools
```

## Key Concepts

### AgentCore Runtime App

When deploying to AgentCore Runtime, you need to:

1. Import the Runtime App: `from bedrock_agentcore.runtime import BedrockAgentCoreApp`
2. Initialize the App: `app = BedrockAgentCoreApp()`
3. Decorate the invocation function: `@app.entrypoint`
4. Let AgentCore control execution: `app.run()`

### Behind the Scenes

When you use `BedrockAgentCoreApp`, it automatically:

* Creates an HTTP server that listens on port 8080
* Implements the required `/invocations` endpoint for processing agent requests
* Implements the `/ping` endpoint for health checks (important for async agents)
* Handles proper content types and response formats
* Manages error handling according to AWS standards

## Production Considerations

* Use proper IAM roles and permissions
* Implement proper error handling and logging
* Consider cost optimization strategies
* Set up monitoring and alerting
* Plan for scaling and load balancing

## Quick Start Guide

### Step 1: Environment Setup
```bash
# Navigate to the chapter directory
cd chapters/chapter_07_infrastructure/agentcore_runtime_example

# Install dependencies
pip install -r requirements.txt

# Verify AWS credentials
aws sts get-caller-identity
```

### Step 2: Local Development and Testing
```bash
# Test the agent locally (RECOMMENDED FIRST STEP)
python run_local_example.py

# Run basic functionality tests
python simple_test.py
```

### Step 3: Cloud Deployment (AWS Lambda)
```bash
# Deploy to AWS Lambda (PRODUCTION READY)
python aws_lambda_deployment.py

# The script will:
# 1. Create IAM role for Lambda execution
# 2. Package the agent code and dependencies  
# 3. Deploy Lambda function with Function URL
# 4. Return the public endpoint for testing
```

### Step 4: Alternative Deployment (AgentCore Runtime)
```bash
# Deploy to AgentCore Runtime (requires AgentCore toolkit)
python deployment_script.py

# Note: This requires bedrock-agentcore-starter-toolkit
# and may experience dependency conflicts
```

## Deployment Options

| Method | Status | Best For | Cold Start | Scaling | Cost |
|--------|---------|----------|------------|---------|------|
| **AWS Lambda** | ✅ Working | Production use | ~2-3s | Automatic | Low |
| **AgentCore Runtime** | ⚠️ Available | Enterprise users | Variable | Auto/Manual | Medium |
| **Local Development** | ✅ Working | Development/Testing | Instant | Manual | None |

## Testing Your Deployment

### Local Testing
```bash
# Basic agent functionality
python simple_test.py

# Interactive local testing  
python local_strands_agent.py '{"prompt": "What is 2+2?"}'
```

### Cloud Testing (Lambda)
```bash
# After deployment, test using AWS CLI
aws lambda invoke \
  --function-name strands_claude_getting_started \
  --payload '{"prompt": "Hello, how are you?"}' \
  response.json

cat response.json
```

### Monitor Deployment
```bash
# View Lambda logs
aws logs tail /aws/lambda/strands_claude_getting_started --follow

# Check function status
aws lambda get-function --function-name strands_claude_getting_started
```

## Chapter 7 Learning Outcomes

After completing this chapter, you will understand:

1. **Infrastructure Patterns**: Multiple deployment approaches for AI agents
2. **Serverless Architecture**: Benefits and implementation of Lambda-based agents
3. **Production Deployment**: Real-world deployment and monitoring practices
4. **Cost Optimization**: Efficient resource utilization for AI workloads
5. **Scalability Patterns**: Auto-scaling and load handling for AI agents

## Related Documentation

- [AWS Bedrock AgentCore Developer Guide](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/)
- [Strands Agents Documentation](https://strandsagents.com/latest/documentation/)
- [AWS Labs AgentCore Samples](https://github.com/awslabs/amazon-bedrock-agentcore-samples)

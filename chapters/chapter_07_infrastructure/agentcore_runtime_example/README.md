# AWS Bedrock AgentCore Runtime Example

This example demonstrates how to deploy AI agents to AWS Bedrock AgentCore Runtime using the official bedrock-agentcore toolkit. 

## What is AWS Bedrock AgentCore Runtime?

AWS Bedrock AgentCore Runtime is a **managed serverless platform** for hosting and running AI agents in the cloud. It provides:

- **Serverless Execution**: No infrastructure management required
- **Auto-scaling**: Automatically scales based on request volume  
- **Built-in Observability**: CloudWatch logs and metrics integration
- **Secure Environment**: Isolated execution with IAM role-based access
- **HTTP API Access**: RESTful API endpoints for agent invocation

## Architecture Overview

```
┌─────────────────┐    ┌────────────────────┐    ┌─────────────────┐
│   Your Client   │───▶│  AgentCore Runtime │───▶│   Your Agent    │
│                 │    │   (AWS Managed)    │    │ (Python Code)   │
└─────────────────┘    └────────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌────────────────────┐
                       │   AWS Bedrock      │
                       │   Models & Tools   │
                       └────────────────────┘
```

## Project Structure

```
agentcore_runtime_example/
├── my_agent.py                    # Simple AgentCore-compatible agent
├── agentcore_strands_agent.py     # Enhanced agent with Windows Unicode fixes
├── requirements.txt               # Minimal dependencies for AgentCore
├── .bedrock_agentcore.yaml        # Deployment configuration (auto-generated)
├── quick_test.py                  # Quick interactive agent testing
├── test_agentcore_deployment.py   # Comprehensive test suite
├── .venv/                         # Virtual environment
└── README.md                      # This documentation
```

## Quick Start

### 1. Prerequisites

- AWS CLI configured with appropriate permissions
- Python 3.9+ with pip
- Docker (for local testing)

### 2. Setup Virtual Environment

```powershell
# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install required packages
pip install bedrock-agentcore strands-agents
```

### 3. Deploy to AWS

```powershell
# Deploy your agent to AgentCore Runtime
agentcore deploy --file my_agent.py
```

The deployment process will:
- Package your agent code
- Build ARM64 container using AWS CodeBuild
- Deploy to AWS Bedrock AgentCore Runtime
- Provide endpoint URL for API access

### 4. Test Your Agent

After deployment, you can test your agent using our provided testing tools:

#### Quick Test (Recommended for beginners)
```powershell
# Interactive quick test - just enter your endpoint URL
python quick_test.py
```

#### Comprehensive Test Suite
```powershell
# Full functionality testing with detailed results
python test_agentcore_deployment.py --endpoint YOUR_ENDPOINT_URL

# Health check only
python test_agentcore_deployment.py --endpoint YOUR_ENDPOINT_URL --health-only
```

#### Manual Testing Options
- **AWS Bedrock Console**: Test directly in the AgentCore section
- **REST API calls**: Use curl, Postman, or similar tools
- **AWS SDK integration**: Programmatic access via boto3

## Understanding the Code

### Simple Agent (`my_agent.py`)

```python
from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent

app = BedrockAgentCoreApp()

@app.entrypoint
def invoke(payload):
    """Main entry point for AgentCore Runtime."""
    agent = Agent()
    result = agent.run(payload.get("query", "Hello from AgentCore!"))
    return {"result": result.message}
```

**Key Components:**
- `BedrockAgentCoreApp`: Main application wrapper for AgentCore compatibility
- `@app.entrypoint`: Decorator marking the function AWS will call
- `payload`: Input from AgentCore containing request data
- Return value: Must be JSON-serializable dictionary

### Enhanced Agent (`agentcore_strands_agent.py`)

Includes Windows Unicode support for proper console output:

```python
import sys
import io

# Windows Unicode fix
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
```

## Configuration File (`.bedrock_agentcore.yaml`)

Auto-generated during deployment:

```yaml
agent:
  name: my-agent
  description: AgentCore runtime example
  memory: 1024Mi
  timeout: 30s
execution_role: arn:aws:iam::ACCOUNT:role/bedrock-agentcore-execution-role
```

## Troubleshooting

### Common Issues

1. **Unicode Encoding Errors (Windows)**
   - **Symptom**: Console shows garbled characters or encoding errors
   - **Solution**: Use `agentcore_strands_agent.py` with UTF-8 wrapper

2. **PowerShell JSON Escaping**
   - **Symptom**: JSON arguments fail in PowerShell commands
   - **Solution**: Use single quotes and escape properly:
   ```powershell
   agentcore invoke --input '{\"query\": \"test\"}'
   ```

3. **Package Dependencies**
   - **Symptom**: Import errors or version conflicts
   - **Solution**: Use minimal `requirements.txt` with only essential packages:
   ```
   bedrock-agentcore
   strands-agents
   ```

4. **IAM Permissions**
   - **Symptom**: Deployment fails with permission errors
   - **Solution**: Ensure your AWS credentials have:
     - `bedrock:*` permissions
     - `codebuild:*` permissions
     - `ecr:*` permissions
5. **Testing Issues**
   - **Symptom**: Test scripts fail to connect or get responses
   - **Solution**: 
     - Verify endpoint URL from AWS Console
     - Ensure agent status is "Ready" 
     - Check network connectivity and firewall settings
     - Install test dependencies: `pip install requests boto3`

### Deployment Status

Check deployment status in AWS Console:
1. Go to AWS Bedrock Console
2. Navigate to "AgentCore" section
3. Look for your agent with "Ready" status

### Testing Your Deployment

Use the provided test scripts to validate your deployment:

```powershell
# Quick interactive test (recommended first step)
python quick_test.py

# Comprehensive test suite with detailed reporting
python test_agentcore_deployment.py --endpoint YOUR_ENDPOINT_URL
```

**Test Script Features:**
- ✅ Health check validation
- 🧪 Multiple test scenarios
- 📊 Performance metrics
- 🔍 Detailed error reporting
- 💡 Troubleshooting guidance

### Logs and Monitoring

- **CloudWatch Logs**: Automatic logging of agent execution
- **CloudWatch Metrics**: Performance and usage metrics
- **AWS X-Ray**: Request tracing (if enabled)

## Learning Exercises

### Exercise 1: Basic Deployment & Testing
1. Deploy the simple agent using `my_agent.py`
2. Run the quick test: `python quick_test.py`
3. Use comprehensive testing: `python test_agentcore_deployment.py --endpoint YOUR_URL`
4. Check CloudWatch logs for execution traces

### Exercise 2: Custom Agent Logic
1. Modify the agent to handle different query types
2. Add error handling and logging
3. Redeploy and test the changes using the test scripts

### Exercise 3: Tool Integration
1. Add external API calls or database connections
2. Use Strands framework tools and capabilities
3. Test end-to-end functionality

### Exercise 4: Production Configuration
1. Configure custom memory and timeout settings
2. Set up proper IAM roles and permissions
3. Add monitoring and alerting

## Key Concepts to Remember

- **AgentCore Runtime** = AWS managed serverless platform for AI agents
- **Minimal Dependencies** = Only include essential packages in requirements.txt
- **ARM64 Architecture** = AgentCore uses ARM64 containers for efficiency
- **@app.entrypoint** = Required decorator for AgentCore function discovery
- **JSON Serializable** = All return values must be JSON-compatible
- **IAM Execution Role** = Required for agent runtime permissions

## Next Steps

1. **Explore Advanced Features**: Custom tools, multi-step workflows, external integrations
2. **Production Deployment**: CI/CD pipelines, staging environments, monitoring
3. **Scale Considerations**: Performance optimization, cost management, multi-region deployment
4. **Security Best Practices**: Least privilege IAM, secret management, audit logging

## Resources

- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Strands Agents Framework](https://github.com/strands-ai/strands)
- [AgentCore Starter Toolkit](https://github.com/aws-samples/bedrock-agentcore-starter-toolkit)
- [AWS CLI Configuration Guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)

---

**Status**: ✅ Successfully deployed to AWS Bedrock AgentCore Runtime
**Agent Status**: Ready and accessible via AWS Console
**Last Updated**: Student learning documentation prepared

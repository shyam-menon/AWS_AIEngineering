# AWS Bedrock AgentCore Runtime Example

This example demonstrates how to deploy AI agents to AWS Bedrock AgentCore Runtime using the Strands framework and Amazon Nova Lite v1:0 model.

## What is AWS Bedrock AgentCore Runtime?

AWS Bedrock AgentCore Runtime is a **managed serverless platform** for hosting and running AI agents in the cloud. It provides:

- **Serverless Execution**: No infrastructure management required
- **Auto-scaling**: Automatically scales based on request volume  
- **Built-in Observability**: CloudWatch logs and metrics integration
- **Secure Environment**: Isolated execution with IAM role-based access
- **AWS API Access**: Accessible via AgentCore CLI and AWS SDKs (not traditional HTTP endpoints)

## Architecture Overview

```
┌─────────────────┐    ┌────────────────────┐    ┌─────────────────┐
│   AgentCore     │───▶│  AgentCore Runtime │───▶│   Your Agent    │
│   CLI / AWS SDK │    │   (AWS Managed)    │    │ (Python Code)   │
└─────────────────┘    └────────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌────────────────────┐
                       │   Amazon Nova      │
                       │   Lite v1:0        │
                       └────────────────────┘
```

## Project Structure

```
agentcore_runtime_example/
├── my_agent.py                    # AgentCore agent using Amazon Nova Lite v1:0
├── agentcore_strands_agent.py     # Alternative agent implementation  
├── requirements.txt               # Python dependencies for deployment
├── .bedrock_agentcore.yaml        # AgentCore deployment configuration
├── agentcore_cli_test.py          # Proper AgentCore testing via CLI
├── quick_test.py                  # HTTP-based test (for learning about wrong approach)
├── test_agentcore_deployment.py   # Comprehensive test suite
├── .dockerignore                  # Docker build exclusions
├── Dockerfile                     # Container configuration
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
agentcore launch
```

The deployment process will:
- Package your agent code into ARM64 container
- Build using AWS CodeBuild  
- Deploy to AWS Bedrock AgentCore Runtime
- Provide Agent ARN for API access

### 4. Test Your Agent

After deployment, you can test your agent using the AgentCore CLI:

#### Recommended Testing Approach
```powershell
# Test via AgentCore CLI (correct method)
agentcore invoke '{"input": "Hello! Can you introduce yourself?"}'

# Check deployment status
agentcore status
```

#### Automated Testing Scripts
```powershell
# CLI-based testing (recommended)
python agentcore_cli_test.py

# Comprehensive test suite (for detailed analysis)
python test_agentcore_deployment.py --arn YOUR_AGENT_ARN
```

#### Important Note About HTTP Testing
The `quick_test.py` script demonstrates a **common mistake**: trying to use HTTP requests with AgentCore ARNs. AgentCore agents are **not accessible via HTTP endpoints** - they use AWS APIs. This script is included for educational purposes to show the wrong approach.

**❌ Wrong Approach:**
```python
# This fails - ARNs are not HTTP URLs
requests.post("https://arn:aws:bedrock-agentcore:...", json=payload)
```

**✅ Correct Approach:**
```powershell
# Use AgentCore CLI or AWS SDK
agentcore invoke '{"input": "your question"}'
```

## Understanding the Code

### Simple Agent (`my_agent.py`)

```python
from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent
from strands.models import BedrockModel

app = BedrockAgentCoreApp()

@app.entrypoint
def invoke(payload):
    """Main entry point for AgentCore Runtime."""
    # Use Amazon Nova Lite v1:0 - accessible model
    model = BedrockModel(model_id="us.amazon.nova-lite-v1:0")
    agent = Agent(model=model)
    
    user_input = payload.get("input", "Hello from AgentCore!")
    result = agent.run(user_input)
    return {"result": result}
```

**Key Components:**
- `BedrockAgentCoreApp`: Main application wrapper for AgentCore compatibility
- `@app.entrypoint`: Decorator marking the function AWS will call
- `BedrockModel`: Configured to use Amazon Nova Lite v1:0 (accessible model)
- `payload`: Input from AgentCore containing request data
- Return value: Must be JSON-serializable dictionary

### Enhanced Agent (`agentcore_strands_agent.py`)

Alternative implementation with additional configuration options.

## Deployment Configuration (`.bedrock_agentcore.yaml`)

Auto-generated during deployment with your specific agent details:

```yaml
default_agent: my_agent
agents:
  my_agent:
    name: my_agent
    entrypoint: my_agent.py
    platform: linux/arm64
    container_runtime: docker
    aws:
      account: '724772080977'
      region: us-east-1
      execution_role: arn:aws:iam::724772080977:role/AmazonBedrockAgentCoreSDKRuntime-us-east-1-xxx
    bedrock_agentcore:
      agent_id: my_agent-xxxx
      agent_arn: arn:aws:bedrock-agentcore:us-east-1:724772080977:runtime/my_agent-xxxx
      agent_session_id: xxxx-xxxx-xxxx-xxxx
```

## Troubleshooting

### Common Issues

1. **Model Access Denied**
   - **Symptom**: Claude Sonnet 4 or other models return access denied errors
   - **Solution**: Use Amazon Nova Lite v1:0 which is generally accessible:
   ```python
   model = BedrockModel(model_id="us.amazon.nova-lite-v1:0")
   ```

2. **Incorrect Strands Agent Syntax**
   - **Symptom**: Agent() constructor errors about model parameters
   - **Solution**: Pass model to Agent constructor:
   ```python
   model = BedrockModel(model_id="us.amazon.nova-lite-v1:0") 
   agent = Agent(model=model)  # Correct syntax
   ```

3. **Testing with Wrong Method**
   - **Symptom**: HTTP requests fail when testing AgentCore agents
   - **Solution**: Use `agentcore invoke` CLI command instead of HTTP requests
   ```powershell
   # Correct: Use CLI
   agentcore invoke '{"input": "test message"}'
   
   # Wrong: HTTP requests to ARNs fail
   curl https://arn:aws:bedrock-agentcore:...
   ```

4. **PowerShell JSON Escaping**
   - **Symptom**: JSON arguments fail in PowerShell commands
   - **Solution**: Use proper escaping or file-based input:
   ```powershell
   # Method 1: Proper escaping
   agentcore invoke '{\"input\": \"test\"}'
   
   # Method 2: Use test scripts
   python agentcore_cli_test.py
   ```

5. **Unicode Encoding Errors (Windows)**
   - **Symptom**: Console shows garbled characters or encoding errors
   - **Solution**: Use `agentcore_strands_agent.py` with UTF-8 wrapper

6. **IAM Permissions**
   - **Symptom**: Deployment fails with permission errors
   - **Solution**: Ensure your AWS credentials have bedrock-agentcore permissions

### Deployment Status

Check deployment status using AgentCore CLI:
```powershell
# Check current status
agentcore status

# View agent details including ARN and endpoint status
```

Or check in AWS Console:
1. Go to AWS Bedrock Console
2. Navigate to "AgentCore" section
3. Look for your agent with "READY" status

### Testing Your Deployment

Use the provided test scripts to validate your deployment:

```powershell
# CLI-based testing (recommended approach)
python agentcore_cli_test.py

# Manual CLI testing
agentcore invoke '{"input": "Hello! Can you introduce yourself?"}'

# Check deployment status
agentcore status
```

**Test Script Features:**
- ✅ Uses correct AgentCore CLI approach
- 🧪 Multiple test scenarios  
- 📊 Success rate reporting
- 🔍 Detailed error handling
- 💡 Educational value

### Logs and Monitoring

- **CloudWatch Logs**: Automatic logging of agent execution
- **CloudWatch Metrics**: Performance and usage metrics
- **AWS X-Ray**: Request tracing (if enabled)

## Learning Exercises

### Exercise 1: Basic Deployment & Testing
1. Deploy the agent using `agentcore launch`
2. Test via CLI: `agentcore invoke '{"input": "Hello"}'`
3. Run automated testing: `python agentcore_cli_test.py`
4. Check CloudWatch logs for execution traces

### Exercise 2: Understanding Wrong vs Right Testing Approaches
1. Try the HTTP-based `quick_test.py` and observe why it fails
2. Use the CLI-based `agentcore_cli_test.py` and see the success
3. Learn the difference between ARNs and HTTP endpoints
4. Understand AgentCore's AWS API-based architecture

### Exercise 3: Model Configuration
1. Experiment with different accessible models (Nova Lite, etc.)
2. Update the BedrockModel configuration
3. Redeploy and test the changes
4. Compare responses from different models

### Exercise 4: Production Configuration
1. Configure custom memory and timeout settings
2. Set up proper IAM roles and permissions
3. Add monitoring and alerting

## Key Concepts to Remember

- **AgentCore Runtime** = AWS managed serverless platform for AI agents
- **ARNs vs URLs** = AgentCore uses ARNs, not HTTP endpoints for access
- **AgentCore CLI** = Correct way to test and invoke deployed agents  
- **Amazon Nova Lite v1:0** = Accessible foundation model for learning
- **BedrockModel Configuration** = Proper way to specify models in Strands agents
- **ARM64 Architecture** = AgentCore uses ARM64 containers for efficiency
- **@app.entrypoint** = Required decorator for AgentCore function discovery
- **JSON Serializable** = All return values must be JSON-compatible

## Key Lessons Learned

1. **Model Access**: Not all Bedrock models are accessible by default - use Nova Lite v1:0 for learning
2. **Testing Methods**: AgentCore agents use AWS APIs, not HTTP endpoints
3. **Syntax Matters**: Strands Agent() constructor requires model parameter when using custom models
4. **Deployment Process**: `agentcore launch` builds ARM64 containers via AWS CodeBuild
5. **Debugging**: CloudWatch logs and `agentcore status` are essential for troubleshooting

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
**Agent ARN**: `arn:aws:bedrock-agentcore:us-east-1:724772080977:runtime/my_agent-i6J8qPAzIl`  
**Model**: Amazon Nova Lite v1:0  
**Testing**: Verified working via `agentcore invoke` CLI  
**Last Updated**: September 4, 2025 - Production deployment validated

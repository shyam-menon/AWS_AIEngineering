"""
Deployment script for AgentCore Runtime.
This script handles the configuration and deployment of the Strands agent to AWS Bedrock AgentCore Runtime.
"""

import boto3
import json
import time
from boto3.session import Session


def check_agentcore_toolkit():
    """Check if AgentCore toolkit is available"""
    try:
        from bedrock_agentcore_starter_toolkit import Runtime
        return True, Runtime
    except ImportError:
        return False, None


def deploy_agent_with_toolkit():
    """
    Deploy the Strands agent using the AgentCore Starter Toolkit
    (This requires the official AWS AgentCore toolkit)
    """
    
    toolkit_available, Runtime = check_agentcore_toolkit()
    
    if not toolkit_available:
        print("❌ AgentCore Starter Toolkit not available")
        print("\n💡 The bedrock_agentcore_starter_toolkit is required for automated deployment.")
        print("This toolkit may require:")
        print("1. Special AWS permissions or preview access")
        print("2. Installation from AWS-specific repositories")
        print("3. AWS Partner or Enterprise account access")
        print("\n🔄 Please use the manual deployment approach below instead.")
        return None
    
    # Get AWS session and region
    boto_session = Session()
    region = boto_session.region_name
    print(f"Deploying to region: {region}")
    
    # Initialize AgentCore Runtime
    agentcore_runtime = Runtime()
    agent_name = "strands_claude_getting_started"
    
    print("Configuring AgentCore Runtime deployment...")
    
    # Configure the deployment
    response = agentcore_runtime.configure(
        entrypoint="agentcore_strands_agent.py",
        auto_create_execution_role=True,
        auto_create_ecr=True,
        requirements_file="requirements.txt",
        region=region,
        agent_name=agent_name
    )
    
    print(f"Configuration response: {response}")
    
    # Launch the agent to AgentCore Runtime
    print("Launching agent to AgentCore Runtime...")
    launch_result = agentcore_runtime.launch()
    
    print(f"Launch initiated. Agent ARN: {launch_result.agent_arn}")
    
    # Check deployment status
    print("Checking deployment status...")
    status_response = agentcore_runtime.status()
    status = status_response.endpoint['status']
    end_status = ['READY', 'CREATE_FAILED', 'DELETE_FAILED', 'UPDATE_FAILED']
    
    while status not in end_status:
        print(f"Current status: {status}")
        time.sleep(10)
        status_response = agentcore_runtime.status()
        status = status_response.endpoint['status']
    
    print(f"Final status: {status}")
    
    if status == 'READY':
        print("✅ Agent successfully deployed to AgentCore Runtime!")
        return {
            'agent_arn': launch_result.agent_arn,
            'ecr_uri': launch_result.ecr_uri,
            'status': status
        }
    else:
        print("❌ Deployment failed!")
        return {'status': status, 'error': 'Deployment failed'}


def deploy_agent_manually():
    """
    Manual deployment approach using direct AWS APIs
    This demonstrates the concepts without requiring the AgentCore toolkit
    """
    
    print("\n" + "="*60)
    print("🔧 MANUAL AGENTCORE DEPLOYMENT GUIDE")
    print("="*60)
    
    print("\nSince the AgentCore Starter Toolkit isn't available, here's how to deploy manually:")
    
    # Step 1: Create ECR Repository
    print("\n1️⃣ Create ECR Repository:")
    print("""
# Create ECR repository for your agent
aws ecr create-repository --repository-name my-strands-agent --region us-east-1

# Get login token
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
    """)
    
    # Step 2: Build Docker Image
    print("\n2️⃣ Build Docker Image:")
    print("""
# Create a Dockerfile for your agent
cat > Dockerfile << EOF
FROM public.ecr.aws/lambda/python:3.12

# Copy requirements and install
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy agent code
COPY agentcore_strands_agent.py .

# Set the entrypoint
CMD ["python", "agentcore_strands_agent.py"]
EOF

# Build and tag the image
docker build -t my-strands-agent .
docker tag my-strands-agent:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/my-strands-agent:latest
    """)
    
    # Step 3: Push to ECR
    print("\n3️⃣ Push to ECR:")
    print("""
# Push the image
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/my-strands-agent:latest
    """)
    
    # Step 4: Create IAM Role
    print("\n4️⃣ Create IAM Role:")
    print("""
# Create execution role with necessary permissions
aws iam create-role --role-name AgentCoreExecutionRole --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"Service": "bedrock-agentcore.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }
    ]
}'

# Attach necessary policies
aws iam attach-role-policy --role-name AgentCoreExecutionRole --policy-arn arn:aws:iam::aws:policy/service-role/AmazonBedrockFullAccess
    """)
    
    # Step 5: Deploy to AgentCore
    print("\n5️⃣ Deploy to AgentCore Runtime:")
    print("""
# Use AWS CLI or boto3 to create AgentCore Runtime
aws bedrock-agentcore create-agent-runtime \\
    --agent-runtime-name my-strands-agent \\
    --role-arn arn:aws:iam::<account-id>:role/AgentCoreExecutionRole \\
    --agent-runtime-artifact containerConfiguration='{containerUri=<account-id>.dkr.ecr.us-east-1.amazonaws.com/my-strands-agent:latest}'
    """)
    
    # Alternative: Show boto3 approach
    print("\n📝 Alternative: Using boto3 directly:")
    
    try:
        # Try to create AgentCore client
        agentcore_control = boto3.client('bedrock-agentcore-control')
        print("✅ AgentCore Control client available")
        
        print("""
# Python code for manual deployment:
import boto3

client = boto3.client('bedrock-agentcore-control')
response = client.create_agent_runtime(
    agentRuntimeName='my-strands-agent',
    roleArn='arn:aws:iam::<account-id>:role/AgentCoreExecutionRole',
    agentRuntimeArtifact={
        'containerConfiguration': {
            'containerUri': '<account-id>.dkr.ecr.us-east-1.amazonaws.com/my-strands-agent:latest'
        }
    },
    networkConfiguration={'networkMode': 'PUBLIC'}
)
        """)
        
    except Exception as e:
        print(f"⚠️ AgentCore Control client not available: {e}")
        print("This may indicate that AgentCore is in preview or requires special access.")
    
    return True


def simulate_deployment():
    """
    Simulate the deployment process for educational purposes
    """
    print("\n" + "="*60)
    print("🎭 SIMULATED DEPLOYMENT (Educational)")
    print("="*60)
    
    print("\nThis simulation shows what would happen during real deployment:")
    
    steps = [
        "📦 Packaging agent code into Docker container...",
        "🏗️ Building container image...", 
        "📤 Pushing to Amazon ECR...",
        "🚀 Creating AgentCore Runtime...",
        "⚙️ Configuring auto-scaling...",
        "🔍 Setting up health checks...",
        "🌐 Exposing API endpoints...",
        "✅ Deployment complete!"
    ]
    
    for i, step in enumerate(steps, 1):
        print(f"\n{i}. {step}")
        time.sleep(1)  # Simulate processing time
        
        if i == 4:
            print("   🔗 Agent ARN: arn:aws:bedrock-agentcore:us-east-1:123456789012:agent-runtime/my-strands-agent")
        elif i == 7:
            print("   🌐 Invocation endpoint: /invocations")
            print("   ❤️ Health check endpoint: /ping")
    
    # Show how to test the deployed agent
    print("\n🧪 Testing Deployed Agent:")
    print("""
import boto3
import json

client = boto3.client('bedrock-agentcore')
response = client.invoke_agent_runtime(
    agentRuntimeArn='arn:aws:bedrock-agentcore:us-east-1:123456789012:agent-runtime/my-strands-agent',
    qualifier='DEFAULT',
    payload=json.dumps({'prompt': 'Hello from AgentCore!'})
)

print(response)
    """)
    
    return {
        'status': 'SIMULATED',
        'agent_arn': 'arn:aws:bedrock-agentcore:us-east-1:123456789012:agent-runtime/my-strands-agent',
        'note': 'This was a simulation for educational purposes'
    }


def test_deployed_agent(agent_arn, region):
    """
    Test the deployed agent by invoking it with a sample payload
    
    Args:
        agent_arn (str): ARN of the deployed agent
        region (str): AWS region
    """
    
    print("\nTesting deployed agent...")
    
    # Create AgentCore client
    agentcore_client = boto3.client('bedrock-agentcore', region_name=region)
    
    # Test payloads
    test_payloads = [
        {"prompt": "What is 2+2?"},
        {"prompt": "What is the weather like?"},
        {"prompt": "Calculate 15 * 7 and tell me the weather"}
    ]
    
    for i, payload in enumerate(test_payloads, 1):
        print(f"\n--- Test {i}: {payload['prompt']} ---")
        
        try:
            response = agentcore_client.invoke_agent_runtime(
                agentRuntimeArn=agent_arn,
                qualifier="DEFAULT",
                payload=json.dumps(payload)
            )
            
            # Handle streaming response
            if "text/event-stream" in response.get("contentType", ""):
                content = []
                for line in response["response"].iter_lines(chunk_size=1):
                    if line:
                        line = line.decode("utf-8")
                        if line.startswith("data: "):
                            line = line[6:]
                            content.append(line)
                result = "\n".join(content)
            else:
                # Handle non-streaming response
                events = []
                for event in response.get("response", []):
                    events.append(event)
                result = json.loads(events[0].decode("utf-8")) if events else "No response"
            
            print(f"Response: {result}")
            
        except Exception as e:
            print(f"Error invoking agent: {e}")


def cleanup_resources(launch_result, region):
    """
    Clean up AWS resources created during deployment
    
    Args:
        launch_result: Result object from the launch operation
        region (str): AWS region
    """
    
    print("\nCleaning up resources...")
    
    try:
        # Create clients
        agentcore_control_client = boto3.client('bedrock-agentcore-control', region_name=region)
        ecr_client = boto3.client('ecr', region_name=region)
        
        # Delete agent runtime
        if hasattr(launch_result, 'agent_id'):
            print(f"Deleting agent runtime: {launch_result.agent_id}")
            agentcore_control_client.delete_agent_runtime(agentRuntimeId=launch_result.agent_id)
        
        # Delete ECR repository
        if hasattr(launch_result, 'ecr_uri'):
            repository_name = launch_result.ecr_uri.split('/')[1]
            print(f"Deleting ECR repository: {repository_name}")
            ecr_client.delete_repository(repositoryName=repository_name, force=True)
        
        print("✅ Cleanup completed!")
        
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")


def main():
    """
    Main deployment function that tries different approaches
    """
    print("🚀 AgentCore Runtime Deployment Script")
    print("=" * 50)
    
    # First, try the automated approach with toolkit
    print("\n🔍 Checking for AgentCore Starter Toolkit...")
    result = deploy_agent_with_toolkit()
    
    if result is None:
        # If toolkit isn't available, show manual approach
        print("\n🔧 Showing manual deployment approach...")
        deploy_agent_manually()
        
        # Run simulation for educational purposes
        print("\n🎭 Running deployment simulation...")
        sim_result = simulate_deployment()
        
        return sim_result
    else:
        return result


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--cleanup":
        print("Cleanup mode - this would require launch_result from previous deployment")
        print("For full cleanup, run the deployment script and use the returned launch_result")
        sys.exit(0)
    
    try:
        # Deploy the agent
        result = main()
        print(f"\n✅ Deployment process completed!")
        print(f"Result: {json.dumps(result, indent=2)}")
        
    except Exception as e:
        print(f"\n❌ Error during deployment: {e}")
        print("\n💡 This is expected if you don't have access to AgentCore toolkit yet.")
        print("Use the manual deployment guide above for production deployment.")
    
    print("\nDeployment script completed!")

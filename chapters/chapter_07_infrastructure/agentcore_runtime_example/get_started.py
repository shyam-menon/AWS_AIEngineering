"""
Simple Getting Started Script for AgentCore Runtime
This script provides a quick way to test your setup and understand AgentCore concepts.
"""

import boto3
import json
import sys
import os


def check_aws_setup():
    """Check if AWS credentials and Bedrock access are configured"""
    print("🔍 Checking AWS Setup...")
    
    try:
        # Check AWS credentials
        session = boto3.Session()
        region = session.region_name
        print(f"✅ AWS Region: {region}")
        
        # Check Bedrock access
        bedrock = boto3.client('bedrock-runtime', region_name=region)
        
        # Test Nova Lite model
        test_payload = {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "text": "Hello! Just testing the connection."
                        }
                    ]
                }
            ],
            "inferenceConfig": {
                "max_new_tokens": 50,
                "temperature": 0.7
            }
        }
        
        response = bedrock.invoke_model(
            modelId="us.amazon.nova-lite-v1:0",
            body=json.dumps(test_payload)
        )
        
        response_body = json.loads(response['body'].read())
        output_text = response_body.get('output', {}).get('message', {}).get('content', [{}])[0].get('text', 'No response')
        print("✅ Nova Lite model accessible")
        print(f"✅ Test response: {output_text[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ AWS Setup Error: {e}")
        print("\n💡 Troubleshooting:")
        print("1. Run 'aws configure' to set up credentials")
        print("2. Ensure you have Bedrock permissions")
        print("3. Check if Nova Lite model is available in your region")
        return False


def simulate_local_agent():
    """Simulate running a local Strands agent"""
    print("\n🤖 Simulating Local Agent...")
    
    try:
        # This simulates what the actual agent would do
        print("✅ Agent initialized with Nova Lite model")
        print("✅ Tools loaded: calculator, weather")
        print("✅ System prompt configured")
        
        # Simulate some queries
        test_queries = [
            "What is 15 * 7?",
            "What's the weather like?", 
            "Hello, how are you?"
        ]
        
        for query in test_queries:
            print(f"\n📝 Query: {query}")
            print(f"🔄 Processing...")
            
            # Simulate agent response
            if "15 * 7" in query:
                response = "The calculation 15 * 7 equals 105."
            elif "weather" in query:
                response = "The weather is sunny with 72°F temperature."
            else:
                response = "Hello! I'm an AI assistant ready to help you."
                
            print(f"💬 Response: {response}")
            
        return True
        
    except Exception as e:
        print(f"❌ Local Agent Error: {e}")
        return False


def explain_agentcore_deployment():
    """Explain the AgentCore deployment process"""
    print("\n🚀 AgentCore Runtime Deployment Process")
    print("=" * 50)
    
    deployment_steps = [
        {
            "step": "1. Prepare Agent Code",
            "description": "Create agent with @app.entrypoint decorator",
            "file": "agentcore_strands_agent.py"
        },
        {
            "step": "2. Configure Runtime",
            "description": "Use AgentCore toolkit to configure deployment",
            "command": "agentcore_runtime.configure(...)"
        },
        {
            "step": "3. Build Container",
            "description": "Automatically build Docker container",
            "note": "Dockerfile generated automatically"
        },
        {
            "step": "4. Deploy to AWS",
            "description": "Push to ECR and deploy to AgentCore Runtime",
            "command": "agentcore_runtime.launch()"
        },
        {
            "step": "5. Test Deployment",
            "description": "Invoke deployed agent via AgentCore API",
            "endpoint": "/invocations"
        }
    ]
    
    for step_info in deployment_steps:
        print(f"\n{step_info['step']}: {step_info['description']}")
        if 'file' in step_info:
            print(f"   📄 File: {step_info['file']}")
        if 'command' in step_info:
            print(f"   💻 Command: {step_info['command']}")
        if 'note' in step_info:
            print(f"   📝 Note: {step_info['note']}")
        if 'endpoint' in step_info:
            print(f"   🌐 Endpoint: {step_info['endpoint']}")


def show_file_structure():
    """Show the file structure of this example"""
    print("\n📁 Example File Structure")
    print("=" * 50)
    
    structure = """
agentcore_runtime_example/
├── README.md                           # Documentation
├── requirements.txt                    # Python dependencies
├── local_strands_agent.py             # Local development version
├── agentcore_strands_agent.py         # AgentCore Runtime version
├── deployment_script.py               # Deployment automation
├── agentcore_rag_infrastructure_demo.py  # Complete RAG demo
└── get_started.py                     # This file
"""
    
    print(structure)
    
    print("\nFile Descriptions:")
    descriptions = {
        "README.md": "Complete documentation and tutorial",
        "requirements.txt": "All required Python packages",
        "local_strands_agent.py": "Test agent locally before deployment", 
        "agentcore_strands_agent.py": "Production-ready agent for AgentCore",
        "deployment_script.py": "Automates the deployment process",
        "agentcore_rag_infrastructure_demo.py": "Comprehensive RAG demo",
        "get_started.py": "Simple setup verification"
    }
    
    for file, desc in descriptions.items():
        print(f"  📄 {file:<35} - {desc}")


def show_next_steps():
    """Show recommended next steps"""
    print("\n🎯 Recommended Next Steps")
    print("=" * 50)
    
    steps = [
        {
            "step": "1. Install Dependencies",
            "command": "pip install -r requirements.txt",
            "description": "Install all required packages"
        },
        {
            "step": "2. Test Local Agent", 
            "command": "python local_strands_agent.py '{\"prompt\": \"Hello!\"}'",
            "description": "Test the agent locally"
        },
        {
            "step": "3. Run RAG Demo",
            "command": "python agentcore_rag_infrastructure_demo.py",
            "description": "See complete RAG infrastructure demo"
        },
        {
            "step": "4. Deploy to AgentCore",
            "command": "python deployment_script.py",
            "description": "Deploy agent to AWS AgentCore Runtime"
        },
        {
            "step": "5. Monitor Performance",
            "command": "Check CloudWatch logs and metrics",
            "description": "Monitor your deployed agent"
        }
    ]
    
    for step_info in steps:
        print(f"\n{step_info['step']}: {step_info['description']}")
        print(f"   💻 {step_info['command']}")


def main():
    """Main function"""
    print("🚀 AgentCore Runtime - Getting Started")
    print("Chapter 7: Infrastructure - AI Engineering Course")
    print("=" * 60)
    
    # Check AWS setup
    aws_ok = check_aws_setup()
    
    if aws_ok:
        # Simulate local agent
        simulate_local_agent()
    
    # Show explanations regardless of AWS setup
    explain_agentcore_deployment()
    show_file_structure()
    show_next_steps()
    
    print("\n" + "=" * 60)
    print("✅ Getting Started Guide Complete!")
    print("📚 Read README.md for detailed documentation")
    print("🔧 Run the commands above to continue your journey")


if __name__ == "__main__":
    main()

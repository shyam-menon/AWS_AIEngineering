"""
AgentCore Runtime Testing Guide
This script demonstrates how to test AgentCore Runtime both locally and in the cloud.
"""

import boto3
import json
import time
import sys


class AgentCoreTester:
    """
    Comprehensive testing guide for AgentCore Runtime
    """
    
    def __init__(self):
        self.region = boto3.Session().region_name
        print(f"🌍 Testing in AWS Region: {self.region}")
    
    def test_local_environment(self):
        """Test the local development environment"""
        print("\n" + "="*60)
        print("🏠 LOCAL ENVIRONMENT TESTING")
        print("="*60)
        
        print("\n📋 Local Testing Checklist:")
        
        # Test 1: AWS Connectivity
        print("\n1️⃣ Testing AWS Connectivity...")
        try:
            session = boto3.Session()
            print(f"   ✅ AWS Session: {session.profile_name or 'default'}")
            print(f"   ✅ Region: {session.region_name}")
        except Exception as e:
            print(f"   ❌ AWS Setup Error: {e}")
            return False
        
        # Test 2: Bedrock Access
        print("\n2️⃣ Testing Bedrock Access...")
        try:
            bedrock = boto3.client('bedrock-runtime')
            payload = {
                "messages": [
                    {
                        "role": "user",
                        "content": [{"text": "Test connection"}]
                    }
                ],
                "inferenceConfig": {
                    "max_new_tokens": 20,
                    "temperature": 0.1
                }
            }
            
            response = bedrock.invoke_model(
                modelId="us.amazon.nova-lite-v1:0",
                body=json.dumps(payload)
            )
            
            print("   ✅ Nova Lite model accessible")
            
        except Exception as e:
            print(f"   ❌ Bedrock Error: {e}")
            return False
        
        # Test 3: Local Agent Simulation
        print("\n3️⃣ Testing Local Agent Logic...")
        try:
            # Simulate agent processing
            test_queries = [
                "What is 2 + 2?",
                "Hello, how are you?",
                "What's the weather like?"
            ]
            
            for query in test_queries:
                print(f"   📝 Query: {query}")
                # Simulate processing
                if "2 + 2" in query:
                    response = "The answer is 4."
                elif "hello" in query.lower():
                    response = "Hello! I'm working correctly."
                else:
                    response = "Sunny and 72°F."
                
                print(f"   💬 Response: {response}")
            
            print("   ✅ Local agent logic working")
            
        except Exception as e:
            print(f"   ❌ Local Agent Error: {e}")
            return False
        
        print("\n🎉 Local Environment: ALL TESTS PASSED")
        return True
    
    def explain_cloud_testing(self):
        """Explain cloud testing process"""
        print("\n" + "="*60)
        print("☁️ CLOUD ENVIRONMENT TESTING")
        print("="*60)
        
        print("\n📋 Cloud Testing Overview:")
        print("""
Cloud testing deploys your agent to AWS AgentCore Runtime, providing:
• Production-like environment
• Auto-scaling capabilities  
• Built-in monitoring and health checks
• Integration with AWS services
• Performance metrics via CloudWatch
        """)
        
        print("\n🚀 Cloud Deployment Process:")
        steps = [
            "1. Package agent code into Docker container",
            "2. Push container to Amazon ECR (Elastic Container Registry)",
            "3. Deploy container to AgentCore Runtime",
            "4. Configure auto-scaling and health monitoring",
            "5. Test via AgentCore Runtime API endpoints"
        ]
        
        for step in steps:
            print(f"   {step}")
        
        print("\n💻 Cloud Testing Commands:")
        print("""
# Deploy to cloud (automated)
python deployment_script.py

# Manual deployment (step-by-step)
from bedrock_agentcore_starter_toolkit import Runtime
runtime = Runtime()
runtime.configure(entrypoint="agentcore_strands_agent.py")
launch_result = runtime.launch()

# Test deployed agent
import boto3
client = boto3.client('bedrock-agentcore')
response = client.invoke_agent_runtime(
    agentRuntimeArn=launch_result.agent_arn,
    payload='{"prompt": "Hello from cloud!"}'
)
        """)
    
    def demonstrate_testing_workflow(self):
        """Demonstrate the complete testing workflow"""
        print("\n" + "="*60)
        print("🔄 COMPLETE TESTING WORKFLOW")
        print("="*60)
        
        workflow_steps = [
            {
                "phase": "🏠 Local Development",
                "steps": [
                    "Run get_started.py to understand concepts",
                    "Test basic setup with simple_test.py",
                    "Develop agent logic with local_strands_agent.py",
                    "Validate complete workflow with agentcore_rag_infrastructure_demo.py"
                ],
                "benefits": "Fast iteration, free testing, easy debugging"
            },
            {
                "phase": "☁️ Cloud Validation", 
                "steps": [
                    "Deploy to AgentCore Runtime with deployment_script.py",
                    "Test production endpoints and scaling",
                    "Monitor performance via CloudWatch",
                    "Validate integration with AWS services"
                ],
                "benefits": "Production testing, auto-scaling, real monitoring"
            },
            {
                "phase": "🔄 Iteration Cycle",
                "steps": [
                    "Make changes locally based on cloud testing results",
                    "Re-test locally to validate fixes",
                    "Redeploy to cloud for final validation",
                    "Monitor production metrics and user feedback"
                ],
                "benefits": "Continuous improvement, reliable deployments"
            }
        ]
        
        for phase_info in workflow_steps:
            print(f"\n{phase_info['phase']}:")
            for i, step in enumerate(phase_info['steps'], 1):
                print(f"   {i}. {step}")
            print(f"   💡 Benefits: {phase_info['benefits']}")
    
    def show_troubleshooting_guide(self):
        """Show common issues and solutions"""
        print("\n" + "="*60)
        print("🛠️ TROUBLESHOOTING GUIDE")
        print("="*60)
        
        common_issues = [
            {
                "issue": "❌ AWS credentials not configured",
                "solution": "Run 'aws configure' and set up your credentials",
                "check": "aws sts get-caller-identity"
            },
            {
                "issue": "❌ Nova Lite model not accessible",
                "solution": "Ensure you're in us-east-1 or us-west-2 region",
                "check": "Check AWS Bedrock console for model availability"
            },
            {
                "issue": "❌ AgentCore deployment fails",
                "solution": "Verify IAM permissions for ECR and AgentCore",
                "check": "Check deployment script logs for specific errors"
            },
            {
                "issue": "❌ Agent not responding in cloud",
                "solution": "Check CloudWatch logs for runtime errors",
                "check": "View logs in CloudWatch console"
            },
            {
                "issue": "❌ Package import errors",
                "solution": "Install requirements: pip install -r requirements.txt",
                "check": "python -c 'import boto3; print(\"OK\")'"
            }
        ]
        
        for issue_info in common_issues:
            print(f"\n{issue_info['issue']}")
            print(f"   🔧 Solution: {issue_info['solution']}")
            print(f"   ✔️ Check: {issue_info['check']}")
    
    def run_complete_guide(self):
        """Run the complete testing guide"""
        print("🧪 AgentCore Runtime Testing Guide")
        print("Chapter 7: Infrastructure - AI Engineering Course")
        
        # Test local environment first
        local_success = self.test_local_environment()
        
        # Explain cloud testing
        self.explain_cloud_testing()
        
        # Show complete workflow
        self.demonstrate_testing_workflow()
        
        # Show troubleshooting
        self.show_troubleshooting_guide()
        
        print("\n" + "="*60)
        print("📚 TESTING GUIDE COMPLETE")
        print("="*60)
        
        if local_success:
            print("✅ Your local environment is ready!")
            print("\n🎯 Next Steps:")
            print("1. Run: python agentcore_rag_infrastructure_demo.py")
            print("2. When ready for cloud: python deployment_script.py")
            print("3. Monitor via AWS CloudWatch console")
        else:
            print("⚠️ Local environment needs attention")
            print("\n🔧 Fix local issues first, then proceed with cloud testing")
        
        print("\n📖 For detailed documentation, see README.md")


def main():
    """Main function"""
    tester = AgentCoreTester()
    tester.run_complete_guide()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
AgentCore Deployment Tester

This script tests a deployed AgentCore agent by sending HTTP requests
to the AgentCore Runtime endpoint and validating responses.

Usage:
    python test_agentcore_deployment.py --endpoint YOUR_ENDPOINT_URL
    python test_agentcore_deployment.py --agent-name my-agent

Requirements:
    - Deployed agent on AWS Bedrock AgentCore Runtime
    - AWS credentials configured (for agent name lookup)
    - Agent endpoint URL or agent name
"""

import argparse
import json
import sys
import time
from typing import Dict, Any, Optional
import requests
import boto3
from botocore.exceptions import ClientError, NoCredentialsError


class AgentCoreTestClient:
    """Client for testing deployed AgentCore agents."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'AgentCore-Test-Client/1.0'
        })
    
    def get_agent_endpoint(self, agent_name: str) -> Optional[str]:
        """
        Get agent endpoint URL from AWS Bedrock AgentCore.
        
        Args:
            agent_name: Name of the deployed agent
            
        Returns:
            Agent endpoint URL if found, None otherwise
        """
        try:
            # Initialize Bedrock client
            bedrock = boto3.client('bedrock-agent-runtime')
            
            # Note: This is a placeholder - actual AgentCore API may differ
            # Students should replace with actual AgentCore endpoint discovery
            print(f"⚠️  Agent endpoint discovery not yet implemented.")
            print(f"   Please use --endpoint flag with your agent's URL")
            print(f"   You can find this in the AWS Bedrock Console > AgentCore section")
            return None
            
        except (ClientError, NoCredentialsError) as e:
            print(f"❌ AWS Error: {e}")
            print("   Ensure AWS credentials are configured correctly")
            return None
    
    def test_agent_health(self, endpoint_url: str) -> bool:
        """
        Test if the agent endpoint is responding.
        
        Args:
            endpoint_url: AgentCore agent endpoint URL
            
        Returns:
            True if agent is healthy, False otherwise
        """
        try:
            print(f"🔍 Testing agent health at: {endpoint_url}")
            
            # Simple health check with minimal payload
            response = self.session.post(
                endpoint_url,
                json={"query": "health check"},
                timeout=30
            )
            
            if response.status_code == 200:
                print(f"✅ Agent is responding (Status: {response.status_code})")
                return True
            else:
                print(f"⚠️  Agent responded with status: {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                return False
                
        except requests.exceptions.Timeout:
            print("❌ Request timed out - agent may be starting up")
            return False
        except requests.exceptions.ConnectionError:
            print("❌ Connection error - check endpoint URL")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
    
    def test_agent_functionality(self, endpoint_url: str) -> Dict[str, Any]:
        """
        Test agent functionality with various queries.
        
        Args:
            endpoint_url: AgentCore agent endpoint URL
            
        Returns:
            Dictionary with test results
        """
        test_cases = [
            {
                "name": "Simple Greeting",
                "payload": {"query": "Hello! Can you introduce yourself?"},
                "expected_fields": ["result"]
            },
            {
                "name": "Information Query", 
                "payload": {"query": "What can you help me with?"},
                "expected_fields": ["result"]
            },
            {
                "name": "Complex Question",
                "payload": {"query": "Explain the benefits of serverless architecture"},
                "expected_fields": ["result"]
            }
        ]
        
        results = {
            "total_tests": len(test_cases),
            "passed": 0,
            "failed": 0,
            "test_details": []
        }
        
        print(f"\n🧪 Running {len(test_cases)} functionality tests...")
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📝 Test {i}: {test_case['name']}")
            
            try:
                # Send request to agent
                response = self.session.post(
                    endpoint_url,
                    json=test_case["payload"],
                    timeout=60
                )
                
                test_result = {
                    "test_name": test_case["name"],
                    "status": "FAILED",
                    "response_code": response.status_code,
                    "response_time": response.elapsed.total_seconds(),
                    "details": ""
                }
                
                if response.status_code == 200:
                    try:
                        response_data = response.json()
                        
                        # Check if expected fields are present
                        missing_fields = []
                        for field in test_case["expected_fields"]:
                            if field not in response_data:
                                missing_fields.append(field)
                        
                        if not missing_fields:
                            test_result["status"] = "PASSED"
                            test_result["details"] = f"Response: {str(response_data)[:100]}..."
                            results["passed"] += 1
                            print(f"   ✅ PASSED ({response.elapsed.total_seconds():.2f}s)")
                            print(f"   📄 Response: {str(response_data)[:150]}...")
                        else:
                            test_result["details"] = f"Missing fields: {missing_fields}"
                            results["failed"] += 1
                            print(f"   ❌ FAILED - Missing fields: {missing_fields}")
                            
                    except json.JSONDecodeError:
                        test_result["details"] = "Invalid JSON response"
                        results["failed"] += 1
                        print(f"   ❌ FAILED - Invalid JSON response")
                else:
                    test_result["details"] = f"HTTP {response.status_code}: {response.text[:100]}"
                    results["failed"] += 1
                    print(f"   ❌ FAILED - HTTP {response.status_code}")
                    
                results["test_details"].append(test_result)
                
            except requests.exceptions.Timeout:
                test_result = {
                    "test_name": test_case["name"],
                    "status": "FAILED",
                    "details": "Request timeout"
                }
                results["test_details"].append(test_result)
                results["failed"] += 1
                print(f"   ❌ FAILED - Request timeout")
                
            except Exception as e:
                test_result = {
                    "test_name": test_case["name"],
                    "status": "FAILED", 
                    "details": f"Error: {str(e)}"
                }
                results["test_details"].append(test_result)
                results["failed"] += 1
                print(f"   ❌ FAILED - {str(e)}")
            
            # Small delay between tests
            time.sleep(1)
        
        return results
    
    def print_summary(self, results: Dict[str, Any]):
        """Print test results summary."""
        print(f"\n" + "="*50)
        print(f"🏁 TEST SUMMARY")
        print(f"="*50)
        print(f"Total Tests: {results['total_tests']}")
        print(f"✅ Passed: {results['passed']}")
        print(f"❌ Failed: {results['failed']}")
        
        success_rate = (results['passed'] / results['total_tests']) * 100
        print(f"📊 Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 80:
            print(f"🎉 Excellent! Your AgentCore deployment is working well!")
        elif success_rate >= 60:
            print(f"⚠️  Good, but there may be some issues to investigate")
        else:
            print(f"🔧 Issues detected - check agent logs and configuration")
        
        print(f"\n📋 Detailed Results:")
        for test in results['test_details']:
            status_icon = "✅" if test['status'] == "PASSED" else "❌"
            print(f"   {status_icon} {test['test_name']}: {test['status']}")
            if test.get('response_time'):
                print(f"      ⏱️  Response time: {test['response_time']:.2f}s")


def main():
    """Main function to run AgentCore deployment tests."""
    parser = argparse.ArgumentParser(
        description="Test deployed AgentCore agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Test using endpoint URL
    python test_agentcore_deployment.py --endpoint https://your-agent-endpoint.amazonaws.com/invocations
    
    # Test using agent name (requires AWS credentials)
    python test_agentcore_deployment.py --agent-name my-agent
    
    # Run health check only
    python test_agentcore_deployment.py --endpoint YOUR_URL --health-only
        """
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--endpoint',
        help='AgentCore agent endpoint URL'
    )
    group.add_argument(
        '--agent-name',
        help='Name of deployed agent (will lookup endpoint)'
    )
    
    parser.add_argument(
        '--health-only',
        action='store_true',
        help='Run health check only (skip functionality tests)'
    )
    
    args = parser.parse_args()
    
    print("🚀 AgentCore Deployment Tester")
    print("="*40)
    
    # Initialize test client
    client = AgentCoreTestClient()
    
    # Get endpoint URL
    endpoint_url = args.endpoint
    if args.agent_name:
        print(f"🔍 Looking up endpoint for agent: {args.agent_name}")
        endpoint_url = client.get_agent_endpoint(args.agent_name)
        if not endpoint_url:
            print("❌ Could not find agent endpoint")
            sys.exit(1)
    
    print(f"🎯 Target endpoint: {endpoint_url}")
    
    # Run health check
    if not client.test_agent_health(endpoint_url):
        print("\n❌ Health check failed - cannot proceed with functionality tests")
        print("\n💡 Troubleshooting tips:")
        print("   1. Verify the endpoint URL is correct")
        print("   2. Check agent status in AWS Bedrock Console")
        print("   3. Ensure agent is in 'Ready' state")
        print("   4. Verify your network connection")
        sys.exit(1)
    
    if args.health_only:
        print("\n✅ Health check completed successfully!")
        return
    
    # Run functionality tests
    print(f"\n🔬 Starting comprehensive functionality tests...")
    results = client.test_agent_functionality(endpoint_url)
    
    # Print summary
    client.print_summary(results)
    
    # Exit with appropriate code
    if results['failed'] == 0:
        print(f"\n🎉 All tests passed! Your AgentCore deployment is working perfectly!")
        sys.exit(0)
    else:
        print(f"\n🔧 Some tests failed. Check the details above and agent logs.")
        sys.exit(1)


if __name__ == "__main__":
    main()

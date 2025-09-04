#!/usr/bin/env python3
"""
Quick AgentCore Test

Simple script to quickly test your deployed AgentCore agent.
Perfect for validating deployment after `agentcore deploy`.

Usage:
    python quick_test.py
    # Then enter your endpoint URL when prompted
"""

import json
import requests
import sys


def test_agent_quick():
    """Quick interactive test of AgentCore agent."""
    
    print("🚀 Quick AgentCore Agent Test")
    print("=" * 35)
    
    # Get endpoint from user
    endpoint = input("\n📍 Enter your AgentCore endpoint URL: ").strip()
    
    if not endpoint:
        print("❌ No endpoint provided")
        return False
    
    if not endpoint.startswith(('http://', 'https://')):
        print("⚠️  Adding https:// prefix to endpoint")
        endpoint = f"https://{endpoint}"
    
    print(f"\n🎯 Testing endpoint: {endpoint}")
    
    # Test cases
    test_queries = [
        "Hello! Can you introduce yourself?",
        "What is AWS AgentCore Runtime?",
        "How are you doing today?"
    ]
    
    print(f"\n🧪 Running {len(test_queries)} quick tests...")
    
    passed = 0
    failed = 0
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📝 Test {i}: {query[:30]}...")
        
        try:
            response = requests.post(
                endpoint,
                json={"query": query},
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'result' in data:
                        print(f"   ✅ SUCCESS - Response: {str(data['result'])[:80]}...")
                        passed += 1
                    else:
                        print(f"   ⚠️  Response missing 'result' field: {data}")
                        failed += 1
                except json.JSONDecodeError:
                    print(f"   ❌ Invalid JSON response: {response.text[:50]}...")
                    failed += 1
            else:
                print(f"   ❌ HTTP {response.status_code}: {response.text[:50]}...")
                failed += 1
                
        except requests.exceptions.Timeout:
            print(f"   ❌ Request timed out")
            failed += 1
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Connection failed - check endpoint URL")
            failed += 1
        except Exception as e:
            print(f"   ❌ Error: {e}")
            failed += 1
    
    # Summary
    print(f"\n" + "="*40)
    print(f"🏁 QUICK TEST RESULTS")
    print(f"="*40)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    
    success_rate = (passed / len(test_queries)) * 100
    print(f"📊 Success Rate: {success_rate:.1f}%")
    
    if success_rate == 100:
        print(f"\n🎉 Perfect! Your AgentCore agent is working great!")
        print(f"💡 Try the comprehensive tester: python test_agentcore_deployment.py --endpoint {endpoint}")
    elif success_rate >= 70:
        print(f"\n✅ Good! Most tests passed - minor issues may exist")
    else:
        print(f"\n🔧 Issues detected - check agent deployment and logs")
        print(f"\n💡 Troubleshooting tips:")
        print(f"   1. Verify endpoint URL in AWS Bedrock Console")
        print(f"   2. Check agent status is 'Ready'")
        print(f"   3. Review CloudWatch logs for errors")
    
    return success_rate == 100


def main():
    """Main function."""
    try:
        success = test_agent_quick()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n\n👋 Test cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

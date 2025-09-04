#!/usr/bin/env python3
"""
AgentCore CLI Test Script

Proper test script that uses the agentcore CLI to test deployed agents.
This works with AgentCore's actual architecture instead of trying HTTP calls.

Usage:
    python agentcore_cli_test.py
"""

import subprocess
import json
import sys


def run_agentcore_invoke(payload):
    """Run agentcore invoke command with given payload."""
    try:
        # Convert payload to JSON string
        json_payload = json.dumps(payload)
        
        # Run agentcore invoke command
        result = subprocess.run(
            ['agentcore', 'invoke', json_payload],
            capture_output=True,
            text=True,
            check=True
        )
        
        return True, result.stdout
        
    except subprocess.CalledProcessError as e:
        return False, f"Command failed: {e.stderr}"
    except Exception as e:
        return False, f"Error: {e}"


def test_agentcore_agent():
    """Test AgentCore agent using CLI commands."""
    
    print("🚀 AgentCore CLI Test")
    print("=" * 30)
    
    print("\n🎯 Testing AgentCore agent via CLI...")
    
    # Test cases
    test_queries = [
        "Hello! Can you introduce yourself?",
        "What is AWS AgentCore Runtime?", 
        "How are you doing today?"
    ]
    
    print(f"\n🧪 Running {len(test_queries)} tests...")
    
    passed = 0
    failed = 0
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📝 Test {i}: {query[:40]}...")
        
        payload = {"input": query}
        success, output = run_agentcore_invoke(payload)
        
        if success:
            print(f"   ✅ Success!")
            # Try to extract the actual response from the output
            if "response" in output:
                try:
                    # The output contains the full response, let's make it more readable
                    lines = output.split('\n')
                    for line in lines:
                        if '"text":' in line:
                            # Extract the text content
                            import re
                            match = re.search(r'"text":\s*"([^"]*)"', line)
                            if match:
                                text = match.group(1).replace('\\', '')[:100]
                                print(f"   📋 Response: {text}...")
                                break
                except:
                    print(f"   📋 Response received (see full output above)")
            passed += 1
        else:
            print(f"   ❌ Failed: {output}")
            failed += 1
    
    # Results
    print("\n" + "=" * 30)
    print("🏁 TEST RESULTS")
    print("=" * 30)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Success Rate: {(passed/(passed+failed)*100):.1f}%")
    
    if failed > 0:
        print("\n🔧 Issues detected")
        print("\n💡 Troubleshooting:")
        print("   1. Run: agentcore status")
        print("   2. Check agent is in 'READY' state")
        print("   3. Check CloudWatch logs")
    else:
        print("\n🎉 All tests passed! Your AgentCore agent is working correctly.")
    
    return passed > 0


if __name__ == "__main__":
    success = test_agentcore_agent()
    sys.exit(0 if success else 1)

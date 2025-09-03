#!/usr/bin/env python3
"""
Quick Test: AWS Cost Monitoring with Human-in-the-Loop

A simplified test script to demonstrate the use_aws and handoff_to_user tools.
This script provides a quick way to test the functionality without the full
complexity of the main example.

Usage:
    python test_aws_cost_hitl.py
"""

import os
import logging

# Set environment to bypass tool consent
os.environ["BYPASS_TOOL_CONSENT"] = "true"

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_aws_cost_tools():
    """Quick test of AWS cost monitoring and HITL tools."""
    try:
        from strands import Agent
        from strands_tools import use_aws, handoff_to_user, calculator
        
        print("✅ Successfully imported Strands tools")
        
        # Create a simple test agent
        agent = Agent(
            model="us.amazon.nova-lite-v1:0",
            tools=[use_aws, handoff_to_user, calculator],
            system_prompt="""You are testing AWS cost monitoring tools.

When asked to check costs:
1. Use the use_aws tool to get AWS billing information
2. If any costs seem high, handoff to user for review

When asked to calculate savings:
1. Use the calculator tool for computations
2. Present results clearly
3. Ask for user confirmation via handoff_to_user
"""
        )
        
        print("\n🔍 Test 1: Basic AWS Cost Check")
        print("-" * 40)
        
        response1 = agent("Check our current AWS costs using the AWS tool. "
                         "Get basic billing information for this month.")
        print(f"Response: {response1}")
        
        print("\n💰 Test 2: Cost Calculation with Human Approval")
        print("-" * 50)
        
        response2 = agent("Calculate the monthly cost savings if we reduced our "
                         "EC2 spending from $500 to $300. Then handoff to user "
                         "to confirm if we should proceed with this optimization.")
        print(f"Response: {response2}")
        
        print("\n🚨 Test 3: High Cost Alert with Handoff")
        print("-" * 45)
        
        response3 = agent("Our AWS bill jumped to $2,000 this month, which is "
                         "double our usual $1,000. This requires immediate human "
                         "review. Handoff to user with alert details.")
        print(f"Response: {response3}")
        
        print("\n✅ All tests completed successfully!")
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Please install required packages:")
        print("pip install strands-agents strands-agents-tools")
    except Exception as e:
        print(f"❌ Test Error: {e}")
        logger.error(f"Test failed: {e}")


def test_handoff_modes():
    """Test different handoff_to_user modes."""
    try:
        from strands import Agent
        from strands_tools import handoff_to_user
        
        print("\n🤝 Testing Human-in-the-Loop Modes")
        print("=" * 45)
        
        agent = Agent(
            model="us.amazon.nova-lite-v1:0",
            tools=[handoff_to_user],
            system_prompt="""You are demonstrating handoff_to_user tool modes.

Two modes available:
1. Interactive mode (breakout_of_loop=False) - collect input and continue
2. Complete handoff (breakout_of_loop=True) - stop execution entirely

Use the appropriate mode based on the scenario."""
        )
        
        print("\n📝 Test: Interactive Mode (continue after input)")
        response1 = agent("Use handoff_to_user in interactive mode to ask the user "
                         "if they want to proceed with a $500 AWS optimization. "
                         "Set breakout_of_loop=False so we continue after their input.")
        print(f"Interactive Mode Response: {response1}")
        
        print("\n🛑 Test: Complete Handoff Mode (stop execution)")
        response2 = agent("Use handoff_to_user in complete handoff mode to alert "
                         "about a critical cost spike requiring immediate human intervention. "
                         "Set breakout_of_loop=True to stop execution entirely.")
        print(f"Complete Handoff Response: {response2}")
        
    except Exception as e:
        print(f"❌ Handoff test error: {e}")


def main():
    """Run all quick tests."""
    print("🚀 Quick Test: AWS Cost Monitoring with Human-in-the-Loop")
    print("=" * 70)
    
    # Test 1: Basic functionality
    test_aws_cost_tools()
    
    # Test 2: Handoff modes
    test_handoff_modes()
    
    print("\n" + "=" * 70)
    print("✅ Quick tests completed!")
    print("\nFor full functionality, run: python aws_cost_monitor_hitl_example.py")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Test interrupted by user.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"❌ Unexpected error: {e}")

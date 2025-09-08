#!/usr/bin/env python3
"""
Quick test script to verify Nova Lite model works with observability examples.
This script provides a simple way to test that all examples work with the Nova Lite model.
"""

import os
import sys
from pathlib import Path

# Add the chapter directory to Python path
chapter_dir = Path(__file__).parent
sys.path.insert(0, str(chapter_dir))

def test_nova_lite_basic():
    """Test basic Nova Lite model functionality with observability."""
    print("🧪 Testing Nova Lite model with basic observability...")
    
    try:
        from strands import Agent
        from strands.models import BedrockModel
        
        # Create Nova Lite model
        model = BedrockModel(
            model_id="us.amazon.nova-lite-v1:0",
            region=os.getenv("AWS_REGION", "us-east-1")
        )
        
        # Create simple agent
        agent = Agent(
            model=model,
            system_prompt="You are a helpful AI assistant. Respond concisely."
        )
        
        # Test simple query
        result = agent("What is 2 + 2? Please answer briefly.")
        
        print(f"✅ Nova Lite response: {result.message}")
        print(f"✅ Token usage: {result.metrics.get_summary().get('accumulated_usage', {})}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Nova Lite: {str(e)}")
        return False

def test_observability_examples():
    """Test that observability examples work with Nova Lite."""
    print("\n🔍 Testing observability examples with Nova Lite...")
    
    try:
        # Import the observability examples
        from strands_observability_examples import ObservabilityExamples
        
        # Create observability demo instance
        demo = ObservabilityExamples()
        
        # Test basic metrics collection
        print("📊 Testing metrics collection...")
        demo.demonstrate_metrics_collection()
        
        print("✅ Observability examples working with Nova Lite!")
        return True
        
    except Exception as e:
        print(f"❌ Error in observability examples: {str(e)}")
        return False

def main():
    """Run all Nova Lite tests."""
    print("🚀 Nova Lite Observability Test Suite")
    print("=" * 50)
    
    # Check environment
    if not os.getenv("AWS_REGION"):
        print("⚠️  Warning: AWS_REGION not set, using default 'us-east-1'")
    
    # Run tests
    tests_passed = 0
    total_tests = 2
    
    if test_nova_lite_basic():
        tests_passed += 1
    
    if test_observability_examples():
        tests_passed += 1
    
    # Results
    print("\n" + "=" * 50)
    print(f"📈 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Nova Lite is working with observability.")
        print("\n💡 Next steps:")
        print("   1. Run: python strands_observability_examples.py")
        print("   2. Run: python agentcore_observability_examples.py")
        print("   3. Run: python observability_dashboard.py")
    else:
        print("❌ Some tests failed. Check your AWS configuration and credentials.")
        sys.exit(1)

if __name__ == "__main__":
    main()

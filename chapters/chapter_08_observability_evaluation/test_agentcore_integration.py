#!/usr/bin/env python3
"""
Test AgentCore Integration
"""

import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

from strands_observability_examples import ObservabilityExamples

def test_agentcore_integration():
    """Test the AgentCore integration specifically."""
    print("🔄 Testing AgentCore Integration...")
    print("=" * 50)
    
    try:
        obs = ObservabilityExamples()
        config, metrics = obs.demonstrate_agentcore_integration()
        
        print("\n✅ AgentCore integration test completed successfully!")
        print(f"📊 Configuration: {type(config)}")
        print(f"📈 Metrics: {type(metrics)}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ AgentCore integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_agentcore_integration()
    sys.exit(0 if success else 1)

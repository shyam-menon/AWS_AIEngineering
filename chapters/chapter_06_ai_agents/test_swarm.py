#!/usr/bin/env python3
"""
Quick test of the Swarm multi-agent pattern implementation.
"""

import os
import sys
from datetime import datetime

# Import our swarm implementation
from swarm_example import SwarmOrchestrator

def quick_swarm_test():
    """Test a single swarm with a simple task."""
    
    print("🐝 Quick Swarm Multi-Agent Test")
    print("=" * 50)
    
    # Initialize orchestrator
    orchestrator = SwarmOrchestrator()
    
    # Test with a simple software development task
    print("\n🔄 Testing Software Development Swarm...")
    print("📋 Task: Create a simple Python function for data validation")
    
    try:
        result = orchestrator.execute_swarm(
            swarm_type="software_development",
            task="Create a simple Python function that validates email addresses using regex"
        )
        
        print(f"\n✅ Status: {result['status']}")
        print(f"👥 Agents Involved: {len(result.get('agents_involved', []))}")
        print(f"🔢 Total Iterations: {result.get('total_iterations', 0)}")
        print(f"⏱️ Execution Time: {result.get('execution_time_ms', 0)}ms")
        
        if result['status'] == "COMPLETED" and result.get('final_result'):
            print(f"\n🎯 Result Preview:")
            content_preview = result['final_result'][:300] + "..." if len(result['final_result']) > 300 else result['final_result']
            print(content_preview)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during swarm execution: {e}")
        return False

if __name__ == "__main__":
    success = quick_swarm_test()
    print(f"\n{'✅ Test passed!' if success else '❌ Test failed!'}")

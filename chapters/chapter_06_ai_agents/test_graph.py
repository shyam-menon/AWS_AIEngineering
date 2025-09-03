#!/usr/bin/env python3
"""
Quick test of the Graph multi-agent pattern implementation.
"""

import os
import sys
from datetime import datetime

# Import our graph implementation
from graph_example import GraphOrchestrator

def quick_graph_test():
    """Test a single graph with a simple task."""
    
    print("📊 Quick Graph Multi-Agent Test")
    print("=" * 50)
    
    # Initialize orchestrator
    orchestrator = GraphOrchestrator()
    
    # Test with a simple research analysis task
    print("\n🔄 Testing Research Analysis Graph...")
    print("📋 Task: Research Python web frameworks and provide recommendations")
    
    try:
        result = orchestrator.execute_graph(
            graph_type="research_analysis",
            task="Research modern Python web frameworks (Flask, FastAPI, Django) and provide implementation recommendations for a new API project"
        )
        
        print(f"\n✅ Status: {result['status']}")
        print(f"📈 Execution Order: {' → '.join(result.get('execution_order', []))}")
        print(f"📊 Nodes Completed: {result.get('completed_nodes', 0)}/{result.get('total_nodes', 0)}")
        print(f"⏱️ Execution Time: {result.get('execution_time_ms', 0)}ms")
        
        if result['status'] == "COMPLETED" and result.get('final_output'):
            print(f"\n🎯 Result Preview:")
            output_preview = result['final_output'][:400] + "..." if len(result['final_output']) > 400 else result['final_output']
            print(output_preview)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during graph execution: {e}")
        return False

if __name__ == "__main__":
    success = quick_graph_test()
    print(f"\n{'✅ Test passed!' if success else '❌ Test failed!'}")

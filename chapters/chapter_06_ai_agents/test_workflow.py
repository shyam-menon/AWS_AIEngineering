#!/usr/bin/env python3
"""
Test script for Simple Workflow Pattern
Quick validation with minimal token usage
"""

import sys
import time
from pathlib import Path

# Add the chapter directory to the path
sys.path.append(str(Path(__file__).parent))

from workflow_example import SimpleWorkflowOrchestrator

def test_simple_workflows():
    """Test simple workflow execution"""
    print("🧪 Testing Simple Workflow Patterns")
    print("=" * 50)
    
    orchestrator = SimpleWorkflowOrchestrator()
    
    # Test 1: Analysis workflow
    print("\n1. Testing Analysis Workflow...")
    result1 = orchestrator.run_analysis_workflow("machine learning basics")
    
    assert result1["status"] == "completed", f"Analysis workflow failed: {result1['status']}"
    assert result1["completed_tasks"] == 3, f"Expected 3 completed tasks, got {result1['completed_tasks']}"
    assert len(result1["execution_order"]) == 3, "Should have 3 tasks in execution order"
    assert result1["execution_order"] == ["research", "analysis", "summary"], "Wrong execution order"
    print("✅ Analysis Workflow: PASSED")
    
    # Test 2: Content workflow
    print("\n2. Testing Content Workflow...")
    result2 = orchestrator.run_content_workflow("Python programming tutorial")
    
    assert result2["status"] == "completed", f"Content workflow failed: {result2['status']}"
    assert result2["completed_tasks"] == 3, f"Expected 3 completed tasks, got {result2['completed_tasks']}"
    assert len(result2["execution_order"]) == 3, "Should have 3 tasks in execution order"
    assert result2["execution_order"] == ["planning", "writing", "review"], "Wrong execution order"
    print("✅ Content Workflow: PASSED")
    
    # Test 3: Basic validation
    print("\n3. Testing Basic Validation...")
    assert len(result1["final_output"]) > 10, "Analysis workflow should produce output"
    assert len(result2["final_output"]) > 10, "Content workflow should produce output"
    assert result1["execution_time_ms"] > 0, "Should track execution time"
    assert result2["execution_time_ms"] > 0, "Should track execution time"
    print("✅ Basic Validation: PASSED")
    
    print("\n🎉 All simple workflow tests passed!")
    print(f"📊 Analysis workflow: {result1['execution_time_ms']:.0f}ms")
    print(f"📊 Content workflow: {result2['execution_time_ms']:.0f}ms")
    
    return True

if __name__ == "__main__":
    try:
        start_time = time.time()
        success = test_simple_workflows()
        duration = time.time() - start_time
        
        if success:
            print(f"\n✅ All tests completed successfully in {duration:.1f}s")
            print("🎯 Simple workflow pattern is working correctly!")
        else:
            print(f"\n❌ Some tests failed after {duration:.1f}s")
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n⚠️ Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error during testing: {e}")
        sys.exit(1)

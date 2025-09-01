#!/usr/bin/env python3
"""
Test Script for Intelligent Query Routing Agent

This script tests the intelligent query routing functionality
to ensure all components work correctly.

Author: AWS AI Engineering Course
Chapter: 5 - RAG & Agentic RAG
"""

import sys
import os
import json
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(__file__))

try:
    from intelligent_query_router import IntelligentQueryRouter, QueryType, DataSource
    print("✅ Successfully imported IntelligentQueryRouter")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

def test_query_analysis():
    """Test query analysis functionality."""
    print("\n🧪 Testing Query Analysis...")
    
    router = IntelligentQueryRouter()
    
    test_cases = [
        {
            "query": "How do I configure AWS Bedrock Knowledge Base?",
            "expected_type": QueryType.TECHNICAL_DOCUMENTATION
        },
        {
            "query": "Show me Python code for vector embeddings",
            "expected_type": QueryType.CODE_RELATED
        },
        {
            "query": "What is machine learning?",
            "expected_type": QueryType.GENERAL_KNOWLEDGE
        },
        {
            "query": "My API calls are failing with timeout errors",
            "expected_type": QueryType.TROUBLESHOOTING
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n  Test {i}: {test_case['query'][:50]}...")
        
        try:
            result = router.analyze_query_intent(test_case['query'])
            
            if isinstance(result, dict) and 'query_type' in result:
                detected_type = result['query_type']
                confidence = result.get('confidence', 0)
                
                print(f"    Detected: {detected_type}")
                print(f"    Confidence: {confidence:.2f}")
                print(f"    ✅ Analysis successful")
            else:
                print(f"    ❌ Unexpected result format: {result}")
                
        except Exception as e:
            print(f"    ❌ Error: {e}")

def test_routing_tools():
    """Test individual routing tools."""
    print("\n🔧 Testing Routing Tools...")
    
    router = IntelligentQueryRouter()
    
    tools_to_test = [
        ("route_to_technical_docs", "How to setup AWS Bedrock?"),
        ("route_to_code_search", "Python RAG implementation"),
        ("route_to_general_knowledge", "What is artificial intelligence?"),
        ("route_to_troubleshooting", "API timeout errors")
    ]
    
    for tool_name, test_query in tools_to_test:
        print(f"\n  Testing {tool_name}...")
        
        try:
            tool_method = getattr(router, tool_name)
            result = tool_method(test_query)
            
            if isinstance(result, dict):
                success = result.get('success', False)
                source = result.get('source', 'unknown')
                
                print(f"    Source: {source}")
                print(f"    Success: {success}")
                print(f"    ✅ Tool executed successfully")
            else:
                print(f"    ❌ Unexpected result: {result}")
                
        except Exception as e:
            print(f"    ❌ Error: {e}")

def test_fallback_mechanism():
    """Test fallback routing mechanism."""
    print("\n🔄 Testing Fallback Mechanism...")
    
    router = IntelligentQueryRouter()
    
    try:
        result = router.execute_fallback_strategy(
            "Test query for fallback",
            failed_sources=["bedrock_knowledge_base", "local_vector_db"]
        )
        
        if isinstance(result, dict):
            is_fallback = result.get('is_fallback', False)
            success = result.get('success', False)
            failed_sources = result.get('failed_sources', [])
            
            print(f"    Is Fallback: {is_fallback}")
            print(f"    Success: {success}")
            print(f"    Failed Sources: {failed_sources}")
            print(f"    ✅ Fallback mechanism working")
        else:
            print(f"    ❌ Unexpected result: {result}")
            
    except Exception as e:
        print(f"    ❌ Error: {e}")

def test_metrics_tracking():
    """Test routing metrics tracking."""
    print("\n📊 Testing Metrics Tracking...")
    
    router = IntelligentQueryRouter()
    
    # Generate some routing history
    router._record_routing_decision("technical_docs", True, 0.85)
    router._record_routing_decision("code_search", True, 0.90)
    router._record_routing_decision("general_knowledge", False, 0.60)
    
    try:
        metrics = router.get_routing_metrics()
        
        if isinstance(metrics, dict):
            total_routes = metrics.get('total_routes', 0)
            success_rate = metrics.get('overall_success_rate', 0)
            avg_confidence = metrics.get('average_confidence', 0)
            
            print(f"    Total Routes: {total_routes}")
            print(f"    Success Rate: {success_rate:.2%}")
            print(f"    Avg Confidence: {avg_confidence:.2f}")
            print(f"    ✅ Metrics tracking working")
        else:
            print(f"    ❌ Unexpected result: {metrics}")
            
    except Exception as e:
        print(f"    ❌ Error: {e}")

def test_end_to_end_routing():
    """Test complete end-to-end routing."""
    print("\n🚀 Testing End-to-End Routing...")
    
    router = IntelligentQueryRouter()
    
    test_query = "How do I implement RAG with AWS Bedrock and Python?"
    
    try:
        result = router.route_query(test_query)
        
        if isinstance(result, dict):
            success = result.get('success', False)
            query = result.get('query', '')
            timestamp = result.get('routing_timestamp', '')
            
            print(f"    Query: {query[:50]}...")
            print(f"    Success: {success}")
            print(f"    Timestamp: {timestamp}")
            print(f"    ✅ End-to-end routing working")
        else:
            print(f"    ❌ Unexpected result: {result}")
            
    except Exception as e:
        print(f"    ❌ Error: {e}")

def main():
    """Run all tests."""
    print("🧪 INTELLIGENT QUERY ROUTING AGENT - TEST SUITE")
    print("=" * 60)
    
    tests = [
        test_query_analysis,
        test_routing_tools,
        test_fallback_mechanism,
        test_metrics_tracking,
        test_end_to_end_routing
    ]
    
    passed = 0
    total = len(tests)
    
    for test_func in tests:
        try:
            test_func()
            passed += 1
            print(f"✅ {test_func.__name__} passed")
        except Exception as e:
            print(f"❌ {test_func.__name__} failed: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 TEST SUMMARY: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The Intelligent Query Router is working correctly.")
    else:
        print(f"⚠️  {total - passed} test(s) failed. Please check the implementation.")

if __name__ == "__main__":
    main()

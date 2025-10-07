#!/usr/bin/env python3
"""
Test Script for Priority-Based RAG System

Run this script to verify that all components are working correctly
before committing to GitHub.
"""

import sys
import os
import unittest
from io import StringIO

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import modules for testing
try:
    from priority_router import PriorityBasedRouter, SourceResult
    from chatbot import PriorityAwareChatBot, InteractiveChatSession
    from data.mock_knowledge_base import get_sample_queries, get_source_statistics
    from utils.config import RouterConfig, ConfigManager
    from utils.helpers import PerformanceTracker, QueryAnalyzer
    IMPORTS_SUCCESSFUL = True
except ImportError as e:
    print(f"❌ Critical import error: {e}")
    IMPORTS_SUCCESSFUL = False

def test_imports():
    """Test that all modules can be imported successfully"""
    print("🧪 Testing imports...")
    
    if IMPORTS_SUCCESSFUL:
        print("  ✅ All imports successful")
        return True
    else:
        print("  ❌ Import failures detected")
        return False

def test_basic_functionality():
    """Test basic functionality of the system"""
    print("\n🧪 Testing basic functionality...")
    
    if not IMPORTS_SUCCESSFUL:
        print("  ❌ Cannot test functionality - imports failed")
        return False
    
    try:
        # Test router initialization
        router = PriorityBasedRouter("demo", use_mock=True)
        print("  ✅ Router initialization successful")
        
        # Test query processing
        results = router.retrieve_with_priority("How to create templates?", max_results=3)
        if results and len(results) > 0:
            print(f"  ✅ Query processing successful ({len(results)} results)")
        else:
            print("  ❌ Query processing failed - no results")
            return False
        
        # Test chatbot initialization
        chatbot = PriorityAwareChatBot("demo", use_mock=True)
        print("  ✅ Chatbot initialization successful")
        
        # Test response generation
        response = chatbot.generate_response("What training is available?")
        if response and "response" in response:
            print("  ✅ Response generation successful")
        else:
            print("  ❌ Response generation failed")
            return False
        
        return True
    except Exception as e:
        print(f"  ❌ Functionality test error: {e}")
        return False

def test_priority_routing():
    """Test that priority routing is working correctly"""
    print("\n🧪 Testing priority routing...")
    
    if not IMPORTS_SUCCESSFUL:
        print("  ❌ Cannot test routing - imports failed")
        return False
    
    try:
        router = PriorityBasedRouter("demo", use_mock=True)
        
        # Test template query - should prioritize Templates
        results = router.retrieve_with_priority("I need a project template", max_results=5)
        
        if results:
            # Check if Templates appear in top results
            top_sources = [r.source for r in results[:3]]
            if "Templates" in top_sources:
                print("  ✅ Template query correctly routed to Templates")
            else:
                print(f"  ⚠️  Template query routing: {top_sources} (Templates not in top 3)")
            
            # Check priority scores
            template_results = [r for r in results if r.source == "Templates"]
            if template_results:
                avg_priority = sum(r.priority for r in template_results) / len(template_results)
                print(f"  ✅ Templates average priority: {avg_priority:.2f}")
            
        # Test process query - should prioritize Process Master Document
        results = router.retrieve_with_priority("What's the development process?", max_results=5)
        
        if results:
            top_sources = [r.source for r in results[:3]]
            if "Process Master Document" in top_sources:
                print("  ✅ Process query correctly routed to Process Master Document")
            else:
                print(f"  ⚠️  Process query routing: {top_sources}")
        
        return True
    except Exception as e:
        print(f"  ❌ Priority routing test error: {e}")
        return False

def test_configuration():
    """Test configuration management"""
    print("\n🧪 Testing configuration...")
    
    if not IMPORTS_SUCCESSFUL:
        print("  ❌ Cannot test configuration - imports failed")
        return False
    
    try:
        
        # Test default configuration
        config = RouterConfig()
        issues = config.validate()
        if not issues:
            print("  ✅ Default configuration is valid")
        else:
            print(f"  ❌ Configuration issues: {issues}")
            return False
        
        # Test priority mapping
        if config.priority_map.get("SDM Playbook") == 1.0:
            print("  ✅ Priority mapping correct")
        else:
            print(f"  ❌ Priority mapping incorrect: {config.priority_map}")
            return False
        
        return True
    except Exception as e:
        print(f"  ❌ Configuration test error: {e}")
        return False

def run_all_tests():
    """Run all tests and return overall result"""
    print("🚀 Priority-Based RAG System - Pre-Commit Tests")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_basic_functionality,
        test_priority_routing,
        test_configuration
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 50)
    if all(results):
        print("🎉 All tests passed! System is ready for commit.")
        return True
    else:
        print("❌ Some tests failed. Please fix issues before committing.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
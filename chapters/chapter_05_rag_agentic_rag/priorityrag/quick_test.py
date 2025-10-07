#!/usr/bin/env python3
"""
Quick Test Script for Priority-Based RAG System

This script provides a simple way to test the priority routing system
with a few sample queries.
"""

import sys
import os

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from priority_router import PriorityBasedRouter, SourceResult
    from chatbot import PriorityAwareChatBot, InteractiveChatSession
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running this script from the priorityrag directory")
    sys.exit(1)

def quick_test():
    """Run a quick test of the priority routing system"""
    
    print("🚀 Priority-Based RAG Quick Test")
    print("=" * 40)
    
    # Initialize the system
    print("📋 Initializing system...")
    chatbot = PriorityAwareChatBot(
        knowledge_base_id="demo",
        use_mock=True
    )
    
    # Test queries
    test_queries = [
        "How do I create a project template?",
        "What's the software development process?", 
        "Show me available training programs",
        "What tools are recommended for analytics?",
        "Give me the latest performance metrics"
    ]
    
    print(f"🧪 Testing {len(test_queries)} queries...\n")
    
    for i, query in enumerate(test_queries, 1):
        print(f"🔍 Query {i}: {query}")
        print("-" * 50)
        
        # Get response
        result = chatbot.generate_response(query)
        
        # Show results
        print(f"🤖 Response: {result['response'][:150]}...")
        
        if result['sources']:
            sources = [s['source'] for s in result['sources'][:3]]
            priorities = [f"{s['priority']:.2f}" for s in result['sources'][:3]]
            print(f"📚 Top Sources: {sources}")
            print(f"🎯 Priorities: {priorities}")
        
        print(f"⏱️  Response Time: {result['metadata']['processing_time']:.2f}s")
        print(f"📊 Confidence: {result['metadata']['confidence']:.2f}")
        print()
    
    # Show metrics
    metrics = chatbot.get_performance_metrics()
    router_metrics = metrics['router_metrics']
    
    print("📈 FINAL METRICS")
    print("=" * 20)
    print(f"✅ Total Queries: {router_metrics['total_queries']}")
    print(f"📊 Success Rate: {router_metrics['success_rate']:.2%}")
    print(f"🎯 Avg Confidence: {router_metrics['average_confidence']:.2f}")
    
    if router_metrics['source_usage']:
        print("\n📚 Source Usage:")
        for source, count in sorted(router_metrics['source_usage'].items(), 
                                   key=lambda x: x[1], reverse=True):
            print(f"  • {source}: {count} times")
    
    print(f"\n🎉 Test completed successfully!")
    print(f"💡 Try running: python demo.py --mode interactive")

if __name__ == "__main__":
    try:
        quick_test()
    except KeyboardInterrupt:
        print("\n\n👋 Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during test: {e}")
        print("💡 Make sure you have installed the requirements: pip install -r requirements.txt")
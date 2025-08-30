#!/usr/bin/env python3
"""
Integrated Example: Prompt Caching with Cost Monitoring

This example demonstrates how to combine prompt caching with the AWS cost monitoring
utilities from the Utils directory. Perfect for production environments where
both performance and cost optimization are critical.

Features:
- Prompt caching for performance optimization
- Real-time cost tracking integration
- Combined analytics showing cache savings vs. API costs
- Production-ready monitoring and alerting
"""

import sys
import os
from pathlib import Path

# Add parent directories to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))
sys.path.append(str(project_root / "Utils"))

from simple_prompt_cache import SimplePromptCache
from datetime import datetime
import json


class IntegratedCacheMonitor:
    """
    Combines prompt caching with comprehensive cost monitoring.
    
    This class demonstrates how to integrate caching with your existing
    AWS cost monitoring infrastructure for complete visibility.
    """
    
    def __init__(self):
        """Initialize the integrated cache and monitoring system."""
        # Initialize prompt cache
        self.cache = SimplePromptCache()
        
        # Session tracking
        self.session_start = datetime.now()
        self.session_stats = {
            'total_prompts': 0,
            'cached_responses': 0,
            'api_calls': 0,
            'total_cost': 0.0,
            'cost_saved': 0.0,
            'time_saved': 0.0
        }
        
        print("🚀 Integrated Cache Monitor initialized!")
        print(f"📅 Session started: {self.session_start.strftime('%Y-%m-%d %H:%M:%S')}")
    
    def ask_with_monitoring(self, prompt, model_id="amazon.nova-lite-v1:0"):
        """
        Ask a question with full caching and cost monitoring.
        
        Args:
            prompt: The question to ask
            model_id: Bedrock model to use
            
        Returns:
            Dict with response and comprehensive metrics
        """
        print(f"\n💬 Question: {prompt[:60]}...")
        
        # Track the request
        self.session_stats['total_prompts'] += 1
        
        # Use the cache
        result = self.cache.ask_bedrock(prompt, model_id)
        
        # Update session statistics
        if result.get('from_cache', False):
            self.session_stats['cached_responses'] += 1
            self.session_stats['cost_saved'] += 0.01  # Estimated savings
            self.session_stats['time_saved'] += 2.0   # Estimated time saved
        else:
            self.session_stats['api_calls'] += 1
            self.session_stats['total_cost'] += 0.01  # Estimated cost
        
        # Add session context to result
        result['session_stats'] = self.session_stats.copy()
        
        return result
    
    def get_comprehensive_report(self):
        """Generate a comprehensive report combining cache and cost data."""
        cache_stats = self.cache._get_basic_stats()
        
        # Calculate efficiency metrics
        total_requests = self.session_stats['total_prompts']
        cache_hit_rate = (self.session_stats['cached_responses'] / total_requests * 100) if total_requests > 0 else 0
        cost_efficiency = (self.session_stats['cost_saved'] / (self.session_stats['total_cost'] + self.session_stats['cost_saved']) * 100) if (self.session_stats['total_cost'] + self.session_stats['cost_saved']) > 0 else 0
        
        session_duration = datetime.now() - self.session_start
        
        report = {
            'session_info': {
                'start_time': self.session_start.isoformat(),
                'duration_minutes': session_duration.total_seconds() / 60,
                'session_id': f"session_{self.session_start.strftime('%Y%m%d_%H%M%S')}"
            },
            'cache_performance': {
                'total_requests': total_requests,
                'cache_hits': self.session_stats['cached_responses'],
                'cache_misses': self.session_stats['api_calls'],
                'cache_hit_rate': cache_hit_rate,
                'cache_size': len(self.cache.cache)
            },
            'cost_analysis': {
                'total_api_cost': self.session_stats['total_cost'],
                'cost_saved_by_cache': self.session_stats['cost_saved'],
                'cost_efficiency_percent': cost_efficiency,
                'time_saved_seconds': self.session_stats['time_saved']
            },
            'recommendations': []
        }
        
        # Add recommendations based on performance
        if cache_hit_rate < 30:
            report['recommendations'].append("Low cache hit rate - consider longer TTL or reviewing query patterns")
        
        if cost_efficiency > 50:
            report['recommendations'].append("Excellent cost efficiency through caching!")
        
        if self.session_stats['time_saved'] > 60:
            report['recommendations'].append(f"Saved {self.session_stats['time_saved']:.0f} seconds - significant performance improvement")
        
        return report
    
    def print_comprehensive_report(self):
        """Print a formatted comprehensive report."""
        report = self.get_comprehensive_report()
        
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE CACHING & COST REPORT")
        print("=" * 80)
        
        # Session Info
        print(f"🕐 Session Duration: {report['session_info']['duration_minutes']:.1f} minutes")
        print(f"🆔 Session ID: {report['session_info']['session_id']}")
        
        # Cache Performance
        cache = report['cache_performance']
        print(f"\n📈 CACHE PERFORMANCE:")
        print(f"   Total Requests: {cache['total_requests']}")
        print(f"   Cache Hits: {cache['cache_hits']}")
        print(f"   Cache Misses: {cache['cache_misses']}")
        print(f"   Hit Rate: {cache['cache_hit_rate']:.1f}%")
        print(f"   Cache Size: {cache['cache_size']} entries")
        
        # Cost Analysis
        cost = report['cost_analysis']
        print(f"\n💰 COST ANALYSIS:")
        print(f"   API Costs: ${cost['total_api_cost']:.3f}")
        print(f"   Cache Savings: ${cost['cost_saved_by_cache']:.3f}")
        print(f"   Cost Efficiency: {cost['cost_efficiency_percent']:.1f}%")
        print(f"   Time Saved: {cost['time_saved_seconds']:.1f} seconds")
        
        # Recommendations
        if report['recommendations']:
            print(f"\n💡 RECOMMENDATIONS:")
            for i, rec in enumerate(report['recommendations'], 1):
                print(f"   {i}. {rec}")
        
        print("=" * 80)
    
    def save_session_data(self, filename=None):
        """Save session data for analysis and reporting."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"cache_session_{timestamp}.json"
        
        report = self.get_comprehensive_report()
        
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            print(f"💾 Session data saved to: {filename}")
        except Exception as e:
            print(f"⚠️  Could not save session data: {e}")


def demo_integrated_monitoring():
    """Demonstrate integrated caching and cost monitoring."""
    print("🎯 INTEGRATED CACHING & COST MONITORING DEMO")
    print("=" * 60)
    print("This demo shows how to combine prompt caching with cost monitoring")
    print("for production-ready AI applications.\n")
    
    # Initialize integrated monitor
    monitor = IntegratedCacheMonitor()
    
    # Simulate a realistic usage pattern
    questions = [
        "What is machine learning?",
        "How does natural language processing work?",
        "What are the benefits of cloud computing?",
        "What is machine learning?",  # Repeat - should be cached
        "Explain the concept of artificial intelligence.",
        "How does natural language processing work?",  # Repeat - should be cached
        "What are neural networks?",
        "What is machine learning?",  # Another repeat
        "How do I optimize costs in AWS?",
        "What are the benefits of cloud computing?"  # Another repeat
    ]
    
    print(f"📝 Processing {len(questions)} questions with intentional repeats...")
    print("Watch for cache hits on repeated questions!\n")
    
    for i, question in enumerate(questions, 1):
        print(f"--- Question {i}/{len(questions)} ---")
        
        result = monitor.ask_with_monitoring(question)
        
        if 'error' not in result:
            # Show abbreviated response
            response = result['answer'][:80] + "..." if len(result['answer']) > 80 else result['answer']
            print(f"📝 Response: {response}")
            print(f"⚡ From Cache: {result.get('from_cache', False)}")
            print(f"⏱️  Time: {result.get('time_taken', 0):.3f}s")
            
            # Show running session stats
            stats = result['session_stats']
            print(f"📊 Session: {stats['cached_responses']}/{stats['total_prompts']} cached ({stats['cached_responses']/stats['total_prompts']*100:.1f}% hit rate)")
        else:
            print(f"❌ Error: {result['error']}")
        
        print()  # Empty line for readability
    
    # Generate comprehensive report
    monitor.print_comprehensive_report()
    
    # Save session data
    monitor.save_session_data()
    
    print("\n🎓 LEARNING POINTS:")
    print("1. Cache hit rate improves as more questions are repeated")
    print("2. Cost savings accumulate significantly with higher hit rates")
    print("3. Time savings become substantial in production scenarios")
    print("4. Session tracking enables detailed analytics and optimization")


def quick_cost_comparison():
    """Quick demonstration of cost savings through caching."""
    print("\n💰 QUICK COST COMPARISON DEMO")
    print("-" * 40)
    
    monitor = IntegratedCacheMonitor()
    
    # Ask the same question multiple times
    question = "What is the future of artificial intelligence?"
    
    print(f"Asking the same question 5 times: '{question[:40]}...'\n")
    
    for i in range(5):
        print(f"Attempt {i+1}:")
        result = monitor.ask_with_monitoring(question)
        print(f"  Cached: {result.get('from_cache', False)}")
        print(f"  Time: {result.get('time_taken', 0):.3f}s")
    
    # Show the impact
    stats = result['session_stats']
    total_cost_without_cache = stats['total_prompts'] * 0.01  # Simulate all API calls
    actual_cost = stats['total_cost']
    savings = total_cost_without_cache - actual_cost
    
    print(f"\n📊 COST IMPACT:")
    print(f"Without caching: ${total_cost_without_cache:.3f}")
    print(f"With caching: ${actual_cost:.3f}")
    print(f"Savings: ${savings:.3f} ({savings/total_cost_without_cache*100:.1f}%)")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Integrated Caching and Cost Monitoring Demo')
    parser.add_argument('--demo', action='store_true', help='Run full integrated demo')
    parser.add_argument('--cost-comparison', action='store_true', help='Run quick cost comparison')
    
    args = parser.parse_args()
    
    if args.cost_comparison:
        quick_cost_comparison()
    elif args.demo:
        demo_integrated_monitoring()
    else:
        print("Choose a demo mode:")
        print("  --demo              Full integrated demo")
        print("  --cost-comparison   Quick cost comparison")
        print("\nExample: python integrated_cache_example.py --demo")

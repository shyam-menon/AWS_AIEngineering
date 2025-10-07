#!/usr/bin/env python3
"""
Priority-Based RAG Demonstration Script

This script demonstrates the intelligent query routing system that prioritizes
knowledge base sources based on document types and query analysis.

Usage:
    python demo.py                    # Run interactive demo
    python demo.py --batch            # Run batch test with sample queries
    python demo.py --metrics          # Show detailed metrics
    python demo.py --config [name]    # Use specific configuration
"""

import argparse
import sys
import os
from typing import List, Dict, Any
import json

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from priority_router import PriorityBasedRouter, SourceResult
    from chatbot import PriorityAwareChatBot, InteractiveChatSession
    from data.mock_knowledge_base import get_sample_queries, get_source_statistics
    from utils.config import RouterConfig, ConfigManager, apply_config_preset
    from utils.helpers import PerformanceTracker, QueryAnalyzer, ResultsFormatter, Logger
except ImportError:
    # If running as a script, try alternative import paths
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from priority_router import PriorityBasedRouter, SourceResult
    from chatbot import PriorityAwareChatBot, InteractiveChatSession
    from data.mock_knowledge_base import get_sample_queries, get_source_statistics
    from utils.config import RouterConfig, ConfigManager, apply_config_preset
    from utils.helpers import PerformanceTracker, QueryAnalyzer, ResultsFormatter, Logger


class PriorityRAGDemo:
    """Main demonstration class for the Priority-Based RAG system"""
    
    def __init__(self, config: RouterConfig = None):
        """Initialize the demo with optional configuration"""
        self.config = config or RouterConfig()
        self.logger = Logger("PriorityRAGDemo")
        self.performance_tracker = PerformanceTracker()
        
        # Initialize components
        self.router = PriorityBasedRouter(
            knowledge_base_id=self.config.knowledge_base_id,
            region=self.config.aws_region,
            use_mock=self.config.use_mock_data
        )
        
        self.chatbot = PriorityAwareChatBot(
            knowledge_base_id=self.config.knowledge_base_id,
            model_id=self.config.bedrock_model_id,
            region=self.config.aws_region,
            use_mock=self.config.use_mock_data
        )
        
        print("🚀 Priority-Based RAG System Initialized")
        print(f"📊 Configuration: Mock Data = {self.config.use_mock_data}")
        print(f"🎯 Priority Sources: {list(self.config.priority_map.keys())}")
    
    def run_interactive_demo(self):
        """Run an interactive demonstration"""
        print("\n" + "="*60)
        print("🤖 INTERACTIVE PRIORITY RAG DEMONSTRATION")
        print("="*60)
        
        session = InteractiveChatSession(self.chatbot)
        session.start_session()
    
    def run_batch_demo(self):
        """Run a batch demonstration with sample queries"""
        print("\n" + "="*60)
        print("📋 BATCH DEMONSTRATION - SAMPLE QUERIES")
        print("="*60)
        
        sample_queries = get_sample_queries()
        
        print(f"Testing {len(sample_queries)} sample queries...\n")
        
        for i, query_info in enumerate(sample_queries, 1):
            query = query_info["query"]
            expected_sources = query_info["expected_sources"]
            category = query_info["category"]
            
            print(f"\n🔍 Test {i}/{len(sample_queries)}: {category.upper()}")
            print(f"Query: '{query}'")
            print(f"Expected Sources: {expected_sources}")
            print("-" * 50)
            
            # Process query
            start_time = time.time()
            result = self.chatbot.generate_response(query)
            response_time = time.time() - start_time
            
            # Extract source information
            sources_used = [s["source"] for s in result["sources"]]
            avg_confidence = result["metadata"]["confidence"]
            avg_priority = sum(s["priority"] for s in result["sources"]) / len(result["sources"]) if result["sources"] else 0
            
            # Record metrics
            self.performance_tracker.record_query(
                query=query,
                response_time=response_time,
                sources_used=sources_used,
                avg_confidence=avg_confidence,
                avg_priority=avg_priority,
                query_type=category
            )
            
            # Display results
            print(f"✅ Response: {result['response'][:150]}...")
            print(f"📚 Sources Used: {sources_used}")
            print(f"🎯 Avg Confidence: {avg_confidence:.2f}")
            print(f"⏱️  Response Time: {response_time:.2f}s")
            
            # Check if expected sources were used
            expected_hit = any(expected in sources_used for expected in expected_sources)
            print(f"✓ Expected Source Hit: {'Yes' if expected_hit else 'No'}")
            
            if i < len(sample_queries):
                input("\n⏸️  Press Enter to continue to next query...")
        
        # Show summary
        print("\n" + "="*60)
        print("📊 BATCH DEMO SUMMARY")
        print("="*60)
        print(self.performance_tracker.generate_report())
    
    def show_routing_analysis(self):
        """Show detailed routing analysis for sample queries"""
        print("\n" + "="*60)
        print("🔍 ROUTING ANALYSIS DEMONSTRATION")
        print("="*60)
        
        analysis_queries = [
            "How do I create a project template?",
            "What's the software development process?",
            "Show me available training programs",
            "What tools are recommended for analytics?",
            "Give me the latest security metrics"
        ]
        
        for query in analysis_queries:
            print(f"\n📝 Query: '{query}'")
            print("-" * 40)
            
            # Analyze query intent
            intent_analysis = QueryAnalyzer.classify_query_intent(query)
            print(f"🎯 Primary Intent: {intent_analysis['primary_intent']}")
            print(f"📏 Query Length: {intent_analysis['query_length']} words")
            
            # Show source preferences
            preferred_sources, match_scores = self.router.analyze_query_for_source_preference(query)
            print(f"🏆 Preferred Sources: {preferred_sources}")
            
            # Get and display results
            results = self.router.retrieve_with_priority(query, max_results=5)
            
            if results:
                print(f"📊 Top Results:")
                for i, result in enumerate(results[:3], 1):
                    print(f"  {i}. {result.source} (Priority: {result.priority:.2f}, "
                          f"Confidence: {result.confidence:.2f})")
                    print(f"     Content: {result.content[:80]}...")
            
            input("\n⏸️  Press Enter for next analysis...")
    
    def show_configuration_demo(self):
        """Demonstrate different configuration options"""
        print("\n" + "="*60)
        print("⚙️  CONFIGURATION DEMONSTRATION")
        print("="*60)
        
        test_query = "How to create a project template?"
        configurations = {
            "balanced": "Balanced weighting between priority, confidence, and query matching",
            "priority_focused": "Heavily weighted towards source priority",
            "confidence_focused": "Heavily weighted towards retrieval confidence"
        }
        
        print(f"Test Query: '{test_query}'\n")
        
        for config_name, description in configurations.items():
            print(f"🔧 Configuration: {config_name.upper()}")
            print(f"📝 Description: {description}")
            print("-" * 40)
            
            # Apply configuration preset
            test_config = RouterConfig()
            apply_config_preset(test_config, config_name)
            
            # Create router with this configuration
            test_router = PriorityBasedRouter(
                knowledge_base_id="demo",
                use_mock=True
            )
            test_router.priority_weight = test_config.priority_weight
            test_router.confidence_weight = test_config.confidence_weight
            test_router.query_match_weight = test_config.query_match_weight
            
            # Get results
            results = test_router.retrieve_with_priority(test_query, max_results=3)
            
            print(f"Weights: Priority={test_config.priority_weight}, "
                  f"Confidence={test_config.confidence_weight}, "
                  f"Query Match={test_config.query_match_weight}")
            
            if results:
                print("Top Results:")
                for i, result in enumerate(results, 1):
                    combined_score = result.metadata.get('combined_score', 0)
                    print(f"  {i}. {result.source} (Combined Score: {combined_score:.3f})")
            
            print()
            input("⏸️  Press Enter for next configuration...")
    
    def show_metrics_dashboard(self):
        """Show comprehensive metrics dashboard"""
        print("\n" + "="*60)
        print("📈 METRICS DASHBOARD")
        print("="*60)
        
        # Router metrics
        router_metrics = self.router.get_routing_metrics()
        print("🎯 ROUTER METRICS:")
        print(f"  Total Queries: {router_metrics['total_queries']}")
        print(f"  Success Rate: {router_metrics['success_rate']:.2%}")
        print(f"  Average Confidence: {router_metrics['average_confidence']:.2f}")
        
        # Performance metrics
        if self.performance_tracker.metrics["queries"]:
            print("\n⚡ PERFORMANCE METRICS:")
            perf_stats = self.performance_tracker.get_summary_stats()
            print(f"  Average Response Time: {perf_stats['avg_response_time']:.2f}s")
            print(f"  Fastest Response: {perf_stats['min_response_time']:.2f}s")
            print(f"  Slowest Response: {perf_stats['max_response_time']:.2f}s")
        
        # Source usage
        if router_metrics["source_usage"]:
            print("\n📚 SOURCE USAGE:")
            total_usage = sum(router_metrics["source_usage"].values())
            for source, count in sorted(router_metrics["source_usage"].items(), key=lambda x: x[1], reverse=True):
                percentage = (count / total_usage) * 100
                print(f"  {source}: {count} queries ({percentage:.1f}%)")
        
        # Knowledge base statistics
        kb_stats = get_source_statistics()
        print(f"\n📊 KNOWLEDGE BASE STATS:")
        print(f"  Total Documents: {kb_stats['total_documents']}")
        print(f"  Source Types: {kb_stats['source_count']}")
        
        for source_type, stats in kb_stats["source_statistics"].items():
            print(f"  {source_type}: {stats['document_count']} docs, "
                  f"Avg length: {stats['avg_content_length']:.0f} chars")
    
    def export_results(self, filename: str = None):
        """Export demonstration results"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"priority_rag_results_{timestamp}.json"
        
        export_data = {
            "configuration": self.config.to_dict(),
            "performance_metrics": self.performance_tracker.get_summary_stats(),
            "router_metrics": self.router.get_routing_metrics(),
            "knowledge_base_stats": get_source_statistics()
        }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"📁 Results exported to: {filename}")


def main():
    """Main function to run the demonstration"""
    parser = argparse.ArgumentParser(description="Priority-Based RAG Demonstration")
    
    parser.add_argument("--mode", choices=["interactive", "batch", "analysis", "config", "metrics"], 
                       default="interactive", help="Demonstration mode")
    parser.add_argument("--config", help="Configuration preset name")
    parser.add_argument("--export", help="Export results to file")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    # Load configuration
    config_manager = ConfigManager()
    
    if args.config:
        try:
            config = config_manager.load_config(args.config)
            print(f"✅ Loaded configuration: {args.config}")
        except FileNotFoundError:
            print(f"❌ Configuration '{args.config}' not found. Using default.")
            config = RouterConfig()
    else:
        config = RouterConfig()
    
    # Set verbose logging if requested
    if args.verbose:
        config.verbose_logging = True
    
    # Initialize demo
    demo = PriorityRAGDemo(config)
    
    try:
        # Run demonstration based on mode
        if args.mode == "interactive":
            demo.run_interactive_demo()
        elif args.mode == "batch":
            demo.run_batch_demo()
        elif args.mode == "analysis":
            demo.show_routing_analysis()
        elif args.mode == "config":
            demo.show_configuration_demo()
        elif args.mode == "metrics":
            demo.show_metrics_dashboard()
        
        # Export results if requested
        if args.export:
            demo.export_results(args.export)
    
    except KeyboardInterrupt:
        print("\n\n👋 Demonstration interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
    
    print("\n🎉 Thank you for trying the Priority-Based RAG system!")


if __name__ == "__main__":
    import time
    from datetime import datetime
    main()
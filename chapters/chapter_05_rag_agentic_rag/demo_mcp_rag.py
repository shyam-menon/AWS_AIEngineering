"""
MCP RAG Demo Script - Comprehensive demonstration of MCP integration

This script provides a guided demonstration of the Model Context Protocol (MCP)
integration with Strands agents for RAG operations.

Author: AI Engineering Course
Version: 1.0.0
"""

import asyncio
import time
import subprocess
import sys
import json
from typing import Dict, Any, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MCPDemo:
    """Comprehensive MCP demonstration class."""
    
    def __init__(self):
        """Initialize the demo."""
        self.server_process = None
        self.demo_queries = [
            {
                "query": "How do I set up AWS Bedrock?",
                "description": "Technical documentation search",
                "expected_tools": ["search_technical_docs", "get_faq_answers"]
            },
            {
                "query": "Show me Python code examples for Strands agents",
                "description": "Code search and examples",
                "expected_tools": ["search_code_examples", "search_technical_docs"]
            },
            {
                "query": "What is the Model Context Protocol?",
                "description": "Comprehensive topic overview",
                "expected_tools": ["get_topic_overview", "search_technical_docs"]
            },
            {
                "query": "How can I optimize costs when using AI models?",
                "description": "FAQ and best practices search",
                "expected_tools": ["get_faq_answers", "search_technical_docs"]
            }
        ]
    
    def print_header(self, title: str, width: int = 60):
        """Print a formatted header."""
        print("\n" + "=" * width)
        print(f" {title} ".center(width))
        print("=" * width)
    
    def print_section(self, title: str, width: int = 60):
        """Print a formatted section header."""
        print("\n" + "-" * width)
        print(f" {title} ")
        print("-" * width)
    
    def check_dependencies(self) -> bool:
        """Check if required dependencies are installed."""
        try:
            import strands
            import mcp
            print("✅ Required packages (strands, mcp) are installed")
            return True
        except ImportError as e:
            print(f"❌ Missing required package: {e}")
            print("Please install required packages:")
            print("pip install strands-agents mcp")
            return False
    
    def start_mcp_server(self) -> bool:
        """Start the MCP knowledge server."""
        try:
            print("🚀 Starting MCP Knowledge Server...")
            self.server_process = subprocess.Popen(
                [sys.executable, "mcp_knowledge_server.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Give server time to start
            time.sleep(3)
            
            # Check if server is running
            if self.server_process.poll() is None:
                print("✅ MCP server started successfully on http://127.0.0.1:8000/mcp/")
                return True
            else:
                print("❌ Failed to start MCP server")
                return False
                
        except Exception as e:
            print(f"❌ Error starting MCP server: {e}")
            return False
    
    def stop_mcp_server(self):
        """Stop the MCP knowledge server."""
        if self.server_process:
            print("🛑 Stopping MCP server...")
            self.server_process.terminate()
            try:
                self.server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.server_process.kill()
                self.server_process.wait()
            print("✅ MCP server stopped")
    
    async def test_basic_mcp_integration(self):
        """Test basic MCP integration with simple queries."""
        self.print_section("Basic MCP Integration Test")
        
        try:
            from mcp_rag_agent import MCPRAGAgent
            
            # Initialize agent
            agent = MCPRAGAgent()
            success = await agent.initialize()
            
            if not success:
                print("❌ Failed to initialize MCP RAG agent")
                return False
            
            print("✅ MCP RAG agent initialized successfully")
            
            # Test simple query
            test_query = "What is AWS Bedrock?"
            print(f"\n🔍 Testing query: '{test_query}'")
            
            result = await agent.query(test_query)
            
            if result["success"]:
                print("✅ Query processed successfully")
                print(f"🛠️ Tools used: {', '.join(result.get('tools_used', []))}")
                print(f"📝 Response length: {len(result['response'])} characters")
                return True
            else:
                print(f"❌ Query failed: {result.get('error', 'Unknown error')}")
                return False
                
        except Exception as e:
            print(f"❌ Error in basic MCP test: {e}")
            return False
    
    async def test_production_features(self):
        """Test production MCP features."""
        self.print_section("Production Features Test")
        
        try:
            from mcp_production_integration import (
                ProductionMCPManager, 
                ProductionRAGAgent, 
                MCPServerConfig
            )
            
            # Configure MCP servers
            server_configs = [
                MCPServerConfig(
                    url="http://127.0.0.1:8000/mcp/",
                    name="primary_knowledge_server",
                    timeout=30
                )
            ]
            
            # Initialize components
            mcp_manager = ProductionMCPManager(server_configs)
            rag_agent = ProductionRAGAgent(mcp_manager)
            
            print("🔧 Initializing production MCP system...")
            await rag_agent.initialize()
            print("✅ Production system initialized")
            
            # Test different search strategies
            strategies = ["quick", "comprehensive", "targeted"]
            test_query = "How do I use Strands agents?"
            
            for strategy in strategies:
                print(f"\n🎯 Testing {strategy} search strategy...")
                
                response = await rag_agent.process_query(
                    query=test_query,
                    search_strategy=strategy
                )
                
                print(f"✅ Strategy: {strategy}")
                print(f"   Success: {response.success}")
                print(f"   Confidence: {response.confidence_score}")
                print(f"   Processing time: {response.processing_time:.2f}s")
                print(f"   Tools used: {len(response.tools_used)}")
            
            # Show metrics
            print("\n📊 Production Metrics:")
            metrics = rag_agent.get_comprehensive_metrics()
            session_metrics = metrics["session_metrics"]
            print(f"   Queries processed: {session_metrics['queries_processed']}")
            print(f"   Success rate: {session_metrics['successful_responses']}/{session_metrics['queries_processed']}")
            print(f"   Average confidence: {session_metrics['average_confidence']:.2f}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error in production features test: {e}")
            return False
    
    def run_test_suite(self) -> bool:
        """Run the comprehensive test suite."""
        self.print_section("Comprehensive Test Suite")
        
        try:
            import subprocess
            
            print("🧪 Running MCP test suite...")
            result = subprocess.run(
                [sys.executable, "test_mcp_rag.py"],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                print("✅ All tests passed successfully")
                print(result.stdout[-500:])  # Show last 500 characters
                return True
            else:
                print("❌ Some tests failed")
                print(result.stderr[-500:])  # Show last 500 characters of errors
                return False
                
        except subprocess.TimeoutExpired:
            print("⏰ Test suite timed out")
            return False
        except Exception as e:
            print(f"❌ Error running test suite: {e}")
            return False
    
    async def run_interactive_demo(self):
        """Run an interactive demo with sample queries."""
        self.print_section("Interactive Demo")
        
        try:
            from mcp_rag_agent import MCPRAGAgent
            
            # Initialize agent
            agent = MCPRAGAgent()
            success = await agent.initialize()
            
            if not success:
                print("❌ Failed to initialize agent for interactive demo")
                return
            
            print("🤖 Running sample queries...")
            
            for i, demo_query in enumerate(self.demo_queries, 1):
                print(f"\n{i}. {demo_query['description']}")
                print(f"   Query: '{demo_query['query']}'")
                
                start_time = time.time()
                result = await agent.query(demo_query['query'])
                processing_time = time.time() - start_time
                
                if result["success"]:
                    print(f"   ✅ Success ({processing_time:.2f}s)")
                    print(f"   🛠️ Tools: {', '.join(result.get('tools_used', []))}")
                    print(f"   📝 Response: {result['response'][:150]}...")
                else:
                    print(f"   ❌ Failed: {result.get('error', 'Unknown error')}")
                
                # Small delay between queries
                await asyncio.sleep(0.5)
            
            # Show final statistics
            stats = agent.get_session_stats()
            print(f"\n📊 Demo Statistics:")
            print(f"   Queries processed: {stats['queries_processed']}")
            print(f"   Tools used: {stats['tools_used']}")
            print(f"   Session duration: {stats['session_duration_minutes']:.1f} minutes")
            
        except Exception as e:
            print(f"❌ Error in interactive demo: {e}")
    
    async def run_complete_demo(self):
        """Run the complete MCP demo."""
        self.print_header("MCP RAG Integration - Complete Demo")
        
        print("🎯 This demo showcases the Model Context Protocol (MCP) integration")
        print("   with Strands agents for advanced RAG operations.")
        print("\n📋 Demo includes:")
        print("   • Dependency checking")
        print("   • MCP server startup")
        print("   • Basic integration testing")
        print("   • Production features demonstration")
        print("   • Interactive query processing")
        print("   • Comprehensive test suite")
        
        # Step 1: Check dependencies
        self.print_section("Step 1: Dependency Check")
        if not self.check_dependencies():
            return
        
        # Step 2: Start MCP server
        self.print_section("Step 2: Start MCP Server")
        if not self.start_mcp_server():
            return
        
        try:
            # Step 3: Test basic integration
            self.print_section("Step 3: Basic Integration Test")
            await self.test_basic_mcp_integration()
            
            # Step 4: Test production features
            self.print_section("Step 4: Production Features Test")
            await self.test_production_features()
            
            # Step 5: Run interactive demo
            self.print_section("Step 5: Interactive Demo")
            await self.run_interactive_demo()
            
            # Step 6: Run test suite
            self.print_section("Step 6: Test Suite")
            self.run_test_suite()
            
            # Final summary
            self.print_header("Demo Complete!")
            print("🎉 MCP RAG integration demo completed successfully!")
            print("\n📚 Next Steps:")
            print("   • Explore the MCP_IMPLEMENTATION_README.md for detailed documentation")
            print("   • Try running the individual scripts manually")
            print("   • Experiment with custom queries and knowledge sources")
            print("   • Review the production integration patterns")
            print("\n🔗 Key Files:")
            print("   • mcp_knowledge_server.py - MCP server implementation")
            print("   • mcp_rag_agent.py - Basic Strands-MCP integration")
            print("   • mcp_production_integration.py - Production-ready system")
            print("   • test_mcp_rag.py - Comprehensive test suite")
            
        finally:
            # Step 7: Cleanup
            self.print_section("Cleanup")
            self.stop_mcp_server()

async def main():
    """Main demo function."""
    demo = MCPDemo()
    await demo.run_complete_demo()

if __name__ == "__main__":
    asyncio.run(main())

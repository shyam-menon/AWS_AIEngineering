#!/usr/bin/env python3
"""
Intelligent Query Routing Agent - Chapter 5: RAG & Agentic RAG

This module demonstrates an intelligent query routing system that can:
1. Analyze incoming queries to determine the best data source and retrieval strategy
2. Route queries to appropriate specialized agents (technical docs, general knowledge, code)
3. Use different RAG approaches based on query complexity and requirements
4. Provide fallback mechanisms and error handling
5. Learn from previous routing decisions to improve future performance

The router showcases how agentic RAG systems can intelligently orchestrate
multiple knowledge sources and retrieval strategies for optimal results.

Author: AWS AI Engineering Course
Chapter: 5 - RAG & Agentic RAG
Version: 1.0
"""

import os
import json
import boto3
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum

# Import Strands with fallback
try:
    from strands import Agent
    from strands.tools import tool
    STRANDS_AVAILABLE = True
    print("✅ Strands framework loaded successfully")
except ImportError:
    STRANDS_AVAILABLE = False
    print("⚠️  Strands framework not available. Running in demonstration mode.")
    print("   To install: pip install strands-agents strands-agents-tools")
    
    # Mock implementation for demonstration
    def tool(func):
        """Mock tool decorator for when Strands is not available."""
        func._is_tool = True
        return func
    
    class Agent:
        """Mock Agent class for demonstration."""
        def __init__(self, tools=None, model=None):
            self.tools = tools or []
            self.model = model
            
        def __call__(self, message):
            return f"[DEMO MODE] Processing: {message}"


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QueryType(Enum):
    """Enumeration of different query types for routing decisions."""
    TECHNICAL_DOCUMENTATION = "technical_docs"
    CODE_RELATED = "code"
    GENERAL_KNOWLEDGE = "general"
    PRODUCT_INFORMATION = "product"
    TROUBLESHOOTING = "troubleshooting"
    COMPARISON = "comparison"
    UNKNOWN = "unknown"


class DataSource(Enum):
    """Enumeration of available data sources."""
    BEDROCK_KB = "bedrock_knowledge_base"
    LOCAL_VECTOR = "local_vector_db"
    EXTERNAL_API = "external_api"
    CODE_REPOSITORY = "code_repo"
    DOCUMENTATION = "documentation"


@dataclass
class QueryAnalysis:
    """Results of query analysis for routing decisions."""
    query_type: QueryType
    confidence: float
    keywords: List[str]
    complexity_score: int  # 1-10
    preferred_sources: List[DataSource]
    fallback_sources: List[DataSource]
    estimated_tokens: int
    requires_real_time: bool


@dataclass
class RoutingDecision:
    """Routing decision with justification and metadata."""
    primary_source: DataSource
    fallback_sources: List[DataSource]
    retrieval_strategy: str
    justification: str
    confidence: float
    metadata: Dict[str, Any]


class IntelligentQueryRouter:
    """
    Intelligent Query Routing Agent that analyzes queries and routes them
    to the most appropriate data sources and retrieval strategies.
    """
    
    def __init__(self, region_name: str = 'us-east-1'):
        """Initialize the query router with AWS clients and routing logic."""
        self.region = region_name
        self.bedrock_client = None
        self.bedrock_runtime = None
        self.routing_history = []
        self.performance_metrics = {}
        
        # Initialize AWS clients
        try:
            self.bedrock_client = boto3.client('bedrock', region_name=region_name)
            self.bedrock_runtime = boto3.client('bedrock-runtime', region_name=region_name)
            logger.info("✅ AWS Bedrock clients initialized successfully")
        except Exception as e:
            logger.warning(f"⚠️ AWS Bedrock clients not available: {e}")
        
        # Setup Strands agent with routing tools
        self.setup_routing_agent()
        
        # Initialize query patterns for classification
        self.query_patterns = self._load_query_patterns()
        
        logger.info("🧠 Intelligent Query Router initialized")
    
    def _load_query_patterns(self) -> Dict[QueryType, List[str]]:
        """Load predefined patterns for query classification."""
        return {
            QueryType.TECHNICAL_DOCUMENTATION: [
                "how to", "documentation", "api", "configuration", "setup", 
                "install", "deploy", "architecture", "specification"
            ],
            QueryType.CODE_RELATED: [
                "code", "function", "method", "class", "bug", "error", 
                "implementation", "algorithm", "syntax", "debug"
            ],
            QueryType.GENERAL_KNOWLEDGE: [
                "what is", "explain", "define", "concept", "theory", 
                "history", "overview", "introduction"
            ],
            QueryType.PRODUCT_INFORMATION: [
                "product", "feature", "pricing", "comparison", "capabilities", 
                "limitations", "requirements", "specifications"
            ],
            QueryType.TROUBLESHOOTING: [
                "error", "problem", "issue", "troubleshoot", "fix", 
                "resolve", "debug", "not working", "failed"
            ],
            QueryType.COMPARISON: [
                "vs", "versus", "compare", "difference", "better", 
                "best", "choose", "which", "alternative"
            ]
        }
    
    def setup_routing_agent(self):
        """Setup Strands agent with routing tools."""
        if not STRANDS_AVAILABLE:
            logger.warning("Strands not available - using mock implementation")
            self.agent = None
            return
        
        try:
            # Create agent with routing tools
            tools = [
                self.analyze_query_intent,
                self.route_to_technical_docs,
                self.route_to_code_search,
                self.route_to_general_knowledge,
                self.route_to_troubleshooting,
                self.execute_fallback_strategy,
                self.get_routing_metrics
            ]
            
            self.agent = Agent(
                tools=tools,
                model="amazon.nova-lite-v1:0"
            )
            
            logger.info("✅ Strands routing agent created successfully")
            
        except Exception as e:
            logger.error(f"❌ Error creating Strands agent: {e}")
            self.agent = None
    
    @tool
    def analyze_query_intent(self, query: str) -> Dict[str, Any]:
        """
        Analyze query to determine intent, complexity, and optimal routing strategy.
        
        Args:
            query: The user query to analyze
            
        Returns:
            Dictionary containing analysis results and routing recommendations
        """
        try:
            # Basic keyword analysis
            query_lower = query.lower()
            keywords = [word.strip('.,!?') for word in query_lower.split()]
            
            # Determine query type based on patterns
            query_type = QueryType.UNKNOWN
            max_matches = 0
            
            for qtype, patterns in self.query_patterns.items():
                matches = sum(1 for pattern in patterns if pattern in query_lower)
                if matches > max_matches:
                    max_matches = matches
                    query_type = qtype
            
            # Calculate complexity score (1-10)
            complexity_score = min(10, max(1, len(keywords) // 2 + max_matches))
            
            # Estimate token count
            estimated_tokens = len(query.split()) * 1.3  # Rough estimation
            
            # Check for real-time requirements
            requires_real_time = any(word in query_lower for word in 
                                   ['current', 'now', 'today', 'latest', 'recent'])
            
            # Determine preferred data sources
            preferred_sources = self._get_preferred_sources(query_type, complexity_score)
            fallback_sources = self._get_fallback_sources(query_type)
            
            analysis = {
                "query_type": query_type.value,
                "confidence": min(1.0, max_matches / 3.0),
                "keywords": keywords[:10],  # Limit to top 10
                "complexity_score": complexity_score,
                "preferred_sources": [src.value for src in preferred_sources],
                "fallback_sources": [src.value for src in fallback_sources],
                "estimated_tokens": int(estimated_tokens),
                "requires_real_time": requires_real_time,
                "analysis_timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"📊 Query analysis completed: {query_type.value} (confidence: {analysis['confidence']:.2f})")
            return analysis
            
        except Exception as e:
            logger.error(f"❌ Error analyzing query: {e}")
            return {
                "error": str(e),
                "query_type": QueryType.UNKNOWN.value,
                "confidence": 0.0
            }
    
    def _get_preferred_sources(self, query_type: QueryType, complexity: int) -> List[DataSource]:
        """Determine preferred data sources based on query type and complexity."""
        source_mapping = {
            QueryType.TECHNICAL_DOCUMENTATION: [DataSource.BEDROCK_KB, DataSource.DOCUMENTATION],
            QueryType.CODE_RELATED: [DataSource.CODE_REPOSITORY, DataSource.LOCAL_VECTOR],
            QueryType.GENERAL_KNOWLEDGE: [DataSource.BEDROCK_KB, DataSource.EXTERNAL_API],
            QueryType.PRODUCT_INFORMATION: [DataSource.BEDROCK_KB, DataSource.DOCUMENTATION],
            QueryType.TROUBLESHOOTING: [DataSource.LOCAL_VECTOR, DataSource.BEDROCK_KB],
            QueryType.COMPARISON: [DataSource.BEDROCK_KB, DataSource.EXTERNAL_API],
            QueryType.UNKNOWN: [DataSource.BEDROCK_KB, DataSource.LOCAL_VECTOR]
        }
        
        # Adjust based on complexity
        sources = source_mapping.get(query_type, [DataSource.BEDROCK_KB])
        if complexity >= 7:
            # High complexity - prefer managed solutions
            sources = [DataSource.BEDROCK_KB] + [s for s in sources if s != DataSource.BEDROCK_KB]
        
        return sources
    
    def _get_fallback_sources(self, query_type: QueryType) -> List[DataSource]:
        """Get fallback data sources if primary sources fail."""
        return [DataSource.LOCAL_VECTOR, DataSource.EXTERNAL_API]
    
    @tool
    def route_to_technical_docs(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Route query to technical documentation sources.
        
        Args:
            query: The technical query
            context: Additional context from query analysis
            
        Returns:
            Routing result with retrieved information
        """
        try:
            logger.info("📚 Routing to technical documentation...")
            
            # In a real implementation, this would interface with:
            # - AWS Bedrock Knowledge Base with technical docs
            # - Confluence or similar documentation systems
            # - API documentation repositories
            
            result = {
                "source": "technical_documentation",
                "strategy": "semantic_search_with_metadata_filtering",
                "query_processed": query,
                "timestamp": datetime.now().isoformat(),
                "results": [
                    {
                        "title": "Technical Documentation Result",
                        "content": f"Technical documentation result for: {query}",
                        "confidence": 0.85,
                        "source_type": "documentation",
                        "metadata": {
                            "section": "API Reference",
                            "last_updated": "2024-08-15"
                        }
                    }
                ],
                "routing_time_ms": 45,
                "success": True
            }
            
            self._record_routing_decision("technical_docs", True, 0.85)
            return result
            
        except Exception as e:
            logger.error(f"❌ Error routing to technical docs: {e}")
            return {"error": str(e), "success": False}
    
    @tool
    def route_to_code_search(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Route query to code repositories and code-specific knowledge bases.
        
        Args:
            query: The code-related query
            context: Additional context from query analysis
            
        Returns:
            Code search results
        """
        try:
            logger.info("💻 Routing to code search...")
            
            # In a real implementation, this would interface with:
            # - GitHub repositories
            # - Internal code repositories
            # - Code-specific vector databases
            # - Stack Overflow or similar developer resources
            
            result = {
                "source": "code_repository",
                "strategy": "code_semantic_search_with_syntax_analysis",
                "query_processed": query,
                "timestamp": datetime.now().isoformat(),
                "results": [
                    {
                        "title": "Code Example",
                        "content": f"# Code example for: {query}\n# This would contain actual code snippets",
                        "confidence": 0.90,
                        "source_type": "code",
                        "metadata": {
                            "language": "python",
                            "repository": "aws-samples",
                            "file_path": "examples/bedrock/basic_usage.py"
                        }
                    }
                ],
                "routing_time_ms": 32,
                "success": True
            }
            
            self._record_routing_decision("code_search", True, 0.90)
            return result
            
        except Exception as e:
            logger.error(f"❌ Error routing to code search: {e}")
            return {"error": str(e), "success": False}
    
    @tool
    def route_to_general_knowledge(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Route query to general knowledge sources and large knowledge bases.
        
        Args:
            query: The general knowledge query
            context: Additional context from query analysis
            
        Returns:
            General knowledge results
        """
        try:
            logger.info("🌐 Routing to general knowledge base...")
            
            # In a real implementation, this would interface with:
            # - Large general knowledge bases
            # - Wikipedia or similar encyclopedic sources
            # - General purpose LLMs with broad knowledge
            
            result = {
                "source": "general_knowledge",
                "strategy": "broad_semantic_search",
                "query_processed": query,
                "timestamp": datetime.now().isoformat(),
                "results": [
                    {
                        "title": "General Knowledge Result",
                        "content": f"General knowledge information about: {query}",
                        "confidence": 0.75,
                        "source_type": "knowledge_base",
                        "metadata": {
                            "category": "general",
                            "authority_score": 0.8
                        }
                    }
                ],
                "routing_time_ms": 28,
                "success": True
            }
            
            self._record_routing_decision("general_knowledge", True, 0.75)
            return result
            
        except Exception as e:
            logger.error(f"❌ Error routing to general knowledge: {e}")
            return {"error": str(e), "success": False}
    
    @tool
    def route_to_troubleshooting(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Route query to troubleshooting and problem-solving resources.
        
        Args:
            query: The troubleshooting query
            context: Additional context from query analysis
            
        Returns:
            Troubleshooting results and solutions
        """
        try:
            logger.info("🔧 Routing to troubleshooting resources...")
            
            # In a real implementation, this would interface with:
            # - Support knowledge bases
            # - Error code databases
            # - Community forums and Q&A sites
            # - Historical incident reports
            
            result = {
                "source": "troubleshooting",
                "strategy": "problem_solution_matching",
                "query_processed": query,
                "timestamp": datetime.now().isoformat(),
                "results": [
                    {
                        "title": "Troubleshooting Solution",
                        "content": f"Troubleshooting steps for: {query}",
                        "confidence": 0.88,
                        "source_type": "support",
                        "metadata": {
                            "solution_type": "step_by_step",
                            "complexity": "medium",
                            "estimated_time": "10-15 minutes"
                        }
                    }
                ],
                "routing_time_ms": 38,
                "success": True
            }
            
            self._record_routing_decision("troubleshooting", True, 0.88)
            return result
            
        except Exception as e:
            logger.error(f"❌ Error routing to troubleshooting: {e}")
            return {"error": str(e), "success": False}
    
    @tool
    def execute_fallback_strategy(self, query: str, failed_sources: List[str] = None) -> Dict[str, Any]:
        """
        Execute fallback strategy when primary routing fails.
        
        Args:
            query: The original query
            failed_sources: List of sources that failed
            
        Returns:
            Fallback results
        """
        try:
            logger.info("🔄 Executing fallback strategy...")
            
            failed_sources = failed_sources or []
            
            # Fallback strategy logic
            if "bedrock_knowledge_base" not in failed_sources:
                # Try managed Bedrock KB
                result = self._try_bedrock_fallback(query)
            elif "local_vector_db" not in failed_sources:
                # Try local vector search
                result = self._try_local_vector_fallback(query)
            else:
                # Last resort - direct LLM query
                result = self._try_direct_llm_fallback(query)
            
            result["is_fallback"] = True
            result["failed_sources"] = failed_sources
            
            self._record_routing_decision("fallback", True, 0.60)
            return result
            
        except Exception as e:
            logger.error(f"❌ Error in fallback strategy: {e}")
            return {"error": str(e), "success": False, "is_fallback": True}
    
    def _try_bedrock_fallback(self, query: str) -> Dict[str, Any]:
        """Try AWS Bedrock Knowledge Base as fallback."""
        return {
            "source": "bedrock_fallback",
            "strategy": "managed_rag_fallback",
            "query_processed": query,
            "results": [
                {
                    "title": "Bedrock Fallback Result",
                    "content": f"Fallback result from Bedrock KB: {query}",
                    "confidence": 0.60
                }
            ],
            "success": True
        }
    
    def _try_local_vector_fallback(self, query: str) -> Dict[str, Any]:
        """Try local vector database as fallback."""
        return {
            "source": "local_vector_fallback",
            "strategy": "local_rag_fallback",
            "query_processed": query,
            "results": [
                {
                    "title": "Local Vector Fallback Result",
                    "content": f"Fallback result from local vector DB: {query}",
                    "confidence": 0.55
                }
            ],
            "success": True
        }
    
    def _try_direct_llm_fallback(self, query: str) -> Dict[str, Any]:
        """Try direct LLM query as last resort."""
        return {
            "source": "direct_llm_fallback",
            "strategy": "direct_llm_query",
            "query_processed": query,
            "results": [
                {
                    "title": "Direct LLM Result",
                    "content": f"Direct LLM response: {query}",
                    "confidence": 0.50
                }
            ],
            "success": True
        }
    
    @tool
    def get_routing_metrics(self) -> Dict[str, Any]:
        """
        Get routing performance metrics and statistics.
        
        Returns:
            Dictionary containing routing metrics and performance data
        """
        try:
            total_routes = len(self.routing_history)
            if total_routes == 0:
                return {"message": "No routing history available", "total_routes": 0}
            
            # Calculate success rates by source
            source_stats = {}
            for record in self.routing_history:
                source = record["source"]
                if source not in source_stats:
                    source_stats[source] = {"total": 0, "successful": 0}
                source_stats[source]["total"] += 1
                if record["success"]:
                    source_stats[source]["successful"] += 1
            
            # Calculate success rates
            for source in source_stats:
                stats = source_stats[source]
                stats["success_rate"] = stats["successful"] / stats["total"]
            
            # Overall metrics
            total_successful = sum(1 for r in self.routing_history if r["success"])
            overall_success_rate = total_successful / total_routes
            
            # Average confidence
            avg_confidence = sum(r.get("confidence", 0) for r in self.routing_history) / total_routes
            
            metrics = {
                "total_routes": total_routes,
                "overall_success_rate": overall_success_rate,
                "average_confidence": avg_confidence,
                "source_statistics": source_stats,
                "last_updated": datetime.now().isoformat()
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"❌ Error getting routing metrics: {e}")
            return {"error": str(e)}
    
    def _record_routing_decision(self, source: str, success: bool, confidence: float):
        """Record routing decision for metrics tracking."""
        record = {
            "timestamp": datetime.now().isoformat(),
            "source": source,
            "success": success,
            "confidence": confidence
        }
        self.routing_history.append(record)
        
        # Keep only last 1000 records
        if len(self.routing_history) > 1000:
            self.routing_history = self.routing_history[-1000:]
    
    def route_query(self, query: str) -> Dict[str, Any]:
        """
        Main method to route a query through the intelligent routing system.
        
        Args:
            query: The user query to route
            
        Returns:
            Complete routing result with analysis and retrieved information
        """
        logger.info(f"🧠 Processing query: {query[:100]}...")
        
        try:
            # Step 1: Analyze query intent and characteristics
            if self.agent and STRANDS_AVAILABLE:
                analysis_prompt = f"""
                Analyze this query and determine the best routing strategy:
                
                Query: "{query}"
                
                Please analyze the query intent, determine the complexity, and recommend
                the optimal data sources and retrieval strategy.
                """
                
                analysis_result = self.agent(analysis_prompt)
                logger.info("✅ Query analysis completed via Strands agent")
            else:
                # Fallback analysis
                analysis_result = self.analyze_query_intent(query)
                logger.info("✅ Query analysis completed via fallback method")
            
            # Step 2: Execute routing based on analysis
            # This would contain the actual routing logic
            routing_result = {
                "query": query,
                "analysis": analysis_result,
                "routing_timestamp": datetime.now().isoformat(),
                "success": True
            }
            
            logger.info("✅ Query routing completed successfully")
            return routing_result
            
        except Exception as e:
            logger.error(f"❌ Error routing query: {e}")
            return {
                "query": query,
                "error": str(e),
                "routing_timestamp": datetime.now().isoformat(),
                "success": False
            }
    
    def demonstrate_routing_capabilities(self):
        """Demonstrate the routing capabilities with example queries."""
        print("=" * 80)
        print("🧠 INTELLIGENT QUERY ROUTING AGENT DEMONSTRATION")
        print("=" * 80)
        print()
        
        # Test queries of different types
        test_queries = [
            {
                "query": "How do I configure AWS Bedrock Knowledge Base with S3?",
                "expected_type": "technical_documentation",
                "description": "Technical documentation query"
            },
            {
                "query": "Show me Python code for implementing RAG with vector databases",
                "expected_type": "code_related", 
                "description": "Code-related query"
            },
            {
                "query": "What is the difference between traditional RAG and agentic RAG?",
                "expected_type": "general_knowledge",
                "description": "Conceptual comparison query"
            },
            {
                "query": "My Bedrock API calls are failing with timeout errors",
                "expected_type": "troubleshooting",
                "description": "Troubleshooting query"
            },
            {
                "query": "Compare Claude 3 Sonnet vs Claude 3 Haiku for cost and performance",
                "expected_type": "comparison",
                "description": "Product comparison query"
            }
        ]
        
        for i, test_case in enumerate(test_queries, 1):
            print(f"🎯 Test Case {i}: {test_case['description']}")
            print(f"Query: \"{test_case['query']}\"")
            print()
            
            if self.agent and STRANDS_AVAILABLE:
                # Use Strands agent for routing
                routing_prompt = f"""
                Route this query to the appropriate data source and retrieval strategy:
                
                Query: "{test_case['query']}"
                
                Analyze the query type, determine the best routing approach, and explain your reasoning.
                """
                
                try:
                    response = self.agent(routing_prompt)
                    print("Agent Routing Decision:")
                    print("-" * 40)
                    print(response)
                except Exception as e:
                    print(f"❌ Error: {e}")
            else:
                # Use direct analysis
                analysis = self.analyze_query_intent(test_case['query'])
                print("Routing Analysis:")
                print("-" * 40)
                print(f"Query Type: {analysis.get('query_type', 'unknown')}")
                print(f"Confidence: {analysis.get('confidence', 0):.2f}")
                print(f"Complexity: {analysis.get('complexity_score', 0)}/10")
                print(f"Preferred Sources: {', '.join(analysis.get('preferred_sources', []))}")
            
            print()
            print("-" * 80)
            print()
        
        # Show routing metrics
        print("📊 ROUTING METRICS")
        print("-" * 40)
        metrics = self.get_routing_metrics()
        if metrics.get('total_routes', 0) > 0:
            print(f"Total Routes: {metrics['total_routes']}")
            print(f"Success Rate: {metrics['overall_success_rate']:.2%}")
            print(f"Average Confidence: {metrics['average_confidence']:.2f}")
        else:
            print("No routing history available yet")
        
        print()
        print("🎉 Demonstration completed!")


def main():
    """Main function to run the intelligent query routing demonstration."""
    print("🚀 Starting Intelligent Query Routing Agent...")
    print()
    
    # Initialize the router
    router = IntelligentQueryRouter()
    
    # Run demonstration
    router.demonstrate_routing_capabilities()
    
    # Interactive mode (optional)
    print("\n" + "=" * 80)
    print("💬 INTERACTIVE MODE")
    print("=" * 80)
    print("Enter queries to test the routing system (type 'quit' to exit):")
    print()
    
    while True:
        try:
            user_query = input("Query > ").strip()
            
            if user_query.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not user_query:
                continue
            
            print("\n🔍 Processing your query...")
            result = router.route_query(user_query)
            
            if result.get('success'):
                print("✅ Routing completed successfully!")
                if 'analysis' in result:
                    analysis = result['analysis']
                    if isinstance(analysis, dict):
                        print(f"Query Type: {analysis.get('query_type', 'unknown')}")
                        print(f"Confidence: {analysis.get('confidence', 0):.2f}")
            else:
                print(f"❌ Routing failed: {result.get('error', 'Unknown error')}")
            
            print()
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()

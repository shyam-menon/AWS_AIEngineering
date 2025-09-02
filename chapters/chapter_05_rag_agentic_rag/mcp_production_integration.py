"""
MCP Production Integration - Production-ready MCP setup for RAG systems

This module demonstrates how to integrate MCP tools into production RAG systems
with proper error handling, monitoring, and scalability considerations.

Author: AI Engineering Course
Version: 1.0.0
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from datetime import datetime, timedelta
import aiohttp
import time
from concurrent.futures import ThreadPoolExecutor
import traceback

# Strands and MCP imports
from strands import Agent
from strands.tools.mcp.mcp_client import MCPClient
from mcp.client.streamable_http import streamablehttp_client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class MCPServerConfig:
    """Configuration for MCP server connection."""
    url: str
    name: str
    timeout: int = 30
    retry_attempts: int = 3
    retry_delay: float = 1.0
    health_check_interval: int = 60

@dataclass
class RAGResponse:
    """Standardized RAG response structure."""
    success: bool
    response: str
    sources: List[Dict[str, Any]]
    confidence_score: float
    processing_time: float
    tools_used: List[str]
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class ProductionMCPManager:
    """
    Production-ready MCP manager with health monitoring, failover, and caching.
    """
    
    def __init__(self, server_configs: List[MCPServerConfig]):
        """
        Initialize the production MCP manager.
        
        Args:
            server_configs: List of MCP server configurations
        """
        self.server_configs = server_configs
        self.mcp_clients = {}
        self.server_health = {}
        self.response_cache = {}
        self.cache_ttl = 300  # 5 minutes
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.metrics = {
            "requests_total": 0,
            "requests_successful": 0,
            "requests_failed": 0,
            "cache_hits": 0,
            "average_response_time": 0.0,
            "server_health_checks": 0
        }
        
    async def initialize(self):
        """Initialize all MCP clients and start health monitoring."""
        logger.info("Initializing Production MCP Manager...")
        
        # Initialize MCP clients for each server
        for config in self.server_configs:
            try:
                client = MCPClient(lambda: streamablehttp_client(config.url))
                self.mcp_clients[config.name] = {
                    "client": client,
                    "config": config,
                    "last_health_check": None
                }
                self.server_health[config.name] = {
                    "healthy": False,
                    "last_check": None,
                    "error_count": 0,
                    "response_times": []
                }
                
                # Perform initial health check
                await self._check_server_health(config.name)
                
            except Exception as e:
                logger.error(f"Failed to initialize MCP client for {config.name}: {e}")
                self.server_health[config.name] = {
                    "healthy": False,
                    "last_check": datetime.now(),
                    "error_count": 1,
                    "response_times": [],
                    "error": str(e)
                }
        
        # Start health monitoring task
        asyncio.create_task(self._health_monitor_loop())
        
        logger.info(f"MCP Manager initialized with {len(self.mcp_clients)} servers")
    
    async def _check_server_health(self, server_name: str) -> bool:
        """Check the health of a specific MCP server."""
        try:
            config = self.mcp_clients[server_name]["config"]
            client = self.mcp_clients[server_name]["client"]
            
            start_time = time.time()
            
            # Try to list tools as a health check
            async with client:
                tools = await client.list_tools()
                
            response_time = time.time() - start_time
            
            # Update health status
            self.server_health[server_name].update({
                "healthy": True,
                "last_check": datetime.now(),
                "error_count": 0,
                "response_time": response_time
            })
            
            # Track response times (keep last 10)
            response_times = self.server_health[server_name]["response_times"]
            response_times.append(response_time)
            if len(response_times) > 10:
                response_times.pop(0)
            
            self.metrics["server_health_checks"] += 1
            
            logger.debug(f"Health check passed for {server_name} ({response_time:.2f}s)")
            return True
            
        except Exception as e:
            self.server_health[server_name].update({
                "healthy": False,
                "last_check": datetime.now(),
                "error_count": self.server_health[server_name]["error_count"] + 1,
                "error": str(e)
            })
            
            logger.warning(f"Health check failed for {server_name}: {e}")
            return False
    
    async def _health_monitor_loop(self):
        """Continuous health monitoring loop."""
        while True:
            try:
                for server_name in self.mcp_clients.keys():
                    await self._check_server_health(server_name)
                
                # Wait for next health check cycle
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                logger.error(f"Error in health monitor loop: {e}")
                await asyncio.sleep(30)  # Shorter delay on error
    
    def _get_cache_key(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Generate cache key for tool calls."""
        return f"{tool_name}:{hash(json.dumps(arguments, sort_keys=True))}"
    
    def _is_cache_valid(self, cache_entry: Dict[str, Any]) -> bool:
        """Check if cache entry is still valid."""
        timestamp = cache_entry.get("timestamp")
        if not timestamp:
            return False
        
        cache_time = datetime.fromisoformat(timestamp)
        return datetime.now() - cache_time < timedelta(seconds=self.cache_ttl)
    
    async def call_tool_with_failover(
        self,
        tool_name: str,
        arguments: Dict[str, Any],
        preferred_server: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Call an MCP tool with automatic failover and caching.
        
        Args:
            tool_name: Name of the tool to call
            arguments: Tool arguments
            preferred_server: Preferred server to use (optional)
            
        Returns:
            Tool response with metadata
        """
        start_time = time.time()
        self.metrics["requests_total"] += 1
        
        # Check cache first
        cache_key = self._get_cache_key(tool_name, arguments)
        if cache_key in self.response_cache:
            cache_entry = self.response_cache[cache_key]
            if self._is_cache_valid(cache_entry):
                self.metrics["cache_hits"] += 1
                logger.debug(f"Cache hit for {tool_name}")
                return {
                    "success": True,
                    "result": cache_entry["result"],
                    "cached": True,
                    "server_used": cache_entry["server"],
                    "processing_time": time.time() - start_time
                }
        
        # Determine server order (preferred first, then by health)
        server_order = []
        if preferred_server and preferred_server in self.mcp_clients:
            server_order.append(preferred_server)
        
        # Add other healthy servers
        healthy_servers = [
            name for name, health in self.server_health.items()
            if health["healthy"] and name != preferred_server
        ]
        server_order.extend(healthy_servers)
        
        # Try each server in order
        last_error = None
        for server_name in server_order:
            try:
                client_info = self.mcp_clients[server_name]
                client = client_info["client"]
                
                logger.debug(f"Attempting {tool_name} on server {server_name}")
                
                async with client:
                    result = await client.call_tool(
                        name=tool_name,
                        arguments=arguments
                    )
                
                # Cache successful result
                self.response_cache[cache_key] = {
                    "result": result,
                    "timestamp": datetime.now().isoformat(),
                    "server": server_name
                }
                
                # Update metrics
                processing_time = time.time() - start_time
                self.metrics["requests_successful"] += 1
                self._update_average_response_time(processing_time)
                
                return {
                    "success": True,
                    "result": result,
                    "cached": False,
                    "server_used": server_name,
                    "processing_time": processing_time
                }
                
            except Exception as e:
                last_error = e
                logger.warning(f"Tool call failed on server {server_name}: {e}")
                
                # Mark server as unhealthy
                self.server_health[server_name]["healthy"] = False
                self.server_health[server_name]["error_count"] += 1
                continue
        
        # All servers failed
        self.metrics["requests_failed"] += 1
        processing_time = time.time() - start_time
        
        return {
            "success": False,
            "error": f"All servers failed. Last error: {last_error}",
            "servers_tried": server_order,
            "processing_time": processing_time
        }
    
    def _update_average_response_time(self, response_time: float):
        """Update the average response time metric."""
        current_avg = self.metrics["average_response_time"]
        total_successful = self.metrics["requests_successful"]
        
        if total_successful == 1:
            self.metrics["average_response_time"] = response_time
        else:
            # Exponential moving average
            alpha = 0.1
            self.metrics["average_response_time"] = (
                alpha * response_time + (1 - alpha) * current_avg
            )
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics and health status."""
        return {
            "performance_metrics": self.metrics.copy(),
            "server_health": self.server_health.copy(),
            "cache_stats": {
                "total_entries": len(self.response_cache),
                "cache_hit_rate": (
                    self.metrics["cache_hits"] / max(self.metrics["requests_total"], 1)
                )
            },
            "timestamp": datetime.now().isoformat()
        }
    
    def clear_cache(self):
        """Clear the response cache."""
        self.response_cache.clear()
        logger.info("Response cache cleared")

class ProductionRAGAgent:
    """
    Production-ready RAG agent with comprehensive monitoring and error handling.
    """
    
    def __init__(self, mcp_manager: ProductionMCPManager):
        """
        Initialize the production RAG agent.
        
        Args:
            mcp_manager: Production MCP manager instance
        """
        self.mcp_manager = mcp_manager
        self.agent = None
        self.session_metrics = {
            "queries_processed": 0,
            "successful_responses": 0,
            "failed_responses": 0,
            "average_confidence": 0.0,
            "session_start": datetime.now().isoformat()
        }
    
    async def initialize(self):
        """Initialize the agent and MCP manager."""
        await self.mcp_manager.initialize()
        
        # Create agent with robust system prompt
        self.agent = Agent(
            model="anthropic.claude-3-sonnet-20240229-v1:0",
            system_prompt=self._get_production_system_prompt()
        )
        
        logger.info("Production RAG Agent initialized")
    
    def _get_production_system_prompt(self) -> str:
        """Get production-grade system prompt."""
        return """You are a production RAG system with access to multiple knowledge sources through MCP tools. Your responses must be:

1. **Accurate and Reliable**: Only provide information you can verify through the available tools
2. **Well-Sourced**: Always cite your sources and indicate confidence levels
3. **Comprehensive**: Use multiple tools when beneficial to provide complete answers
4. **Error-Aware**: Gracefully handle failures and explain limitations
5. **Consistent**: Maintain the same quality across all responses

Available knowledge sources:
- Technical documentation
- Code examples and implementations  
- FAQ database
- Comprehensive topic overviews

When responding:
- Search multiple sources when the query warrants it
- Provide confidence scores for your answers
- Include source citations with relevance scores
- Suggest follow-up questions or related topics
- If tools fail, explain what happened and provide best-effort responses
- Always be honest about the limitations of available information
"""
    
    async def process_query(
        self,
        query: str,
        search_strategy: str = "comprehensive",
        confidence_threshold: float = 0.7
    ) -> RAGResponse:
        """
        Process a query with comprehensive error handling and monitoring.
        
        Args:
            query: User query
            search_strategy: Search strategy (quick, comprehensive, targeted)
            confidence_threshold: Minimum confidence threshold for responses
            
        Returns:
            RAGResponse with complete metadata
        """
        start_time = time.time()
        self.session_metrics["queries_processed"] += 1
        
        try:
            # Determine search tools based on strategy
            search_tools = self._get_search_tools(search_strategy)
            
            # Execute searches with failover
            search_results = {}
            tools_used = []
            
            for tool_name, tool_args in search_tools.items():
                result = await self.mcp_manager.call_tool_with_failover(
                    tool_name=tool_name,
                    arguments={**tool_args, "query": query}
                )
                
                if result["success"]:
                    search_results[tool_name] = result["result"]
                    tools_used.append(tool_name)
                else:
                    logger.warning(f"Tool {tool_name} failed: {result.get('error')}")
            
            # Synthesize response
            if search_results:
                synthesis_prompt = self._create_synthesis_prompt(query, search_results)
                response_text = await self.agent.run_async(synthesis_prompt)
                
                # Calculate confidence score
                confidence_score = self._calculate_confidence(search_results, tools_used)
                
                # Extract sources
                sources = self._extract_sources(search_results)
                
                # Check confidence threshold
                if confidence_score < confidence_threshold:
                    response_text += f"\n\n⚠️ Note: This response has a confidence score of {confidence_score:.2f}, which is below the threshold of {confidence_threshold}. Please verify the information independently."
                
                processing_time = time.time() - start_time
                self.session_metrics["successful_responses"] += 1
                self._update_average_confidence(confidence_score)
                
                return RAGResponse(
                    success=True,
                    response=str(response_text),
                    sources=sources,
                    confidence_score=confidence_score,
                    processing_time=processing_time,
                    tools_used=tools_used,
                    metadata={
                        "search_strategy": search_strategy,
                        "search_results_count": len(search_results),
                        "cache_hits": sum(1 for r in search_results.values() if r.get("cached", False))
                    }
                )
            else:
                # No search results available
                processing_time = time.time() - start_time
                self.session_metrics["failed_responses"] += 1
                
                return RAGResponse(
                    success=False,
                    response="I apologize, but I couldn't retrieve any information to answer your query. This might be due to service issues or the query being outside my knowledge base.",
                    sources=[],
                    confidence_score=0.0,
                    processing_time=processing_time,
                    tools_used=[],
                    error="No search results available",
                    metadata={"search_strategy": search_strategy}
                )
                
        except Exception as e:
            processing_time = time.time() - start_time
            self.session_metrics["failed_responses"] += 1
            
            logger.error(f"Error processing query: {e}")
            logger.error(traceback.format_exc())
            
            return RAGResponse(
                success=False,
                response=f"An error occurred while processing your query: {str(e)}",
                sources=[],
                confidence_score=0.0,
                processing_time=processing_time,
                tools_used=[],
                error=str(e),
                metadata={"search_strategy": search_strategy}
            )
    
    def _get_search_tools(self, strategy: str) -> Dict[str, Dict[str, Any]]:
        """Get search tools based on strategy."""
        if strategy == "quick":
            return {
                "search_technical_docs": {"max_results": 2},
                "get_faq_answers": {}
            }
        elif strategy == "comprehensive":
            return {
                "search_technical_docs": {"max_results": 5},
                "search_code_examples": {},
                "get_faq_answers": {},
                "get_topic_overview": {}
            }
        elif strategy == "targeted":
            return {
                "get_topic_overview": {}
            }
        else:
            # Default to comprehensive
            return self._get_search_tools("comprehensive")
    
    def _create_synthesis_prompt(self, query: str, search_results: Dict[str, Any]) -> str:
        """Create synthesis prompt for multiple search results."""
        prompt = f"""Based on the following search results for "{query}", provide a comprehensive response:

SEARCH RESULTS:
"""
        
        for tool_name, result in search_results.items():
            prompt += f"\n### {tool_name.replace('_', ' ').title()}:\n"
            
            # Extract content based on result structure
            if isinstance(result, dict) and "content" in result:
                content = result["content"]
                if isinstance(content, list) and content:
                    # Handle MCP response format
                    content_data = content[0].get("text", {})
                    if "results" in content_data:
                        for item in content_data["results"][:3]:  # Limit to top 3
                            prompt += f"- {item.get('title', 'Item')}: {str(item)[:200]}...\n"
                    else:
                        prompt += f"{str(content_data)[:300]}...\n"
                else:
                    prompt += f"{str(content)[:300]}...\n"
            else:
                prompt += f"{str(result)[:300]}...\n"
        
        prompt += """
Please provide a comprehensive response that:
1. Directly answers the user's query
2. Synthesizes information from multiple sources
3. Includes relevant code examples if available
4. Cites sources with confidence indicators
5. Suggests related topics or follow-up questions

Format your response professionally with clear sections and proper citations.
"""
        
        return prompt
    
    def _calculate_confidence(self, search_results: Dict[str, Any], tools_used: List[str]) -> float:
        """Calculate confidence score based on search results."""
        if not search_results:
            return 0.0
        
        base_confidence = 0.5  # Base confidence for having any results
        
        # Boost confidence based on number of sources
        source_boost = min(len(search_results) * 0.1, 0.3)
        
        # Boost confidence based on specific tools used
        tool_boost = 0.0
        if "get_topic_overview" in tools_used:
            tool_boost += 0.1
        if "search_technical_docs" in tools_used:
            tool_boost += 0.1
        
        # Check for cached results (slightly lower confidence)
        cache_penalty = 0.0
        cached_results = sum(1 for r in search_results.values() if r.get("cached", False))
        if cached_results == len(search_results):
            cache_penalty = 0.05
        
        final_confidence = min(base_confidence + source_boost + tool_boost - cache_penalty, 1.0)
        return round(final_confidence, 2)
    
    def _extract_sources(self, search_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract source information from search results."""
        sources = []
        
        for tool_name, result in search_results.items():
            sources.append({
                "tool": tool_name,
                "cached": result.get("cached", False),
                "server": result.get("server_used", "unknown"),
                "processing_time": result.get("processing_time", 0.0)
            })
        
        return sources
    
    def _update_average_confidence(self, confidence: float):
        """Update average confidence metric."""
        current_avg = self.session_metrics["average_confidence"]
        successful_count = self.session_metrics["successful_responses"]
        
        if successful_count == 1:
            self.session_metrics["average_confidence"] = confidence
        else:
            # Moving average
            alpha = 0.1
            self.session_metrics["average_confidence"] = (
                alpha * confidence + (1 - alpha) * current_avg
            )
    
    def get_comprehensive_metrics(self) -> Dict[str, Any]:
        """Get comprehensive metrics including MCP manager metrics."""
        return {
            "session_metrics": self.session_metrics.copy(),
            "mcp_metrics": self.mcp_manager.get_metrics(),
            "session_duration_minutes": (
                datetime.now() - datetime.fromisoformat(self.session_metrics["session_start"])
            ).total_seconds() / 60
        }

# Example usage and demonstration
async def demo_production_rag():
    """Demonstrate the production RAG system."""
    print("🏭 Production MCP RAG System Demo")
    print("=" * 50)
    
    # Configure MCP servers
    server_configs = [
        MCPServerConfig(
            url="http://127.0.0.1:8000/mcp/",
            name="primary_knowledge_server",
            timeout=30
        )
        # Add more servers for true production setup
    ]
    
    # Initialize components
    mcp_manager = ProductionMCPManager(server_configs)
    rag_agent = ProductionRAGAgent(mcp_manager)
    
    try:
        await rag_agent.initialize()
        print("✅ Production RAG system initialized")
        
        # Test queries
        test_queries = [
            "How do I set up AWS Bedrock?",
            "Show me code examples for Strands agents",
            "What are best practices for cost optimization?",
            "Explain the Model Context Protocol"
        ]
        
        for query in test_queries:
            print(f"\n🔍 Query: {query}")
            
            response = await rag_agent.process_query(
                query=query,
                search_strategy="comprehensive"
            )
            
            print(f"✅ Success: {response.success}")
            print(f"🎯 Confidence: {response.confidence_score}")
            print(f"⏱️ Time: {response.processing_time:.2f}s")
            print(f"🛠️ Tools: {', '.join(response.tools_used)}")
            
            if response.success:
                print(f"📝 Response: {response.response[:200]}...")
            else:
                print(f"❌ Error: {response.error}")
        
        # Show metrics
        print("\n📊 Final Metrics:")
        metrics = rag_agent.get_comprehensive_metrics()
        print(json.dumps(metrics, indent=2, default=str))
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(demo_production_rag())

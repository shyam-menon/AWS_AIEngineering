"""
MCP RAG Agent - Strands Agent with Model Context Protocol Integration

This module demonstrates how to create a Strands agent that uses MCP tools
for advanced RAG operations. The agent can search multiple knowledge sources,
synthesize information, and provide comprehensive responses.

Author: AI Engineering Course
Version: 1.0.0
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any
import traceback
from datetime import datetime

# Strands and MCP imports
from strands import Agent
from strands.tools.mcp import MCPClient
from mcp import StdioServerParameters, stdio_client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MCPRAGAgent:
    """
    A RAG-enabled agent that uses MCP tools for knowledge retrieval and synthesis.
    """
    
    def __init__(self, mcp_server_command: str = "python", mcp_server_args: List[str] = None):
        """
        Initialize the MCP RAG Agent.
        
        Args:
            mcp_server_command: Command to run the MCP server (default: "python")
            mcp_server_args: Arguments for the MCP server (default: ["mcp_stdio_server.py"])
        """
        self.mcp_server_command = mcp_server_command
        self.mcp_server_args = mcp_server_args or ["mcp_knowledge_server.py"]
        self.mcp_client = None
        self.agent = None
        self.session_stats = {
            "queries_processed": 0,
            "tools_used": {},
            "session_start": datetime.now().isoformat()
        }
        
    def create_mcp_client(self):
        """Create MCP client with stdio connection to the knowledge server."""
        return MCPClient(
            lambda: stdio_client(
                StdioServerParameters(
                    command=self.mcp_server_command,
                    args=self.mcp_server_args
                )
            )
        )
    
    async def initialize(self):
        """Initialize the MCP client and Strands agent."""
    async def initialize(self):
        """Initialize the MCP client and Strands agent."""
        try:
            logger.info("Connecting to MCP knowledge server...")
            
            # Create MCP client
            self.mcp_client = self.create_mcp_client()
            
            # Use context manager to get tools
            with self.mcp_client:
                tools = self.mcp_client.list_tools_sync()
                
                logger.info(f"Retrieved {len(tools)} tools from MCP server:")
                for tool in tools:
                    tool_name = getattr(tool, 'name', getattr(tool, 'function', {}).get('name', 'Unknown'))
                    tool_desc = getattr(tool, 'description', getattr(tool, 'function', {}).get('description', 'No description'))
                    logger.info(f"  - {tool_name}: {tool_desc}")
                
                # Create Strands agent with MCP tools
                self.agent = Agent(
                    model="us.amazon.nova-lite-v1:0",
                    tools=tools,
                    system_prompt=self._get_system_prompt()
                )
            
            logger.info("MCP RAG Agent initialized successfully")
            return True
                
        except Exception as e:
            logger.error(f"Failed to initialize MCP RAG Agent: {e}")
            logger.error(traceback.format_exc())
            return False
    
    def cleanup(self):
        """Clean up MCP client connection"""
        try:
            if self.mcp_client:
                # The context manager handles cleanup automatically
                logger.info("MCP client connection cleaned up")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the RAG agent."""
        return """You are an intelligent RAG (Retrieval-Augmented Generation) agent with access to a comprehensive knowledge base through MCP tools. Your role is to:

1. **Analyze User Queries**: Understand what information the user is seeking
2. **Search Knowledge Sources**: Use available MCP tools to find relevant information from:
   - Technical documentation
   - Code examples and snippets
   - Frequently asked questions
   - Comprehensive topic overviews

3. **Synthesize Information**: Combine information from multiple sources to provide comprehensive answers
4. **Provide Context**: Always cite your sources and explain the relevance of the information
5. **Be Helpful**: Offer additional resources or suggest follow-up queries when appropriate

Available Tools:
- search_technical_docs: Search technical documentation
- search_code_examples: Find relevant code snippets
- get_faq_answers: Get answers from FAQ database
- get_topic_overview: Get comprehensive information about topics
- add_knowledge_entry: Add new information to the knowledge base
- get_knowledge_stats: Get statistics about the knowledge base

When responding:
- Use multiple tools when beneficial to provide comprehensive answers
- Cite the sources of your information
- Provide code examples when relevant
- Suggest related topics or follow-up questions
- If information is not found, explain what you searched and suggest alternatives
"""

    async def query(self, user_query: str) -> Dict[str, Any]:
        """
        Process a user query using MCP tools and generate a comprehensive response.
        
        Args:
            user_query: The user's question or request
            
        Returns:
            Dictionary containing the response and metadata
        """
        if not self.agent:
            return {
                "error": "Agent not initialized. Call initialize() first.",
                "success": False
            }
        
        try:
            logger.info(f"Processing query: {user_query}")
            
            # Track query
            self.session_stats["queries_processed"] += 1
            
            # Use the agent to process the query within MCP client context
            with self.mcp_client:
                response = str(self.agent(user_query))
            
            # Extract tool usage information
            tools_used = []
            if hasattr(response, 'tool_calls') and response.tool_calls:
                for tool_call in response.tool_calls:
                    tool_name = tool_call.name
                    tools_used.append(tool_name)
                    
                    # Update session stats
                    if tool_name in self.session_stats["tools_used"]:
                        self.session_stats["tools_used"][tool_name] += 1
                    else:
                        self.session_stats["tools_used"][tool_name] = 1
                
            return {
                "success": True,
                "query": user_query,
                "response": response,
                "tools_used": tools_used,
                "timestamp": datetime.now().isoformat(),
                "session_stats": self.session_stats.copy()
            }
                
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            logger.error(traceback.format_exc())
            return {
                "success": False,
                "error": str(e),
                "query": user_query,
                "timestamp": datetime.now().isoformat()
            }
    
    async def search_and_synthesize(self, query: str, search_types: List[str] = None) -> Dict[str, Any]:
        """
        Perform targeted searches and synthesize the results.
        
        Args:
            query: Search query
            search_types: List of search types to perform (technical_docs, code_examples, faqs, overview)
            
        Returns:
            Synthesized results from multiple sources
        """
        if not self.mcp_client:
            return {"error": "MCP client not initialized"}
        
        if search_types is None:
            search_types = ["technical_docs", "code_examples", "faqs"]
        
        results = {
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "searches_performed": [],
            "synthesized_response": ""
        }
        
        try:
            with self.mcp_client:
                # Perform different types of searches
                if "technical_docs" in search_types:
                    tech_results = self.mcp_client.call_tool_sync(
                        name="search_technical_docs",
                        arguments={"query": query, "max_results": 3}
                    )
                    results["technical_docs"] = tech_results
                    results["searches_performed"].append("technical_docs")
                
                if "code_examples" in search_types:
                    code_results = self.mcp_client.call_tool_sync(
                        name="search_code_examples",
                        arguments={"query": query}
                    )
                    results["code_examples"] = code_results
                    results["searches_performed"].append("code_examples")
                
                if "faqs" in search_types:
                    faq_results = self.mcp_client.call_tool_sync(
                        name="get_faq_answers",
                        arguments={"query": query}
                    )
                    results["faqs"] = faq_results
                    results["searches_performed"].append("faqs")
                
                if "overview" in search_types:
                    overview_results = self.mcp_client.call_tool_sync(
                        name="get_topic_overview",
                        arguments={"topic": query}
                    )
                    results["overview"] = overview_results
                    results["searches_performed"].append("overview")
                
                # Synthesize the results
                synthesis_prompt = self._create_synthesis_prompt(query, results)
                response = await self.agent.run_async(synthesis_prompt)
                results["synthesized_response"] = str(response)
                
        except Exception as e:
            results["error"] = str(e)
            logger.error(f"Error in search and synthesis: {e}")
        
        return results
    
    def _create_synthesis_prompt(self, query: str, search_results: Dict[str, Any]) -> str:
        """Create a prompt for synthesizing search results."""
        prompt = f"""Based on the following search results for the query "{query}", provide a comprehensive and well-structured response:

SEARCH RESULTS:
"""
        
        # Add technical documentation results
        if "technical_docs" in search_results:
            prompt += "\n## Technical Documentation:\n"
            tech_data = search_results["technical_docs"].get("content", [])
            if isinstance(tech_data, list) and tech_data:
                for result in tech_data[0].get("text", {}).get("results", []):
                    prompt += f"- {result.get('title', 'Unknown')}: {result.get('content', '')[:200]}...\n"
        
        # Add code examples
        if "code_examples" in search_results:
            prompt += "\n## Code Examples:\n"
            code_data = search_results["code_examples"].get("content", [])
            if isinstance(code_data, list) and code_data:
                for result in code_data[0].get("text", {}).get("results", []):
                    prompt += f"- {result.get('title', 'Unknown')}: {result.get('content', '')}\n"
        
        # Add FAQ results
        if "faqs" in search_results:
            prompt += "\n## FAQ Answers:\n"
            faq_data = search_results["faqs"].get("content", [])
            if isinstance(faq_data, list) and faq_data:
                for result in faq_data[0].get("text", {}).get("results", []):
                    prompt += f"- Q: {result.get('question', 'Unknown')}\n  A: {result.get('answer', '')}\n"
        
        prompt += """
Please synthesize this information to provide a comprehensive answer that:
1. Directly addresses the user's query
2. Combines information from multiple sources when relevant
3. Provides practical examples and code when applicable
4. Cites the sources of information
5. Suggests follow-up questions or related topics if appropriate

Response:"""
        
        return prompt
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Get current session statistics."""
        return {
            **self.session_stats,
            "session_duration_minutes": (
                datetime.now() - datetime.fromisoformat(self.session_stats["session_start"])
            ).total_seconds() / 60
        }

# CLI Interface for testing
async def main():
    """Main function for CLI testing of the MCP RAG Agent."""
    print("🤖 MCP RAG Agent - Interactive Demo")
    print("=" * 50)
    
    # Initialize the agent
    agent = MCPRAGAgent()
    
    print("Initializing MCP RAG Agent...")
    success = await agent.initialize()
    
    if not success:
        print("❌ Failed to initialize agent. Make sure the MCP server is running.")
        print("Start the server with: python mcp_knowledge_server.py")
        return
    
    print("✅ Agent initialized successfully!")
    print("\nAvailable commands:")
    print("  - Ask any question")
    print("  - Type 'stats' to see session statistics")
    print("  - Type 'search <query>' for detailed search")
    print("  - Type 'quit' to exit")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("\n🧑 Query: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            elif user_input.lower() == 'stats':
                stats = agent.get_session_stats()
                print(f"\n📊 Session Statistics:")
                print(f"  Queries processed: {stats['queries_processed']}")
                print(f"  Session duration: {stats['session_duration_minutes']:.1f} minutes")
                print(f"  Tools used: {stats['tools_used']}")
                continue
            elif user_input.lower().startswith('search '):
                search_query = user_input[7:].strip()
                print(f"\n🔍 Performing detailed search for: {search_query}")
                results = await agent.search_and_synthesize(search_query)
                print(f"\n🤖 Agent Response:\n{results.get('synthesized_response', 'No response generated')}")
                continue
            elif not user_input:
                continue
            
            # Process regular query
            print("\n🔍 Processing query...")
            result = await agent.query(user_input)
            
            if result["success"]:
                print(f"\n🤖 Agent Response:\n{result['response']}")
                if result.get('tools_used'):
                    print(f"\n🛠️ Tools used: {', '.join(result['tools_used'])}")
            else:
                print(f"\n❌ Error: {result.get('error', 'Unknown error')}")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
    
    print("\n👋 Thanks for using MCP RAG Agent!")
    stats = agent.get_session_stats()
    print(f"Final stats: {stats['queries_processed']} queries processed in {stats['session_duration_minutes']:.1f} minutes")
    
    # Clean up connections
    agent.cleanup()

if __name__ == "__main__":
    asyncio.run(main())

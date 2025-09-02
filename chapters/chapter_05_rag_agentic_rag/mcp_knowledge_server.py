#!/usr/bin/env python3
"""
MCP Knowledge Server - A Model Context Protocol server for RAG operations using stdio.

This module demonstrates how to create an MCP server that provides knowledge retrieval
tools for Strands agents using stdio transport. The server simulates a knowledge base 
with different data sources and retrieval capabilities commonly used in RAG applications.

Author: AI Engineering Course
Version: 1.0.0
"""

import asyncio
import logging
from typing import List, Optional, Any
from mcp.server.stdio import stdio_server
from mcp.server import Server
from mcp.types import Tool, TextContent
import numpy as np
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the MCP server instance
server = Server("rag-knowledge-server")

# Simulated knowledge base for demonstration
KNOWLEDGE_BASE = {
    "technical_docs": [
        {
            "id": "doc_001",
            "title": "AWS Bedrock Overview",
            "content": "Amazon Bedrock is a fully managed service that offers a choice of high-performing foundation models (FMs) from leading AI companies like AI21 Labs, Anthropic, Cohere, Meta, Stability AI, and Amazon via a single API, along with a broad set of capabilities you need to build generative AI applications with security, privacy, and responsible AI.",
            "category": "AWS Services",
            "source": "AWS Documentation",
            "tags": ["aws", "bedrock", "ai", "ml"],
            "last_updated": "2024-01-15"
        },
        {
            "id": "doc_002", 
            "title": "Strands Agent Framework",
            "content": "Strands is an open-source framework for building intelligent AI agents that can use tools, maintain conversations, and integrate with external systems. It provides a simple yet powerful API for creating conversational AI applications with built-in support for function calling and memory management.",
            "category": "AI Frameworks",
            "source": "Strands Documentation",
            "tags": ["strands", "agents", "framework", "ai"],
            "last_updated": "2024-01-10"
        },
        {
            "id": "doc_003",
            "title": "Model Context Protocol (MCP)",
            "content": "The Model Context Protocol (MCP) is an open standard that enables AI assistants to securely access external data sources and tools. It provides a standardized way for AI models to retrieve contextual information, execute functions, and interact with various systems while maintaining security and privacy.",
            "category": "Protocols",
            "source": "MCP Specification",
            "tags": ["mcp", "protocol", "ai", "tools"],
            "last_updated": "2024-01-20"
        }
    ],
    "code_examples": [
        {
            "id": "code_001",
            "title": "Basic Strands Agent",
            "code": '''from strands import Agent

agent = Agent(
    model="anthropic.claude-3-sonnet-20240229-v1:0",
    system_prompt="You are a helpful assistant."
)

response = agent("What is machine learning?")
print(response)''',
            "language": "python",
            "description": "Simple example of creating and using a Strands agent",
            "complexity": "beginner",
            "tags": ["strands", "python", "basic"]
        },
        {
            "id": "code_002",
            "title": "MCP Client Example",
            "code": '''from strands.tools.mcp import MCPClient
from mcp import StdioServerParameters, stdio_client

mcp_client = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(
            command="python",
            args=["my_mcp_server.py"]
        )
    )
)

with mcp_client:
    tools = mcp_client.list_tools_sync()
    result = mcp_client.call_tool_sync("my_tool", {"arg": "value"})''',
            "language": "python",
            "description": "Example of connecting to an MCP server using Strands",
            "complexity": "intermediate",
            "tags": ["mcp", "strands", "client"]
        }
    ],
    "faqs": [
        {
            "id": "faq_001",
            "question": "What is the difference between RAG and fine-tuning?",
            "answer": "RAG (Retrieval-Augmented Generation) retrieves relevant information at inference time to supplement the model's knowledge, while fine-tuning permanently updates the model's parameters with new data. RAG is more flexible for dynamic information and doesn't require retraining, while fine-tuning creates a specialized model for specific tasks.",
            "category": "AI Concepts",
            "tags": ["rag", "fine-tuning", "ai"]
        },
        {
            "id": "faq_002",
            "question": "How do I handle rate limits with AWS Bedrock?",
            "answer": "AWS Bedrock has request rate limits and token limits per model. To handle them: 1) Implement exponential backoff for retries, 2) Use batch processing for multiple requests, 3) Monitor your usage with CloudWatch, 4) Request quota increases if needed, 5) Implement caching to reduce redundant calls.",
            "category": "AWS",
            "tags": ["aws", "bedrock", "rate-limits"]
        }
    ]
}

def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate simple word overlap similarity between two texts."""
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    if not words1 or not words2:
        return 0.0
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union) if union else 0.0

@server.list_tools()
async def list_tools() -> List[Tool]:
    """List all available tools."""
    return [
        Tool(
            name="search_technical_docs",
            description="Search technical documentation for relevant information",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "max_results": {"type": "integer", "description": "Maximum number of results", "default": 5}
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="search_code_examples",
            description="Search code examples and snippets",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "language": {"type": "string", "description": "Programming language filter"}
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_faq_answers",
            description="Get answers to frequently asked questions",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Question or topic"}
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_topic_overview",
            description="Retrieve comprehensive information about a specific topic",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "Topic name"}
                },
                "required": ["topic"]
            }
        ),
        Tool(
            name="add_knowledge_entry",
            description="Add new knowledge to the knowledge base",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {"type": "string", "description": "Knowledge category"},
                    "title": {"type": "string", "description": "Entry title"},
                    "content": {"type": "string", "description": "Entry content"},
                    "tags": {"type": "array", "items": {"type": "string"}, "description": "Tags"}
                },
                "required": ["category", "title", "content"]
            }
        ),
        Tool(
            name="get_knowledge_stats",
            description="Get statistics about the knowledge base",
            inputSchema={
                "type": "object",
                "properties": {},
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> List[TextContent]:
    """Handle tool calls."""
    try:
        if name == "search_technical_docs":
            return await search_technical_docs(arguments.get("query", ""), arguments.get("max_results", 5))
        elif name == "search_code_examples":
            return await search_code_examples(arguments.get("query", ""), arguments.get("language"))
        elif name == "get_faq_answers":
            return await get_faq_answers(arguments.get("query", ""))
        elif name == "get_topic_overview":
            return await get_topic_overview(arguments.get("topic", ""))
        elif name == "add_knowledge_entry":
            return await add_knowledge_entry(
                arguments.get("category", ""),
                arguments.get("title", ""),
                arguments.get("content", ""),
                arguments.get("tags", [])
            )
        elif name == "get_knowledge_stats":
            return await get_knowledge_stats()
        else:
            raise ValueError(f"Unknown tool: {name}")
    except Exception as e:
        logger.error(f"Error in tool {name}: {e}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]

async def search_technical_docs(query: str, max_results: int = 5) -> List[TextContent]:
    """Search through technical documentation using semantic similarity."""
    logger.info(f"Searching technical docs for: {query}")
    
    results = []
    for doc in KNOWLEDGE_BASE["technical_docs"]:
        # Calculate relevance score
        title_score = calculate_similarity(query, doc["title"]) * 2.0
        content_score = calculate_similarity(query, doc["content"])
        tag_score = max([calculate_similarity(query, tag) for tag in doc["tags"]], default=0) * 1.5
        
        total_score = title_score + content_score + tag_score
        
        if total_score > 0.1:  # Minimum relevance threshold
            results.append({
                "title": doc["title"],
                "content": doc["content"][:500] + "..." if len(doc["content"]) > 500 else doc["content"],
                "category": doc["category"],
                "source": doc["source"],
                "relevance_score": round(total_score, 3),
                "last_updated": doc["last_updated"]
            })
    
    # Sort by relevance score and limit results
    results.sort(key=lambda x: x["relevance_score"], reverse=True)
    results = results[:max_results]
    
    # Format results as TextContent
    response_text = f"Found {len(results)} technical documentation results for '{query}':\n\n"
    for i, result in enumerate(results, 1):
        response_text += f"{i}. **{result['title']}** (Score: {result['relevance_score']})\n"
        response_text += f"   Category: {result['category']}\n"
        response_text += f"   Content: {result['content']}\n"
        response_text += f"   Source: {result['source']}\n\n"
    
    return [TextContent(type="text", text=response_text)]

async def search_code_examples(query: str, language: Optional[str] = None) -> List[TextContent]:
    """Search through code examples and snippets."""
    logger.info(f"Searching code examples for: {query}")
    
    results = []
    for example in KNOWLEDGE_BASE["code_examples"]:
        # Filter by language if specified
        if language and example["language"] != language.lower():
            continue
            
        # Calculate relevance score
        title_score = calculate_similarity(query, example["title"]) * 2.0
        desc_score = calculate_similarity(query, example["description"])
        tag_score = max([calculate_similarity(query, tag) for tag in example["tags"]], default=0) * 1.5
        
        total_score = title_score + desc_score + tag_score
        
        if total_score > 0.1:
            results.append({
                "title": example["title"],
                "code": example["code"],
                "description": example["description"],
                "language": example["language"],
                "complexity": example["complexity"],
                "relevance_score": round(total_score, 3)
            })
    
    # Sort by relevance score
    results.sort(key=lambda x: x["relevance_score"], reverse=True)
    
    # Format results as TextContent
    response_text = f"Found {len(results)} code examples for '{query}':\n\n"
    for i, result in enumerate(results, 1):
        response_text += f"{i}. **{result['title']}** (Score: {result['relevance_score']})\n"
        response_text += f"   Language: {result['language']}\n"
        response_text += f"   Complexity: {result['complexity']}\n"
        response_text += f"   Description: {result['description']}\n"
        response_text += f"   Code:\n```{result['language']}\n{result['code']}\n```\n\n"
    
    return [TextContent(type="text", text=response_text)]

async def get_faq_answers(query: str) -> List[TextContent]:
    """Get answers to frequently asked questions."""
    logger.info(f"Searching FAQs for: {query}")
    
    results = []
    for faq in KNOWLEDGE_BASE["faqs"]:
        # Calculate relevance score
        question_score = calculate_similarity(query, faq["question"]) * 2.0
        answer_score = calculate_similarity(query, faq["answer"])
        tag_score = max([calculate_similarity(query, tag) for tag in faq["tags"]], default=0) * 1.5
        
        total_score = question_score + answer_score + tag_score
        
        if total_score > 0.1:
            results.append({
                "question": faq["question"],
                "answer": faq["answer"],
                "category": faq["category"],
                "relevance_score": round(total_score, 3)
            })
    
    # Sort by relevance score
    results.sort(key=lambda x: x["relevance_score"], reverse=True)
    
    # Format results as TextContent
    response_text = f"Found {len(results)} FAQ answers for '{query}':\n\n"
    for i, result in enumerate(results, 1):
        response_text += f"{i}. **Q: {result['question']}** (Score: {result['relevance_score']})\n"
        response_text += f"   **A:** {result['answer']}\n"
        response_text += f"   Category: {result['category']}\n\n"
    
    return [TextContent(type="text", text=response_text)]

async def get_topic_overview(topic: str) -> List[TextContent]:
    """Retrieve comprehensive information about a specific topic."""
    logger.info(f"Getting topic overview for: {topic}")
    
    # Search across all categories
    doc_results = await search_technical_docs(topic, max_results=3)
    code_results = await search_code_examples(topic)
    faq_results = await get_faq_answers(topic)
    
    # Combine all results
    overview_text = f"# Topic Overview: {topic}\n\n"
    
    if doc_results and doc_results[0].text.strip():
        overview_text += "## Documentation\n"
        overview_text += doc_results[0].text + "\n"
    
    if code_results and code_results[0].text.strip():
        overview_text += "## Code Examples\n"
        overview_text += code_results[0].text + "\n"
    
    if faq_results and faq_results[0].text.strip():
        overview_text += "## Frequently Asked Questions\n"
        overview_text += faq_results[0].text + "\n"
    
    return [TextContent(type="text", text=overview_text)]

async def add_knowledge_entry(category: str, title: str, content: str, tags: List[str] = None) -> List[TextContent]:
    """Add new knowledge to the knowledge base."""
    logger.info(f"Adding knowledge entry: {title}")
    
    if tags is None:
        tags = []
    
    new_entry = {
        "id": f"user_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "title": title,
        "content": content,
        "category": category,
        "source": "User Contributed",
        "tags": tags,
        "last_updated": datetime.now().strftime("%Y-%m-%d")
    }
    
    # Add to appropriate category
    if category.lower() in ["technical_docs", "documentation", "docs"]:
        KNOWLEDGE_BASE["technical_docs"].append(new_entry)
    elif category.lower() in ["code", "code_examples", "examples"]:
        new_entry.update({
            "code": content,
            "language": "unknown",
            "description": title,
            "complexity": "user-defined"
        })
        KNOWLEDGE_BASE["code_examples"].append(new_entry)
    elif category.lower() in ["faq", "faqs", "questions"]:
        new_entry.update({
            "question": title,
            "answer": content
        })
        KNOWLEDGE_BASE["faqs"].append(new_entry)
    else:
        # Default to technical docs
        KNOWLEDGE_BASE["technical_docs"].append(new_entry)
    
    response_text = f"✅ Successfully added knowledge entry:\n"
    response_text += f"Title: {title}\n"
    response_text += f"Category: {category}\n"
    response_text += f"Tags: {', '.join(tags) if tags else 'None'}\n"
    response_text += f"Entry ID: {new_entry['id']}\n"
    
    return [TextContent(type="text", text=response_text)]

async def get_knowledge_stats() -> List[TextContent]:
    """Get statistics about the knowledge base."""
    logger.info("Getting knowledge base statistics")
    
    stats = {
        "technical_docs": len(KNOWLEDGE_BASE["technical_docs"]),
        "code_examples": len(KNOWLEDGE_BASE["code_examples"]),
        "faqs": len(KNOWLEDGE_BASE["faqs"])
    }
    
    total_entries = sum(stats.values())
    
    # Get unique tags
    all_tags = set()
    for category in KNOWLEDGE_BASE.values():
        for item in category:
            if "tags" in item:
                all_tags.update(item["tags"])
    
    # Get categories
    categories = set()
    for category in KNOWLEDGE_BASE.values():
        for item in category:
            if "category" in item:
                categories.add(item["category"])
    
    response_text = f"📊 Knowledge Base Statistics\n\n"
    response_text += f"**Total Entries:** {total_entries}\n\n"
    response_text += f"**By Category:**\n"
    response_text += f"- Technical Documentation: {stats['technical_docs']}\n"
    response_text += f"- Code Examples: {stats['code_examples']}\n"
    response_text += f"- FAQs: {stats['faqs']}\n\n"
    response_text += f"**Unique Tags:** {len(all_tags)}\n"
    response_text += f"**Content Categories:** {len(categories)}\n\n"
    response_text += f"**Available Tags:** {', '.join(sorted(all_tags))}\n"
    response_text += f"**Content Categories:** {', '.join(sorted(categories))}\n"
    
    return [TextContent(type="text", text=response_text)]

async def main():
    """Main function to run the MCP server."""
    logger.info("Starting MCP Knowledge Server (stdio)")
    
    # Check if we're running in standalone mode (for testing)
    import sys
    if sys.stdin.isatty():
        logger.info("Running in standalone demo mode")
        print("\n🤖 MCP Knowledge Server - Demo Mode")
        print("=" * 50)
        print("This server is designed to be used with Strands agents via MCP.")
        print("To test the server:")
        print("1. Run 'python mcp_rag_agent.py' for interactive agent")
        print("2. Run 'python test_mcp_rag.py' for automated tests")
        print("3. Run 'python demo_mcp_rag.py' for guided demo")
        print("\nServer tools available:")
        tools = await list_tools()
        for i, tool in enumerate(tools, 1):
            print(f"  {i}. {tool.name}: {tool.description}")
        print("\nPress Ctrl+C to exit...")
        
        # Keep the server running for demonstration
        try:
            await asyncio.Event().wait()  # Wait indefinitely
        except KeyboardInterrupt:
            print("\n👋 MCP Knowledge Server stopped")
            return
    else:
        # Normal MCP server mode (called by Strands agent)
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())

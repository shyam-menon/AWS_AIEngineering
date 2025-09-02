# Model Context Protocol (MCP) Integration with Strands Agents

This directory contains a comprehensive implementation of Model Context Protocol (MCP) integration with Strands agents for advanced RAG (Retrieval-Augmented Generation) operations.

## 🎯 Overview

The Model Context Protocol (MCP) enables Strands agents to connect to external tools and data sources in a standardized way. This implementation demonstrates how to build production-ready RAG systems using MCP tools for knowledge retrieval and synthesis.

## 📁 Files Structure

### Core Implementation Files

#### `mcp_knowledge_server.py` - MCP Server Implementation
- **Purpose**: Creates an MCP server that provides knowledge retrieval tools
- **Key Features**:
  - Technical documentation search with semantic similarity
  - Code examples and snippets search  
  - FAQ database with relevance scoring
  - Comprehensive topic overviews across all knowledge sources
  - Knowledge base management (add entries, get statistics)
  - Simulated vector embeddings for semantic search
- **Tools Provided**:
  - `search_technical_docs`: Search technical documentation
  - `search_code_examples`: Find code snippets by language/complexity
  - `get_faq_answers`: Query FAQ database
  - `get_topic_overview`: Comprehensive multi-source information
  - `add_knowledge_entry`: Add new knowledge to the database
  - `get_knowledge_stats`: Get knowledge base statistics
- **Usage**: Run as standalone server on `http://localhost:8000/mcp/`

#### `mcp_rag_agent.py` - Strands Agent with MCP Integration
- **Purpose**: Demonstrates basic MCP integration with Strands agents
- **Key Features**:
  - Connects to MCP knowledge server
  - Processes natural language queries using MCP tools
  - Synthesizes information from multiple sources
  - Session tracking and metrics
  - Interactive CLI interface for testing
- **Capabilities**:
  - Automatic tool selection based on query type
  - Multi-source information synthesis
  - Error handling and graceful degradation
  - Conversational query processing

#### `mcp_production_integration.py` - Production-Ready MCP System
- **Purpose**: Production-grade MCP integration with comprehensive monitoring
- **Key Features**:
  - Multi-server failover and load balancing
  - Health monitoring and automatic recovery
  - Response caching with TTL
  - Comprehensive metrics and observability
  - Configurable search strategies (quick, comprehensive, targeted)
  - Confidence scoring and quality assurance
- **Components**:
  - `ProductionMCPManager`: Handles multiple MCP servers with failover
  - `ProductionRAGAgent`: Production RAG agent with advanced features
  - `RAGResponse`: Standardized response format with metadata
  - `MCPServerConfig`: Server configuration management

#### `test_mcp_rag.py` - Comprehensive Test Suite
- **Purpose**: Complete testing framework for MCP implementation
- **Test Categories**:
  - Knowledge base structure and content validation
  - MCP agent functionality and error handling
  - Production manager features (caching, failover, metrics)
  - Integration scenarios and edge cases
  - Async operation testing
- **Features**:
  - Unit tests for all components
  - Mock objects for isolated testing
  - Performance and reliability testing
  - Error handling validation

## 🚀 Quick Start

### 1. Start the MCP Knowledge Server

```bash
# Navigate to the chapter directory
cd c:\Code\Personal\AWS_AIEngineering\chapters\chapter_05_rag_agentic_rag

# Start the MCP server
python mcp_knowledge_server.py
```

The server will start on `http://localhost:8000/mcp/` and provide 6 knowledge tools.

### 2. Run the Basic MCP RAG Agent

In a new terminal:

```bash
# Run the interactive MCP RAG agent
python mcp_rag_agent.py
```

This will start an interactive CLI where you can:
- Ask questions about AWS Bedrock, Strands Agents, or MCP
- Type 'stats' to see session statistics
- Type 'search <query>' for detailed multi-source search
- Type 'quit' to exit

### 3. Test the Production Integration

```bash
# Run the production demo
python mcp_production_integration.py
```

This demonstrates:
- Multi-server setup with health monitoring
- Automatic failover and caching
- Comprehensive metrics collection
- Different search strategies

### 4. Run the Test Suite

```bash
# Run all tests
python test_mcp_rag.py

# Or use pytest for detailed output
pytest test_mcp_rag.py -v
```

## 🔧 Key Concepts Demonstrated

### 1. MCP Tool Integration
- **Tool Discovery**: Automatic discovery of available MCP tools
- **Parameter Mapping**: Seamless parameter extraction from natural language
- **Response Handling**: Structured processing of tool responses

### 2. Intelligent Query Routing
- **Query Analysis**: Understanding user intent and information needs
- **Tool Selection**: Choosing appropriate tools based on query characteristics
- **Multi-Tool Workflows**: Combining multiple tools for comprehensive responses

### 3. Production Considerations
- **Error Handling**: Graceful handling of tool failures and network issues
- **Performance Optimization**: Caching, connection pooling, and request optimization
- **Monitoring**: Health checks, metrics collection, and observability
- **Scalability**: Multi-server support and load distribution

### 4. Quality Assurance
- **Confidence Scoring**: Automatic confidence assessment for responses
- **Source Citation**: Proper attribution of information sources
- **Response Validation**: Quality checks and threshold-based filtering

## 💡 Example Interactions

### Basic Query Processing
```python
# User asks: "How do I set up AWS Bedrock?"
# Agent automatically:
# 1. Searches technical documentation
# 2. Finds relevant setup guides
# 3. Searches for code examples
# 4. Checks FAQ for common issues
# 5. Synthesizes comprehensive response with sources
```

### Multi-Source Synthesis
```python
# User asks: "Show me Strands agent examples"
# System retrieves:
# - Technical documentation about Strands framework
# - Code examples with different complexity levels
# - FAQ answers about common implementation issues
# - Comprehensive topic overview with related concepts
```

### Production Features
```python
# Production system provides:
# - Automatic failover if primary MCP server fails
# - Cached responses for frequently asked questions
# - Health monitoring of all connected services
# - Detailed metrics for performance optimization
# - Configurable confidence thresholds
```

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Query    │───▶│  Strands Agent   │───▶│  MCP Knowledge  │
│                 │    │                  │    │     Server      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │  Query Analysis  │    │  Tool Execution │
                       │  & Tool Selection│    │  & Response     │
                       └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │   Multi-Source   │◀───│   Synthesized   │
                       │   Information    │    │    Response     │
                       │   Retrieval      │    │                 │
                       └──────────────────┘    └─────────────────┘
```

## 🔍 Advanced Features

### Custom Knowledge Integration
The system supports adding new knowledge sources:

```python
# Add custom knowledge entry
await mcp_client.call_tool(
    name="add_knowledge_entry",
    arguments={
        "entry_type": "technical_docs",
        "entry_id": "custom_integration",
        "title": "Custom Integration Guide",
        "content": "...",
        "category": "integrations"
    }
)
```

### Performance Monitoring
Comprehensive metrics tracking:

```python
metrics = rag_agent.get_comprehensive_metrics()
# Returns:
# - Query processing statistics
# - Tool usage patterns
# - Response time analytics
# - Cache hit rates
# - Server health status
```

### Flexible Search Strategies
Different approaches for different needs:

- **Quick Strategy**: Fast responses using 2 primary tools
- **Comprehensive Strategy**: Detailed search across all sources  
- **Targeted Strategy**: Focused search for specific topics

## 🎓 Learning Outcomes

By exploring this MCP implementation, you will learn:

1. **MCP Protocol Fundamentals**: How to create and connect MCP servers and clients
2. **Tool Integration Patterns**: Best practices for integrating external tools with AI agents
3. **Production RAG Architecture**: Scalable patterns for production RAG systems
4. **Error Handling & Resilience**: Building robust systems with proper error handling
5. **Performance Optimization**: Caching, connection management, and optimization techniques
6. **Quality Assurance**: Confidence scoring, validation, and quality control
7. **Monitoring & Observability**: Comprehensive monitoring for production systems

## 🔗 Integration with Other Examples

This MCP implementation complements other Chapter 5 examples:

- **Intelligent Query Router**: Shows how MCP tools can be integrated into routing decisions
- **Production RAG Integration**: Demonstrates how MCP fits into larger RAG systems
- **Nova Lite Applications**: Can be extended with MCP tools for specialized domains

## 📚 Additional Resources

- [MCP Specification](https://modelcontextprotocol.io/): Official MCP documentation
- [Strands MCP Documentation](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/tools/mcp-tools/): Strands-specific MCP integration guide
- [Strands Agents Examples](https://strandsagents.com/latest/documentation/docs/examples/): More Strands agent examples
- [Production Deployment Guide](https://strandsagents.com/latest/documentation/docs/user-guide/deploy/): Deploying Strands agents in production

## 🚨 Important Notes

1. **Server Dependencies**: The MCP knowledge server must be running before starting the agents
2. **Network Configuration**: Ensure proper network connectivity between components
3. **Resource Management**: Monitor memory usage with large knowledge bases
4. **Security Considerations**: Implement proper authentication in production environments
5. **Scalability Planning**: Consider load balancing and horizontal scaling for high-traffic scenarios

This implementation provides a complete foundation for building sophisticated RAG systems using the Model Context Protocol with Strands agents, suitable for both learning and production deployment.

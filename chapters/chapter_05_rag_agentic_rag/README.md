# Chapter 5: RAG & Agentic RAG

This chapter demonstrates advanced Retrieval-Augmented Generation (RAG) patterns with a focus on **agentic RAG** - where AI agents intelligently orchestrate multiple data sources, routing strategies, and retrieval approaches to provide optimal responses.

## 🎯 Learning Objectives
- Master intelligent query routing and analysis
- Understand agentic RAG vs traditional RAG patterns
- Build production-ready multi-source RAG systems
- Implement self-improving routing mechanisms
- Learn advanced Strands Agent framework patterns
- Create robust fallback and error handling strategies

## 🚀 Code Examples

### 🧠 Intelligent Query Routing Agent
**Primary Example**: Advanced agentic RAG system that demonstrates intelligent query routing

**`intelligent_query_router.py`** - **Main Implementation**
- **What it does**: Creates an intelligent routing agent that analyzes incoming queries and routes them to optimal data sources
- **Key Features**:
  - Query intent classification (technical docs, code, troubleshooting, comparison, general knowledge)
  - Multi-source routing to different data sources based on query characteristics
  - Intelligent fallback mechanisms when primary sources fail
  - Performance tracking and metrics collection for continuous improvement
  - Real-time query complexity assessment and confidence scoring
- **Strands Tools**: 7 specialized tools including `analyze_query_intent`, `route_to_technical_docs`, `route_to_code_search`, etc.
- **Demonstrates**: How agents make intelligent routing decisions, multi-tool workflows, and sophisticated reasoning

**`test_intelligent_router.py`** - **Test Suite**
- **What it does**: Comprehensive testing of all routing functionality
- **Tests Covered**: Query analysis, individual tool testing, fallback mechanisms, metrics tracking, end-to-end routing
- **Validates**: All 5 test scenarios pass, ensuring robust functionality

**`production_rag_integration.py`** - **Production Integration Example**
- **What it does**: Shows how to integrate the intelligent router into a real production RAG system
- **Features**: Multiple data source simulation, result synthesis, confidence ranking, source optimization
- **Demonstrates**: Production patterns for multi-source RAG systems

**`INTELLIGENT_QUERY_ROUTING_README.md`** - **Comprehensive Documentation**
- 50+ page detailed guide covering architecture, implementation, and usage patterns
- Complete API documentation for all tools and methods
- Real-world integration examples and troubleshooting guide

### 🤖 Nova Lite Applications (Agentic Patterns)
**Secondary Examples**: Demonstrate various agentic application patterns

**`nova_lite_apps.py`** - **Specialized Professional Applications**
- **What it does**: Collection of specialized applications built on Amazon Nova Lite
- **Applications Include**:
  - Content Creator: Generates blogs, articles, emails, social media posts with style control
  - Code Assistant: Provides code help, debugging, optimization, and architecture advice  
  - Business Analyst: Performs data analysis, market research, and strategic recommendations
  - Research Assistant: Conducts literature reviews, summarizes papers, analyzes trends
  - Technical Writer: Creates documentation, API guides, tutorials, and technical content
- **Agentic Features**: Each application adapts its behavior based on context and user needs
- **Demonstrates**: How to build domain-specific AI applications with specialized prompting and reasoning

**`test_nova_lite.py`** - **Basic Functionality Testing**
- **What it does**: Tests core Nova Lite model capabilities and streaming responses
- **Validates**: Model connectivity, response generation, streaming functionality, error handling

### 🔌 Model Context Protocol (MCP) Integration
**Advanced Example**: Complete MCP implementation for production RAG systems

**`mcp_knowledge_server.py`** - **MCP Server Implementation**
- **What it does**: Creates an MCP server providing 6 specialized knowledge retrieval tools
- **Key Features**: 
  - Technical documentation search with semantic similarity
  - Code examples search by language/complexity
  - FAQ database with relevance scoring
  - Comprehensive topic overviews across all knowledge sources
  - Dynamic knowledge base management and statistics
- **Tools Provided**: `search_technical_docs`, `search_code_examples`, `get_faq_answers`, `get_topic_overview`, `add_knowledge_entry`, `get_knowledge_stats`
- **Demonstrates**: How to build knowledge servers that Strands agents can connect to via MCP

**`mcp_rag_agent.py`** - **Strands Agent with MCP Integration**
- **What it does**: Demonstrates basic MCP integration with interactive query processing
- **Key Features**: 
  - Automatic MCP tool discovery and integration
  - Natural language to tool parameter mapping
  - Multi-source information synthesis
  - Session tracking and interactive CLI interface
- **Demonstrates**: How Strands agents can seamlessly use external MCP tools for knowledge retrieval

**`mcp_production_integration.py`** - **Production-Ready MCP System**
- **What it does**: Production-grade MCP system with comprehensive monitoring and failover
- **Key Features**:
  - Multi-server failover and health monitoring
  - Response caching with TTL and performance optimization
  - Configurable search strategies (quick, comprehensive, targeted)
  - Confidence scoring and quality assurance
  - Comprehensive metrics and observability
- **Components**: `ProductionMCPManager`, `ProductionRAGAgent`, `RAGResponse`, `MCPServerConfig`
- **Demonstrates**: Enterprise-ready MCP integration patterns with reliability and scalability

**`test_mcp_rag.py`** - **Comprehensive MCP Test Suite**
- **What it does**: Complete testing framework for MCP implementation
- **Test Coverage**: Knowledge base validation, agent functionality, production features, integration scenarios
- **Validates**: Tool integration, error handling, performance, async operations, metrics collection

**`demo_mcp_rag.py`** - **Interactive MCP Demonstration**
- **What it does**: Guided demonstration of MCP capabilities with real-time interaction
- **Features**: Step-by-step MCP tool usage, different search scenarios, production patterns showcase
- **Use Case**: Perfect for learning MCP concepts and seeing the integration in action

**`mcp_requirements.txt`** - **MCP Dependencies**
- **Contains**: All required packages for MCP functionality including `strands-agents`, `mcp` packages
- **Usage**: Install with `pip install -r mcp_requirements.txt`

**`MCP_IMPLEMENTATION_README.md`** - **Complete MCP Documentation**
- **Coverage**: Comprehensive guide to MCP concepts, implementation patterns, and best practices
- **Sections**: Architecture overview, tool development, production deployment, troubleshooting
- **Audience**: Developers implementing MCP in production environments

**`MCP_IMPLEMENTATION_README.md`** - **Complete MCP Documentation**
- **What it covers**: Detailed guide for MCP implementation, usage patterns, and production deployment
- **Includes**: Architecture diagrams, example interactions, advanced features, and learning outcomes

## 🏗️ Architecture Patterns Demonstrated

### 1. Intelligent Query Routing
```
User Query → Intent Analysis → Route Selection → Data Source Query → Result Synthesis
     ↓              ↓               ↓                 ↓                ↓
 Natural Language  Query Type    Optimal Source   Multiple Results   Best Answer
   Processing    Classification    Selection        Retrieval        Generation
```

### 2. Multi-Source RAG Orchestra​​tion
- **Bedrock Knowledge Base**: Managed, scalable document retrieval
- **Local Vector Database**: Fast, customizable similarity search  
- **Code Repositories**: Syntax-aware code search and examples
- **Support Knowledge Base**: Problem-solution matching for troubleshooting
- **External APIs**: Real-time information and general knowledge

### 3. Agentic Decision Making
- **Query Analysis**: Understanding user intent and context
- **Source Selection**: Choosing optimal data sources based on query characteristics
- **Fallback Strategies**: Graceful degradation when primary sources fail
- **Performance Learning**: Tracking success rates to improve future routing decisions

### 4. Model Context Protocol (MCP) Architecture
```
Strands Agent ↔ MCP Client ↔ MCP Server ↔ Knowledge Sources
      ↓              ↓           ↓              ↓
 Natural Query  Tool Discovery  Tool Execution  Data Retrieval
   Processing    & Selection     & Response     & Processing
```

- **Tool Discovery**: Automatic discovery of available MCP tools
- **Parameter Mapping**: Seamless natural language to tool parameter conversion
- **Multi-Server Support**: Failover and load balancing across multiple MCP servers
- **Response Synthesis**: Intelligent combination of results from multiple tools

### � RAG Evaluation and Monitoring
**Production-Ready Framework**: Comprehensive RAG evaluation using Amazon Bedrock as judge

**`rag_evaluation_framework.py`** - **Core Evaluation Framework**
- **What it does**: Automated evaluation of RAG systems using Amazon Bedrock as judge model
- **Key Features**:
  - Faithfulness evaluation (measures hallucination vs factual grounding)
  - Context relevance assessment (evaluates retrieval quality)
  - Answer relevance scoring (measures query-answer alignment)
  - Batch evaluation capabilities for large datasets
  - Integration with AWS Knowledge Base for retrieval testing
- **Metrics**: 3 core metrics with 0.0-1.0 scoring and comprehensive reporting
- **Demonstrates**: Production-grade RAG evaluation using your course content knowledge base

**`advanced_rag_evaluation.py`** - **Continuous Monitoring & A/B Testing**
- **What it does**: Advanced evaluation capabilities for production RAG systems
- **Key Features**:
  - Continuous monitoring pipeline with scheduled evaluations
  - A/B testing framework for comparing RAG configurations
  - Performance degradation detection and alerting
  - Statistical analysis for configuration comparison
  - Automated performance tracking and trending
- **Components**: `ContinuousRAGEvaluator`, `RAGABTester`, `RAGConfiguration`
- **Demonstrates**: Enterprise monitoring patterns for production RAG systems

**`cloudwatch_integration.py`** - **AWS CloudWatch Integration**
- **What it does**: Enterprise monitoring with AWS CloudWatch dashboards and alerts
- **Key Features**:
  - Automated metric publishing to CloudWatch
  - Custom dashboard creation for RAG performance visualization
  - Alarm configuration for performance thresholds
  - SNS integration for automated alerting
  - Cost optimization through metric aggregation
- **Components**: `CloudWatchRAGMonitor` with comprehensive AWS integration
- **Demonstrates**: Production monitoring and alerting for RAG systems

**`demo_rag_evaluation_with_knowledge_base.py`** - **Interactive Demonstration**
- **What it does**: Practical demonstration using your course content knowledge base
- **Features**: Real-time evaluation with your Knowledge Base (PIWCGRFREL), Amazon Nova Lite integration, CSV/JSON result export
- **Use Case**: Perfect for learning RAG evaluation concepts and testing with real data

**`test_rag_evaluation.py`** - **Comprehensive Test Suite**
- **What it does**: Complete testing framework with 95%+ code coverage
- **Test Coverage**: All evaluation metrics, A/B testing, CloudWatch integration, mock AWS services
- **Validates**: Framework reliability and production readiness

**`rag_evaluation_requirements.txt`** - **Python Dependencies**
- **Contains**: All required packages including boto3, pandas, numpy, matplotlib, pytest
- **Usage**: Install with `pip install -r rag_evaluation_requirements.txt`

**`RAG_EVALUATION_README.md`** - **Complete Documentation**
- **Coverage**: Comprehensive guide to RAG evaluation concepts, implementation, and production deployment
- **Sections**: Quick start, metrics explanation, advanced features, troubleshooting, best practices
- **Audience**: Students and practitioners implementing RAG evaluation in production

## 🏗️ Architecture Patterns Demonstrated

### 1. Intelligent Query Routing
```
User Query → Intent Analysis → Route Selection → Data Source Query → Result Synthesis
     ↓              ↓               ↓                 ↓                ↓
 Natural Language  Query Type    Optimal Source   Multiple Results   Best Answer
   Processing    Classification    Selection        Retrieval        Generation
```

### 2. Multi-Source RAG Orchestration
- **Bedrock Knowledge Base**: Managed, scalable document retrieval
- **Local Vector Database**: Fast, customizable similarity search  
- **Code Repositories**: Syntax-aware code search and examples
- **Support Knowledge Base**: Problem-solution matching for troubleshooting
- **External APIs**: Real-time information and general knowledge

### 3. Agentic Decision Making
- **Query Analysis**: Understanding user intent and context
- **Source Selection**: Choosing optimal data sources based on query characteristics
- **Fallback Strategies**: Graceful degradation when primary sources fail
- **Performance Learning**: Tracking success rates to improve future routing decisions

### 4. Model Context Protocol (MCP) Architecture
```
Strands Agent ↔ MCP Client ↔ MCP Server ↔ Knowledge Sources
      ↓              ↓           ↓              ↓
 Natural Query  Tool Discovery  Tool Execution  Data Retrieval
   Processing    & Selection     & Response     & Processing
```

### 5. RAG Evaluation Pipeline
```
RAG System → Evaluation Framework → Judge Model → Metrics → Monitoring Dashboard
     ↓              ↓                    ↓           ↓           ↓
 Query/Answer   Faithfulness         Nova Lite    Scores    CloudWatch Alerts
  Generation    Context Relevance     Judge      Analytics   SNS Notifications
               Answer Relevance      Model      Trending     A/B Test Results
```

## 🔧 Technical Implementation Highlights

### Strands Agent Framework Integration
- **7 Specialized Tools**: Each tool handles specific routing scenarios
- **Multi-Tool Workflows**: Agents chain multiple tools for complex queries
- **Intelligent Reasoning**: Visible agent thinking processes for transparency
- **Error Handling**: Robust error recovery and fallback mechanisms

### Model Context Protocol (MCP) Integration
- **6 MCP Tools**: Comprehensive knowledge retrieval capabilities
- **Production Architecture**: Multi-server failover, health monitoring, caching
- **Quality Assurance**: Confidence scoring and response validation
- **Extensible Design**: Easy addition of new knowledge sources and tools

### RAG Evaluation Framework
- **3 Core Metrics**: Faithfulness, context relevance, and answer relevance evaluation
- **Amazon Nova Lite Judge**: Uses your available model for automated evaluation
- **Knowledge Base Integration**: Direct integration with Knowledge Base PIWCGRFREL
- **Production Monitoring**: CloudWatch dashboards, alerts, and A/B testing capabilities
- **Comprehensive Testing**: 95%+ code coverage with mock AWS services

### Query Classification Engine
- **5 Query Types**: Technical docs, code, general knowledge, troubleshooting, comparison
- **Pattern Matching**: Keyword analysis and semantic understanding
- **Confidence Scoring**: Reliability metrics for routing decisions
- **Complexity Assessment**: 1-10 scale for query difficulty analysis

### Performance Optimization
- **Metrics Tracking**: Success rates, confidence scores, response times
- **Source Statistics**: Performance analysis by data source type
- **Adaptive Routing**: Learning from historical performance to improve decisions
- **Cost Optimization**: Token usage tracking and cost-aware routing

## 🎯 Real-World Applications

### Enterprise Knowledge Management
- Route employee queries to appropriate departmental knowledge bases
- Connect questions with domain experts and specialized resources
- Ensure access to most current and authoritative information

### Customer Support Systems  
- Intelligently route simple queries to self-service resources
- Escalate complex issues to human agents with context
- Provide product-specific support routing based on query analysis

### Development and DevOps
- Smart routing between code repositories and documentation
- Environment-specific routing (dev, staging, production contexts)  
- Integration with development tools and monitoring systems

## 🚀 Quick Start

### Prerequisites
```bash
# Ensure you're in the virtual environment
.\.venv\Scripts\Activate.ps1  # Windows
# or
source .venv/bin/activate     # macOS/Linux

# Verify Strands installation
python -c "from strands import Agent; print('Strands ready!')"
```

### Running the Examples

1. **Test the Intelligent Query Router**:
   ```bash
   python test_intelligent_router.py
   # Expected: 5/5 tests pass
   ```

2. **Run the Interactive Demo**:
   ```bash
   python intelligent_query_router.py
   # Features: Live query analysis and routing demonstration
   ```

3. **Model Context Protocol (MCP) Examples**:
   
   **View MCP Server Demo** (standalone mode):
   ```bash
   python mcp_knowledge_server.py
   # Shows available tools and usage instructions
   # Press Ctrl+C to exit
   ```
   
   **Run the Interactive MCP RAG Agent**:
   ```bash
   python mcp_rag_agent.py
   # Interactive CLI - the server runs automatically as subprocess
   # Try queries like: "What is AWS Bedrock?" or "Show me Strands examples"
   ```
   
   **Test the Production MCP Integration**:
   ```bash
   python mcp_production_integration.py
   # Demonstrates production features with monitoring
   ```
   
   **Run MCP Test Suite**:
   ```bash
   python test_mcp_rag.py
   # Comprehensive testing of all MCP functionality
   ```
   
   **Interactive Demo with Step-by-Step Guide**:
   ```bash
   python demo_mcp_rag.py
   # Guided demonstration of MCP capabilities
   ```

4. **RAG Evaluation Framework**:
   
   **Quick RAG Evaluation Test**:
   ```bash
   # Install evaluation dependencies
   pip install -r rag_evaluation_requirements.txt
   
   # Run demonstration with your knowledge base
   python demo_rag_evaluation_with_knowledge_base.py
   # Shows: Real-time evaluation using Knowledge Base PIWCGRFREL
   ```
   
   **Run Comprehensive Evaluation**:
   ```bash
   python rag_evaluation_framework.py
   # Demonstrates: Core evaluation framework with sample data
   ```
   
   **Test Advanced Features**:
   ```bash
   python advanced_rag_evaluation.py
   # Shows: A/B testing and continuous monitoring
   ```
   
   **CloudWatch Integration**:
   ```bash
   python cloudwatch_integration.py
   # Demonstrates: Production monitoring and alerting
   ```
   
   **Run Test Suite**:
   ```bash
   python test_rag_evaluation.py
   # Comprehensive testing of evaluation framework
   ```

5. **Production Integration Examples**:
   ```bash
   python production_rag_integration.py
   # Shows: Multi-source RAG system in action
   ```

6. **Explore Nova Lite Applications**:
   ```bash
   python nova_lite_apps.py
   # Demonstrates: Specialized agentic applications
   ```

## 📊 Expected Results

When you run the examples, you'll see:

### Intelligent Query Analysis
```
🎯 Query: "How do I configure AWS Bedrock Knowledge Base with S3?"
📊 Analysis: technical_docs (confidence: 0.85)
🎯 Routing: bedrock_knowledge_base → documentation (fallback)
✅ Success: 90% confidence, 2 sources consulted
```

### Agent Reasoning Process
```
<thinking>
The query involves AWS service configuration, indicating it's a technical 
documentation request. I'll route to technical docs first, then code search 
for examples, providing comprehensive guidance.
</thinking>
```

### Multi-Source Results
```
1. Technical Documentation (confidence: 85%)
2. Code Examples (confidence: 90%)  
3. Troubleshooting Guide (confidence: 75%)
```

### RAG Evaluation Results
```
🔍 Query: "What is Amazon Bedrock?"
📚 Retrieved 2 documents (2458 characters)
📊 Evaluation Results:
   📈 Faithfulness Score: 1.0 (factual, no hallucination)
   📈 Context Relevance Score: 1.0 (highly relevant retrieval)
   📈 Answer Relevance Score: 1.0 (directly answers query)
   📈 Overall Score: 1.00 (excellent RAG performance)
✅ RAG Evaluation Test Complete!
```

## 🔗 Integration with Other Chapters

- **Chapter 3**: Advanced tool use patterns and agent architecture foundations
- **Chapter 4**: RAG fundamentals, vector databases, and retrieval strategies  
- **Chapter 6**: Multi-agent systems and agent orchestration patterns
- **Chapter 7**: Infrastructure scaling and production deployment strategies

## 🎉 Success Metrics

You'll master agentic RAG when you can:
- [ ] Build intelligent query classification systems
- [ ] Implement multi-source routing strategies  
- [ ] Create robust fallback mechanisms
- [ ] Track and optimize routing performance
- [ ] Design self-improving agentic systems
- [ ] Handle diverse query types intelligently
- [ ] Scale routing across multiple data sources
- [ ] Evaluate RAG system performance using automated metrics
- [ ] Implement continuous monitoring and A/B testing for RAG systems
- [ ] Create production-ready RAG evaluation pipelines

## 📚 Additional Resources

- [Strands Agents Documentation](https://strandsagents.com/)
- [AWS Bedrock Knowledge Bases Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)
- [RAG Architecture Best Practices](https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-knowledge-bases-now-supports-advanced-parsing-chunking-and-multimodal-document-processing/)
- [Agentic AI Patterns](https://www.anthropic.com/research)

## 🚀 Next Steps

Proceed to **Chapter 6: AI Agents** to explore:
- Multi-agent system architectures
- Agent communication protocols  
- Advanced orchestration patterns
- Human-in-the-loop integration

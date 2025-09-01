# Intelligent Query Routing Agent - Chapter 5: RAG & Agentic RAG

This directory contains an advanced demonstration of intelligent query routing using the Strands Agent framework, showcasing how to build sophisticated agentic RAG systems that can intelligently route queries to optimal data sources and retrieval strategies.

## 📚 Learning Objectives

After working through this example, you will understand:

1. **Query Intent Analysis**: How to analyze queries to determine optimal routing strategies
2. **Multi-Source RAG**: How to orchestrate multiple data sources and retrieval approaches
3. **Intelligent Routing**: How agents make decisions about data source selection
4. **Fallback Mechanisms**: How to implement robust error handling and fallback strategies
5. **Performance Optimization**: How to track and optimize routing decisions over time
6. **Agentic Patterns**: How to build self-improving routing systems using agents

## 🗂️ Files Overview

- `intelligent_query_router.py` - Main intelligent routing agent implementation
- `INTELLIGENT_QUERY_ROUTING_README.md` - This documentation file

## 🚀 Quick Start

### Prerequisites

1. **Strands Agents Installation**:
   ```bash
   pip install strands-agents strands-agents-tools
   ```

2. **AWS Configuration**:
   ```bash
   aws configure
   # Ensure access to Amazon Bedrock
   ```

3. **Environment Setup**:
   ```bash
   # From the chapter_05_rag_agentic_rag directory
   cd chapters/chapter_05_rag_agentic_rag
   ```

### Running the Demonstration

```bash
# Run the intelligent query routing demonstration
python intelligent_query_router.py
```

**Expected Output**:
- Query analysis demonstrations
- Routing decision examples
- Interactive query testing mode
- Performance metrics display

## 🧠 How Intelligent Query Routing Works

### Architecture Overview

```
User Query → Query Analysis → Route Decision → Data Source Selection → Result Synthesis
     ↓              ↓              ↓                    ↓                 ↓
  Intent       Query Type    Optimal Source      Retrieval Strategy   Final Response
  Analysis     Classification    Selection         Execution           Generation
```

### Routing Decision Process

1. **Query Analysis**:
   - Intent classification (technical, code, general, troubleshooting, etc.)
   - Complexity assessment (1-10 scale)
   - Keyword extraction and pattern matching
   - Real-time requirement detection

2. **Source Selection**:
   - Primary source identification based on query type
   - Fallback source preparation
   - Confidence scoring for routing decisions

3. **Strategy Optimization**:
   - Retrieval strategy selection (semantic search, code search, etc.)
   - Parameter optimization based on query characteristics
   - Performance tracking and learning

## 🔧 Query Types and Routing Strategies

### 1. Technical Documentation Queries

**Example**: "How do I configure AWS Bedrock Knowledge Base with S3?"

**Routing Strategy**:
- Primary: AWS Bedrock Knowledge Base (managed documentation)
- Secondary: Documentation repositories
- Retrieval: Semantic search with metadata filtering

**Tools Used**:
- `route_to_technical_docs()`
- Structured documentation retrieval
- Version-aware content selection

### 2. Code-Related Queries

**Example**: "Show me Python code for implementing RAG with vector databases"

**Routing Strategy**:
- Primary: Code repositories and code-specific knowledge bases
- Secondary: Developer forums and Q&A sites
- Retrieval: Code semantic search with syntax analysis

**Tools Used**:
- `route_to_code_search()`
- Syntax-aware retrieval
- Repository integration

### 3. General Knowledge Queries

**Example**: "What is the difference between traditional RAG and agentic RAG?"

**Routing Strategy**:
- Primary: Large general knowledge bases
- Secondary: Academic papers and research databases
- Retrieval: Broad semantic search with concept matching

**Tools Used**:
- `route_to_general_knowledge()`
- Conceptual understanding
- Multi-source synthesis

### 4. Troubleshooting Queries

**Example**: "My Bedrock API calls are failing with timeout errors"

**Routing Strategy**:
- Primary: Support knowledge bases and error databases
- Secondary: Community forums and incident reports
- Retrieval: Problem-solution matching

**Tools Used**:
- `route_to_troubleshooting()`
- Error pattern recognition
- Solution recommendation

### 5. Comparison Queries

**Example**: "Compare Claude 3 Sonnet vs Claude 3 Haiku for cost and performance"

**Routing Strategy**:
- Primary: Product documentation and specifications
- Secondary: Benchmarking databases and user reviews
- Retrieval: Multi-faceted comparison analysis

**Tools Used**:
- Comparative analysis tools
- Multi-source aggregation
- Structured comparison output

## 🛠️ Strands Agent Tools

### Core Routing Tools

1. **`analyze_query_intent(query: str)`**
   - Analyzes query to determine intent and routing strategy
   - Returns structured analysis with confidence scores
   - Performs keyword extraction and pattern matching

2. **`route_to_technical_docs(query: str, context: dict)`**
   - Routes queries to technical documentation sources
   - Implements semantic search with metadata filtering
   - Returns structured documentation results

3. **`route_to_code_search(query: str, context: dict)`**
   - Routes code-related queries to appropriate repositories
   - Performs syntax-aware code search
   - Returns relevant code snippets with metadata

4. **`route_to_general_knowledge(query: str, context: dict)`**
   - Routes general knowledge queries to broad knowledge bases
   - Implements concept-based retrieval
   - Returns comprehensive knowledge synthesis

5. **`route_to_troubleshooting(query: str, context: dict)`**
   - Routes problem queries to support resources
   - Matches problems with proven solutions
   - Returns step-by-step troubleshooting guidance

6. **`execute_fallback_strategy(query: str, failed_sources: list)`**
   - Executes fallback routing when primary sources fail
   - Implements graceful degradation
   - Ensures query resolution through alternative paths

7. **`get_routing_metrics()`**
   - Provides routing performance metrics and statistics
   - Tracks success rates by source
   - Enables routing optimization

### Agent Decision-Making

The Strands agent uses these tools to:

1. **Analyze Intent**: Understand what the user is really asking for
2. **Select Strategy**: Choose the optimal routing approach
3. **Execute Retrieval**: Perform targeted information retrieval
4. **Handle Failures**: Implement fallback mechanisms gracefully
5. **Learn and Adapt**: Improve routing decisions over time

## 🎯 Demonstration Scenarios

### 1. Multi-Type Query Analysis

**Scenario**: Agent analyzes different query types and routes appropriately

**Test Queries**:
- Technical: "How to setup AWS Bedrock Knowledge Base?"
- Code: "Python RAG implementation example"
- General: "What is retrieval-augmented generation?"
- Troubleshooting: "Bedrock API timeout errors"
- Comparison: "FAISS vs Pinecone for vector storage"

### 2. Intelligent Fallback Handling

**Scenario**: Primary routing fails, agent uses fallback strategies

**Flow**:
1. Primary source (Bedrock KB) fails
2. Agent tries secondary source (Local Vector DB)
3. If all sources fail, uses direct LLM query
4. Tracks failure reasons for future optimization

### 3. Performance Optimization

**Scenario**: Agent learns from routing decisions to improve performance

**Metrics Tracked**:
- Success rates by source type
- Average confidence scores
- Query complexity correlation
- Response time optimization

## 🔍 Query Analysis Deep Dive

### Intent Classification

The router uses sophisticated pattern matching to classify queries:

```python
query_patterns = {
    QueryType.TECHNICAL_DOCUMENTATION: [
        "how to", "documentation", "api", "configuration", 
        "setup", "install", "deploy", "architecture"
    ],
    QueryType.CODE_RELATED: [
        "code", "function", "method", "class", "bug", 
        "error", "implementation", "algorithm"
    ],
    # ... additional patterns
}
```

### Complexity Scoring

Queries are scored 1-10 based on:
- Number of keywords
- Pattern matches
- Technical depth indicators
- Multi-part question detection

### Confidence Calculation

Routing confidence is calculated using:
- Pattern match strength
- Historical success rates
- Source availability
- Query clarity metrics

## 📊 Expected Results

When you run the demonstration, you'll see:

### 1. Query Analysis Output
```
🎯 Test Case 1: Technical documentation query
Query: "How do I configure AWS Bedrock Knowledge Base with S3?"

Routing Analysis:
----------------------------------------
Query Type: technical_docs
Confidence: 0.85
Complexity: 6/10
Preferred Sources: bedrock_knowledge_base, documentation
```

### 2. Routing Decisions
```
Agent Routing Decision:
----------------------------------------
Based on the query analysis, I'm routing this to technical documentation 
sources because it involves specific AWS service configuration. The query 
shows high confidence for technical documentation with keywords like 
"configure", "AWS Bedrock", and "Knowledge Base".

Primary Source: bedrock_knowledge_base
Fallback Sources: documentation, local_vector_db
Strategy: semantic_search_with_metadata_filtering
```

### 3. Performance Metrics
```
📊 ROUTING METRICS
----------------------------------------
Total Routes: 5
Success Rate: 100.00%
Average Confidence: 0.82
Source Statistics:
  - technical_docs: 2 routes, 100% success
  - code_search: 1 route, 100% success
  - general_knowledge: 2 routes, 100% success
```

## 🌟 Real-World Applications

### Enterprise Knowledge Management

- **Multi-Department Routing**: Route queries to appropriate departmental knowledge bases
- **Expertise Matching**: Connect queries with domain experts and specialized resources
- **Content Governance**: Ensure queries access most current and authoritative information

### Customer Support Systems

- **Tiered Support Routing**: Route simple queries to self-service, complex ones to human agents
- **Product-Specific Routing**: Direct queries to appropriate product documentation and support resources
- **Escalation Management**: Intelligent escalation based on query complexity and urgency

### Development and DevOps

- **Code vs Documentation**: Smart routing between code repositories and documentation
- **Environment-Specific**: Route based on development, staging, or production contexts
- **Tool Integration**: Connect with appropriate development tools and monitoring systems

### Research and Analysis

- **Academic vs Practical**: Route between academic papers and practical implementations
- **Temporal Relevance**: Consider recency requirements for routing decisions
- **Interdisciplinary Queries**: Handle queries spanning multiple domains intelligently

## 🚨 Troubleshooting

### Common Issues

1. **Strands Import Errors**:
   ```bash
   pip install strands-agents strands-agents-tools
   ```

2. **AWS Authentication**:
   ```bash
   aws configure
   # Ensure proper IAM permissions for Bedrock
   ```

3. **Routing Confidence Low**:
   - Check query clarity and specificity
   - Review pattern matching rules
   - Adjust confidence thresholds

4. **Fallback Activation**:
   - Verify primary source availability
   - Check network connectivity
   - Review error handling logic

### Debugging Tips

1. **Enable Verbose Logging**:
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Test Individual Tools**:
   ```python
   router = IntelligentQueryRouter()
   result = router.analyze_query_intent("test query")
   print(result)
   ```

3. **Monitor Routing Metrics**:
   ```python
   metrics = router.get_routing_metrics()
   print(f"Success rate: {metrics['overall_success_rate']:.2%}")
   ```

## 📈 Performance Considerations

### Optimization Strategies

1. **Caching**: Cache analysis results for similar queries
2. **Batch Processing**: Process multiple queries efficiently
3. **Source Prioritization**: Optimize source order based on performance
4. **Load Balancing**: Distribute load across multiple sources

### Scalability Patterns

1. **Horizontal Scaling**: Multiple router instances for high volume
2. **Async Processing**: Non-blocking routing for better throughput
3. **Circuit Breakers**: Prevent cascading failures in source systems
4. **Rate Limiting**: Respect source system limitations

## 🔗 Integration with Other Chapters

- **Chapter 3**: Tool use patterns and agent architecture
- **Chapter 4**: Vector database integration and RAG foundations
- **Chapter 6**: Multi-agent systems and agent orchestration
- **Chapter 7**: Infrastructure scaling and deployment patterns

## 📚 Further Reading

- Strands Agents Documentation
- Query Understanding in Information Retrieval
- Multi-Source Information Fusion
- Intelligent Routing in Distributed Systems
- RAG Architecture Best Practices

## 🎉 Success Metrics

You'll know you've mastered intelligent query routing when:

- [ ] You can build query classifiers for your domain
- [ ] You understand how to optimize routing decisions
- [ ] You can implement robust fallback mechanisms
- [ ] You can track and improve routing performance
- [ ] Your system handles diverse query types intelligently
- [ ] You can scale routing across multiple data sources
- [ ] Your agents make contextually appropriate routing decisions

## 🚀 Next Steps

1. **Extend Query Types**: Add domain-specific query classifications
2. **Custom Sources**: Integrate your own data sources and APIs
3. **Learning Systems**: Implement machine learning for routing optimization
4. **Multi-Modal Routing**: Handle image, audio, and video queries
5. **Real-Time Adaptation**: Implement dynamic routing based on system performance
6. **A/B Testing**: Test different routing strategies for optimization

This intelligent query routing system demonstrates the power of agentic RAG, where AI agents don't just retrieve information, but intelligently orchestrate the entire information retrieval process for optimal results.

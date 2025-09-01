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

## 🔧 Technical Implementation Highlights

### Strands Agent Framework Integration
- **7 Specialized Tools**: Each tool handles specific routing scenarios
- **Multi-Tool Workflows**: Agents chain multiple tools for complex queries
- **Intelligent Reasoning**: Visible agent thinking processes for transparency
- **Error Handling**: Robust error recovery and fallback mechanisms

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

3. **Try the Production Integration**:
   ```bash
   python production_rag_integration.py
   # Shows: Multi-source RAG system in action
   ```

4. **Explore Nova Lite Applications**:
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

# Chapter 4: Storage for Retrieval

This chapter covers storage solutions for retrieval-based AI systems, featuring a comprehensive hands-on RAG demo that compares DIY (local FAISS) and managed (AWS Bedrock Knowledge Bases) approaches.

## 🎯 Learning Objectives
- Build and deploy local vector databases using FAISS
- Master AWS Bedrock Knowledge Bases for managed RAG
- Understand trade-offs between DIY and managed approaches  
- Implement intelligent fallback strategies with Strands agents
- Apply best practices for production RAG systems

## 🚀 Quick Start

Navigate to the comprehensive RAG demo:

```bash
cd rag-samples/
make setup
make demo-local    # Try local FAISS approach
```

**Windows PowerShell Users:**
If `make` is not available, use the PowerShell script:
```powershell
cd rag-samples/
.\run-demo.ps1 setup
.\run-demo.ps1 demo-local    # Try local FAISS approach
```

For the full AWS experience:
```bash
make up            # Create AWS infrastructure (⚠️ charges apply)
make demo-kb       # Test Bedrock Knowledge Base
make agent         # Run intelligent agent wrapper
make down          # Clean up AWS resources
```

**Windows PowerShell equivalent:**
```powershell
.\setup-kb.ps1              # Create AWS infrastructure (⚠️ charges apply)
.\run-demo.ps1 demo-kb      # Test Bedrock Knowledge Base
.\run-demo.ps1 agent        # Run intelligent agent wrapper
.\teardown-kb.ps1           # Clean up AWS resources
```

## 📁 Code Examples

### [📖 Complete RAG Demo](./rag-samples/)
**Two-path implementation comparing local vs managed RAG approaches**

**Path A - DIY Approach:**
- [`rag_vector_local.py`](./rag-samples/rag_vector_local.py) - Local FAISS implementation
- [`common.py`](./rag-samples/common.py) - Shared utilities and AWS integration
- Full control over chunking, indexing, and retrieval

**Path B - Managed Approach:**
- [`rag_bedrock_kb.py`](./rag-samples/rag_bedrock_kb.py) - AWS Bedrock Knowledge Base integration
- Automatic scaling and enterprise features
- Simple API-based retrieval

**Agent Orchestration:**
- [`strands_agent.py`](./rag-samples/strands_agent.py) - Intelligent wrapper using Strands framework
- Automatic fallback from managed to local approach
- Clear indication of which backend answered

**Monitoring & Observability:**
- [`bedrock_kb_monitoring.py`](./rag-samples/bedrock_kb_monitoring.py) - Comprehensive CloudWatch monitoring
- Real-time dashboards, automated alerting, performance analysis
- Custom metrics and cost optimization
- [`monitoring.env.example`](./rag-samples/monitoring.env.example) - Configuration template

**Infrastructure Automation:**
- [`scripts/setup-kb.sh`](./rag-samples/scripts/setup-kb.sh) - AWS infrastructure creation (Linux/macOS)
- [`scripts/teardown-kb.sh`](./rag-samples/scripts/teardown-kb.sh) - Complete cleanup (Linux/macOS)
- [`setup-kb.ps1`](./rag-samples/setup-kb.ps1) - AWS infrastructure creation (Windows PowerShell)
- [`teardown-kb.ps1`](./rag-samples/teardown-kb.ps1) - Complete cleanup (Windows PowerShell)
- [`Makefile`](./rag-samples/Makefile) - Workflow automation (Linux/macOS)
- [`run-demo.ps1`](./rag-samples/run-demo.ps1) - Windows PowerShell automation script

## 🏗️ Architecture Highlights

### Local FAISS Approach
- **Components**: FAISS IndexFlatIP, tiktoken chunking, AWS Bedrock embeddings
- **Advantages**: Full control, no infrastructure costs, fast local search
- **Use cases**: Development, cost optimization, custom chunking strategies

### AWS Bedrock Knowledge Bases  
- **Components**: S3 storage, OpenSearch Serverless, automatic ingestion
- **Advantages**: Fully managed, auto-scaling, enterprise security
- **Use cases**: Production deployments, large datasets, enterprise requirements

### Intelligent Agent Wrapper
- **Strategy**: Try managed approach first, fallback to local
- **Tools**: KB retrieval, local retrieval, comparison mode
- **Benefits**: Robust fallback, cost optimization, clear source attribution

## 💰 Cost Management

The demo includes comprehensive cost management:

**Estimated Costs:**
- 1-hour demo: $0.25-0.75
- Full day (if left running): $3-4  
- Local-only: Nearly free (API calls only)

**Cost Control Features:**
- Ephemeral infrastructure (auto-cleanup)
- Cost estimation tools (`make cost-estimate`)
- Local-only development mode
- Detailed usage tracking

## 📚 Key Topics Covered

### 1. Vector Databases in Practice
- FAISS implementation with L2 normalization
- Embedding generation with Amazon Titan v2
- Efficient similarity search strategies
- Index persistence and loading

### 2. Managed Knowledge Bases
- AWS Bedrock Knowledge Base setup
- OpenSearch Serverless configuration
- Document ingestion and chunking strategies
- Hybrid search (semantic + keyword)

### 3. Production RAG Patterns
- Error handling and fallback mechanisms
- Source citation and provenance tracking
- Performance optimization techniques
- Monitoring and observability

### 4. AI Agent Integration
- Strands framework integration
- Multi-tool agent orchestration
- Intelligent decision making
- User experience optimization

### 5. Comprehensive Monitoring & Observability
- CloudWatch dashboard creation with 6 widget types
- Automated alerting for 4 critical metrics (latency, errors, usage, performance)
- Real-time log monitoring with metric filters
- Custom metrics for performance scoring and quality tracking
- Automated performance analysis with 0-100 scoring
- Cost tracking and optimization recommendations

## 📊 Monitoring Deep Dive

### CloudWatch Integration
The demo includes a comprehensive monitoring system (`bedrock_kb_monitoring.py`) that provides:

**Real-time Dashboards:**
- Query volume and patterns
- Latency analysis (P50, P95, P99)
- Error rates and failure types
- Cost tracking and optimization
- Custom performance metrics
- Log insights with filtering

**Intelligent Alerting:**
- High latency detection (>2000ms)
- Error rate monitoring (>5%)
- Usage spike alerts (>100 queries/min)
- Performance score warnings (<70/100)

**Performance Analysis:**
- Automated scoring based on latency (40%), accuracy (30%), reliability (20%), efficiency (10%)
- AI-driven optimization recommendations
- Trend analysis and forecasting
- Cost per query optimization

### Monitoring Commands
```bash
# Set up comprehensive monitoring
make monitor-setup

# Create CloudWatch dashboard
make monitor-dashboard

# Generate performance report
make monitor-report

# Check current status
make monitor-status

# Clean up monitoring resources
make monitor-cleanup
```

**Windows PowerShell equivalent:**
```powershell
# Set up comprehensive monitoring
.\run-demo.ps1 monitor-setup

# Check current status
.\run-demo.ps1 monitor-status

# Generate performance report
.\run-demo.ps1 monitor-report
```

### Monitoring Configuration
Configure monitoring through `.env` file:
```bash
cp monitoring.env.example .env
# Edit with your AWS settings and Knowledge Base ID
```

## 🛠️ Prerequisites
- **Completed**: Chapters 1-3 (especially Strands agent framework from Chapter 1)
- **AWS Account**: With Bedrock model access enabled
- **Python**: 3.10+ with development environment
- **Understanding**: Embeddings, vector similarity, basic RAG concepts

## 🧪 Testing and Validation

Comprehensive testing included:
- Unit tests for core components
- Integration tests with mocked AWS services
- Performance benchmarks
- Error handling validation

Run the test suite:
```bash
cd rag-samples/
make test
```

## 🔧 Troubleshooting

Built-in troubleshooting tools:
- Environment validation (`make validate`)
- Debug mode with verbose logging
- Comprehensive error messages with solutions
- AWS connectivity testing

Get help:
```bash
make troubleshoot    # Built-in troubleshooting guide
make debug-env       # Environment debug information
```

## 📖 Documentation

Each component includes comprehensive documentation:
- **[README.md](./rag-samples/README.md)**: Complete setup and usage guide
- **Inline comments**: Educational explanations throughout code
- **Error messages**: Actionable next steps for common issues
- **Makefile help**: `make help` for available commands

## 🎓 Educational Features

Designed specifically for workshop and learning environments:
- **Step-by-step progression**: From simple to complex
- **Clear comparisons**: Side-by-side approach analysis
- **Cost awareness**: Built-in cost estimation and warnings
- **Best practices**: Production-ready patterns and error handling
- **Extensibility**: Clean architecture for student modifications

## 🔄 Next Steps

After mastering this chapter:
1. **Chapter 5**: [RAG & Agentic RAG](../chapter_05_rag_agentic_rag/) - Advanced patterns
2. **Chapter 6**: [AI Agents](../chapter_06_ai_agents/) - Multi-agent systems
3. **Practical extensions**: Add reranking, hybrid search, evaluation metrics

## 🔗 Resources

### Course Materials
- [Course Overview](../../Course.md) - Complete theoretical foundation
- [Chapter 1 Code](../chapter_01_coding_ml_fundamentals/) - Strands framework basics
- [Cost Monitoring Tools](../../Utils/) - AWS usage tracking

### External Documentation
- [AWS Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)
- [FAISS Documentation](https://faiss.ai/cpp_api/index.html)
- [Strands Agents Framework](https://strandsagents.com/)
- [OpenSearch Serverless](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless.html)

---

**🚨 Important**: This demo creates AWS resources that incur charges. Always run `make down` or `scripts/teardown-kb.sh` when finished to stop billing. Use `make run-kb-ephemeral` for automatic cleanup.

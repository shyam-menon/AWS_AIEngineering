# RAG Demo: Storage for Retrieval

**AWS AI Engineering Course - Chapter 4**

This repository demonstrates two approaches to building Retrieval-Augmented Generation (RAG) systems:

1. **Path A (DIY)**: Local FAISS index with AWS Bedrock embeddings and chat
2. **Path B (Managed)**: AWS Bedrock Knowledge Bases with automatic indexing

Both approaches use the same source documents and demonstrate the trade-offs between control/cost (DIY) and simplicity/scalability (managed).

## 🎯 Learning Objectives

After completing this demo, you will understand:

- How to build RAG systems with local vector storage (FAISS)
- How to leverage AWS Bedrock Knowledge Bases for managed RAG
- Trade-offs between DIY and managed approaches
- How to use Strands agents to orchestrate multiple retrieval backends
- Best practices for RAG system architecture and error handling

## 📋 Prerequisites

### AWS Account Setup
- Active AWS account with programmatic access
- AWS CLI installed and configured
- Access to AWS Bedrock models:
  - `amazon.titan-embed-text-v2:0` (embeddings)
  - `amazon.nova-lite-v1:0` (chat)

### Development Environment
- Python 3.10 or higher
- 4GB+ RAM (for FAISS operations)
- Internet connection for AWS API calls
- AWS CLI installed and configured (`aws configure`)

**Platform Support:**
- ✅ Windows (PowerShell)
- ✅ macOS (bash/zsh)  
- ✅ Linux (bash)

**Note for Windows Users**: Some commands use `make` which may not be available by default. You can run the Python scripts directly or install `make` via chocolatey: `choco install make`

### Model Access Setup
1. Visit [AWS Bedrock Console](https://console.aws.amazon.com/bedrock/home#/modelaccess)
2. Enable model access for:
   - Amazon Titan Embed Text v2
   - Amazon Nova Lite v1
3. Wait for approval (usually immediate)

## 🚀 Quick Start

### Option 1: Local RAG Only (No AWS Charges)
```bash
# Clone and setup
git clone <repo-url>
cd rag-samples

# Install dependencies
pip install -r requirements.txt
# OR use make if available: make setup

# Run local FAISS demo
python rag_vector_local.py --question "What is AI Engineering?"
# OR use make: make demo-local
```

**Windows PowerShell Users:**
```powershell
# If make is not available, run directly:
python rag_vector_local.py --question "What is AI Engineering?"
python strands_agent.py --question "How do RAG systems work?"
```

### Option 2: Full Demo with AWS Knowledge Base
```bash
# Setup environment
make setup

# Create AWS infrastructure (⚠️ incurs charges)
make up

# Run Knowledge Base demo
make demo-kb

# Run agent wrapper (tries both approaches)
make agent

# Clean up AWS resources (stops charges)
make down
```

### Option 3: Ephemeral Demo (Full Cycle)
```bash
# Run complete demo with automatic cleanup
make run-kb-ephemeral
```

## 📁 Project Structure

```
rag-samples/
├── data/sample_docs/          # Sample documents for indexing
│   ├── 01_intro.md           # AI Engineering introduction
│   ├── 02_design.md          # System design patterns
│   └── 03_ops.md             # Operations and deployment
├── scripts/
│   ├── setup-kb.sh           # AWS infrastructure creation
│   └── teardown-kb.sh        # AWS cleanup script
├── tests/                     # Test suite
├── .env.example              # Configuration template
├── .gitignore               # Git ignore patterns
├── common.py                # Shared utilities
├── rag_vector_local.py      # Local FAISS implementation
├── rag_bedrock_kb.py        # Bedrock KB implementation
├── strands_agent.py         # Agent wrapper
├── requirements.txt         # Python dependencies
├── Makefile                 # Workflow automation
└── README.md               # This file
```

## 🔧 Configuration

### Environment Setup
1. Copy the configuration template:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your settings:
   ```bash
   # AWS Configuration (credentials will be read from ~/.aws/credentials)
   AWS_REGION=us-east-1
   # DO NOT set AWS_ACCESS_KEY_ID or AWS_SECRET_ACCESS_KEY here
   # They will be automatically read from your AWS CLI configuration
   
   # Model Configuration
   BEDROCK_EMBED_MODEL_ID=amazon.titan-embed-text-v2:0
   BEDROCK_CHAT_MODEL_ID=amazon.nova-lite-v1:0
   
   # Tuning Parameters
   CHUNK_SIZE=800
   CHUNK_OVERLAP=120
   TOP_K_RESULTS=4
   TEMPERATURE=0.2
   ```

   **⚠️ Important**: If you already have AWS CLI configured (`aws configure`), 
   do NOT add AWS credentials to `.env` as they will override your working credentials.

### Knowledge Base Configuration
When you run `make up`, a `.kb.env` file is automatically created with:
- Knowledge Base ID
- S3 bucket details  
- OpenSearch collection information
- IAM role ARNs

**⚠️ Important**: Never commit `.kb.env` to version control.

## 🎮 Usage Examples

### Interactive Demos

**Local FAISS (Interactive)**
```bash
python rag_vector_local.py --interactive
```

**Knowledge Base (Interactive)**
```bash
python rag_bedrock_kb.py --interactive
```

**Agent Wrapper (Interactive)**
```bash
python strands_agent.py --interactive
```

### Single Questions

**Local FAISS**
```bash
python rag_vector_local.py --question "What is AI Engineering?"
```

**Knowledge Base**
```bash
python rag_bedrock_kb.py --question "How do RAG systems work?"
```

**Agent (Auto-routing)**
```bash
python strands_agent.py --question "What are vector databases?"
```

### Comparison Mode

**Compare Both Approaches**
```bash
python strands_agent.py --compare --question "How do you monitor AI systems?"
```

## 🏗️ Architecture Deep Dive

### Local FAISS Approach (DIY)

**Components:**
- Document loading and chunking (`tiktoken` for accurate token counting)
- FAISS IndexFlatIP for cosine similarity search
- AWS Bedrock for embeddings and chat
- Local index persistence

**Advantages:**
- Full control over chunking and retrieval
- No ongoing AWS infrastructure costs
- Fast local search
- Easy to customize and debug

**Disadvantages:**
- Manual index management
- Limited scalability
- No built-in document ingestion pipeline

### AWS Bedrock Knowledge Base (Managed)

**Components:**
- S3 for document storage
- OpenSearch Serverless for vector indexing
- Automatic document chunking and embedding
- Built-in retrieve_and_generate API

**Advantages:**
- Fully managed infrastructure
- Automatic scaling
- Enterprise-grade security
- Built-in ingestion pipelines

**Disadvantages:**
- Higher cost for small datasets
- Less control over chunking/retrieval
- Vendor lock-in
- Cold start latency

### Agent Wrapper (Strands)

**Strategy:**
1. Try Bedrock Knowledge Base first
2. Fall back to local FAISS if KB unavailable
3. Provide clear indication of which backend answered
4. Include source citations from both approaches

**Tools:**
- `attempt_kb_retrieval()`: Query Knowledge Base
- `attempt_local_retrieval()`: Query local FAISS  
- `compare_approaches()`: Side-by-side comparison

## 💰 Cost Management

### AWS Charges Breakdown

**OpenSearch Serverless** (Primary cost)
- Base: $0.24/OCU/hour
- Minimum: 0.5 OCU = ~$2.88/day
- Demo usage: ~$0.12-0.50/hour

**Bedrock API Calls**
- Embeddings: ~$0.0001/1K tokens
- Chat: ~$0.0008/1K input tokens  
- Demo total: ~$0.10-0.50

**S3 Storage**
- Small docs: ~$0.01/month (negligible)

### Cost Optimization Tips

1. **Use ephemeral workflow**: `make run-kb-ephemeral`
2. **Clean up immediately**: `make down` after demos
3. **Monitor usage**: Check AWS billing dashboard
4. **Use local-only mode** for development: `make local-only`

### Estimated Demo Costs
- 1-hour demo: $0.25-0.75
- Full day (if left running): $3-4
- Local-only: Nearly free (just API calls)

## ✅ Verified Functionality

This demo has been thoroughly tested and verified to work with:

**✅ Core Components:**
- Document loading and chunking (3 sample docs, 10,310 characters)
- FAISS vector indexing with 1024-dimensional embeddings
- AWS Bedrock integration (Titan v2 embeddings + Nova Lite chat)
- Intelligent agent wrapper with fallback strategies
- All 18 unit tests passing

**✅ Error Handling:**
- Graceful fallback when Knowledge Base not configured
- Educational error messages for setup guidance
- Proper AWS credential detection and validation
- Platform-specific command variations (Windows/macOS/Linux)

**✅ Performance:**
- Fast local FAISS search with cosine similarity
- Efficient index persistence and loading
- Configurable retrieval parameters (top-k, chunk size, etc.)
- Source citation in all responses

## 🧪 Testing

### Run Test Suite
```bash
make test
```

### Manual Testing
```bash
# Test AWS connectivity
make validate

# Test local FAISS
python rag_vector_local.py --question "Test question"

# Test Knowledge Base
python rag_bedrock_kb.py --status
```

### Debug Mode
```bash
# Enable verbose logging
echo "DEBUG=true" >> .env

# Check environment
make debug-env
```

## 🔍 Troubleshooting

### Common Issues

**1. AWS Credentials Not Found**
```bash
# Check credentials
aws sts get-caller-identity

# Configure if needed
aws configure
```

**⚠️ Important**: If you get "security token invalid" errors after configuring AWS CLI, 
make sure your `.env` file does NOT contain `AWS_ACCESS_KEY_ID` or `AWS_SECRET_ACCESS_KEY` 
as they will override your working credentials.

**2. Model Access Denied**
- Visit [Bedrock Model Access](https://console.aws.amazon.com/bedrock/home#/modelaccess)
- Enable required models
- Wait for approval

**3. Knowledge Base Not Found**
```bash
# Check status
make status

# Recreate if needed
make down && make up
```

**4. Local FAISS Index Missing**
```bash
# Build index
python rag_vector_local.py --rebuild

# Or force rebuild
make rebuild-local
```

**5. Import Errors**
```bash
# Install dependencies
pip install -r requirements.txt
# OR: make install-deps (if make available)

# Check installation
pip list | grep -E 'boto3|faiss|numpy'
```

**6. Nova Model Format Errors**
If you see "system is not a valid enum value" errors:
- This has been fixed in the current version
- Nova Lite doesn't support system role messages
- The fix incorporates system prompts into user messages

**7. Windows PowerShell Issues**
```powershell
# Use Remove-Item instead of rm
Remove-Item filename.txt

# Use pip directly if make is unavailable
pip install -r requirements.txt

# Run Python scripts directly
python rag_vector_local.py --help
```

### Region-Specific Issues

**Bedrock Availability:**
- us-east-1 (Virginia) ✅ Recommended
- us-west-2 (Oregon) ✅
- eu-west-1 (Ireland) ✅

**Set region in .env:**
```bash
AWS_REGION=us-east-1
```

### Performance Issues

**Slow Embedding Generation:**
- Reduce `CHUNK_SIZE` in `.env`
- Use smaller document sets
- Consider batch processing

**High Memory Usage:**
- Reduce `TOP_K_RESULTS`
- Clear FAISS index: `make clean`
- Restart Python process

## 🎓 Educational Notes

### Key Concepts Demonstrated

**Vector Similarity Search:**
- Embedding generation with Titan v2
- L2 normalization for cosine similarity
- FAISS IndexFlatIP for efficient search

**RAG Pipeline:**
- Document chunking strategies
- Context assembly and formatting
- Prompt engineering for accurate responses

**Error Handling:**
- Graceful degradation with fallbacks
- Clear error messages with next steps
- Robust AWS API error handling

**Production Considerations:**
- Cost monitoring and optimization
- Security best practices
- Monitoring and observability

### Extension Ideas

1. **Add more retrieval strategies:**
   - Hybrid search (keyword + semantic)
   - Reranking with cross-encoders
   - Query expansion techniques

2. **Enhance the agent:**
   - Memory across conversations
   - User preference learning
   - Multi-modal inputs

3. **Improve chunking:**
   - Semantic chunking
   - Document structure awareness
   - Metadata-based filtering

4. **Add evaluation:**
   - Retrieval accuracy metrics
   - Answer quality assessment
   - A/B testing framework

## 📚 Additional Resources

### AWS Documentation
- [Bedrock User Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/)
- [Knowledge Bases Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)
- [OpenSearch Serverless Guide](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless.html)

### Technical References
- [FAISS Documentation](https://faiss.ai/)
- [Strands Agents Framework](https://strandsagents.com/)
- [RAG Best Practices](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-best-practices.html)

### Course Materials
- [Chapter 5: RAG & Agentic RAG](../chapter_05_rag_agentic_rag/)
- [Chapter 6: AI Agents](../chapter_06_ai_agents/)
- [Cost Monitoring Tools](../../Utils/)

## 🤝 Contributing

This is an educational project. Suggestions for improvements:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Update documentation
5. Submit a pull request

## 📄 License

This project is part of the AWS AI Engineering Course and is provided for educational purposes.

---

**⚠️ Important Reminders:**
- Always run `make down` after demos to stop AWS charges
- Never commit AWS credentials or `.kb.env` files
- Monitor your AWS billing dashboard
- Use `make troubleshoot` if you encounter issues

**🎯 Next Steps:**
After mastering this RAG demo, proceed to [Chapter 5](../chapter_05_rag_agentic_rag/) to learn about advanced agentic RAG patterns and the Model Context Protocol (MCP).

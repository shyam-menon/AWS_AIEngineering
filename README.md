# AWS AI Engineering with Strands Agents

A comprehensive course and collection of practical examples demonstrating how to build, deploy, and manage sophisticated AI applications using Amazon Web Services (AWS) and the Strands Agents framework.

## 📚 Course Structure

This repository is organized into **11 chapters** that take you from fundamentals to production deployment:

```
AWS_AIEngineering/
├── chapters/                    # Chapter-wise course content
│   ├── chapter_01_coding_ml_fundamentals/    # Python, AWS basics, ML fundamentals
│   ├── chapter_02_llm_apis/                  # LLM APIs, AWS Bedrock, structured outputs
│   ├── chapter_03_model_adaptation/          # Prompt engineering, tool use, fine-tuning
│   ├── chapter_04_storage_for_retrieval/     # Vector databases, graph databases, hybrid retrieval
│   ├── chapter_05_rag_agentic_rag/          # RAG systems, agentic patterns, MCP
│   ├── chapter_06_ai_agents/                 # AI agents, Strands framework, multi-agent systems
│   ├── chapter_07_infrastructure/            # AWS infrastructure, deployment, scaling
│   ├── chapter_08_observability_evaluation/  # Monitoring, evaluation, observability
│   ├── chapter_09_security/                  # Guardrails, testing, ethics, security
│   ├── chapter_10_forward_looking/           # Voice/vision agents, robotics, computer use
│   └── chapter_11_complete_integration/      # Production customer support agent
├── examples/                    # Legacy examples (still available)
│   ├── ec2/                    # EC2 service examples
│   ├── bedrock/                # AWS Bedrock examples  
│   └── strands/                # Strands library examples
├── docs/                       # Documentation and guides
│   └── Course.md              # Complete course documentation (9400+ lines)
├── requirements.txt            # Python dependencies
└── README.md                  # This file
```

## 🎯 Learning Path

### **Beginner Track** (Chapters 1-3)
- Chapter 1: **Coding & ML Fundamentals** - Python, AWS basics, EC2
- Chapter 2: **LLM APIs** - Bedrock, model interaction, structured outputs  
- Chapter 3: **Model Adaptation** - Prompt engineering, conversations, tool use

### **Intermediate Track** (Chapters 4-7)
- Chapter 4: **Storage for Retrieval** - Vector databases, knowledge bases
- Chapter 5: **RAG & Agentic RAG** - Retrieval systems, agentic patterns
- Chapter 6: **AI Agents** - Strands framework, multi-agent systems
- Chapter 7: **Infrastructure** - Production deployment, scaling

### **Advanced Track** (Chapters 8-11)
- Chapter 8: **Observability & Evaluation** - Monitoring, evaluation frameworks
- Chapter 9: **Security** - Guardrails, testing, ethical considerations
- Chapter 10: **Forward Looking** - Emerging technologies, future trends
- Chapter 11: **Complete Integration** - Production customer support agent

## 🚀 Quick Start

### 1. Setup Environment
```powershell
# Create virtual environment (if not exists)
python -m venv .venv

# Activate virtual environment
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure AWS Credentials
```powershell
# Option 1: AWS CLI
aws configure

# Option 2: Environment Variables
$env:AWS_ACCESS_KEY_ID="your_key"
$env:AWS_SECRET_ACCESS_KEY="your_secret"
$env:AWS_DEFAULT_REGION="us-east-1"
```

### 3. Run Examples
```powershell
# List EC2 instances
python examples\ec2\ec2_list.py

# Interactive AI chat with Nova Lite
python examples\bedrock\nova_lite_chat.py

# Extract JSON data from text
python examples\bedrock\bedrock_json_output.py --mode examples

# Specialized AI applications
python examples\bedrock\nova_lite_apps.py --help
```

## 📚 Examples Overview

### 🖥️ EC2 Examples
- **`ec2_list.py`** - List and display EC2 instances across regions

### 🤖 Bedrock (AI/ML) Examples
- **`test_nova_lite.py`** - Basic Nova Lite model invocation
- **`nova_lite_chat.py`** - Interactive chat interface
- **`nova_lite_cli.py`** - Command-line interface with presets
- **`nova_lite_apps.py`** - Professional applications (content, code, research, business)
- **`bedrock_json_output.py`** - Structured JSON data extraction from text

### 🔗 Strands Library Examples
*Coming soon - examples demonstrating Strands library integration*

## 🎯 Use Cases

### Infrastructure Management
- Monitor EC2 instances across multiple regions
- Automate AWS resource discovery and reporting

### AI-Powered Applications
- Content generation and editing
- Code assistance and review
- Business analysis and strategy
- Creative writing and storytelling

### Hybrid Workflows
- Combine AWS services with AI capabilities
- Automated reporting with natural language summaries
- Intelligent infrastructure monitoring

## 📖 Documentation

- **[Nova Lite Guide](docs/NOVA_LITE_GUIDE.md)** - Complete guide for Amazon Nova Lite
- **[AWS Configuration](docs/aws_config_examples.txt)** - AWS credentials setup examples

## 🛠️ Requirements

### AWS Services Access
- **EC2**: `ec2:DescribeInstances`
- **Bedrock**: `bedrock:InvokeModel`, `bedrock:ListFoundationModels`

### Python Dependencies
- `boto3` - AWS SDK for Python
- `botocore` - Core functionality for Boto3
- Additional dependencies as needed for Strands integration

## 🔧 Development

### Adding New Examples

1. **EC2 Examples**: Add to `examples/ec2/`
2. **Bedrock Examples**: Add to `examples/bedrock/`
3. **Strands Examples**: Add to `examples/strands/`

### Best Practices
- Include error handling and logging
- Use environment variables for configuration
- Add documentation and examples
- Follow AWS security best practices

## 🚨 Security Notes

- Never commit AWS credentials to version control
- Use IAM roles when possible
- Follow principle of least privilege
- Regularly rotate access keys

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve these examples.

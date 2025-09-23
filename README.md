# AWS AI Engineering with Strands Agents

A comprehensive course and collection of practical examples demonstrating how to build, deploy, and manage sophisticated AI applications using Amazon Web Services (AWS) and the Strands Agents framework.

## 📖 Complete Course Documentation

**📚 [Course.md](./Course.md) - Complete Course Guide (12,000+ lines)**

The comprehensive course documentation covers all theoretical concepts, detailed explanations, and learning objectives. This README focuses on practical implementation and quick start guides.

## 📚 Course Structure

![AI Engineering Fundamentals Curriculum (2025 Roadmap)](./Diagrams/AI%20Engineering%20Fundamentals%20Curriculum%20(2025%20Roadmap).png)

This repository is organized into **11 chapters** that take you from fundamentals to production deployment:

**📁 [Browse All Chapters](./chapters/)** | **📖 [Course.md](./Course.md)** | **💰 [Cost Monitoring](./Utils/)**

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
├── Utils/                       # Cost monitoring and usage tracking utilities
│   ├── ai_usage_monitor.py     # Comprehensive AWS usage monitoring
│   ├── token_tracker.py        # Real-time session tracking
│   ├── bedrock_with_tracking.py # Integrated Bedrock client with tracking
│   ├── usage_examples.py       # Usage examples and best practices
│   └── README.md              # Utilities documentation
├── docs/                       # Documentation and guides
│   ├── implementation_prompt.md # AI prompts for development
|   ├── decision_tree.md # Decision making for AI apps
├── requirements.txt            # Python dependencies
├── Course.md                   # Course material
└── README.md                  # This file
```

## 🎯 Learning Path

### **Beginner Track** (Chapters 1-3)
- Chapter 1: **[Coding & ML Fundamentals](./chapters/chapter_01_coding_ml_fundamentals/)** - Python, AWS basics, EC2 | [📖 Theory](./Course.md#chapter-1-coding--ml-fundamentals)
- Chapter 2: **[LLM APIs](./chapters/chapter_02_llm_apis/)** - Bedrock, structured outputs, caching | [📖 Theory](./Course.md#chapter-2-llm-apis)
- Chapter 3: **[Model Adaptation](./chapters/chapter_03_model_adaptation/)** - Prompt engineering, tool use | [📖 Theory](./Course.md#chapter-3-model-adaptation)

### **Intermediate Track** (Chapters 4-6)
- Chapter 4: **[Storage for Retrieval](./chapters/chapter_04_storage_retrieval/)** - Vector databases, hybrid retrieval | [📖 Theory](./Course.md#chapter-4-storage-for-retrieval)
- Chapter 5: **[RAG & Agentic RAG](./chapters/chapter_05_rag_agentic/)** - Advanced retrieval, MCP, Strands | [📖 Theory](./Course.md#chapter-5-rag--agentic-rag)
- Chapter 6: **[AI Agents](./chapters/chapter_06_ai_agents/)** - Multi-agent systems, memory, human-in-loop | [📖 Theory](./Course.md#chapter-6-ai-agents)

### **Advanced Track** (Chapters 7-11)
- Chapter 7: **[Infrastructure](./chapters/chapter_07_infrastructure/)** - AWS AgentCore, CI/CD, deployment | [📖 Theory](./Course.md#chapter-7-infrastructure)
- Chapter 8: **[Observability & Evaluation](./chapters/chapter_08_observability_evaluation/)** - Monitoring, evaluation | [📖 Theory](./Course.md#chapter-8-observability--evaluation)
- Chapter 9: **[Security](./chapters/chapter_09_security/)** - Guardrails, testing, ethics | [📖 Theory](./Course.md#chapter-9-security)
- Chapter 10: **[Forward Looking](./chapters/chapter_10_forward_looking/)** - Voice/vision, robotics, computer use | [📖 Theory](./Course.md#chapter-10-forward-looking-elements)
- Chapter 11: **[Complete Integration](./chapters/chapter_11_complete_integration/)** - Production customer support agent | [📖 Theory](./Course.md#chapter-11-complete-integration---building-a-production-customer-support-agent)

### **Key Resources**
- **💰 [Utils/](./Utils/)** - AI usage monitoring and cost tracking tools
- **📋 [requirements.txt](./requirements.txt)** - Python dependencies

### How to Use This Course
1. **📖 Read Theory**: Start with [Course.md](./Course.md) for comprehensive understanding
2. **💻 Practice Code**: Work through [chapter folders](./chapters/) for hands-on experience  
3. **💰 Monitor Costs**: Use [Utils/](./Utils/) to track AI usage and AWS billing
4. **🔄 Iterate**: Combine theory and practice for complete mastery

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

# Interactive AI chat with Nova Lite
python examples\bedrock\nova_lite_chat.py

# Extract JSON data from text
python examples\bedrock\bedrock_json_output.py --mode examples

# Specialized AI applications
python examples\bedrock\nova_lite_apps.py --help

# Strands agent examples
python chapters\chapter_01_coding_ml_fundamentals\simple_strands_example.py
python examples\strands\strands_integration.py

# Monitor AI usage and costs
python Utils\ai_usage_monitor.py --days 7

# Monitor ALL AWS service costs  
python Utils\aws_billing_monitor.py --days 7 --quiet

# Quick cost dashboard
python Utils\aws_cost_dashboard.py

# Track tokens in real-time
python Utils\usage_examples.py
```

## 📚 Examples Overview

### 🤖 Bedrock (AI/ML) Examples
- **`test_nova_lite.py`** - Basic Nova Lite model invocation
- **`nova_lite_chat.py`** - Interactive chat interface
- **`nova_lite_cli.py`** - Command-line interface with presets
- **`nova_lite_apps.py`** - Professional applications (content, code, research, business)
- **`bedrock_json_output.py`** - Structured JSON data extraction from text

### 🔗 Strands Library Examples
- **`simple_strands_example.py`** - Basic Strands agent example from [Chapter 1](./chapters/chapter_01_coding_ml_fundamentals/)
- **`python_strands_agents.py`** - Comprehensive Strands framework demonstration from [Chapter 1](./chapters/chapter_01_coding_ml_fundamentals/)
- **`strands_integration.py`** - AWS-Strands integration example from [examples/strands/](./examples/strands/)

### 💰 AI Usage and Cost Monitoring
- **`ai_usage_monitor.py`** - Comprehensive monitoring with CloudWatch and Cost Explorer
- **`aws_billing_monitor.py`** - Complete AWS billing across ALL services (EC2, S3, Bedrock, etc.)
- **`aws_cost_dashboard.py`** - Quick daily cost dashboard with alerts
- **`token_tracker.py`** - Real-time session tracking and cost calculation
- **`bedrock_with_tracking.py`** - Integrated Bedrock client with automatic tracking
- **`usage_examples.py`** - Complete usage examples and best practices

## 🎯 Use Cases

### Infrastructure Management
- Monitor EC2 instances across multiple regions
- Automate AWS resource discovery and reporting

### AI-Powered Applications
- Content generation and editing
- Code assistance and review
- Business analysis and strategy
- Creative writing and storytelling

### Cost Management & Monitoring
- Track AI token usage in real-time
- Monitor costs across different models (Nova Lite vs Claude)
- Set budget alerts and cost optimization
- Session-based tracking for project management

### Hybrid Workflows
- Combine AWS services with AI capabilities
- Automated reporting with natural language summaries
- Intelligent infrastructure monitoring

## 📖 Documentation

### 📚 Primary Course Materials
- **[Course.md](./Course.md)** - **Complete Course Guide (9,400+ lines)**
  - Comprehensive theoretical content for all 11 chapters
  - Detailed explanations and learning objectives
  - References to official AWS and Strands documentation
  - In-depth concepts and methodologies

### 📁 Chapter-Specific Guides
- **[Chapter 1 Guide](./chapters/chapter_01_coding_ml_fundamentals/README.md)** - Python, AWS basics, ML fundamentals
- **[Chapter 2 Guide](./chapters/chapter_02_llm_apis/README.md)** - LLM APIs, Bedrock, caching, evaluation
- **[Chapter 3 Guide](./chapters/chapter_03_model_adaptation/README.md)** - Prompt engineering, tool use
- **[All Chapter Guides](./chapters/README.md)** - Complete chapter overview

### 🛠️ Specialized Documentation
- **[Nova Lite Guide](./docs/NOVA_LITE_GUIDE.md)** - Complete guide for Amazon Nova Lite
- **[AWS Configuration](./docs/aws_config_examples.txt)** - AWS credentials setup examples
- **[Utils Documentation](./Utils/README.md)** - AI usage monitoring and cost tracking guide

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

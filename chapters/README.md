# AI Engineering with AWS and Strands Agents - Course Chapters

This directory contains chapter-wise organization of code examples and exercises for the AI Engineering course. Each chapter builds upon the previous ones, providing a structured learning path from fundamentals to production deployment.

## Course Structure

### [Chapter 1: Coding & ML Fundamentals](./chapter_01_coding_ml_fundamentals/)
Foundation skills in Python, Bash, statistics, and ML concepts
- **Topics**: Python for AI, AWS basics, EC2 fundamentals
- **Code**: Basic AWS interaction, infrastructure setup

### [Chapter 2: LLM APIs](./chapter_02_llm_apis/)
Working with Large Language Models and AWS Bedrock
- **Topics**: LLM types, structured outputs, prompt caching, multimodal models
- **Code**: Bedrock setup, model interaction, JSON extraction

### [Chapter 3: Model Adaptation](./chapter_03_model_adaptation/)
Customizing LLMs through prompt engineering and tool use
- **Topics**: **Comprehensive prompt engineering principles**, tool use, fine-tuning, graph databases
- **Code**: **Interactive prompt engineering demo**, advanced conversations, Nova Lite interactions

### [Chapter 4: Storage for Retrieval](./chapter_04_storage_for_retrieval/)
Storage solutions for retrieval-based AI systems
- **Topics**: Vector databases, graph databases, hybrid retrieval, Knowledge Bases
- **Code**: *Coming soon*

### [Chapter 5: RAG & Agentic RAG](./chapter_05_rag_agentic_rag/)
Retrieval-Augmented Generation and agentic patterns
- **Topics**: Data preparation, retrieval, generation, reranking, MCP, Strands RAG
- **Code**: Nova Lite applications, agentic patterns

### [Chapter 6: AI Agents](./chapter_06_ai_agents/)
Building sophisticated AI agents with Strands framework
- **Topics**: Agent patterns, multi-agent systems, memory, human-in-loop, A2A/ACP
- **Code**: Strands integration, agent frameworks

### [Chapter 7: Infrastructure](./chapter_07_infrastructure/)
Production infrastructure for AI applications
- **Topics**: AWS Bedrock, AgentCore, CI/CD, model routing, LLM deployment
- **Code**: Infrastructure management, deployment patterns

### [Chapter 8: Observability & Evaluation](./chapter_08_observability_evaluation/)
Monitoring and evaluating AI systems
- **Topics**: Instrumentation, observability platforms, evaluation techniques
- **Code**: *Coming soon*

### [Chapter 9: Security](./chapter_09_security/)
Safety, reliability, and ethical considerations
- **Topics**: Guardrails, testing, ethics, security architecture
- **Code**: *Coming soon*

### [Chapter 10: Forward Looking Elements](./chapter_10_forward_looking/)
Emerging AI technologies and future directions
- **Topics**: Voice/vision agents, robotics, computer use, CLI agents, automated prompts
- **Code**: *Coming soon*

### [Chapter 11: Complete Integration](./chapter_11_complete_integration/)
Production customer support agent implementation
- **Topics**: End-to-end system design, deployment, monitoring
- **Code**: *Complete integration project coming soon*

## How to Use This Course

1. **Sequential Learning**: Work through chapters in order, as each builds on previous concepts
2. **Hands-on Practice**: Run the code examples in each chapter
3. **Prerequisites**: Check each chapter's README for specific requirements
4. **Environment Setup**: Ensure AWS credentials and required packages are installed
5. **Documentation**: Refer to the main Course.md for detailed explanations

## Quick Start

1. **Setup Environment**:
   ```bash
   # Create virtual environment
   python -m venv .venv
   .venv\Scripts\Activate.ps1  # Windows
   
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Configure AWS**:
   ```bash
   aws configure
   # Or set environment variables
   ```

3. **Start with Chapter 1**:
   ```bash
   cd chapters/chapter_01_coding_ml_fundamentals
   python ec2_list.py
   ```

## Prerequisites

- **Python 3.8+** with pip
- **AWS Account** with appropriate permissions
- **AWS CLI** configured
- **Git** for version control
- **Basic programming knowledge**

## Course Resources

- **Main Documentation**: [Course.md](../docs/Course.md) - Complete course content
- **AWS Documentation**: [AWS Bedrock User Guide](https://docs.aws.amazon.com/bedrock/)
- **Strands Documentation**: [Strands Agents](https://strandsagents.com/)
- **Code Repository**: GitHub repository with all examples

## Progress Tracking

- [ ] Chapter 1: Coding & ML Fundamentals
- [ ] Chapter 2: LLM APIs
- [ ] Chapter 3: Model Adaptation
- [ ] Chapter 4: Storage for Retrieval
- [ ] Chapter 5: RAG & Agentic RAG
- [ ] Chapter 6: AI Agents
- [ ] Chapter 7: Infrastructure
- [ ] Chapter 8: Observability & Evaluation
- [ ] Chapter 9: Security
- [ ] Chapter 10: Forward Looking Elements
- [ ] Chapter 11: Complete Integration

## Support and Community

- **Issues**: Report problems via GitHub issues
- **Discussions**: Join community discussions
- **Updates**: Check for course updates and new content

## License and Usage

This course material is designed for educational purposes. Please follow AWS pricing guidelines and best practices when running examples.

---

*Last updated: August 2025*

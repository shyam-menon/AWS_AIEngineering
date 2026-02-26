# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a comprehensive AI Engineering curriculum (11 chapters) teaching how to build production AI applications on AWS using **AWS Bedrock** and the **Strands Agents** framework. The codebase contains 100+ working Python examples progressing from fundamentals to production deployment.

## Environment Setup

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/Scripts/activate  # Windows: .venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

AWS credentials must be configured before running any Bedrock or AWS examples:
```bash
aws configure
# or set: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION
```

## Running Examples

```bash
# Run any chapter example directly
python chapters/chapter_01_coding_ml_fundamentals/simple_strands_example.py

# Run cost monitoring utilities
python Utils/ai_usage_monitor.py --days 7
python Utils/aws_cost_dashboard.py

# Chapter 4 RAG demo (has a Makefile)
cd chapters/chapter_04_storage_for_retrieval/rag-samples
make demo-local    # No AWS infra needed
make demo-kb       # Requires Bedrock Knowledge Base
```

There is no global test runner. Individual files are self-contained and run as scripts.

## Architecture & Key Concepts

### Chapter Progression
Each chapter builds on the previous. Key chapters by tier:
- **Beginner (1-3)**: Python basics, Bedrock API invocation, prompt engineering
- **Intermediate (4-6)**: RAG with FAISS/Bedrock KBs, agentic RAG, multi-agent systems
- **Advanced (7-11)**: AgentCore deployment, observability (CloudWatch/X-Ray), security guardrails, capstone

### Primary AWS Services
- **AWS Bedrock** (`bedrock-runtime`) — LLM inference, Knowledge Bases, Guardrails
- **AWS AgentCore Runtime** — Serverless agent hosting (Chapter 7)
- **CloudWatch** — Logging, metrics, tracing
- **X-Ray** — Distributed tracing (via OpenTelemetry)

### Primary Model
Default model throughout: `amazon.nova-lite-v1:0`. Overridden via `BEDROCK_MODEL_ID` env var.

### Strands Agents Framework
The main agent framework used in Chapters 3–11. Multi-agent patterns covered:
- **Agents as Tools** — Hierarchical orchestrator + specialist agents
- **Swarm** — Autonomous peer collaboration with shared context handoff
- **Graph** — DAG-based execution with dependency tracking
- **Workflow** — Sequential pipeline processing

## Common Code Patterns

### Bedrock API Invocation
```python
body = {
    "schemaVersion": "messages-v1",
    "messages": [{"role": "user", "content": [{"text": prompt}]}],
    "inferenceConfig": {"maxTokens": 1000, "temperature": 0.7, "topP": 0.9}
}
response = bedrock_client.invoke_model(
    modelId="amazon.nova-lite-v1:0",
    body=json.dumps(body),
    contentType='application/json'
)
```

### Strands Tool Definition
```python
@tool
def my_tool(param: str) -> Dict[str, Any]:
    """Clear description — the agent uses this to decide when to call the tool."""
    return {"result": value}
```

### Graceful Dependency Handling
Many files include fallback mock classes when Strands is unavailable:
```python
try:
    from strands import Agent
    STRANDS_AVAILABLE = True
except ImportError:
    STRANDS_AVAILABLE = False
    class Agent:  # Mock for demo mode
        ...
```

### AWS Client Initialization
```python
region = os.getenv("AWS_REGION", "us-east-1")
bedrock_client = boto3.client('bedrock-runtime', region_name=region)
```

## Key Environment Variables

| Variable | Default | Purpose |
|---|---|---|
| `AWS_REGION` | `us-east-1` | AWS region for all services |
| `BEDROCK_MODEL_ID` | `amazon.nova-lite-v1:0` | Default LLM model |
| `BEDROCK_GUARDRAIL_ID` | — | Guardrail identifier (Chapter 9) |
| `KNOWLEDGE_BASE_ID` | — | Bedrock Knowledge Base ID (Chapters 4-5) |
| `BEDROCK_INFERENCE_PROFILE_ID` | — | Multi-region inference profile (Chapter 7) |
| `LOG_LEVEL` | `INFO` | Logging verbosity |
| `OTEL_TRACES_SAMPLER_ARG` | `0.1` | OpenTelemetry sampling rate (Chapter 8) |

## Key Files to Know

- [requirements.txt](requirements.txt) — Top-level Python dependencies (`strands-agents`, `boto3`)
- [Utils/README.md](Utils/README.md) — Cost monitoring utilities documentation
- [docs/decision_tree.md](docs/decision_tree.md) — Decision guide for AI app architecture choices
- [docs/implementation_prompt.md](docs/implementation_prompt.md) — AI prompts for development assistance
- [chapters/chapter_04_storage_for_retrieval/rag-samples/](chapters/chapter_04_storage_for_retrieval/rag-samples/) — DIY (FAISS) vs managed (Bedrock KB) RAG comparison
- [chapters/chapter_06_ai_agents/](chapters/chapter_06_ai_agents/) — All multi-agent patterns with runnable examples
- [chapters/chapter_07_infrastructure/agentcore_runtime_example/](chapters/chapter_07_infrastructure/agentcore_runtime_example/) — AgentCore deployment with `.bedrock_agentcore.yaml`

## Model Pricing Reference (as of 2025)

| Model | Input (per 1K tokens) | Output (per 1K tokens) |
|---|---|---|
| `amazon.nova-lite-v1:0` | $0.00006 | $0.00024 |
| `amazon.nova-pro-v1:0` | $0.0008 | $0.0032 |
| Claude 3.5 Sonnet | $0.003 | $0.015 |

Nova Lite is the default for cost efficiency during development and evaluation.

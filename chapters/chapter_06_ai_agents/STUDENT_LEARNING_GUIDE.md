# AI Agents - Student Learning Guide

## 🎯 Chapter 6 Learning Objectives
Master AI agent design patterns, multi-agent systems, and production-ready implementations using AWS Bedrock and the Strands framework.

## 📚 Recommended Learning Path

### Phase 1: Foundations (Start Here)
**Goal**: Understand core agent concepts and basic tool usage

1. **`comprehensive_strands_concepts_demo.py`** ⭐ **START HERE**
   - Covers ALL fundamental Strands concepts in one comprehensive example
   - Enterprise quoting system with business rules and persistence
   - **Key Concepts**: Agent Loop, State Management, Hooks, Structured Output
   - **Run**: `python comprehensive_strands_concepts_demo.py`

2. **`simple_tool_agent.py`** 
   - Foundation patterns for tool-augmented agents
   - Built-in tools, custom tools, and AWS Bedrock integration
   - **Run**: `python simple_tool_agent.py`

### Phase 2: Multi-Agent Systems
**Goal**: Learn collaboration patterns between multiple AI agents

3. **Agents as Tools** - Hierarchical delegation
   - **Test First**: `python agents_as_tools_example.py`
   - Orchestrator routes queries to domain specialists
   - Simple manager-specialist pattern

4. **Workflow** - Sequential processing
   - **Test First**: `python test_workflow.py` (quick demo)
   - **Full Example**: `python workflow_example.py`
   - Linear task progression with state management

5. **Swarm** - Autonomous collaboration  
   - **Test First**: `python test_swarm.py` (quick demo)
   - **Full Example**: `python swarm_example.py`
   - Self-organizing teams with intelligent handoff

6. **Graph** - Network-based execution
   - **Test First**: `python test_graph.py` (quick demo)  
   - **Full Example**: `python graph_example.py`
   - DAG execution with parallel processing

### Phase 3: Advanced Integration
**Goal**: Production-ready agents with real-world integrations

7. **Customer Support Agent** ⭐ **ADVANCED HIGHLIGHT**
   - **Interactive Examples**: `python customer_support_examples.py`
   - Intent classification, emotion detection, smart escalation
   - **Key Features**: AWS Bedrock Nova Lite, human handoff, knowledge lookup
   - **Architecture**: Multi-tool workflow with intelligent routing

8. **Interactive Web UI Demo** ⭐ **VISUAL HIGHLIGHT**
   - **Web Interface**: `python customer_support_ui.py`
   - Interactive chat interface with real-time workflow visualization
   - **Features**: Intent classification display, escalation detection, tone analysis
   - **Perfect for**: Testing scenarios and seeing agent decision-making process

9. **Human-in-the-Loop Testing**
   - **Focused Demo**: `python simple_handoff_demo.py`
   - Learn how agents hand off to humans for complex decisions
   - **Key Tool**: `handoff_to_user` from strands-tools

10. **AWS Cost Monitoring** (Optional)
   - **Quick Test**: `python test_aws_cost_hitl.py`
   - **Full Example**: `python aws_cost_monitor_hitl_example.py` (requires AWS setup)
   - Production workflow with AWS services integration

## 🛠️ Setup Instructions

### Prerequisites
```bash
# Ensure you're in the virtual environment
cd c:\Code\Personal\AWS_AIEngineering
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# For advanced AWS examples (optional)
pip install strands-agents-tools

# Verify AWS credentials for Bedrock (if using AWS examples)
aws configure list
```

### Quick Verification
```bash
cd chapters\chapter_06_ai_agents
python simple_tool_agent.py
```

## 📋 Example Categories

### 🟢 Basic Examples (Everyone Should Try)
- `comprehensive_strands_concepts_demo.py` - **Core concepts**
- `simple_tool_agent.py` - **Basic patterns** 
- `test_workflow.py` - **Quick multi-agent test**
- `customer_support_examples.py` - **Advanced agent workflow**
- `customer_support_ui.py` - **🎮 Interactive Web UI Demo** ⭐ **MUST TRY**

### 🟡 Intermediate Examples
- `agents_as_tools_example.py` - **Hierarchical agents**
- `swarm_example.py` - **Collaborative agents**
- `graph_example.py` - **Network agents**  
- `workflow_example.py` - **Sequential agents**

### 🔴 Advanced Examples (Requires AWS Setup)
- `aws_cost_monitor_hitl_example.py` - **Production AWS integration**
- `test_aws_cost_hitl.py` - **Community tools testing**

## 🎮 Interactive Features

### Customer Support Agent Demo
```python
# 🎮 BEST OPTION: Interactive Web UI (Recommended!)
python customer_support_ui.py
# Opens browser at http://localhost:5000
# Features: Real-time workflow visualization, escalation detection, example scenarios

# Command Line Version
python customer_support_examples.py

# Test different customer scenarios:
# 1. Angry customer (escalation)
# 2. Polite inquiry (automated response)
# 3. Technical issue (specialist routing)  
# 4. Billing problem (management escalation)
```

### Human Handoff Testing
```python
# Learn human-in-the-loop patterns
python simple_handoff_demo.py

# Choose from:
# 1. Basic handoff demonstration
# 2. Customer support integration
# 3. Both demos
```

## 📖 Documentation Deep Dives

Each pattern includes comprehensive documentation:

- **`COMPREHENSIVE_CONCEPTS_README.md`** - Core Strands concepts
- **`SIMPLE_TOOL_AGENT_README.md`** - Basic agent patterns
- **`AGENTS_AS_TOOLS_README.md`** - Hierarchical patterns  
- **`SWARM_README.md`** - Collaboration patterns
- **`GRAPH_README.md`** - Network patterns
- **`WORKFLOW_README.md`** - Sequential patterns
- **`CUSTOMER_SUPPORT_AGENT_README.md`** - Advanced integration
- **`AWS_COST_MONITOR_HITL_README.md`** - Production examples

## 🔧 Key Technologies

### Models & Services
- **Amazon Bedrock**: Nova Lite model (`amazon.nova-lite-v1:0`)
- **AWS Cost Explorer**: Real-time cost monitoring
- **Strands Framework**: Agent orchestration and tooling

### Core Tools
- **Built-in Strands Tools**: Calculator, file operations, time functions
- **Community Tools** (`strands-tools`): AWS integration, human handoff
- **Custom Tools**: Intent classification, knowledge lookup, escalation logic

## 🎯 Learning Outcomes

After completing this chapter, you should understand:

✅ **Agent Fundamentals**: Agent loop, state management, conversation handling
✅ **Tool Integration**: Built-in tools, custom tools, community tools  
✅ **Multi-Agent Patterns**: Hierarchical, collaborative, network, sequential
✅ **Production Features**: Error handling, monitoring, scalability
✅ **Human Integration**: When and how to hand off to human operators
✅ **AWS Integration**: Bedrock models, cost monitoring, production workflows

## 🚀 Next Steps

1. **Start with Phase 1** - Get foundations solid
2. **Pick one multi-agent pattern** - Deep dive on what interests you most
3. **Try customer support agent** - See advanced integration in action  
4. **Experiment with modifications** - Adapt examples for your use cases
5. **Explore production deployment** - Consider Chapter 7 (Infrastructure)

## 💡 Pro Tips

- **Run examples multiple times** - Agent responses vary with each execution
- **Read the error messages** - They guide you to proper AWS/tool setup
- **Experiment with prompts** - Try different customer queries and scenarios
- **Check token usage** - Monitor costs when using AWS Bedrock
- **Use breakpoints** - Step through code to understand agent flow

---
**Happy Learning!** 🤖✨

Questions? Check the individual README files for each pattern or experiment with the interactive examples.

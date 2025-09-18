# Chapter 6: AI Agents

This chapter explores the exciting world of AI agents, including design patterns, multi-agent systems, memory management, human-in-the-loop integration, and comprehensive usage of the Strands Agent framework.

## Learning Objectives
- Understand AI agent design patterns and implementation
- Build and deploy multi-agent systems using Strands framework
- Master tool-augmented agents with custom and built-in tools
- Implement collaborative agent patterns (Swarm, Graph, Workflow, etc.)
- Learn production-ready agent architectures
- Understand agent coordination and communication patterns

## Code Examples

### Core Strands Agent Concepts

#### Comprehensive Concepts Demo ✅ NEW
**All Core Concepts in One Example**
- **Files**: `comprehensive_strands_concepts_demo.py` + `COMPREHENSIVE_CONCEPTS_README.md`
- **Concepts**: Agent Loop, State Management, Session Management, Hooks, Structured Output, Conversation Management
- **Demo**: Enterprise quoting system with business rules, persistence, and type-safe extraction
- **Architecture**: Production-ready agent with full lifecycle management, guardrails, and observability

### Basic Agent Patterns

#### Simple Tool-Augmented Agents
- **`simple_tool_agent.py`** - Foundation example with built-in and custom tools
- **`simple_tool_agent_improved.py`** - Enhanced version with better prompting strategies
- **`SIMPLE_TOOL_AGENT_README.md`** - Comprehensive documentation and learning guide

### Multi-Agent Systems (4/5 Patterns Implemented)

#### 1. Agents as Tools ✅ COMPLETED
**Pattern**: Hierarchical delegation with specialized agent expertise
- **Files**: `agents_as_tools_example.py` + `AGENTS_AS_TOOLS_README.md`
- **Concept**: Orchestrator agent routes queries to domain specialists
- **Demo**: Research, product recommendations, travel planning, code assistance
- **Architecture**: Manager-specialist delegation pattern

#### 2. Swarm ✅ COMPLETED  
**Pattern**: Collaborative autonomous agents with shared context
- **Files**: `swarm_example.py` + `SWARM_README.md` + `test_swarm.py`
- **Concept**: Self-organizing teams with intelligent handoff coordination
- **Demo**: Content creation pipeline (research → coding → review)
- **Architecture**: Autonomous collaboration with shared memory

#### 3. Graph ✅ COMPLETED
**Pattern**: Network-based agent execution with dependency management
- **Files**: `graph_example.py` + `GRAPH_README.md` + `test_graph.py` 
- **Concept**: Directed Acyclic Graph (DAG) with parallel processing
- **Demo**: Research analysis pipeline with fact-checking and reporting
- **Architecture**: Node-based execution with output propagation

#### 4. Workflow ✅ COMPLETED
**Pattern**: Sequential pipeline processing with context passing
- **Files**: `workflow_example.py` + `WORKFLOW_README.md` + `test_workflow.py`
- **Concept**: Linear task progression with state management
- **Demo**: Content creation workflow (plan → draft → review → publish)
- **Architecture**: Token-optimized sequential processing

#### 5. A2A (Agent-to-Agent) 🚧 PLANNED
**Pattern**: Direct peer-to-peer agent communication
- **Concept**: Autonomous agents with direct messaging capabilities
- **Use Cases**: Negotiation systems, distributed decision-making

### Advanced Tool Integration Examples

#### Customer Support Agent with Intent Classification & Human Handoff ✅ NEW
**Pattern**: Multi-tool workflow with intelligent escalation and human-in-the-loop
- **Files**: `customer_support_agent.py` + `CUSTOMER_SUPPORT_AGENT_README.md` + `test_customer_support_agent.py`
- **Tools Used**: Custom intent classifier + knowledge lookup + escalation check + `handoff_to_user`
- **Model**: Amazon Nova Lite (amazon.nova-lite-v1:0) for intent classification
- **Concept**: Sophisticated customer support workflow with automated analysis and smart escalation
- **Features**:
  - Intent classification (returns, technical support, billing, etc.)
  - Emotion detection (happy, neutral, frustrated, angry)
  - Mock AWS Bedrock Knowledge Base integration
  - Intelligent escalation based on emotion, urgency, and complexity
  - Human handoff with comprehensive context packages
  - Automated response generation for simple queries

**Workflow**:
```
Customer Query → Intent Classification → Knowledge Lookup + Escalation Check → Human Handoff OR Response Generation
```

**Example Scenarios**:
```python
# Angry customer - automatic escalation to management
"This product is complete garbage! I want my money back RIGHT NOW!"
# → Escalated with high priority + empathy guidance

# Polite inquiry - automated response  
"Hi, could you help me understand your return policy please?"
# → Automated friendly response with policy details

# Technical urgency - escalated to specialists
"My device stopped working and I need it for presentation tomorrow!"
# → Escalated to technical team with urgency context
```

#### AWS Cost Monitoring with Human-in-the-Loop ✅ IMPLEMENTED
**Pattern**: Community tools integration with production workflows
- **Files**: `aws_cost_monitor_hitl_example.py` + `AWS_COST_MONITOR_HITL_README.md` + `test_aws_cost_hitl.py`
- **Tools Used**: `use_aws` (AWS service integration) + `handoff_to_user` (human-in-the-loop)
- **Concept**: Intelligent cost monitoring with human oversight and approval workflows
- **Features**: 
  - Real-time AWS cost monitoring and alerts
  - Budget threshold management with human approval
  - Cost optimization recommendations
  - Interactive approval workflows for high-cost operations
  - Production-ready error handling and logging

**Example Use Cases**:
```python
# Automated cost monitoring with human oversight
agent = AWSCostMonitoringAgent(monthly_budget_limit=1000.0, alert_threshold=0.8)
agent.run_cost_monitoring_session()

# Human approval for high-cost operations
agent.approve_high_cost_operation("Scale RDS cluster", estimated_cost=800.0)

# Interactive cost optimization
agent.check_service_costs("EC2")  # AI analysis + human decision making
```

## Quick Start

### Prerequisites
```bash
# Install required dependencies
pip install -r requirements.txt

# For AWS cost monitoring example, also install:
pip install strands-agents-tools

# Ensure AWS credentials are configured for Bedrock access
aws configure
```

### Test Individual Patterns
```bash
# Test basic tool-augmented agents
python simple_tool_agent.py

# Test multi-agent patterns
python test_swarm.py       # Quick Swarm demo
python test_graph.py       # Quick Graph demo  
python test_workflow.py    # Quick Workflow demo

# Test advanced tool integration
python test_aws_cost_hitl.py          # Quick AWS tools test
python aws_cost_monitor_hitl_example.py # Full cost monitoring demo

# Run full examples
python agents_as_tools_example.py  # Complete hierarchical system
python swarm_example.py            # Full collaborative pipeline
python graph_example.py            # Complete DAG workflow
python workflow_example.py         # Sequential content pipeline
```

## Architecture Overview

### Tool-Augmented Agents
- **Built-in Tools**: Calculator, file operations, time functions
- **Community Tools**: AWS integration, human-in-the-loop, specialized functions
- **Custom Tools**: Text processing, character analysis
- **Integration**: AWS Bedrock Nova Lite model
- **Features**: Interactive and demonstration modes

### Multi-Agent Coordination Patterns

| Pattern | Coordination | Use Case | Complexity |
|---------|-------------|----------|------------|
| **Agents as Tools** | Hierarchical | Domain routing | Low |
| **Swarm** | Autonomous | Collaboration | Medium |
| **Graph** | Dependency-based | Complex workflows | High |
| **Workflow** | Sequential | Pipelines | Medium |
| **A2A** | Peer-to-peer | Negotiation | High |

## Multi-Agent System Patterns

This chapter provides complete implementations of 5 key multi-agent patterns using the Strands framework:

### 1. Agents as Tools ✅ IMPLEMENTED
**Pattern**: Specialized agents wrapped as callable tools used by an orchestrator agent
- **File**: `agents_as_tools_example.py`
- **Documentation**: `AGENTS_AS_TOOLS_README.md`
- **Concept**: Hierarchical delegation with specialized expertise
- **Architecture**: Orchestrator + 4 specialist agents (Research, Product, Travel, Code)
- **Use Cases**: Complex queries requiring domain specialists

### 2. Swarm ✅ IMPLEMENTED
**Pattern**: Collaborative agents working together on shared tasks
- **File**: `swarm_example.py`
- **Documentation**: `SWARM_README.md`
- **Test**: `test_swarm.py`
- **Concept**: Autonomous collaboration with shared context and handoff tools
- **Architecture**: 3 specialized swarms (Software Dev, Content Creation, Business Analysis)
- **Use Cases**: Complex collaborative tasks, distributed problem-solving

### 3. Graph ✅ IMPLEMENTED
**Pattern**: Network-based agent interactions with defined relationships
- **File**: `graph_example.py`
- **Documentation**: `GRAPH_README.md`
- **Test**: `test_graph.py`
- **Concept**: Deterministic DAG execution with dependency management
- **Architecture**: 4 graph topologies (Sequential, Parallel, Conditional, Hybrid)
- **Use Cases**: Complex workflows, dependency resolution, parallel processing

### 4. Workflow ✅ IMPLEMENTED
**Pattern**: Sequential agent processing chains
- **File**: `workflow_example.py`
- **Documentation**: `WORKFLOW_README.md` 
- **Test**: `test_workflow.py`
- **Concept**: Token-efficient sequential processing with task management
- **Architecture**: SimpleWorkflowEngine with 2 workflow templates
- **Use Cases**: Data processing pipelines, approval workflows

### 5. A2A (Agent-to-Agent) 🚧 PLANNED
**Pattern**: Direct communication between autonomous agents
- **Concept**: Peer-to-peer agent interaction and negotiation
- **Use Cases**: Negotiation, distributed decision-making, autonomous coordination

## Production Features

### Error Handling & Monitoring
- Comprehensive logging with structured output
- Error recovery and graceful degradation
- Performance monitoring and token usage tracking
- AWS integration with proper credential management

### Scalability & Performance
- Token-optimized implementations to minimize costs
- Modular architecture for easy extension
- Windows and cross-platform compatibility
- Configurable timeouts and retry mechanisms

### Educational Design
- Progressive complexity from simple to advanced patterns
- Comprehensive documentation for each pattern
- Working examples that students can run immediately
- Clear architecture diagrams and explanations

## Technical Implementation

### Model Configuration
- **Primary Model**: `us.amazon.nova-lite-v1:0` (AWS Bedrock)
- **Framework**: Strands Agents SDK
- **Tools**: Built-in Strands tools + custom implementations
- **Platform**: Windows-compatible implementation

### Key Dependencies
```
strands-agents>=0.1.0
strands-agents-tools>=0.1.0
boto3>=1.34.0
python-dotenv>=1.0.0
```

## Learning Path

### Beginner (Start Here)
1. **`simple_tool_agent.py`** - Understand basic agent concepts
2. **`test_workflow.py`** - See simple sequential processing
3. **`test_aws_cost_hitl.py`** - Quick test of community tools

### Intermediate
1. **`test_swarm.py`** - Explore collaborative agents
2. **`test_graph.py`** - Understand dependency-based execution
3. **`agents_as_tools_example.py`** - Learn hierarchical patterns
4. **`aws_cost_monitor_hitl_example.py`** - Advanced tool integration

### Advanced
1. **Custom tool development** - Extend agent capabilities
2. **Multi-pattern combinations** - Hybrid architectures
3. **Production deployment** - Scale and monitor systems

## File Organization

```
chapter_06_ai_agents/
├── README.md                           # This comprehensive guide
├── requirements.txt                    # Dependencies
├── .gitignore                         # Git exclusions
│
├── simple_tool_agent.py               # Foundation patterns
├── simple_tool_agent_improved.py      # Enhanced implementations
├── SIMPLE_TOOL_AGENT_README.md        # Basic agent guide
│
├── agents_as_tools_example.py         # Hierarchical pattern
├── AGENTS_AS_TOOLS_README.md          # Hierarchical guide
│
├── swarm_example.py                   # Collaborative pattern
├── SWARM_README.md                    # Collaboration guide
├── test_swarm.py                      # Quick swarm demo
│
├── graph_example.py                   # Network pattern
├── GRAPH_README.md                    # Network guide
├── test_graph.py                      # Quick graph demo
│
├── workflow_example.py                # Sequential pattern
├── WORKFLOW_README.md                 # Pipeline guide
├── test_workflow.py                   # Quick workflow demo
│
├── aws_cost_monitor_hitl_example.py   # AWS tools + HITL integration
├── AWS_COST_MONITOR_HITL_README.md    # AWS cost monitoring guide
└── test_aws_cost_hitl.py              # Quick AWS tools test
```

## Community Tools Integration

Our examples demonstrate advanced usage of the `strands-agents-tools` community package:

### AWS Integration Tools
- **`use_aws`**: Direct AWS service integration for cost monitoring, resource management
- **Capabilities**: Cost Explorer API, Billing data, Resource usage, Service-specific costs

### Human-in-the-Loop Tools  
- **`handoff_to_user`**: Interactive approval workflows and human oversight
- **Modes**: Interactive input collection, Complete execution handoff
- **Use Cases**: Budget approvals, Critical decision points, Anomaly investigation

### Example Integration Patterns
```python
# AWS cost monitoring with human approval
from strands_tools import use_aws, handoff_to_user

agent = Agent(tools=[use_aws, handoff_to_user])
response = agent("Check AWS costs, if over budget, handoff to user for approval")

# Interactive vs Complete handoff modes
agent.tool.handoff_to_user("Approve $500 spending?", breakout_of_loop=False)  # Continue
agent.tool.handoff_to_user("Critical alert!", breakout_of_loop=True)         # Stop
```

## Comprehensive Learning Path

### Recommended Order
1. **Start with Core Concepts** - Run `comprehensive_strands_concepts_demo.py` to understand all fundamental mechanisms
2. **Basic Patterns** - Explore `simple_tool_agent.py` for foundational tool usage
3. **Multi-Agent Systems** - Progress through Agents as Tools → Swarm → Graph → Workflow
4. **Advanced Integration** - Experiment with AWS Cost Monitoring HITL example

### Key Learning Outcomes
- **Agent Loop**: Understanding the request-response-tool execution cycle
- **State Management**: Conversation history, agent state, and request state usage
- **Session Management**: Persistence across application restarts
- **Hooks System**: Lifecycle event customization for monitoring, security, and business rules
- **Structured Output**: Type-safe data extraction using Pydantic models
- **Conversation Management**: Context optimization strategies
- **Multi-Agent Coordination**: Collaboration patterns for complex problem solving

## AWS Services Integration

- **Amazon Bedrock**: AI model inference and enhancement
- **Amazon Cost Explorer**: Real-time cost monitoring and analysis  
- **AWS Budgets**: Budget tracking and automated alerts
- **Amazon S3**: Data storage and retrieval
- **Amazon Lambda**: Serverless processing triggers
- **Amazon EventBridge**: Event-driven workflows
- **Amazon SQS**: Message queuing for async processing

## Future Development

### Planned Enhancements
- **A2A Pattern Implementation** - Direct agent communication
- **Memory Management** - Persistent agent state
- **Human-in-the-Loop** - Interactive approval workflows
- **Advanced Monitoring** - Real-time agent performance tracking
- **Cloud Deployment** - AWS Lambda and EKS examples

### Integration Opportunities
- **Amazon Bedrock Knowledge Bases** - RAG-enhanced agents
- **AWS Step Functions** - Workflow orchestration
- **Amazon EventBridge** - Event-driven agent triggers
- **Amazon S3** - Persistent agent memory storage

## Notes

- All implementations are production-ready with comprehensive error handling
- Examples are optimized for educational use with clear documentation
- Token usage is optimized to minimize costs during learning
- All patterns work with AWS Bedrock Nova Lite model
- Windows-compatible implementations with cross-platform support

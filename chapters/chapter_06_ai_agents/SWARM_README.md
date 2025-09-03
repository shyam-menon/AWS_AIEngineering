# Swarm Multi-Agent Pattern Example

This example demonstrates the **"Swarm"** pattern, where multiple specialized agents collaborate autonomously as a team with shared context and working memory. Unlike hierarchical patterns, Swarm agents coordinate themselves through emergent intelligence.

## 🐝 Swarm Architecture Overview

```
Task Input
    ↓
🐝 Autonomous Agent Swarm
┌─────────────────────────────────────────────────────────┐
│  👥 Shared Working Memory & Context                     │
│                                                         │
│  Agent A ←→ Agent B ←→ Agent C ←→ Agent D              │
│     ↕         ↕         ↕         ↕                    │
│  Handoff   Handoff   Handoff   Handoff                 │
│   Tools     Tools     Tools     Tools                  │
└─────────────────────────────────────────────────────────┘
    ↓
Collective Intelligence Result
```

### Key Swarm Characteristics

1. **Self-Organization**: Agents decide autonomously when to collaborate
2. **Shared Context**: All agents access the same working memory
3. **Tool-Based Coordination**: Handoff tools enable seamless collaboration
4. **Emergent Intelligence**: Team intelligence exceeds individual capabilities
5. **Dynamic Task Distribution**: Work flows to the most appropriate agent

## 🔧 Swarm Types Implemented

### 1. Software Development Swarm 💻

**Agents**: Researcher → Architect → Coder → Reviewer

- **Researcher**: Technology research, requirements analysis, feasibility studies
- **Architect**: System design, technology selection, architectural patterns
- **Coder**: Implementation, coding standards, debugging
- **Reviewer**: Code quality, security, performance optimization

**Flow Example**:
```
Task: "Design a REST API for task management"
→ Researcher analyzes requirements and tech options
→ Architect designs system architecture
→ Coder implements the API endpoints
→ Reviewer validates code quality and security
```

### 2. Content Creation Swarm 📝

**Agents**: Content Researcher → Writer → Editor → Designer

- **Content Researcher**: Topic research, audience analysis, trend identification
- **Content Writer**: Engaging content creation, storytelling, SEO optimization
- **Content Editor**: Style editing, fact-checking, readability optimization
- **Content Designer**: Visual design, layout, user experience

**Flow Example**:
```
Task: "Create healthcare AI blog post"
→ Researcher gathers healthcare AI insights and trends
→ Writer creates compelling, informative content
→ Editor refines style, clarity, and accuracy
→ Designer optimizes visual presentation
```

### 3. Business Analysis Swarm 📊

**Agents**: Business Analyst → Strategist → Financial Advisor → Presenter

- **Business Analyst**: Process analysis, requirements gathering, market research
- **Strategist**: Strategic planning, competitive analysis, roadmap development
- **Financial Advisor**: Financial modeling, ROI analysis, business cases
- **Presenter**: Executive presentations, data visualization, stakeholder communication

**Flow Example**:
```
Task: "Analyze AI customer service platform opportunity"
→ Analyst researches market and requirements
→ Strategist develops go-to-market strategy
→ Financial Advisor creates business case and projections
→ Presenter packages insights for executives
```

## 🚀 Advanced Swarm Features

### Autonomous Coordination

Agents use built-in coordination tools to collaborate:

```python
# Agents can hand off to any other agent when needed
handoff_to_agent(
    agent_name="architect",
    message="Need system design for the API requirements",
    context={"requirements": "...", "constraints": "..."}
)
```

### Shared Context Management

All agents access shared working memory:

```python
# Swarm maintains context including:
# - Original task description
# - Agent history and handoffs
# - Knowledge contributed by each agent
# - Available agents for collaboration
```

### Safety Mechanisms

Built-in protections prevent infinite loops:

```python
swarm = Swarm(
    nodes=[researcher, architect, coder, reviewer],
    max_handoffs=15,              # Limit total handoffs
    max_iterations=20,            # Limit total iterations
    execution_timeout=600.0,      # 10-minute timeout
    node_timeout=180.0,           # 3-minute per-agent timeout
    repetitive_handoff_detection_window=6,  # Detect ping-pong
    repetitive_handoff_min_unique_agents=2  # Require diversity
)
```

### Performance Monitoring

Comprehensive execution metrics:

```python
result = swarm("Design a REST API...")

# Access detailed results
print(f"Status: {result.status}")
print(f"Agents involved: {[node.node_id for node in result.node_history]}")
print(f"Total iterations: {result.execution_count}")
print(f"Execution time: {result.execution_time}ms")
```

## 📋 Usage Examples

### Basic Swarm Execution

```bash
python swarm_example.py
```

### What You'll See

1. **Software Development Demo**: API design with full development lifecycle
2. **Content Creation Demo**: Healthcare AI blog post creation process
3. **Business Analysis Demo**: Market opportunity analysis and strategy
4. **Interactive Mode**: Custom tasks with your chosen swarm type

### Example Output

```
🐝 Demo 1: Software Development Swarm
────────────────────────────────────
📋 Task: Design and implement a REST API for task management
🐝 Swarm Type: software_development
🔄 Starting autonomous agent collaboration...

✅ Status: COMPLETED
👥 Agents Involved: researcher → architect → coder → reviewer
🔢 Total Iterations: 8
⏱️ Execution Time: 45,230ms

🎯 Final Result:
Based on the collaborative analysis by our development team, here's the complete REST API design...
```

## 💡 Key Learning Outcomes

### 1. Emergent Intelligence
- **Collective Problem-Solving**: Teams solve complex problems better than individuals
- **Shared Knowledge**: Agents build on each other's contributions
- **Adaptive Coordination**: Work flows naturally to the right expertise

### 2. Autonomous Collaboration
- **Self-Organization**: Agents decide when and how to collaborate
- **Dynamic Workflows**: No fixed sequence—agents coordinate as needed
- **Context Awareness**: Shared memory enables informed decisions

### 3. Scalable Architecture
- **Modular Teams**: Add or remove agents without breaking workflows
- **Flexible Coordination**: Handoff tools enable any-to-any collaboration
- **Domain Specialization**: Each agent focuses on their expertise

### 4. Production Considerations
- **Timeout Management**: Prevent runaway executions
- **Loop Detection**: Avoid infinite agent ping-pong
- **Performance Monitoring**: Track collaboration effectiveness

## 🔄 Extension Ideas

### Custom Swarm Types

```python
# Create domain-specific swarms
marketing_swarm = Swarm([
    market_researcher,
    campaign_strategist, 
    content_creator,
    performance_analyst
])

# Legal analysis swarm
legal_swarm = Swarm([
    legal_researcher,
    contract_analyst,
    compliance_checker,
    risk_assessor
])
```

### Advanced Coordination

```python
# Multi-modal inputs
from strands.types.content import ContentBlock

content_blocks = [
    ContentBlock(text="Analyze this product image"),
    ContentBlock(image={"format": "png", "source": {"bytes": image_data}})
]

result = swarm(content_blocks)
```

### Async Execution

```python
# Non-blocking swarm execution
async def run_multiple_swarms():
    tasks = [
        swarm1.invoke_async("Task 1"),
        swarm2.invoke_async("Task 2"), 
        swarm3.invoke_async("Task 3")
    ]
    results = await asyncio.gather(*tasks)
    return results
```

## 🎓 Educational Value

This example teaches:

1. **Collaborative AI Systems**: How agents work together autonomously
2. **Emergent Intelligence**: Collective capabilities beyond individual agents
3. **Dynamic Coordination**: Self-organizing team structures
4. **Shared Context Management**: Distributed working memory patterns
5. **Production-Ready Patterns**: Safety, monitoring, and scalability

## 📚 Comparison with Other Patterns

| Pattern | Coordination | Structure | Use Case |
|---------|-------------|-----------|----------|
| **Swarm** | Autonomous, shared context | Self-organizing team | Complex collaborative tasks |
| **Agents as Tools** | Hierarchical routing | Orchestrator + specialists | Domain-specific queries |
| **Workflow** | Sequential pipeline | Fixed sequence | Process automation |
| **Graph** | Dependency-based | Network structure | Complex relationships |
| **A2A** | Peer-to-peer | Direct communication | Negotiation, consensus |

## 🚀 Advanced Features

### Swarm as a Tool

```python
from strands_tools import swarm

# Use swarm as a tool within another agent
orchestrator = Agent(
    tools=[swarm],
    system_prompt="Create and manage swarms to solve complex tasks"
)

# The agent can dynamically create swarms
result = orchestrator("Research and develop a comprehensive AI strategy")
```

### Multi-Modal Processing

```python
# Handle text, images, and other content types
swarm = Swarm([image_analyzer, text_processor, report_generator])

# Process mixed content
result = swarm([
    ContentBlock(text="Analyze this data visualization"),
    ContentBlock(image=chart_image),
    ContentBlock(text="Create executive summary")
])
```

This Swarm pattern demonstrates the power of autonomous agent collaboration, where specialized teams work together with shared intelligence to solve complex problems that exceed individual agent capabilities.

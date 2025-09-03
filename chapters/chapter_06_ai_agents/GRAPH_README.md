# Graph Multi-Agent Pattern Example

This example demonstrates the **"Graph"** pattern, where agents are organized as nodes in a Directed Acyclic Graph (DAG) with explicit dependencies and deterministic execution order based on the graph topology.

## 📊 Graph Architecture Overview

```
Entry Point Node
       ↓
   Node A ←─── Dependencies define execution order
    ↓  ↓
Node B  Node C ←─── Nodes execute when dependencies complete
    ↓  ↓
   Node D ←────── Output propagates along edges
    ↓
Final Result
```

### Key Graph Characteristics

1. **Deterministic Execution**: Nodes execute in topological order based on dependencies
2. **Output Propagation**: Results flow from dependencies to dependent nodes
3. **Clear Dependencies**: Explicit edge definitions manage execution flow
4. **Conditional Logic**: Dynamic routing based on node results
5. **Hybrid Workflows**: Mix AI agents with deterministic business logic

## 🏗️ Graph Components

### 1. GraphNode
Represents a node in the graph with:
- **node_id**: Unique identifier for the node
- **executor**: The Agent or MultiAgentBase instance to execute
- **dependencies**: Set of nodes this node depends on
- **execution_status**: Current status (PENDING, EXECUTING, COMPLETED, FAILED)
- **result**: The NodeResult after execution

### 2. GraphEdge
Represents a connection between nodes with:
- **from_node**: Source node
- **to_node**: Target node
- **condition**: Optional function for conditional edge traversal

### 3. GraphBuilder
Provides interface for constructing graphs:
- **add_node()**: Add an agent or multi-agent system as a node
- **add_edge()**: Create a dependency between nodes
- **set_entry_point()**: Define starting nodes for execution
- **build()**: Validate and create the Graph instance

## 🔧 Graph Topologies Implemented

### 1. Research Analysis Pipeline 📚

**Topology**: Sequential Pipeline
```
Research → Analysis → Fact-Check → Report
```

**Agents**: Researcher → Analyst → Fact-Checker → Report Writer

- **Researcher**: Comprehensive information gathering and source identification
- **Analyst**: Data analysis, pattern recognition, and insight extraction
- **Fact-Checker**: Accuracy verification and bias detection
- **Report Writer**: Professional documentation and presentation

**Use Case**: "Research the impact of AI on healthcare and create comprehensive analysis"

### 2. Parallel Processing Workflow ⚡

**Topology**: Parallel Processing with Aggregation
```
Coordinator → [Technical, Business, Operations] → Aggregator
```

**Agents**: 
- **Coordinator**: Task decomposition and work distribution
- **Technical Worker**: Technical feasibility and implementation analysis
- **Business Worker**: Business case development and ROI analysis
- **Operations Worker**: Process design and operational planning
- **Aggregator**: Multi-dimensional synthesis and integration

**Use Case**: "Develop comprehensive AI customer service platform strategy"

### 3. Conditional Branching Logic 🔀

**Topology**: Dynamic Workflow Routing
```
Classifier → [Technical Branch OR Business Branch] → Specialized Reports
```

**Agents**:
- **Classifier**: Intelligent task categorization and routing decisions
- **Technical Specialist**: Deep technical analysis for technical tasks
- **Business Specialist**: Strategic business analysis for business tasks
- **Technical Reporter**: Engineering-focused documentation
- **Business Reporter**: Executive-focused strategic documentation

**Flow Example**:
```
Task: "Design fraud detection system"
→ Classifier determines: TECHNICAL
→ Routes to Technical Specialist
→ Technical Reporter creates engineering documentation
```

### 4. Hybrid Custom Nodes 🔧

**Topology**: AI + Deterministic Processing
```
AI Input Processing → Data Validation → Business Rules → AI Output Generation
```

**Components**:
- **AI Input Processor**: Intelligent data preprocessing and structuring
- **Data Validation Node**: Deterministic validation (custom node)
- **Business Rules Node**: Deterministic rule application (custom node)
- **AI Output Generator**: Intelligent final result synthesis

**Custom Nodes**:
```python
# Deterministic data validation
class DataValidationNode(MultiAgentBase):
    def _validate_data(self, content: str) -> str:
        # Length checks, format validation, content analysis
        return validation_results

# Business rules enforcement
class BusinessRulesNode(MultiAgentBase):
    def _apply_business_rules(self, content: str) -> str:
        # Policy compliance, requirement validation
        return compliance_results
```

## 🚀 Advanced Graph Features

### Conditional Edge Traversal

```python
def is_technical_task(state):
    """Only traverse if classifier determined technical focus."""
    classifier_result = state.results.get("classifier")
    if not classifier_result:
        return False
    
    result_text = str(classifier_result.result)
    return "TECHNICAL" in result_text.upper()

# Add conditional edge
builder.add_edge("classifier", "technical_specialist", condition=is_technical_task)
```

### Input Propagation

Graphs automatically build input for each node:

1. **Entry points** receive the original task as input
2. **Dependent nodes** receive combined input including:
   - The original task
   - Results from all completed dependency nodes

```
Original Task: [The original task text]

Inputs from previous nodes:

From research:
  - Researcher: [Research findings and sources]

From analysis:
  - Analyst: [Data analysis and insights]
```

### Custom Node Types

Extend `MultiAgentBase` for deterministic business logic:

```python
class FunctionNode(MultiAgentBase):
    """Execute deterministic Python functions as graph nodes."""
    
    def __init__(self, func, name: str = None):
        super().__init__()
        self.func = func
        self.name = name or func.__name__
    
    async def invoke_async(self, task, **kwargs):
        # Execute function and wrap in AgentResult
        result = self.func(task)
        # ... return MultiAgentResult
```

### Performance Monitoring

Comprehensive execution tracking:

```python
result = graph("Analyze market trends...")

# Access detailed results
print(f"Status: {result.status}")
print(f"Execution order: {[node.node_id for node in result.execution_order]}")
print(f"Total nodes: {result.total_nodes}")
print(f"Completed: {result.completed_nodes}")
print(f"Failed: {result.failed_nodes}")
print(f"Execution time: {result.execution_time}ms")
```

## 📋 Usage Examples

### Basic Graph Execution

```bash
python graph_example.py
```

### What You'll See

1. **Research Analysis Demo**: Sequential pipeline processing research tasks
2. **Parallel Processing Demo**: Coordinated multi-dimensional analysis
3. **Conditional Branching Demo**: Dynamic workflow routing based on task type
4. **Hybrid Custom Nodes Demo**: AI + deterministic processing combination
5. **Interactive Mode**: Test custom tasks with different graph topologies

### Example Output

```
📊 Demo 1: Research Analysis Pipeline
────────────────────────────────────
📋 Task: Research AI impact on healthcare delivery
🏗️ Topology: Research → Analysis → Fact-Check → Report
🔄 Starting graph execution...

✅ Status: COMPLETED
📈 Execution Order: research → analysis → fact_check → report
📊 Nodes Completed: 4/4
⏱️ Execution Time: 45,230ms

🎯 Final Result:
Comprehensive Healthcare AI Impact Report

Executive Summary:
Based on extensive research and fact-checked analysis...
```

## 💡 Key Learning Outcomes

### 1. Deterministic Workflows
- **Predictable Execution**: DAG structure ensures consistent execution order
- **Dependency Management**: Clear relationships between processing steps
- **Parallel Optimization**: Independent branches execute concurrently

### 2. Structured Coordination
- **Explicit Dependencies**: No ambiguity about execution requirements
- **Output Propagation**: Results automatically flow to dependent nodes
- **Failure Handling**: Failed nodes prevent dependent execution

### 3. Flexible Topologies
- **Sequential Pipelines**: Linear processing chains
- **Parallel Processing**: Concurrent workstream coordination
- **Conditional Branching**: Dynamic workflow routing
- **Hybrid Patterns**: AI agents + deterministic business logic

### 4. Production Benefits
- **Reliability**: Deterministic execution reduces unexpected behaviors
- **Scalability**: Parallel branches improve performance
- **Maintainability**: Clear dependency structure aids debugging
- **Compliance**: Custom nodes ensure business rule enforcement

## 🔄 Extension Ideas

### Nested Multi-Agent Patterns

```python
# Use Swarm as a node within a Graph
from strands.multiagent import Swarm

research_swarm = Swarm([
    medical_researcher,
    technology_researcher,
    economic_researcher
])

builder = GraphBuilder()
builder.add_node(research_swarm, "research_team")
builder.add_node(analyst, "analysis")
builder.add_edge("research_team", "analysis")
```

### Multi-Modal Processing

```python
from strands.types.content import ContentBlock

# Process images + text through graph
content_blocks = [
    ContentBlock(text="Analyze this medical scan"),
    ContentBlock(image={"format": "png", "source": {"bytes": image_data}})
]

result = graph(content_blocks)
```

### Dynamic Graph Construction

```python
from strands_tools import graph

# Agents can create graphs dynamically
agent = Agent(
    tools=[graph], 
    system_prompt="Create a graph of agents to solve the user's query."
)

agent("Design a TypeScript REST API and write the code")
```

## 🎓 Educational Value

This example teaches:

1. **Structured Workflows**: How to design deterministic agent coordination
2. **Dependency Management**: Managing complex agent relationships
3. **Conditional Logic**: Dynamic workflow routing based on results
4. **Hybrid Systems**: Combining AI creativity with deterministic control
5. **Performance Optimization**: Parallel execution and efficient coordination

## 📚 Comparison with Other Patterns

| Pattern | Coordination | Structure | Best For |
|---------|-------------|-----------|----------|
| **Graph** | Dependency-based | DAG with explicit edges | Complex workflows with dependencies |
| **Swarm** | Autonomous handoffs | Self-organizing team | Collaborative problem-solving |
| **Agents as Tools** | Hierarchical routing | Orchestrator + specialists | Domain-specific queries |
| **Workflow** | Sequential pipeline | Linear processing chain | Step-by-step processes |
| **A2A** | Peer-to-peer | Direct communication | Negotiation and consensus |

## 🚀 Advanced Features

### Asynchronous Execution

```python
async def run_graph():
    result = await graph.invoke_async("Research market trends...")
    return result

result = asyncio.run(run_graph())
```

### Graph as a Tool

```python
from strands_tools import graph

orchestrator = Agent(
    tools=[graph],
    system_prompt="Create and execute graphs to solve complex tasks"
)

# Agent dynamically creates and executes graphs
result = orchestrator("Analyze competitor strategies and develop response plan")
```

### Multi-Modal Graph Inputs

```python
# Handle mixed content types
graph_input = [
    ContentBlock(text="Analyze these financial charts"),
    ContentBlock(image=chart_image),
    ContentBlock(text="Generate investment recommendations")
]

result = graph(graph_input)
```

## 🏭 Production Considerations

### Graph Design Best Practices

1. **Acyclic Structure**: Ensure no cycles in dependency graph
2. **Meaningful Node IDs**: Use descriptive names for debugging
3. **Error Handling**: Plan for node failure scenarios
4. **Performance**: Balance parallelism with resource constraints
5. **Monitoring**: Track execution metrics and bottlenecks

### Validation and Testing

```python
# GraphBuilder validates structure
try:
    graph = builder.build()
except ValueError as e:
    print(f"Graph validation failed: {e}")

# Test individual nodes and edge conditions
def test_conditional_edge():
    mock_state = create_mock_state()
    assert is_technical_task(mock_state) == True
```

This Graph pattern demonstrates the power of structured, dependency-based agent coordination, enabling complex workflows with deterministic execution, parallel optimization, and hybrid AI + business logic processing.

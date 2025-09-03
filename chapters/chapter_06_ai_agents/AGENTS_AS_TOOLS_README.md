# Agents as Tools - Multi-Agent System Example

This example demonstrates the **"Agents as Tools"** pattern, a fundamental multi-agent architecture where specialized AI agents are wrapped as callable functions (tools) that can be used by an orchestrator agent.

## 🎯 Architecture Overview

The system implements a hierarchical multi-agent structure:

```
User Query
    ↓
🎯 Orchestrator Agent
    ↓
┌─────────────────────────────────────────────────────────┐
│  🔬 Research Assistant     🛍️ Product Recommendation    │
│  ✈️ Travel Planner         💻 Code Helper              │
└─────────────────────────────────────────────────────────┘
```

### Key Components

1. **Orchestrator Agent**: Analyzes user queries and routes them to appropriate specialists
2. **Research Assistant**: Handles scientific questions, factual information, and academic research
3. **Product Recommendation Assistant**: Provides shopping advice and product comparisons
4. **Travel Planning Assistant**: Creates itineraries and travel recommendations
5. **Code Helper Assistant**: Offers programming assistance and technical support

## 🔧 Implementation Details

### Specialized Agent Tools

Each specialized agent is implemented as a `@tool` decorated function:

```python
@tool
def research_assistant(query: str) -> str:
    """
    Process and respond to research-related queries with factual information.
    """
    research_agent = Agent(
        model="us.amazon.nova-lite-v1:0",
        system_prompt=specialized_research_prompt,
        tools=[calculator, current_time]
    )
    return research_agent(query)
```

### Orchestrator Configuration

The orchestrator uses an intelligent system prompt to route queries:

```python
orchestrator = Agent(
    model="us.amazon.nova-lite-v1:0",
    system_prompt=orchestrator_routing_prompt,
    tools=[
        research_assistant,
        product_recommendation_assistant,
        travel_planning_assistant,
        code_helper_assistant
    ]
)
```

## 🚀 Features Demonstrated

### 1. Intelligent Query Routing
The orchestrator automatically determines which specialist to use based on query content:

- **Research questions** → Research Assistant
- **Shopping queries** → Product Recommendation Assistant  
- **Travel planning** → Travel Planning Assistant
- **Programming questions** → Code Helper Assistant
- **Simple questions** → Direct response

### 2. Specialized Expertise
Each agent has:
- **Focused system prompts** optimized for their domain
- **Relevant tools** suited to their tasks
- **Domain-specific knowledge** and response patterns

### 3. Hierarchical Delegation
The system mimics human team dynamics:
- **Manager (Orchestrator)** coordinates and delegates
- **Specialists** handle domain-specific tasks
- **Clear chain of command** for decision-making

### 4. Modular Architecture
- Specialists can be **added, removed, or modified** independently
- Each agent is **self-contained** and focused
- **Easy to extend** with new specialists

## 📋 Usage Examples

### Research Query
```
User: "What is quantum computing and how does it differ from classical computing?"
→ Routes to Research Assistant
→ Provides detailed scientific explanation
```

### Product Recommendation
```
User: "I need a laptop for data science work under $2000"
→ Routes to Product Recommendation Assistant  
→ Analyzes requirements and suggests specific models
```

### Travel Planning
```
User: "Plan a 5-day trip to Tokyo for tech and culture"
→ Routes to Travel Planning Assistant
→ Creates detailed itinerary with tech sites and cultural activities
```

### Programming Help
```
User: "How do I implement binary search in Python?"
→ Routes to Code Helper Assistant
→ Provides implementation with explanations
```

### Complex Multi-Domain Query
```
User: "Business trip to San Francisco, need tech meetups and presentation laptop"
→ Orchestrator coordinates multiple specialists
→ Travel assistant handles meetups, product assistant handles laptop
```

## 🏃‍♂️ Running the Example

### Prerequisites
```bash
pip install strands-agents strands-agents-tools
```

### Basic Execution
```bash
python agents_as_tools_example.py
```

### What You'll See
1. **Capability Demonstrations**: 5 example queries showing different specialists
2. **Interactive Mode Option**: Chat with the multi-agent system
3. **Routing Explanations**: See which specialists are chosen and why

## 💡 Key Learning Outcomes

### 1. Separation of Concerns
- Each agent has a **single, focused responsibility**
- Easier to **understand, test, and maintain**
- **Specialized expertise** leads to better results

### 2. Scalable Architecture
- **Add new specialists** without changing existing code
- **Independent development** of different capabilities
- **Modular deployment** and updates

### 3. Intelligent Coordination
- **Automatic routing** based on query analysis
- **Context-aware delegation** to appropriate specialists
- **Fallback handling** for edge cases

### 4. Best Practices
- **Clear tool documentation** helps orchestrator make decisions
- **Focused system prompts** improve specialist performance
- **Consistent response patterns** enable reliable integration

## 🔄 Extension Ideas

### Add New Specialists
```python
@tool
def legal_advisor(query: str) -> str:
    """Provide legal guidance and contract analysis."""
    # Implementation here

@tool  
def financial_analyst(query: str) -> str:
    """Handle financial calculations and investment advice."""
    # Implementation here
```

### Enhanced Routing Logic
- **Multi-agent coordination** for complex queries
- **Confidence scoring** for routing decisions
- **Fallback chains** when primary specialist fails

### Tool Integration
- **External APIs** for real-time data
- **Database connections** for persistent knowledge
- **File processing** capabilities

## 🎓 Educational Value

This example teaches:

1. **Multi-agent design patterns** and architectures
2. **Tool abstraction** and agent composition
3. **Hierarchical AI systems** and delegation
4. **Modular development** approaches
5. **Production-ready patterns** for complex AI systems

## 📚 Related Patterns

- **Swarm**: Collaborative agents working together
- **Graph**: Network-based agent interactions  
- **Workflow**: Sequential agent processing chains
- **A2A (Agent-to-Agent)**: Direct agent communication

This "Agents as Tools" pattern provides the foundation for building sophisticated multi-agent systems that can handle complex, multi-domain queries through intelligent specialization and coordination.

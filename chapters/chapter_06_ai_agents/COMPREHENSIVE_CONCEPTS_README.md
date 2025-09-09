# Comprehensive Strands Concepts Demo

This example demonstrates all the core Strands Agent concepts covered in Chapter 6 through a practical enterprise quoting system and project analysis use case.

## 🎯 Concepts Demonstrated

### 1. **Agent Loop**
- Automatic request processing cycle
- Tool selection and execution
- Response generation with context

### 2. **State Management**
- **Conversation History**: Automatically managed message sequences
- **Agent State**: Persistent key-value storage (`agent.state.set/get`)
- **Request State**: Per-call scratchpad data via hooks

### 3. **Session Management**
- `FileSessionManager` for local persistence
- Cross-application restart continuity
- Session restoration with full state

### 4. **Conversation Management**
- `SummarizingConversationManager` with custom domain prompts
- `SlidingWindowConversationManager` for efficient context
- Token-aware conversation truncation

### 5. **Hooks System**
- **RequestLoggingHook**: Lifecycle logging and telemetry
- **FixedCalculatorPrecision**: Parameter enforcement
- **DiscountGuardrail**: Business rule validation and result modification
- **SecurityHook**: Input validation and output scanning

### 6. **Tools**
- `calculator`: Mathematical operations with precision control
- `price_lookup`: Simulated enterprise pricing system
- `track_user_action`: Agent state mutation and action logging
- `get_system_info`: System and agent state introspection

### 7. **Structured Output**
- `QuoteIntent`: Enterprise quote extraction with validation
- `ProjectAnalysis`: Technical project assessment
- Type-safe Pydantic models with business constraints

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Strands Agent                            │
├─────────────────────────────────────────────────────────────┤
│ Conversation Management (Summarizing/SlidingWindow)        │
│ Session Management (FileSessionManager)                    │
├─────────────────────────────────────────────────────────────┤
│ Hooks Layer:                                               │
│ • RequestLoggingHook (telemetry)                          │
│ • FixedCalculatorPrecision (parameter enforcement)         │
│ • DiscountGuardrail (business rules)                      │
│ • SecurityHook (input/output validation)                  │
├─────────────────────────────────────────────────────────────┤
│ Tools Layer:                                               │
│ • calculator (math operations)                            │
│ • price_lookup (enterprise pricing)                       │
│ • track_user_action (state management)                    │
│ • get_system_info (introspection)                         │
├─────────────────────────────────────────────────────────────┤
│ Agent State:                                               │
│ • tenant, preferred_currency                              │
│ • action_count, action_history                            │
│ • target_discount_pct (with policy enforcement)           │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Running the Demo

### Prerequisites
```bash
pip install strands
```

### Basic Execution
```bash
python comprehensive_strands_concepts_demo.py
```

### What You'll See

**Demo 1: Enterprise Quoting System**
- Multi-turn conversation building context
- Agent state management across interactions  
- Hook-based guardrails (discount clamping)
- Direct tool calls (recorded and hidden)
- Structured output extraction

**Demo 2: Project Analysis**
- Different agent configuration
- Alternative conversation management strategy
- Structured technical assessment

**Demo 3: Session Persistence**
- Agent creation with session
- Simulated application restart
- State and conversation restoration

## 🔍 Key Implementation Details

### Hook Implementation
```python
class DiscountGuardrail(HookProvider):
    """Business rule enforcement through hooks."""
    MAX_DISCOUNT = 12.0
    
    def register_hooks(self, registry: HookRegistry) -> None:
        registry.add_callback(BeforeToolInvocationEvent, self._before_tool)
        registry.add_callback(AfterToolInvocationEvent, self._after_tool)
    
    def _before_tool(self, event: BeforeToolInvocationEvent) -> None:
        # Clamp discount before pricing tool
        if event.tool_use["name"] == "price_lookup":
            desired = event.agent.state.get("target_discount_pct")
            if desired and desired > self.MAX_DISCOUNT:
                event.agent.state.set("target_discount_pct", self.MAX_DISCOUNT)
    
    def _after_tool(self, event: AfterToolInvocationEvent) -> None:
        # Apply discount to pricing results
        if event.tool_use["name"] == "price_lookup":
            # Post-process pricing with approved discount
```

### Agent State Management
```python
# Persistent business data (not sent to model)
agent.state.set("target_discount_pct", 18.0)
agent.state.set("action_count", count + 1)

# Cross-call state access in tools
@tool
def track_user_action(action: str, agent: Agent) -> str:
    count = agent.state.get("action_count") or 0
    agent.state.set("action_count", count + 1)
    return f"Recorded action='{action}' (total={count + 1})"
```

### Structured Output Extraction
```python
class QuoteIntent(BaseModel):
    customer_name: str = Field(description="Customer or tenant name")
    sites: conint(ge=1) = Field(description="Number of sites/locations")
    devices: conint(ge=1) = Field(description="Total devices to manage")
    service_tier: Literal["Basic", "Standard", "Premium"]
    target_discount_pct: confloat(ge=0, le=20) = 0.0

# Extract typed object from conversation
quote = agent.structured_output(
    QuoteIntent,
    "Extract the final quote intent as a typed object."
)
```

## 📊 Expected Output

The demo produces detailed logging showing:

1. **Hook Events**: Request lifecycle, tool execution, guardrail enforcement
2. **Agent State Changes**: Action tracking, discount clamping, business data
3. **Tool Execution**: Calculator operations, price lookups, system queries
4. **Structured Extraction**: Type-safe business objects with validation
5. **Session Persistence**: State restoration across "application restarts"

## 🎓 Learning Outcomes

After running this demo, you'll understand:

- How the agent loop orchestrates complex interactions
- When and how to use different types of state
- How hooks provide powerful customization points
- How to implement business rules and guardrails
- How structured output eliminates parsing complexity
- How session management enables production deployments
- How conversation management balances context and performance

## 🔧 Customization Ideas

**Extend the Demo:**
- Add more business rules via hooks
- Implement custom conversation management strategies
- Create domain-specific tools for your use case
- Add monitoring and observability hooks
- Experiment with different model providers

**Production Considerations:**
- Replace `FileSessionManager` with `S3SessionManager` for cloud deployment
- Add comprehensive error handling and retries
- Implement authentication and authorization hooks
- Add rate limiting and quota management
- Integrate with enterprise systems (CRM, ERP, etc.)

This comprehensive example showcases how Strands Agents can handle enterprise-grade requirements while maintaining clean, extensible architecture through its core concepts.

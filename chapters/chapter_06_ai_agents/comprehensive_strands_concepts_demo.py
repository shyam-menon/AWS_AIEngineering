"""
Strands Agents – Complete Example
---------------------------------
Concepts demonstrated:
- Conversation History (auto-managed via Agent)
- Agent State (durable key-value)
- Request State (per-call scratchpad via a hook)
- Session Management (FileSessionManager)
- Conversation Management (SummarizingConversationManager with custom prompt)
    # Basic turns – Conversation History builds up automatically
    response1 = agent("Hi, we need a managed device services quote.")
    print(f"Response 1: {str(response1)[:100]}...")
    
    response2 = agent("Customer is Acme Corp with 3 sites and 120 devices.")
    print(f"Response 2: {str(response2)[:100]}...")
    
    response3 = agent("Service tier should be Premium, SLA around 8 hours, currency INR.")
    print(f"Response 3: {str(response3)[:100]}...")
    
    response4 = agent("Target discount would be 18% if possible.")  # too high; guardrail will clamp later
    print(f"Response 4: {str(response4)[:100]}...")ging, guardrails, fixed tool args, result post-processing)
- Tools (calculator + price lookup + user action tracking)
- Structured Output (Pydantic)
"""

from typing import Any, List, Literal, Optional, Dict
from pydantic import BaseModel, Field, conint, confloat, ValidationError
import os
import json
import time

# Strands imports (names follow the docs you shared)
from strands import Agent, tool
from strands.agent.conversation_manager import (
    SlidingWindowConversationManager,
    SummarizingConversationManager,
)
from strands.session.file_session_manager import FileSessionManager
from strands.hooks import HookProvider, HookRegistry

# Experimental hook events for tool/model lifecycle (per docs)
from strands.experimental.hooks import (
    BeforeToolInvocationEvent,
    AfterToolInvocationEvent,
    BeforeModelInvocationEvent,
    AfterModelInvocationEvent,
)

from strands.hooks import (
    AgentInitializedEvent,
    BeforeInvocationEvent,
    AfterInvocationEvent,
    MessageAddedEvent,
)

# --------------------------
# 1) Structured Output Model
# --------------------------

class QuoteIntent(BaseModel):
    """Typed object to distill a chat into a quote request."""
    customer_name: str = Field(description="Customer or tenant name")
    sites: conint(ge=1) = Field(description="Number of sites/locations covered")
    devices: conint(ge=1) = Field(description="Total devices to manage")
    service_tier: Literal["Basic", "Standard", "Premium"]
    sla_hours: conint(ge=4, le=24) = Field(description="Response SLA in hours")
    currency: Literal["INR", "USD", "EUR"] = "INR"
    target_discount_pct: confloat(ge=0, le=20) = 0.0
    notes: List[str] = Field(default_factory=list)


class ProjectAnalysis(BaseModel):
    """Analysis of project requirements and recommendations."""
    project_name: str = Field(description="Name of the project")
    complexity_score: confloat(ge=1, le=10) = Field(description="Complexity rating 1-10")
    estimated_hours: conint(ge=1) = Field(description="Estimated development hours")
    technologies: List[str] = Field(description="Recommended technologies")
    risks: List[str] = Field(description="Identified project risks")
    budget_range: str = Field(description="Estimated budget range")


# --------------------------
# 2) Simple Demo "Tools"
# --------------------------

@tool
def calculator(expression: str, precision: int = 2) -> str:
    """
    A tiny calculator that respects precision (for demo purposes).
    In real code, use a robust parser (don't eval user input).
    """
    # Extremely naive: parse "A op B" where op in {+,-,*,/}
    parts = expression.strip().split()
    if len(parts) != 3:
        return f"Unsupported expression: {expression}"
    a, op, b = parts
    try:
        x = float(a)
        y = float(b)
    except ValueError:
        return f"Invalid numbers in: {expression}"

    if op == "+": val = x + y
    elif op == "-": val = x - y
    elif op == "*": val = x * y
    elif op == "/": val = x / y if y != 0 else float("inf")
    else: return f"Unsupported operator: {op}"

    return f"{round(val, precision)}"


@tool
def price_lookup(sku: str, quantity: int, currency: str = "INR") -> Dict[str, Any]:
    """
    Fake price lookup that returns a dict. Imagine calling PriceHub/BRIM.
    """
    base_prices = {
        "HP-MDS-BASE": {"INR": 12500, "USD": 150, "EUR": 140},
        "DELL-SRV-STD": {"INR": 8500, "USD": 100, "EUR": 95},
        "CISCO-NET-PRO": {"INR": 15500, "USD": 185, "EUR": 175}
    }
    
    base_price = base_prices.get(sku, {"INR": 10000, "USD": 120, "EUR": 110}).get(currency, 10000)
    total = base_price * quantity
    
    return {
        "sku": sku,
        "unit_price": base_price,
        "quantity": quantity,
        "currency": currency,
        "subtotal": total,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }


@tool
def track_user_action(action: str, agent: Agent) -> str:
    """
    Demonstrates Agent State usage across calls.
    """
    count = agent.state.get("action_count") or 0
    actions = agent.state.get("action_history") or []
    
    agent.state.set("action_count", count + 1)
    agent.state.set("last_action", action)
    actions.append({"action": action, "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")})
    agent.state.set("action_history", actions[-10:])  # Keep last 10 actions
    
    return f"Recorded action='{action}' (total={count + 1})"


@tool
def get_system_info(agent: Agent) -> Dict[str, Any]:
    """
    Retrieve system and agent state information.
    """
    # Fix for AgentState.get() API
    try:
        action_count = agent.state.get("action_count") or 0
    except:
        action_count = 0
        
    try:
        last_action = agent.state.get("last_action") or "None"
    except:
        last_action = "None"
        
    try:
        tenant = agent.state.get("tenant") or "Unknown"
    except:
        tenant = "Unknown"
        
    try:
        currency = agent.state.get("preferred_currency") or "INR"
    except:
        currency = "INR"
    
    return {
        "agent_name": agent.name,
        "total_actions": action_count,
        "last_action": last_action,
        "session_info": {
            "tenant": tenant,
            "currency": currency
        },
        "conversation_length": len(agent.messages),
        "current_time": time.strftime("%Y-%m-%d %H:%M:%S")
    }


# -------------------------------------
# 3) Hooks: Logging, Guardrails, Fixes
# -------------------------------------

class RequestLoggingHook(HookProvider):
    """Logs request lifecycle + basic telemetry."""
    
    def __init__(self):
        self.total_requests = 0
        self.total_tools_called = 0
        self.start_time = 0.0
    
    def register_hooks(self, registry: HookRegistry) -> None:
        registry.add_callback(BeforeInvocationEvent, self._before)
        registry.add_callback(AfterInvocationEvent, self._after)
        registry.add_callback(MessageAddedEvent, self._message_added)
        registry.add_callback(BeforeModelInvocationEvent, self._before_model)
        registry.add_callback(AfterModelInvocationEvent, self._after_model)
        registry.add_callback(BeforeToolInvocationEvent, self._before_tool)
        registry.add_callback(AfterToolInvocationEvent, self._after_tool)

    def _before(self, event: BeforeInvocationEvent) -> None:
        # Track requests (simplified without request_state)
        self.total_requests += 1
        self.start_time = time.time()
        print(f"[Hook] ▶ Request start (id={self.total_requests}) agent={event.agent.name}")

    def _after(self, event: AfterInvocationEvent) -> None:
        duration = time.time() - getattr(self, 'start_time', time.time())
        print(f"[Hook] ■ Request end (id={self.total_requests}) duration={duration:.2f}s")

    def _message_added(self, event: MessageAddedEvent) -> None:
        role = event.message.get("role")
        content_preview = str(event.message.get("content", []))[:50] + "..."
        print(f"[Hook] + Message added (role={role}) content={content_preview}")

    def _before_model(self, event: BeforeModelInvocationEvent) -> None:
        print("[Hook] 🤖 Before model invocation")

    def _after_model(self, event: AfterModelInvocationEvent) -> None:
        print("[Hook] 🤖 After model invocation")

    def _before_tool(self, event: BeforeToolInvocationEvent) -> None:
        tool_name = event.tool_use["name"]
        print(f"[Hook] 🔧 Before tool: {tool_name}")

    def _after_tool(self, event: AfterToolInvocationEvent) -> None:
        tool_name = event.tool_use["name"]
        self.total_tools_called += 1
        print(f"[Hook] 🔧 After tool: {tool_name} (total tools: {self.total_tools_called})")


class FixedCalculatorPrecision(HookProvider):
    """
    Force calculator.precision=1 regardless of what the agent/model provides.
    """
    def register_hooks(self, registry: HookRegistry) -> None:
        registry.add_callback(BeforeToolInvocationEvent, self._fix)

    def _fix(self, event: BeforeToolInvocationEvent) -> None:
        if event.tool_use["name"] == "calculator":
            event.tool_use["input"]["precision"] = 1  # enforce
            print("[Hook] ⚙ Fixed calculator.precision=1")


class DiscountGuardrail(HookProvider):
    """
    Guardrail: clamp target_discount_pct ≤ policy (e.g., 12%) before price tool calls.
    Also demonstrates result post-processing.
    """
    MAX_DISCOUNT = 12.0

    def register_hooks(self, registry: HookRegistry) -> None:
        registry.add_callback(BeforeToolInvocationEvent, self._before_tool)
        registry.add_callback(AfterToolInvocationEvent, self._after_tool)

    def _before_tool(self, event: BeforeToolInvocationEvent) -> None:
        if event.tool_use["name"] == "price_lookup":
            # Read user's intended discount (if the agent put it in agent state)
            desired = event.agent.state.get("target_discount_pct")
            if desired and desired > self.MAX_DISCOUNT:
                print(f"[Hook] 🔒 Clamping discount {desired}% → {self.MAX_DISCOUNT}% (policy)")
                event.agent.state.set("target_discount_pct", self.MAX_DISCOUNT)

    def _after_tool(self, event: AfterToolInvocationEvent) -> None:
        if event.tool_use["name"] == "price_lookup":
            # Post-process: apply discount from agent state if present
            result = event.result
            subtotal = result.get("subtotal")
            pct = event.agent.state.get("target_discount_pct") or 0.0
            if subtotal is not None and pct > 0:
                discounted = round(subtotal * (1 - pct / 100), 2)
                result["discount_pct"] = pct
                result["total_after_discount"] = discounted
                print(f"[Hook] ✔ Applied {pct}% discount; total={discounted}")


class SecurityHook(HookProvider):
    """Security monitoring and input validation."""
    
    def __init__(self):
        self.sensitive_patterns = ["password", "ssn", "credit card", "api_key"]
        self.blocked_tools = ["dangerous_operation", "delete_data"]
    
    def register_hooks(self, registry: HookRegistry) -> None:
        registry.add_callback(BeforeToolInvocationEvent, self._validate_tool)
        registry.add_callback(AfterToolInvocationEvent, self._scan_output)
    
    def _validate_tool(self, event: BeforeToolInvocationEvent) -> None:
        tool_name = event.tool_use["name"]
        if tool_name in self.blocked_tools:
            print(f"[Hook] 🚫 Blocked dangerous tool: {tool_name}")
            # In real implementation, you could raise an exception here
    
    def _scan_output(self, event: AfterToolInvocationEvent) -> None:
        # Scan tool output for sensitive information
        result_str = str(event.result).lower()
        for pattern in self.sensitive_patterns:
            if pattern in result_str:
                print(f"[Hook] ⚠️ Sensitive pattern '{pattern}' detected in output")


# ---------------------------------------------------
# 4) Conversation Management + Session Management
# ---------------------------------------------------

# Custom domain summarization prompt (preserve IDs, SKUs, quantities, SLAs)
DOMAIN_SUMMARY_PROMPT = """
You are summarizing an enterprise quoting conversation. Create concise bullet points that:
- Preserve customer name, sites, device counts, SKUs, service tier, SLA hours, and currency
- Preserve tool steps and key numeric outputs (prices, totals, discounts)
- Omit chit-chat; keep only actionable facts and decisions
- Use third-person, neutral tone
Format as short bullet points.
"""

def create_session_directory():
    """Create session directory if it doesn't exist."""
    session_dir = "./agent_sessions"
    if not os.path.exists(session_dir):
        os.makedirs(session_dir)
    return session_dir


# -------------------------
# 5) Demo Functions
# -------------------------

def demo_basic_concepts():
    """Demonstrate basic agent concepts."""
    print("\n" + "="*60)
    print("DEMO 1: Basic Concepts")
    print("="*60)
    
    # Create session directory
    session_dir = create_session_directory()
    
    # Set up conversation and session management
    summarizer = SummarizingConversationManager(
        summary_ratio=0.35,
        preserve_recent_messages=10,
        summarization_system_prompt=DOMAIN_SUMMARY_PROMPT
    )
    
    session_manager = FileSessionManager(
        session_id="demo-user-basic",
        storage_dir=session_dir
    )
    
    # Create agent with all hooks
    agent = Agent(
        name="QuoterAgent",
        model="us.amazon.nova-lite-v1:0",
        tools=[calculator, price_lookup, track_user_action, get_system_info],
        hooks=[
            RequestLoggingHook(), 
            FixedCalculatorPrecision(), 
            DiscountGuardrail(),
            SecurityHook()
        ],
        conversation_manager=summarizer,
        session_manager=session_manager,
        # Seed some durable state (Agent State)
        state={
            "tenant": "Acme Corp",
            "preferred_currency": "INR",
            "action_count": 0,
        },
        system_prompt="""You are an enterprise quoting assistant. Help customers with:
        - Device management service quotes
        - Price calculations and discounts
        - Recording customer interactions
        Use tools when needed and maintain professional communication."""
    )
    
    print("\n--- Basic Conversation Turns ---")
    
    # Basic turns – Conversation History builds up automatically
    response1 = agent("Hi, we need a managed device services quote.")
    print(f"Response 1: {str(response1)[:100]}...")
    
    response2 = agent("Customer is Acme Corp with 3 sites and 120 devices.")
    print(f"Response 2: {str(response2)[:100]}...")
    
    response3 = agent("Service tier should be Premium, SLA around 8 hours, currency INR.")
    print(f"Response 3: {str(response3)[:100]}...")
    
    response4 = agent("Target discount would be 18% if possible.")  # too high; guardrail will clamp later
    print(f"Response 4: {str(response4)[:100]}...")
    
    # Store durable business facts in Agent State (not sent to the model)
    agent.state.set("target_discount_pct", 18.0)  # will be clamped to 12% by DiscountGuardrail
    print(f"Set target discount in agent state: 18% (will be clamped)")
    
    return agent


def demo_tool_usage(agent):
    """Demonstrate direct tool usage and state management."""
    print("\n--- Direct Tool Usage ---")
    
    # Use tools – direct tool call (recorded by default)
    price = agent.tool.price_lookup(sku="HP-MDS-BASE", quantity=120, currency=agent.state.get("preferred_currency"))
    print(f"Price lookup result: {price}")
    
    # Demonstrate a direct tool call NOT recorded in history (keeps context lean)
    calc_hidden = agent.tool.calculator(expression="2 / 3", record_direct_tool_call=False)
    print(f"Hidden calculation (not in history): {calc_hidden}")
    
    # Track a user action (modifies Agent State)
    agent("Please record that we requested a premium quote")
    track_result = agent.tool.track_user_action(action="requested_premium_quote", agent=agent)
    print(f"Action tracking result: {track_result}")
    
    # Get system information
    system_info = agent.tool.get_system_info(agent=agent)
    print(f"System info: {json.dumps(system_info, indent=2)}")


def demo_structured_output(agent):
    """Demonstrate structured output capabilities."""
    print("\n--- Structured Output ---")
    
    # Use Structured Output to capture final, typed "intent" from the whole chat
    try:
        quote = agent.structured_output(
            QuoteIntent,
            "Extract the final quote intent as a typed object based on our conversation."
        )
        print("\n=== STRUCTURED QUOTE INTENT ===")
        print(f"Customer:  {quote.customer_name}")
        print(f"Sites:     {quote.sites}")
        print(f"Devices:   {quote.devices}")
        print(f"Tier:      {quote.service_tier}")
        print(f"SLA (h):   {quote.sla_hours}")
        print(f"Currency:  {quote.currency}")
        print(f"Target %:  {quote.target_discount_pct}")
        print(f"Notes:     {quote.notes}")
        
        return quote
        
    except ValidationError as e:
        print(f"[Error] Structured output failed: {e}")
        return None


def demo_project_analysis():
    """Demonstrate a different use case with project analysis."""
    print("\n" + "="*60)
    print("DEMO 2: Project Analysis with Different Tools")
    print("="*60)
    
    # Create a different agent for project analysis
    project_agent = Agent(
        name="ProjectAnalyst",
        model="us.amazon.nova-lite-v1:0",
        tools=[calculator, get_system_info],
        hooks=[RequestLoggingHook()],
        conversation_manager=SlidingWindowConversationManager(window_size=15),
        system_prompt="""You are a technical project analyst. Help assess project requirements,
        estimate complexity, and provide technology recommendations."""
    )
    
    # Project discussion
    project_agent("I need to build a web application for real-time data visualization with 1000+ concurrent users.")
    project_agent("It should handle streaming data from IoT sensors and display interactive charts.")
    project_agent("Budget is around $50,000 and timeline is 6 months.")
    
    # Extract structured analysis
    try:
        analysis = project_agent.structured_output(
            ProjectAnalysis,
            "Analyze this project and provide a structured assessment."
        )
        
        print("\n=== PROJECT ANALYSIS ===")
        print(f"Project:     {analysis.project_name}")
        print(f"Complexity:  {analysis.complexity_score}/10")
        print(f"Est. Hours:  {analysis.estimated_hours}")
        print(f"Tech Stack:  {', '.join(analysis.technologies)}")
        print(f"Risks:       {', '.join(analysis.risks)}")
        print(f"Budget:      {analysis.budget_range}")
        
    except ValidationError as e:
        print(f"[Error] Project analysis failed: {e}")


def demo_session_persistence():
    """Demonstrate session persistence across 'restarts'."""
    print("\n" + "="*60)
    print("DEMO 3: Session Persistence")
    print("="*60)
    
    session_dir = create_session_directory()
    
    print("--- Creating Agent with Session ---")
    # Create agent with session
    agent1 = Agent(
        name="PersistentAgent",
        model="us.amazon.nova-lite-v1:0",
        tools=[track_user_action, get_system_info],
        session_manager=FileSessionManager(
            session_id="persistent-demo",
            storage_dir=session_dir
        ),
        state={"demo_counter": 0}
    )
    
    # Have some interactions
    agent1("Hello, I'm starting a new session.")
    agent1.state.set("demo_counter", 5)
    agent1.tool.track_user_action("session_started", agent=agent1)
    
    print(f"Agent 1 state: {agent1.state.get()}")
    print(f"Agent 1 message count: {len(agent1.messages)}")
    
    print("\n--- Simulating Application Restart ---")
    # Simulate restart - create new agent with same session ID
    agent2 = Agent(
        name="PersistentAgent",
        model="us.amazon.nova-lite-v1:0",
        tools=[track_user_action, get_system_info],
        session_manager=FileSessionManager(
            session_id="persistent-demo",  # Same session ID
            storage_dir=session_dir
        )
    )
    
    print(f"Agent 2 state: {agent2.state.get()}")
    print(f"Agent 2 message count: {len(agent2.messages)}")
    
    # Continue conversation
    response = agent2("Do you remember our previous conversation?")
    print(f"Continuation response: {str(response)[:100]}...")


def print_agent_summary(agent):
    """Print comprehensive agent state summary."""
    print("\n=== AGENT STATE SNAPSHOT ===")
    print(f"Agent Name:    {agent.name}")
    
    # Use try/except for state access since API doesn't support default values
    try:
        action_count = agent.state.get('action_count') or 0
    except:
        action_count = 0
    
    try:
        last_action = agent.state.get('last_action') or 'None'
    except:
        last_action = 'None'
        
    try:
        discount_pct = agent.state.get('target_discount_pct') or 0
    except:
        discount_pct = 0
        
    try:
        tenant = agent.state.get('tenant') or 'Unknown'
    except:
        tenant = 'Unknown'
        
    try:
        currency = agent.state.get('preferred_currency') or 'INR'
    except:
        currency = 'INR'
    
    print(f"Action Count:  {action_count}")
    print(f"Last Action:   {last_action}")
    print(f"Discount %:    {discount_pct}")
    print(f"Tenant:        {tenant}")
    print(f"Currency:      {currency}")
    print(f"Messages:      {len(agent.messages)} in conversation history")
    
    # Show recent actions if available
    try:
        action_history = agent.state.get("action_history") or []
    except:
        action_history = []
        
    if action_history:
        print("\nRecent Actions:")
        for action in action_history[-3:]:  # Show last 3
            print(f"  - {action['action']} at {action['timestamp']}")


def main():
    """Run all demonstrations."""
    print("🚀 Strands Agents - Comprehensive Concepts Demo")
    print("This demo showcases all core Strands Agent concepts in action.")
    
    try:
        # Demo 1: Basic concepts with enterprise quoting
        agent = demo_basic_concepts()
        demo_tool_usage(agent)
        quote = demo_structured_output(agent)
        print_agent_summary(agent)
        
        # Demo 2: Different use case
        demo_project_analysis()
        
        # Demo 3: Session persistence
        demo_session_persistence()
        
        print("\n" + "="*60)
        print("✅ All demos completed successfully!")
        print("="*60)
        
        print("\n📚 Concepts Demonstrated:")
        print("• Agent Loop: Automatic request processing and tool execution")
        print("• State Management: Persistent agent state and conversation history")
        print("• Session Management: Cross-restart persistence with FileSessionManager")
        print("• Hooks: Logging, guardrails, tool modification, and security")
        print("• Tools: Calculator, price lookup, action tracking, system info")
        print("• Structured Output: Type-safe Pydantic model extraction")
        print("• Conversation Management: Summarizing and sliding window strategies")
        
        if quote:
            print(f"\n💼 Final Quote Summary:")
            print(f"   Customer: {quote.customer_name} | Devices: {quote.devices}")
            print(f"   Service: {quote.service_tier} | SLA: {quote.sla_hours}h")
            print(f"   Discount: {quote.target_discount_pct}% | Currency: {quote.currency}")
            
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

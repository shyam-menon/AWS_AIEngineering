#!/usr/bin/env python3
"""
Simple handoff_to_user Demo

A focused demonstration of how the handoff_to_user tool works
for human-in-the-loop interactions.

Author: AWS AI Engineering Course
Date: September 2025
"""

try:
    from strands import Agent
    from strands_tools import handoff_to_user
    
    print("✅ Strands agents and handoff_to_user imported successfully!")
    
    def demo_basic_handoff():
        """Demonstrate basic handoff_to_user functionality."""
        
        print("\n🎯 HANDOFF_TO_USER DEMO")
        print("=" * 50)
        print("This shows how an AI agent can hand off to a human")
        print("when it encounters something it can't handle.")
        print("=" * 50)
        
        # Create a simple agent with handoff capability
        print("🤖 Creating agent with handoff_to_user tool...")
        agent = Agent(
            tools=[handoff_to_user],
            model="amazon.nova-lite-v1:0"
        )
        print("✅ Agent created!")
        
        # Scenario: Agent needs human help
        print("\n📋 Scenario: Customer has a complex billing dispute")
        print("🤖 Agent realizes it needs human assistance...")
        
        customer_query = """
I've been charged three times for the same service this month, 
and when I called your billing department, they told me it was 
a system error but it still hasn't been fixed after two weeks. 
I need someone with authority to resolve this immediately and 
also compensate me for the inconvenience. This is affecting my 
business operations and I'm considering legal action.
"""
        
        print(f"💬 Customer Query: {customer_query.strip()}")
        print("\n🤖 Agent processing...")
        print("   (Agent will realize this needs human intervention)")
        
        # The agent will use handoff_to_user when it determines human help is needed
        prompt = f"""
You are a customer service AI. The customer has this complex issue: {customer_query.strip()}

This appears to be a complex billing dispute involving:
- Multiple incorrect charges  
- Previous failed resolution attempts
- Potential legal implications
- Business impact claims

This requires human intervention. Please use the handoff_to_user tool to connect 
the customer with a human agent who can handle billing disputes and authorization for compensation.
"""
        
        try:
            result = agent(prompt)
            print("\n✅ Handoff process completed!")
            print("📋 The agent successfully handed off to human assistance")
            
        except KeyboardInterrupt:
            print("\n⏹️ Demo interrupted by user")
        except Exception as e:
            print(f"\n❌ Error during handoff: {e}")
    
    def demo_customer_support_handoff():
        """Demonstrate handoff in customer support context."""
        
        print("\n🎯 CUSTOMER SUPPORT INTEGRATION DEMO")
        print("=" * 50)
        
        try:
            from customer_support_agent import create_customer_support_agent
            
            print("🤖 Creating customer support agent...")
            agent = create_customer_support_agent()
            print("✅ Customer support agent created with handoff capability!")
            
            # Test with an escalation scenario
            escalation_query = "I am absolutely furious! Your product broke after one day and I want an IMMEDIATE refund plus compensation for my wasted time. I will be posting negative reviews everywhere if this isn't resolved RIGHT NOW!"
            
            print(f"\n😡 Angry Customer: {escalation_query}")
            print("\n🤖 Customer support agent processing...")
            print("   (Should detect anger and escalate to human)")
            
            result = agent(escalation_query)
            print("\n✅ Customer support handoff completed!")
            
        except ImportError:
            print("❌ Customer support agent not available for this test")
        except Exception as e:
            print(f"❌ Error in customer support demo: {e}")
    
    if __name__ == "__main__":
        print("🚀 HANDOFF_TO_USER DEMONSTRATIONS")
        print("=" * 60)
        print("Choose a demo to run:")
        print("1. Basic handoff demonstration")
        print("2. Customer support integration")
        print("3. Both demos")
        print("=" * 60)
        
        choice = input("Enter choice (1/2/3) or press Enter for basic demo: ").strip()
        
        if choice == "2":
            demo_customer_support_handoff()
        elif choice == "3":
            demo_basic_handoff()
            demo_customer_support_handoff()
        else:
            demo_basic_handoff()
        
        print("\n📚 How handoff_to_user works:")
        print("─" * 40)
        print("1. 🤖 Agent determines human help is needed")
        print("2. 📞 Agent calls handoff_to_user tool")
        print("3. ⏸️  Execution pauses and prompts for human input")
        print("4. 👤 Human provides input/decision in terminal")
        print("5. 🔄 Agent receives human input and continues")
        print("6. ✅ Workflow completes with human guidance")

except ImportError as e:
    print("❌ Required libraries not available.")
    print(f"   Error: {e}")
    print("   Please install: pip install strands-agents strands-agents-tools")

except Exception as e:
    print(f"❌ Unexpected error: {e}")

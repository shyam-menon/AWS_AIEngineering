#!/usr/bin/env python3
"""
Customer Support Agent Usage Examples

This file demonstrates how to use the customer support agent with 
practical examples and different scenarios.

Author: AWS AI Engineering Course
Date: September 2025
"""

from customer_support_agent import create_customer_support_agent

def run_example_scenarios():
    """Run example scenarios to demonstrate the customer support agent capabilities."""
    
    print("🎯 CUSTOMER SUPPORT AGENT DEMO")
    print("=" * 60)
    print("This demonstrates a production-ready customer support workflow")
    print("with intelligent intent classification and human handoff capabilities.")
    print("=" * 60)
    
    # Create the agent
    print("\n🤖 Creating Customer Support Agent...")
    try:
        agent = create_customer_support_agent()
        print("✅ Agent created successfully!")
        print("📋 Agent capabilities:")
        print("   • Intent classification using Amazon Nova Lite")
        print("   • Knowledge base lookup (mock implementation)")
        print("   • Intelligent escalation decision making")
        print("   • Human handoff with full context")
        print("   • Automated response generation")
        
    except Exception as e:
        print(f"❌ Error creating agent: {e}")
        print("   Please ensure AWS credentials and Bedrock access are configured")
        return
    
    # Example scenarios
    scenarios = [
        {
            "title": "🔥 Scenario 1: Angry Customer (High Priority Escalation)",
            "description": "Customer using strong negative language with immediate refund demand",
            "query": "This product is complete garbage! I want my money back RIGHT NOW! This is the worst purchase I've ever made!",
            "expected_outcome": "Should escalate to management team due to angry emotion and immediate demand"
        },
        {
            "title": "😊 Scenario 2: Polite Return Inquiry (Automated Response)",
            "description": "Neutral customer asking about return policy",
            "query": "Hi there! I purchased a product last week but it's not quite what I expected. Could you please help me understand your return policy?",
            "expected_outcome": "Should handle automatically with knowledge base information"
        },
        {
            "title": "⚡ Scenario 3: Urgent Technical Issue (Technical Escalation)",
            "description": "Time-sensitive technical problem requiring expert help",
            "query": "My device stopped working completely and I need it for an important presentation tomorrow morning. This is very urgent - can someone help me immediately?",
            "expected_outcome": "Should escalate to technical specialists due to high urgency"
        },
        {
            "title": "💰 Scenario 4: Billing Dispute (Medium Priority)",
            "description": "Customer concerned about billing charges",
            "query": "I noticed some charges on my bill that I don't recognize. Could someone help me understand what these are for? I'm a bit concerned about this.",
            "expected_outcome": "May escalate due to billing sensitivity, depends on emotion analysis"
        }
    ]
    
    # Run each scenario
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{'-'*60}")
        print(f"{scenario['title']}")
        print(f"{'-'*60}")
        print(f"📝 Description: {scenario['description']}")
        print(f"🎯 Expected: {scenario['expected_outcome']}")
        print(f"\n💬 Customer Query:")
        print(f'   "{scenario["query"]}"')
        print(f"\n🤖 Agent Analysis:")
        
        try:
            # Process with agent
            result = agent(scenario["query"])
            print(f"✅ Scenario {i} processed successfully!")
            
        except Exception as e:
            print(f"❌ Error in scenario {i}: {e}")
            if "credentials" in str(e).lower():
                print("   💡 This error suggests AWS credentials are not configured")
                print("      Run 'aws configure' to set up your credentials")
            elif "bedrock" in str(e).lower():
                print("   💡 This error suggests Bedrock model access is not enabled")
                print("      Enable amazon.nova-lite-v1:0 model access in AWS Bedrock console")
        
        print(f"\n{'-'*60}")
    
    print(f"\n🎉 DEMO COMPLETED!")
    print("=" * 60)
    print("Key Features Demonstrated:")
    print("✅ Multi-stage analysis workflow")
    print("✅ Emotion and urgency detection") 
    print("✅ Intelligent escalation decisions")
    print("✅ Context-aware response generation")
    print("✅ Human handoff preparation")
    print("=" * 60)


def demonstrate_individual_tools():
    """Demonstrate individual tools without requiring full AWS integration."""
    
    print("\n🛠️ INDIVIDUAL TOOLS DEMONSTRATION")
    print("=" * 50)
    print("Testing tools that work without AWS credentials...")
    
    try:
        from customer_support_agent import lookup_knowledge_base, check_escalation_needed, prepare_human_handoff, generate_customer_response
        
        # Test data
        sample_intent_data = {
            "intent": "RETURNS_REFUNDS",
            "confidence": 0.95,
            "customer_emotion": "angry",
            "urgency": "high",
            "escalation_triggers": ["negative_language", "immediate_demand"],
            "key_phrases": ["garbage", "money back", "NOW!"]
        }
        
        print("\n📚 Testing Knowledge Lookup...")
        knowledge = lookup_knowledge_base(sample_intent_data)
        print(f"   ✅ Found {len(knowledge.get('relevant_articles', []))} articles")
        print(f"   📋 Sample article: {knowledge.get('relevant_articles', ['None'])[0]}")
        
        print("\n🚨 Testing Escalation Check...")
        escalation = check_escalation_needed(sample_intent_data)
        print(f"   🎯 Decision: {'ESCALATE' if escalation.get('escalate') else 'NO ESCALATION'}")
        print(f"   📊 Score: {escalation.get('escalation_score', 0)}/10")
        print(f"   🏢 Department: {escalation.get('suggested_department', 'unknown')}")
        
        if escalation.get('escalate'):
            print("\n👥 Testing Human Handoff Preparation...")
            handoff = prepare_human_handoff(escalation, sample_intent_data, knowledge)
            print(f"   ✅ Handoff package prepared")
            print(f"   📋 Priority: {handoff.get('priority', 'unknown')}")
            print(f"   🎯 Department: {handoff.get('department', 'unknown')}")
        
        print("\n💬 Testing Response Generation...")
        response = generate_customer_response(sample_intent_data, knowledge, escalation)
        print(f"   ✅ Response generated")
        print(f"   🎨 Tone: {response.get('tone', 'unknown')}")
        print(f"   ⏰ Resolution time: {response.get('estimated_resolution_time', 'unknown')}")
        
        print("\n✅ All individual tools working correctly!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Error testing tools: {e}")


def main():
    """Main function to run customer support agent demonstrations."""
    
    print("🚀 CUSTOMER SUPPORT AGENT EXAMPLES")
    print("=" * 60)
    print()
    print("This file demonstrates two modes:")
    print("1. Full agent scenarios (requires AWS credentials)")
    print("2. Individual tool testing (works without AWS)")
    print()
    print("Choose your mode based on your setup:")
    print()
    
    # Test individual tools first (always works)
    demonstrate_individual_tools()
    
    # Try full scenarios if possible
    print("\n" + "="*60)
    print("Now attempting full agent scenarios...")
    print("(This requires AWS credentials and Bedrock access)")
    print("="*60)
    
    try:
        run_example_scenarios()
    except Exception as e:
        print(f"\n❌ Full scenarios not available: {e}")
        print("\n💡 To enable full scenarios:")
        print("   1. Configure AWS credentials: aws configure")
        print("   2. Enable Bedrock model access for amazon.nova-lite-v1:0")
        print("   3. Ensure network connectivity to AWS")


if __name__ == "__main__":
    main()

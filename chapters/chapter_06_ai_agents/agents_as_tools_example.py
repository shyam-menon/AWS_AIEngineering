#!/usr/bin/env python3
"""
Agents as Tools Example - Multi-Agent System

This example demonstrates the "Agents as Tools" pattern where specialized agents
are wrapped as callable functions (tools) that can be used by an orchestrator agent.

The system includes:
- Research Assistant Agent (for factual information)
- Product Recommendation Agent (for shopping advice)
- Travel Planning Agent (for trip recommendations)
- Code Helper Agent (for programming assistance)
- Main Orchestrator Agent (routes queries to specialists)

This creates a hierarchical multi-agent system where each agent has specialized
expertise and the orchestrator intelligently delegates tasks.
"""

import logging
from typing import Dict, Any, Optional
from strands import Agent, tool
from strands_tools import calculator, current_time, file_read

# Configure logging for better visibility
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# ===============================
# SPECIALIZED AGENT TOOL FUNCTIONS
# ===============================

@tool
def research_assistant(query: str) -> str:
    """
    Process and respond to research-related queries with factual information.
    
    Use this agent for:
    - Scientific questions
    - Historical facts
    - General knowledge queries
    - Academic research topics
    
    Args:
        query: A research question requiring factual information
        
    Returns:
        A detailed research answer with explanations
    """
    try:
        logger.info(f"🔬 Research Assistant processing: {query}")
        
        # Define specialized system prompt for research
        research_system_prompt = """You are a specialized research assistant with expertise in 
        providing factual, well-sourced information. Focus on:
        - Accuracy and factual correctness
        - Clear explanations of complex topics
        - Scientific and academic rigor
        - Citing sources when possible
        
        Provide comprehensive but concise answers to research questions."""
        
        # Create specialized research agent
        research_agent = Agent(
            model="us.amazon.nova-lite-v1:0",
            system_prompt=research_system_prompt,
            tools=[calculator, current_time]  # Research-relevant tools
        )
        
        # Process the research query
        response = research_agent(f"Research question: {query}")
        
        logger.info("✅ Research Assistant completed successfully")
        return f"🔬 Research Assistant Response:\n{response}"
        
    except Exception as e:
        logger.error(f"❌ Error in research assistant: {e}")
        return f"❌ Research Assistant Error: Unable to process query - {str(e)}"


@tool
def product_recommendation_assistant(query: str) -> str:
    """
    Handle product recommendation queries by suggesting appropriate products.
    
    Use this agent for:
    - Product comparisons
    - Shopping advice
    - Feature recommendations
    - Purchase decisions
    
    Args:
        query: A product inquiry with user preferences
        
    Returns:
        Personalized product recommendations with reasoning
    """
    try:
        logger.info(f"🛍️ Product Recommendation Assistant processing: {query}")
        
        # Define specialized system prompt for product recommendations
        product_system_prompt = """You are a specialized product recommendation assistant. 
        Focus on:
        - Understanding user needs and preferences
        - Comparing product features and benefits
        - Considering budget constraints
        - Providing personalized recommendations
        - Explaining the reasoning behind recommendations
        
        Always ask clarifying questions if user needs are unclear."""
        
        # Create specialized product recommendation agent
        product_agent = Agent(
            model="us.amazon.nova-lite-v1:0",
            system_prompt=product_system_prompt,
            tools=[calculator, current_time]  # Tools for price calculations, etc.
        )
        
        # Process the product query
        response = product_agent(f"Product recommendation request: {query}")
        
        logger.info("✅ Product Recommendation Assistant completed successfully")
        return f"🛍️ Product Recommendation Assistant Response:\n{response}"
        
    except Exception as e:
        logger.error(f"❌ Error in product recommendation assistant: {e}")
        return f"❌ Product Recommendation Error: Unable to process query - {str(e)}"


@tool
def travel_planning_assistant(query: str) -> str:
    """
    Create travel itineraries and provide travel advice.
    
    Use this agent for:
    - Trip planning and itineraries
    - Destination recommendations
    - Travel logistics
    - Cultural and activity suggestions
    
    Args:
        query: A travel planning request with destination and preferences
        
    Returns:
        A detailed travel itinerary or travel advice
    """
    try:
        logger.info(f"✈️ Travel Planning Assistant processing: {query}")
        
        # Define specialized system prompt for travel planning
        travel_system_prompt = """You are a specialized travel planning assistant with expertise in:
        - Creating detailed travel itineraries
        - Recommending destinations based on preferences
        - Suggesting activities and attractions
        - Providing practical travel advice
        - Considering budget, time, and logistics
        
        Create comprehensive and practical travel plans."""
        
        # Create specialized travel planning agent
        travel_agent = Agent(
            model="us.amazon.nova-lite-v1:0",
            system_prompt=travel_system_prompt,
            tools=[calculator, current_time]  # Tools for date calculations, etc.
        )
        
        # Process the travel query
        response = travel_agent(f"Travel planning request: {query}")
        
        logger.info("✅ Travel Planning Assistant completed successfully")
        return f"✈️ Travel Planning Assistant Response:\n{response}"
        
    except Exception as e:
        logger.error(f"❌ Error in travel planning assistant: {e}")
        return f"❌ Travel Planning Error: Unable to process query - {str(e)}"


@tool
def code_helper_assistant(query: str) -> str:
    """
    Provide programming assistance and code-related help.
    
    Use this agent for:
    - Code debugging and troubleshooting
    - Programming concept explanations
    - Code optimization suggestions
    - Technology recommendations
    
    Args:
        query: A programming or technical question
        
    Returns:
        Technical assistance with code examples and explanations
    """
    try:
        logger.info(f"💻 Code Helper Assistant processing: {query}")
        
        # Define specialized system prompt for coding assistance
        code_system_prompt = """You are a specialized programming assistant with expertise in:
        - Multiple programming languages (Python, JavaScript, Java, C++, etc.)
        - Debugging and troubleshooting code issues
        - Best practices and design patterns
        - Code optimization and performance
        - Technology stack recommendations
        
        Provide clear, practical coding solutions with explanations."""
        
        # Create specialized code helper agent
        code_agent = Agent(
            model="us.amazon.nova-lite-v1:0",
            system_prompt=code_system_prompt,
            tools=[calculator, current_time, file_read]  # Tools for technical tasks
        )
        
        # Process the coding query
        response = code_agent(f"Programming question: {query}")
        
        logger.info("✅ Code Helper Assistant completed successfully")
        return f"💻 Code Helper Assistant Response:\n{response}"
        
    except Exception as e:
        logger.error(f"❌ Error in code helper assistant: {e}")
        return f"❌ Code Helper Error: Unable to process query - {str(e)}"


# ===============================
# ORCHESTRATOR AGENT
# ===============================

class AgentsAsToolsOrchestrator:
    """
    Main orchestrator agent that coordinates specialized agent tools.
    
    This agent analyzes user queries and routes them to the appropriate
    specialized agent based on the query content and intent.
    """
    
    def __init__(self):
        """Initialize the orchestrator with all specialized agent tools."""
        logger.info("🎯 Initializing Agents as Tools Orchestrator...")
        
        # Define the orchestrator system prompt with clear routing guidance
        orchestrator_system_prompt = """You are an intelligent orchestrator agent that coordinates 
        specialized AI assistants. Your role is to:
        
        1. Analyze user queries to understand their intent and domain
        2. Route queries to the most appropriate specialized agent
        3. Provide direct answers for simple questions that don't require specialization
        
        Available Specialized Agents:
        
        🔬 research_assistant - Use for:
        - Scientific questions and research topics
        - Historical facts and academic queries
        - General knowledge and factual information
        - Complex explanations requiring accuracy
        
        🛍️ product_recommendation_assistant - Use for:
        - Product comparisons and shopping advice
        - Purchase recommendations and feature analysis
        - Budget-conscious buying decisions
        - Technology and consumer goods guidance
        
        ✈️ travel_planning_assistant - Use for:
        - Trip planning and itinerary creation
        - Destination recommendations
        - Travel logistics and advice
        - Cultural activities and attractions
        
        💻 code_helper_assistant - Use for:
        - Programming questions and debugging
        - Code optimization and best practices
        - Technology stack recommendations
        - Technical troubleshooting
        
        Routing Guidelines:
        - For simple greetings or basic questions, answer directly
        - For complex queries that span multiple domains, use the most relevant specialist
        - Always explain which specialist you're consulting and why
        - If uncertain about routing, choose the most relevant specialist
        
        Be helpful, efficient, and always prioritize the user's needs."""
        
        # Create the orchestrator agent with all specialized tools
        self.orchestrator = Agent(
            model="us.amazon.nova-lite-v1:0",
            system_prompt=orchestrator_system_prompt,
            tools=[
                research_assistant,
                product_recommendation_assistant,
                travel_planning_assistant,
                code_helper_assistant,
                calculator,
                current_time
            ]
        )
        
        logger.info("✅ Orchestrator initialized successfully!")
        logger.info(f"🔧 Available specialist tools: {len(self.orchestrator.tool_names)} total")
    
    def process_query(self, user_query: str) -> str:
        """
        Process a user query by routing it to appropriate specialists.
        
        Args:
            user_query: The user's question or request
            
        Returns:
            The response from the orchestrator and/or specialists
        """
        try:
            logger.info(f"🎯 Processing user query: {user_query}")
            
            # Use the orchestrator to analyze and route the query
            response = self.orchestrator(user_query)
            
            logger.info("✅ Query processed successfully")
            return str(response)
            
        except Exception as e:
            logger.error(f"❌ Error processing query: {e}")
            return f"❌ I encountered an error while processing your request: {str(e)}"
    
    def demonstrate_capabilities(self):
        """Demonstrate the multi-agent system with various example queries."""
        
        demo_queries = [
            {
                "category": "Research Question",
                "query": "What is quantum computing and how does it differ from classical computing?",
                "expected_agent": "research_assistant",
                "emoji": "🔬"
            },
            {
                "category": "Product Recommendation",
                "query": "I need a laptop for data science work under $2000. What would you recommend?",
                "expected_agent": "product_recommendation_assistant",
                "emoji": "🛍️"
            },
            {
                "category": "Travel Planning",
                "query": "Plan a 5-day trip to Tokyo for someone interested in technology and culture",
                "expected_agent": "travel_planning_assistant",
                "emoji": "✈️"
            },
            {
                "category": "Code Help",
                "query": "How do I implement a binary search algorithm in Python?",
                "expected_agent": "code_helper_assistant",
                "emoji": "💻"
            },
            {
                "category": "Complex Multi-Domain",
                "query": "I'm planning a business trip to San Francisco and need recommendations for tech meetups and a good laptop for presentations",
                "expected_agent": "multiple_agents",
                "emoji": "🌐"
            }
        ]
        
        print("\n" + "="*80)
        print("🎯 AGENTS AS TOOLS - MULTI-AGENT SYSTEM DEMONSTRATION")
        print("="*80)
        print("\nThis example shows how an orchestrator agent coordinates specialized agents")
        print("to handle different types of queries using the 'Agents as Tools' pattern.\n")
        
        for i, demo in enumerate(demo_queries, 1):
            print(f"\n{demo['emoji']} Demo {i}: {demo['category']}")
            print("-" * 60)
            print(f"❓ Query: {demo['query']}")
            print(f"🎯 Expected to use: {demo['expected_agent']}")
            print("\n🤖 Orchestrator Response:")
            
            try:
                response = self.process_query(demo['query'])
                print(response)
            except Exception as e:
                print(f"❌ Error: {e}")
            
            print("\n" + "."*60)
    
    def interactive_mode(self):
        """Run the multi-agent system in interactive mode."""
        print("\n" + "="*80)
        print("🎯 INTERACTIVE MODE - Multi-Agent System with Specialized Tools")
        print("="*80)
        print("💡 The orchestrator will automatically route your queries to specialists:")
        print("   🔬 Research questions → Research Assistant")
        print("   🛍️ Shopping/product queries → Product Recommendation Assistant")
        print("   ✈️ Travel planning → Travel Planning Assistant")
        print("   💻 Programming questions → Code Helper Assistant")
        print("   📞 Simple questions → Direct response")
        print("   • Type 'quit' to exit")
        print("-" * 80)
        
        while True:
            try:
                user_input = input("\n🗣️  You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("👋 Thank you for exploring the Agents as Tools pattern!")
                    break
                
                if not user_input:
                    print("📝 Please enter a query or 'quit' to exit.")
                    continue
                
                print("\n🎯 Orchestrator: ", end="")
                response = self.process_query(user_input)
                print(response)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Thanks for trying the multi-agent system!")
                break
            except Exception as e:
                logger.error(f"Error in interactive mode: {e}")
                print(f"❌ Sorry, I encountered an error: {e}")


def main():
    """Main function to run the Agents as Tools demonstration."""
    
    print("🎯 Agents as Tools - Multi-Agent System Example")
    print("=" * 55)
    print("\nThis example demonstrates the 'Agents as Tools' pattern where:")
    print("• Specialized agents are wrapped as tools")
    print("• An orchestrator routes queries to appropriate specialists")
    print("• Each agent has focused expertise and optimized prompts")
    
    try:
        # Initialize the multi-agent orchestrator
        orchestrator = AgentsAsToolsOrchestrator()
        
        # Run capability demonstrations
        orchestrator.demonstrate_capabilities()
        
        # Ask user if they want to try interactive mode
        print("\n" + "="*80)
        try_interactive = input("🎮 Would you like to try interactive mode? (y/n): ").strip().lower()
        
        if try_interactive in ['y', 'yes']:
            orchestrator.interactive_mode()
        else:
            print("👍 Demo completed! You can run this script again to explore more.")
            
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"❌ Fatal error: {e}")
        print("🔧 Please check your Strands installation and try again.")


if __name__ == "__main__":
    main()

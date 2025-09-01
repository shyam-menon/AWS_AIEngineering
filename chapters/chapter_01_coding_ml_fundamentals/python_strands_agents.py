#!/usr/bin/env python3
"""
Python Fundamentals: Strands Agents Framework

This module demonstrates the Strands Agents framework - an open-source framework
for building AI agents that can interact with users, tools, and other agents.

Strands Agents provides a simple and powerful way to create, manage, and deploy
agents for AI engineering applications.

Author: AWS AI Engineering Course
Date: August 2025
"""

# Note: This is a demonstration of the Strands Agents framework
# The actual strands library may need to be installed separately

try:
    from strands import Agent
    from strands.tools import tool
    from strands_tools import calculator, current_time
    STRANDS_AVAILABLE = True
except ImportError:
    STRANDS_AVAILABLE = False
    print("⚠️  Strands library not installed. Running in demonstration mode.")
    print("   To install: pip install strands-agents strands-agents-tools")
    print()


class MockAgent:
    """Mock Agent class for demonstration when strands is not available."""
    
    def __init__(self, name="Demo Agent", description="A mock agent for demonstration"):
        self.name = name
        self.description = description
        self.conversation_history = []
    
    def __call__(self, message):
        """Simulate agent response."""
        self.conversation_history.append(("user", message))
        
        # Simple response logic for demonstration
        if "hello" in message.lower():
            response = f"Hello! I'm {self.name}. How can I assist you with AI engineering today?"
        elif "weather" in message.lower():
            response = "I'm an AI engineering agent, but I can help you build weather-related AI applications!"
        elif "code" in message.lower():
            response = "I can help you understand Python fundamentals for AI development. What specific topic interests you?"
        elif "ai" in message.lower() or "agent" in message.lower():
            response = "I'm designed to help with AI engineering tasks. I can assist with data processing, model training, and deployment strategies."
        else:
            response = f"I understand you said: '{message}'. As an AI engineering agent, I can help you with Python, AWS, and machine learning concepts."
        
        self.conversation_history.append(("agent", response))
        return response
    
    def get_history(self):
        """Get conversation history."""
        return self.conversation_history
    
    def reset(self):
        """Reset conversation history."""
        self.conversation_history = []


def basic_agent_example():
    """Demonstrate basic Strands agent creation and interaction."""
    print("=== BASIC STRANDS AGENT EXAMPLE ===")
    print()
    
    if STRANDS_AVAILABLE:
        # Create a real Strands agent with tools using Nova Lite
        try:
            agent = Agent(
                tools=[calculator, current_time],
                model="amazon.nova-lite-v1:0"
            )
            print("✅ Created Strands Agent with calculator and current_time tools (Nova Lite model)")
            
            # Basic interaction - just like the quickstart
            print("\n1. Basic Agent Interaction:")
            response = agent("Hello, world!")
            print(f"   User: Hello, world!")
            print(f"   Agent: {response}")
            print()
            
            # Test with tool usage
            print("2. Agent with Tool Usage:")
            tool_response = agent("What time is it and what is 25 * 48?")
            print(f"   User: What time is it and what is 25 * 48?")
            print(f"   Agent: {tool_response}")
            print()
            
        except Exception as e:
            print(f"⚠️  Error creating real Strands agent: {e}")
            print("   This might be due to missing AWS credentials or model access.")
            print("   Falling back to mock agent demonstration...")
            _create_mock_agent_demo()
    else:
        _create_mock_agent_demo()


def _create_mock_agent_demo():
    """Create mock agent demonstration when Strands is not available."""
    # Use mock agent for demonstration
    agent = MockAgent()
    print("🔧 Created Mock Agent (for demonstration)")
    
    print()
    
    # Basic interaction
    print("1. Basic Agent Interaction:")
    response = agent("Hello, world!")
    print(f"   User: Hello, world!")
    print(f"   Agent: {response}")
    print()
    
    # Multiple interactions
    print("2. Multiple Interactions:")
    messages = [
        "What can you help me with?",
        "Tell me about AI engineering",
        "How do I get started with Python for AI?"
    ]
    
    for msg in messages:
        response = agent(msg)
        print(f"   User: {msg}")
        print(f"   Agent: {response}")
        print()


def advanced_agent_features():
    """Demonstrate advanced Strands agent features."""
    print("=== ADVANCED STRANDS AGENT FEATURES ===")
    print()
    
    # Custom agent with specific capabilities
    if STRANDS_AVAILABLE:
        try:
            # Real Strands agent with custom configuration using Nova Lite
            ai_tutor = Agent(model="amazon.nova-lite-v1:0")  # Nova Lite for faster responses
            print("✅ Created AI Tutor Agent (Nova Lite model)")
            
            # Try a simple interaction first
            response = ai_tutor("Hello! I'm a student learning AI engineering.")
            print("✅ AI Tutor agent working successfully!")
            print(f"   Sample response: {response[:100]}...")
            
        except Exception as e:
            print(f"⚠️  Error with real Strands AI Tutor: {e}")
            print("   This is likely due to AWS Bedrock model access.")
            print("   Falling back to mock agent demonstration...")
            _create_mock_ai_tutor_demo()
    else:
        _create_mock_ai_tutor_demo()


def _create_mock_ai_tutor_demo():
    """Create mock AI tutor demonstration."""
    ai_tutor = MockAgent(
        name="AI Engineering Tutor",
        description="Specialized agent for AI engineering education"
    )
    print("🔧 Created Mock AI Engineering Tutor")
    
    print()
    
    # Educational interactions
    print("1. AI Engineering Tutoring:")
    educational_queries = [
        "Explain machine learning basics",
        "What is the difference between supervised and unsupervised learning?",
        "How do I choose the right AWS service for my AI project?"
    ]
    
    for query in educational_queries:
        response = ai_tutor(query)
        print(f"   Student: {query}")
        print(f"   Tutor: {response}")
        print()


def agent_with_tools():
    """Demonstrate Strands agent with tool integration."""
    print("=== STRANDS AGENT WITH TOOLS ===")
    print()
    
    if STRANDS_AVAILABLE:
        try:
            # Define a custom tool using the @tool decorator (from the quickstart)
            @tool
            def letter_counter(word: str, letter: str) -> int:
                """
                Count occurrences of a specific letter in a word.
                
                Args:
                    word (str): The input word to search in
                    letter (str): The specific letter to count
                
                Returns:
                    int: The number of occurrences of the letter in the word
                """
                if not isinstance(word, str) or not isinstance(letter, str):
                    return 0
                
                if len(letter) != 1:
                    raise ValueError("The 'letter' parameter must be a single character")
                
                return word.lower().count(letter.lower())
            
            # Create agent with multiple tools using Nova Lite
            agent = Agent(
                tools=[calculator, current_time, letter_counter],
                model="amazon.nova-lite-v1:0"
            )
            print("✅ Created Strands Agent with calculator, current_time, and letter_counter tools (Nova Lite model)")
            print()
            
            # Test the agent with a multi-tool request (from the quickstart)
            print("1. Multi-Tool Request (from Strands quickstart):")
            message = """
            I have 3 requests:
            
            1. What is the time right now?
            2. Calculate 3111696 / 74088
            3. Tell me how many letter R's are in the word "strawberry" 🍓
            """
            
            print(f"   User: {message.strip()}")
            response = agent(message)
            print(f"   Agent: {response}")
            print()
            
        except Exception as e:
            print(f"⚠️  Error with real Strands agent tools: {e}")
            print("   Falling back to mock AWS agent demonstration...")
            _create_mock_aws_agent_demo()
    else:
        _create_mock_aws_agent_demo()


def _create_mock_aws_agent_demo():
    """Create mock AWS agent demonstration."""
    # Simulate an agent with AWS tools
    class AWSAgent:
        """Mock AWS-integrated agent."""
        
        def __init__(self):
            self.tools = ["s3_browser", "bedrock_chat", "ec2_manager"]
            self.name = "AWS AI Assistant"
        
        def __call__(self, message):
            if "s3" in message.lower():
                return "I can help you browse S3 buckets and manage data for your AI projects."
            elif "bedrock" in message.lower():
                return "I can assist with AWS Bedrock AI models for text generation and analysis."
            elif "ec2" in message.lower():
                return "I can help you manage EC2 instances for training and deploying AI models."
            else:
                return f"I'm an AWS AI assistant with access to tools: {', '.join(self.tools)}"
        
        def list_tools(self):
            return self.tools
    
    aws_agent = AWSAgent()
    print("🔧 Created Mock AWS Agent")
    print(f"   Available tools: {aws_agent.list_tools()}")
    
    print()
    
    # Tool-based interactions
    print("1. AWS Service Interactions:")
    aws_queries = [
        "Help me set up an S3 bucket for training data",
        "I want to use Bedrock for text generation",
        "Launch an EC2 instance for model training"
    ]
    
    for query in aws_queries:
        response = aws_agent(query)
        print(f"   User: {query}")
        print(f"   Agent: {response}")
        print()


def multi_agent_conversation():
    """Demonstrate multiple agents working together."""
    print("=== MULTI-AGENT CONVERSATION ===")
    print()
    
    # Create multiple specialized agents
    if STRANDS_AVAILABLE:
        data_agent = Agent()  # Specialized for data processing
        ml_agent = Agent()    # Specialized for ML models
        deploy_agent = Agent() # Specialized for deployment
        print("✅ Created specialized Strands agents")
    else:
        data_agent = MockAgent("Data Specialist", "Handles data processing and preparation")
        ml_agent = MockAgent("ML Engineer", "Manages model training and evaluation")
        deploy_agent = MockAgent("DevOps Engineer", "Handles deployment and infrastructure")
        print("🔧 Created Mock specialized agents")
    
    print()
    
    # Simulate a collaborative AI project workflow
    print("1. AI Project Workflow Collaboration:")
    
    # Data preparation phase
    data_task = "Process customer reviews dataset for sentiment analysis"
    data_response = data_agent(data_task)
    print(f"   Project Manager: {data_task}")
    print(f"   Data Specialist: {data_response}")
    print()
    
    # Model development phase
    ml_task = "Train a sentiment analysis model on the processed data"
    ml_response = ml_agent(ml_task)
    print(f"   Project Manager: {ml_task}")
    print(f"   ML Engineer: {ml_response}")
    print()
    
    # Deployment phase
    deploy_task = "Deploy the sentiment analysis model to AWS"
    deploy_response = deploy_agent(deploy_task)
    print(f"   Project Manager: {deploy_task}")
    print(f"   DevOps Engineer: {deploy_response}")
    print()


def agent_best_practices():
    """Demonstrate best practices for using Strands agents."""
    print("=== STRANDS AGENT BEST PRACTICES ===")
    print()
    
    print("1. AWS Bedrock Setup Requirements:")
    setup_steps = [
        "Configure AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)",
        "Enable Bedrock model access in AWS Console",
        "Request access to Claude 4 Sonnet model",
        "Verify region settings (default: us-east-1)",
        "Check IAM permissions for Bedrock:InvokeModel",
        "Test connectivity with simple Bedrock API calls"
    ]
    
    for i, step in enumerate(setup_steps, 1):
        print(f"   {i}. {step}")
    print()
    
    print("2. Agent Design Principles:")
    principles = [
        "Single Responsibility: Each agent should have a clear, focused purpose",
        "Tool Integration: Agents should leverage appropriate tools and APIs",
        "Error Handling: Implement robust error handling and fallback strategies",
        "Conversation Memory: Maintain context across interactions",
        "Security: Implement proper authentication and authorization",
        "Monitoring: Log interactions and monitor agent performance"
    ]
    
    for i, principle in enumerate(principles, 1):
        print(f"   {i}. {principle}")
    print()
    
    print("3. AI Engineering Use Cases:")
    use_cases = [
        "Data Pipeline Automation: Agents that manage ETL processes",
        "Model Training Orchestration: Agents that coordinate training workflows",
        "Deployment Management: Agents that handle CI/CD for ML models",
        "Monitoring and Alerting: Agents that watch system health",
        "User Support: Agents that help developers with AI tools",
        "Code Generation: Agents that assist with writing AI code"
    ]
    
    for i, use_case in enumerate(use_cases, 1):
        print(f"   {i}. {use_case}")
    print()


def practical_ai_engineering_example():
    """Practical example for AI engineering workflows."""
    print("=== PRACTICAL AI ENGINEERING WITH STRANDS ===")
    print()
    
    if STRANDS_AVAILABLE:
        ai_engineer = Agent()
        print("✅ Created AI Engineering Assistant")
    else:
        ai_engineer = MockAgent("AI Engineering Assistant", "Helps with end-to-end AI workflows")
        print("🔧 Created Mock AI Engineering Assistant")
    
    print()
    
    # Simulate a complete AI project workflow
    print("1. End-to-End AI Project Workflow:")
    
    workflow_steps = [
        "Help me plan a recommendation system for an e-commerce platform",
        "What data do I need to collect for training?",
        "Which AWS services should I use for this project?",
        "How do I set up the training pipeline?",
        "What's the best way to deploy and monitor the model?"
    ]
    
    for step in workflow_steps:
        response = ai_engineer(step)
        print(f"   Developer: {step}")
        print(f"   AI Assistant: {response}")
        print()


def main():
    """Main demonstration function."""
    print("🤖 STRANDS AGENTS FRAMEWORK DEMONSTRATION")
    print("=" * 50)
    print()
    
    if not STRANDS_AVAILABLE:
        print("📝 NOTE: This demonstration uses mock agents to show Strands concepts.")
        print("   Install the actual strands library for full functionality.")
        print()
    
    # Run all examples
    basic_agent_example()
    print("\n" + "="*60 + "\n")
    
    advanced_agent_features()
    print("\n" + "="*60 + "\n")
    
    agent_with_tools()
    print("\n" + "="*60 + "\n")
    
    multi_agent_conversation()
    print("\n" + "="*60 + "\n")
    
    agent_best_practices()
    print("\n" + "="*60 + "\n")
    
    practical_ai_engineering_example()
    
    print("=" * 60)
    print("SUMMARY: Strands Agents Framework")
    print("=" * 60)
    if STRANDS_AVAILABLE:
        print("✅ Strands library is available")
    else:
        print("⚠️  Strands library demonstration mode")
    print("✅ Basic agent creation and interaction")
    print("✅ Advanced agent features and customization")
    print("✅ Tool integration for AWS services")
    print("✅ Multi-agent collaboration patterns")
    print("✅ Best practices for AI engineering")
    print("✅ Practical AI project workflow examples")
    print()
    print("🎯 Next Steps:")
    print("   1. Install strands library: pip install strands")
    print("   2. Explore agent customization options")
    print("   3. Integrate with AWS services")
    print("   4. Build your first AI engineering agent!")


if __name__ == "__main__":
    main()

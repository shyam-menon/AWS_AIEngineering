#!/usr/bin/env python3
"""
Simple Strands Agent Example

This is a basic working example of the Strands Agents framework based on the 
official quickstart guide. This demonstrates the exact code from the documentation.

To run this example:
1. Ensure AWS credentials are configured
2. Ensure Bedrock model access is enabled
3. Run: python simple_strands_example.py

Author: AWS AI Engineering Course
Date: August 2025
"""

try:
    from strands import Agent, tool
    from strands_tools import calculator, current_time
    
    print("✅ Strands Agents library is available!")
    print("🔧 Creating a simple agent with tools...")
    
    # Define a custom tool as a Python function using the @tool decorator
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
    
    # Create an agent with tools from the community-driven strands-tools package
    # as well as our custom letter_counter tool, using Amazon Nova Lite model
    agent = Agent(
        tools=[calculator, current_time, letter_counter],
        model="amazon.nova-lite-v1:0"
    )
    
    print("✅ Agent created successfully with Amazon Nova Lite!")
    print("🤖 Agent has access to:")
    print("   - Calculator (from strands-tools)")
    print("   - Current time (from strands-tools)")
    print("   - Letter counter (custom tool)")
    print("   - Model: Amazon Nova Lite (amazon.nova-lite-v1:0)")
    print()
    
    # Ask the agent a question that uses the available tools
    print("📝 Sending request to agent...")
    message = """
    I have 3 requests:
    
    1. What is the time right now?
    2. Calculate 3111696 / 74088
    3. Tell me how many letter R's are in the word "strawberry" 🍓
    """
    
    print("User:", message.strip())
    print("\n" + "="*50)
    print("Agent Response:")
    print("="*50)
    
    result = agent(message)
    
    print("\n" + "="*50)
    print("✅ Agent completed successfully!")
    
except ImportError as e:
    print("❌ Strands Agents library not available.")
    print(f"   Error: {e}")
    print("   Please install with: pip install strands-agents strands-agents-tools")
    
except Exception as e:
    print(f"❌ Error running Strands agent: {e}")
    print("\n🔧 Troubleshooting:")
    print("   1. Check AWS credentials are configured")
    print("   2. Ensure Bedrock model access is enabled")
    print("   3. Verify network connectivity")
    print("   4. Check AWS region settings")
    
    print(f"\n📋 Error details: {type(e).__name__}: {e}")

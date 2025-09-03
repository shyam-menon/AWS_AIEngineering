#!/usr/bin/env python3
"""
Simple Tool-Augmented Agent with Strands

This example demonstrates how to create a simple agent that can use various tools
to perform tasks beyond text generation. The agent can:
- Perform mathematical calculations
- Get current time and date
- Read files
- Count characters in text (custom tool)
- Process text in various ways (custom tool)

This showcases the power of tool-augmented agents in the Strands framework.
Note: This version is Windows-compatible (shell tool excluded).
"""

import logging
from typing import Dict, Any
from strands import Agent, tool
from strands_tools import calculator, current_time, file_read

# Note: shell tool is not compatible with Windows, so we exclude it

# Configure logging for better visibility
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@tool
def character_counter(text: str) -> str:
    """
    Count various types of characters in a given text.
    
    Args:
        text (str): The text to analyze
        
    Returns:
        str: A detailed breakdown of character counts
    """
    if not isinstance(text, str):
        return "Error: Input must be a string"
    
    # Count different types of characters
    total_chars = len(text)
    letters = sum(c.isalpha() for c in text)
    digits = sum(c.isdigit() for c in text)
    spaces = sum(c.isspace() for c in text)
    punctuation = sum(not c.isalnum() and not c.isspace() for c in text)
    
    # Build the result string
    result = f"Character Analysis for: '{text}'\n"
    result += f"📊 Total characters: {total_chars}\n"
    result += f"🔤 Letters: {letters}\n"
    result += f"🔢 Digits: {digits}\n"
    result += f"⬜ Spaces: {spaces}\n"
    result += f"❗ Punctuation: {punctuation}"
    
    return result


@tool
def text_processor(text: str, operation: str = "uppercase") -> str:
    """
    Process text in various ways.
    
    Args:
        text (str): The text to process
        operation (str): The operation to perform (uppercase, lowercase, reverse, title)
        
    Returns:
        str: The processed text
    """
    if not isinstance(text, str):
        return "Error: Input must be a string"
    
    operations = {
        "uppercase": text.upper(),
        "lowercase": text.lower(),
        "reverse": text[::-1],
        "title": text.title(),
        "length": f"Text length: {len(text)} characters"
    }
    
    if operation not in operations:
        return f"Error: Unknown operation '{operation}'. Available: {', '.join(operations.keys())}"
    
    return f"Operation '{operation}' result: {operations[operation]}"


class SimpleToolAgent:
    """
    A simple tool-augmented agent that demonstrates the power of combining
    LLMs with various tools for enhanced capabilities.
    """
    
    def __init__(self):
        """Initialize the agent with various tools."""
        logger.info("🚀 Initializing Simple Tool-Augmented Agent...")
        
        # Create the agent with built-in and custom tools
        # Using Amazon Nova Lite model which is available in your AWS account
        self.agent = Agent(
            model="us.amazon.nova-lite-v1:0",  # Use Nova Lite model
            tools=[
                calculator,           # Built-in: Mathematical calculations
                current_time,         # Built-in: Current date and time
                file_read,           # Built-in: Read file contents
                # shell,             # Built-in: Execute shell commands (not compatible with Windows)
                character_counter,   # Custom: Character analysis
                text_processor       # Custom: Text processing
            ],
            system_prompt="""You are a helpful assistant with access to various tools. 
            You can perform calculations, get the current time, read files,
            analyze text, and process text in various ways. Always use the appropriate tool 
            when needed and explain what you're doing."""
        )
        
        logger.info("✅ Agent initialized successfully!")
        logger.info(f"🔧 Available tools: {self.agent.tool_names}")
    
    def demonstrate_capabilities(self):
        """Demonstrate the agent's capabilities with various example queries."""
        
        demo_queries = [
            {
                "description": "Mathematical Calculation",
                "query": "What is the square root of 144 plus 25% of 200?",
                "emoji": "🧮"
            },
            {
                "description": "Current Time",
                "query": "What time is it right now?",
                "emoji": "🕐"
            },
            {
                "description": "Text Analysis",
                "query": "Analyze the characters in the text 'Hello, World! 123'",
                "emoji": "📝"
            },
            {
                "description": "Text Processing",
                "query": "Convert the text 'artificial intelligence' to uppercase",
                "emoji": "🔤"
            },
            {
                "description": "Complex Multi-Tool Query",
                "query": """I need you to:
                1. Calculate 15 * 8 + 32
                2. Get the current time
                3. Analyze the character count in 'AI Engineering 2025!'
                4. Convert 'strands agents' to title case
                Please do all of these tasks.""",
                "emoji": "🔧"
            }
        ]
        
        print("\n" + "="*70)
        print("🤖 SIMPLE TOOL-AUGMENTED AGENT DEMONSTRATION")
        print("="*70)
        
        for i, demo in enumerate(demo_queries, 1):
            print(f"\n{demo['emoji']} Demo {i}: {demo['description']}")
            print("-" * 50)
            print(f"❓ Query: {demo['query']}")
            print("\n🤖 Agent Response:")
            
            try:
                response = self.agent(demo['query'])
                print(response)
            except Exception as e:
                logger.error(f"Error in demo {i}: {e}")
                print(f"❌ Error: {e}")
            
            print("\n" + "."*50)
    
    def interactive_mode(self):
        """Run the agent in interactive mode."""
        print("\n" + "="*70)
        print("🎯 INTERACTIVE MODE - Chat with the Tool-Augmented Agent")
        print("="*70)
        print("💡 Try queries like:")
        print("   • 'Calculate 25 * 16 / 4'")
        print("   • 'What time is it?'")
        print("   • 'Count characters in Hello World'")
        print("   • 'Convert my name to uppercase'")
        print("   • Type 'quit' to exit")
        print("-" * 70)
        
        while True:
            try:
                user_input = input("\n🗣️  You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("👋 Goodbye! Thanks for trying the tool-augmented agent!")
                    break
                
                if not user_input:
                    print("📝 Please enter a query or 'quit' to exit.")
                    continue
                
                print("🤖 Agent: ", end="")
                response = self.agent(user_input)
                print(response)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Thanks for trying the tool-augmented agent!")
                break
            except Exception as e:
                logger.error(f"Error in interactive mode: {e}")
                print(f"❌ Sorry, I encountered an error: {e}")
    
    def get_tool_info(self) -> Dict[str, Any]:
        """Get information about available tools."""
        return {
            "tool_names": self.agent.tool_names,
            "agent_info": {
                "model": str(self.agent.model),
                "system_prompt": self.agent.system_prompt
            }
        }


def main():
    """Main function to run the simple tool-augmented agent demo."""
    
    print("🔧 Simple Tool-Augmented Agent with Strands")
    print("=" * 50)
    
    try:
        # Initialize the agent
        agent = SimpleToolAgent()
        
        # Show tool information
        tool_info = agent.get_tool_info()
        print(f"\n📋 Tool Information:")
        print(f"🔧 Available Tools: {', '.join(tool_info['tool_names'])}")
        
        # Run demonstrations
        agent.demonstrate_capabilities()
        
        # Ask user if they want to try interactive mode
        print("\n" + "="*70)
        try_interactive = input("🎮 Would you like to try interactive mode? (y/n): ").strip().lower()
        
        if try_interactive in ['y', 'yes']:
            agent.interactive_mode()
        else:
            print("👍 Demo completed! You can run this script again to try interactive mode.")
            
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"❌ Fatal error: {e}")
        print("🔧 Please check your Strands installation and try again.")


if __name__ == "__main__":
    main()

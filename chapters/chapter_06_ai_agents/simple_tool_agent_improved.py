#!/usr/bin/env python3
"""
Simple Tool-Augmented Agent with Strands - Improved Version

This improved example demonstrates better tool usage patterns and shows
how to encourage the agent to use custom tools effectively.
"""

import logging
from typing import Dict, Any
from strands import Agent, tool
from strands_tools import calculator, current_time, file_read

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
    Use this tool when asked to analyze character counts or breakdown text composition.
    
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
    Process text in various ways. Use this tool for text transformations.
    
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


class ImprovedToolAgent:
    """
    An improved tool-augmented agent with better tool usage patterns.
    """
    
    def __init__(self):
        """Initialize the agent with tools and improved prompting."""
        logger.info("🚀 Initializing Improved Tool-Augmented Agent...")
        
        # Enhanced system prompt that encourages tool usage
        system_prompt = """You are a helpful assistant with access to powerful tools. 
        IMPORTANT: Always use the appropriate tools when available instead of doing tasks manually.
        
        Available tools:
        - calculator: Use for ALL mathematical calculations
        - current_time: Use to get the current date and time
        - file_read: Use to read file contents
        - character_counter: Use to analyze character counts in text
        - text_processor: Use to transform text (uppercase, lowercase, reverse, title case)
        
        When a user asks for text analysis, character counting, or text processing, 
        ALWAYS use the appropriate tool rather than doing it manually."""
        
        self.agent = Agent(
            model="us.amazon.nova-lite-v1:0",
            tools=[
                calculator,
                current_time,
                file_read,
                character_counter,
                text_processor
            ],
            system_prompt=system_prompt
        )
        
        logger.info("✅ Agent initialized successfully!")
        logger.info(f"🔧 Available tools: {self.agent.tool_names}")
    
    def demonstrate_focused_examples(self):
        """Demonstrate specific tool usage with focused examples."""
        
        examples = [
            {
                "name": "Calculator Tool",
                "query": "Use the calculator to compute 15 * 8 + 32",
                "emoji": "🧮"
            },
            {
                "name": "Current Time Tool",
                "query": "Please use the current_time tool to tell me what time it is",
                "emoji": "🕐"
            },
            {
                "name": "Character Counter Tool",
                "query": "Use the character_counter tool to analyze 'Hello, World! 123'",
                "emoji": "📝"
            },
            {
                "name": "Text Processor Tool",
                "query": "Use the text_processor to convert 'artificial intelligence' to uppercase",
                "emoji": "🔤"
            },
            {
                "name": "Multi-Tool Workflow",
                "query": """Please perform these tasks using the appropriate tools:
                1. Calculate 25 * 4
                2. Get the current time
                3. Count characters in 'Strands AI'
                4. Convert 'hello world' to title case""",
                "emoji": "🔧"
            }
        ]
        
        print("\n" + "="*70)
        print("🤖 IMPROVED TOOL-AUGMENTED AGENT DEMONSTRATION")
        print("="*70)
        
        for i, example in enumerate(examples, 1):
            print(f"\n{example['emoji']} Example {i}: {example['name']}")
            print("-" * 50)
            print(f"❓ Query: {example['query']}")
            print("\n🤖 Agent Response:")
            
            try:
                response = self.agent(example['query'])
                print(response)
            except Exception as e:
                logger.error(f"Error in example {i}: {e}")
                print(f"❌ Error: {e}")
            
            print("\n" + "."*50)
    
    def interactive_mode(self):
        """Run the agent in interactive mode with tool usage hints."""
        print("\n" + "="*70)
        print("🎯 INTERACTIVE MODE - Enhanced Tool Usage")
        print("="*70)
        print("💡 Try these tool-specific queries:")
        print("   • 'Use calculator for 50 / 2'")
        print("   • 'Get current time'")
        print("   • 'Count characters in my text'")
        print("   • 'Convert text to uppercase'")
        print("   • Type 'quit' to exit")
        print("-" * 70)
        
        while True:
            try:
                user_input = input("\n🗣️  You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("👋 Goodbye! Thanks for trying the improved tool agent!")
                    break
                
                if not user_input:
                    print("📝 Please enter a query or 'quit' to exit.")
                    continue
                
                print("🤖 Agent: ", end="")
                response = self.agent(user_input)
                print(response)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                logger.error(f"Error in interactive mode: {e}")
                print(f"❌ Sorry, I encountered an error: {e}")


def main():
    """Main function to run the improved tool agent demo."""
    
    print("🔧 Improved Simple Tool-Augmented Agent with Strands")
    print("=" * 55)
    
    try:
        # Initialize the agent
        agent = ImprovedToolAgent()
        
        # Run focused demonstrations
        agent.demonstrate_focused_examples()
        
        # Ask user if they want to try interactive mode
        print("\n" + "="*70)
        try_interactive = input("🎮 Would you like to try interactive mode? (y/n): ").strip().lower()
        
        if try_interactive in ['y', 'yes']:
            agent.interactive_mode()
        else:
            print("👍 Demo completed! Run with interactive mode to explore more.")
            
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"❌ Fatal error: {e}")


if __name__ == "__main__":
    main()

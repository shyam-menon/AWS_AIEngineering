"""
Local Strands Agent for experimentation and development.
This version runs locally without AgentCore Runtime integration.
"""

from strands import Agent, tool
from strands_tools import calculator
import argparse
import json
from strands.models import BedrockModel


# Create a custom weather tool
@tool
def weather():
    """Get current weather information"""
    # Dummy implementation for demonstration
    return "sunny with 72°F temperature"


def create_agent():
    """Create and configure the Strands agent"""
    model_id = "us.amazon.nova-lite-v1:0"
    model = BedrockModel(model_id=model_id)
    
    agent = Agent(
        model=model,
        tools=[calculator, weather],
        system_prompt="You're a helpful assistant. You can do simple math calculations and tell the weather."
    )
    
    return agent


def run_agent_locally(payload):
    """
    Run the agent locally with a given payload
    
    Args:
        payload (dict): Input payload containing the user prompt
        
    Returns:
        str: Agent's response
    """
    agent = create_agent()
    user_input = payload.get("prompt", "Hello!")
    print(f"User input: {user_input}")
    
    response = agent(user_input)
    return response.message['content'][0]['text']


if __name__ == "__main__":
    # Command-line interface for testing
    parser = argparse.ArgumentParser(description="Run Strands Agent locally")
    parser.add_argument("payload", type=str, help="JSON payload with user prompt")
    args = parser.parse_args()
    
    try:
        payload = json.loads(args.payload)
        result = run_agent_locally(payload)
        print(f"Agent response: {result}")
    except json.JSONDecodeError:
        print("Error: Invalid JSON payload")
    except Exception as e:
        print(f"Error: {e}")

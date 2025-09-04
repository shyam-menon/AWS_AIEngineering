"""
AgentCore Runtime ready Strands Agent - Production Version
This version is optimized for deployment to AWS Bedrock AgentCore Runtime.
"""

from strands import Agent, tool
from strands_tools import calculator
import json
import os
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands.models import BedrockModel

# Initialize the AgentCore Runtime App
app = BedrockAgentCoreApp()


# Create a custom weather tool
@tool
def weather():
    """Get current weather information"""
    # Mock weather data for demonstration
    return "sunny with 72°F temperature"


# Initialize the agent (this happens once when the container starts)
print("🚀 Initializing Strands Agent with Nova Lite...")
model_id = "us.amazon.nova-lite-v1:0"
model = BedrockModel(model_id=model_id)

agent = Agent(
    model=model,
    tools=[calculator, weather],
    system_prompt="You're a helpful assistant. You can do simple math calculations and tell the weather."
)
print("✅ Agent initialized successfully")


@app.entrypoint
def strands_agent_bedrock(payload):
    """
    Main entrypoint for AgentCore Runtime.
    This function will be called for each agent invocation.
    
    Args:
        payload (dict): Input payload from AgentCore Runtime
        
    Returns:
        str: Agent's response
    """
    try:
        user_input = payload.get("prompt", "Hello!")
        print(f"📥 User input: {user_input}")
        
        response = agent(user_input)
        agent_response = response.message['content'][0]['text']
        
        print(f"📤 Agent response: {agent_response}")
        return agent_response
        
    except Exception as e:
        error_msg = f"Error processing request: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg


if __name__ == "__main__":
    # When deployed to AgentCore Runtime, this starts the HTTP server
    print("🌟 Starting AgentCore Runtime...")
    app.run()

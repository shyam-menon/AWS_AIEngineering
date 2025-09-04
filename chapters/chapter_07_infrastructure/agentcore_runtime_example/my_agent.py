from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent
from strands.models import BedrockModel

app = BedrockAgentCoreApp()
# Create Nova Lite model and pass it to the agent
nova_lite_model = BedrockModel(model_id="us.amazon.nova-lite-v1:0")
agent = Agent(model=nova_lite_model)

@app.entrypoint
def invoke(payload):
    """Your AI agent function"""
    user_message = payload.get("query", payload.get("prompt", "Hello! How can I help you today?"))
    result = agent(user_message)
    return {"result": result.message}

if __name__ == "__main__":
    app.run()

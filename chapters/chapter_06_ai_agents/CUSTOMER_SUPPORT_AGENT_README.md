# Customer Support Agent with Intent Classification and Human Handoff

This example demonstrates a sophisticated customer support workflow using Strands Agents that combines AI automation with intelligent human escalation. The agent processes customer queries through multiple analysis stages to provide appropriate responses or escalate to human agents when needed.

## 🎯 System Overview

The customer support agent implements a multi-stage workflow that analyzes customer queries and routes them appropriately:

```
Customer Query → Intent Classification → Knowledge Lookup + Escalation Check → Human Handoff OR Response Generation
```

## 🧠 Workflow Components

### 1. Intent Classification Tool
- **Model**: Amazon Nova Lite (amazon.nova-lite-v1:0)
- **Function**: Analyzes customer queries for intent, emotion, and urgency
- **Output**: Structured classification with escalation triggers

**Example Output:**
```json
{
  "intent": "RETURNS_REFUNDS",
  "confidence": 0.98,
  "reasoning": "Customer explicitly requesting money back with negative product feedback",
  "urgency": "high",
  "customer_emotion": "angry",
  "key_phrases": ["garbage", "money back", "NOW!"],
  "escalation_triggers": ["negative_product_language", "immediate_demand"]
}
```

### 2. Knowledge Lookup Tool
- **Function**: Mock implementation of AWS Bedrock Knowledge Base
- **Purpose**: Retrieves relevant policies, procedures, and articles
- **Input**: Intent classification data
- **Output**: Contextual knowledge for response generation

**Example Output:**
```json
{
  "relevant_articles": ["30-day return policy", "Refund processing procedures"],
  "procedures": ["Verify purchase date", "Process refund request"],
  "policies": "Full refund available within 30 days of purchase for any reason",
  "escalation_triggers": ["Customer expressing extreme dissatisfaction"]
}
```

### 3. Escalation Check Tool
- **Function**: Evaluates whether human intervention is needed
- **Criteria**: Customer emotion, urgency level, intent complexity, escalation triggers
- **Scoring**: Weighted algorithm determines escalation necessity

**Escalation Triggers:**
- 😡 Angry/frustrated customer emotion
- ⚡ High urgency requests  
- 💰 Financial issues (refunds, billing disputes)
- 🔄 Repeat complaints
- 🗣️ Negative product language

**Example Output:**
```json
{
  "escalate": true,
  "escalation_reason": "Customer expressing anger with immediate refund demand",
  "priority_level": "high", 
  "suggested_department": "management",
  "customer_context": "Angry customer demanding immediate refund, requires empathetic handling"
}
```

### 4. Human Handoff Tool  
- **Function**: Prepares comprehensive context package for human agents
- **Integration**: Uses `handoff_to_user` from strands-tools
- **Content**: Complete analysis, suggested actions, customer context

**Handoff Package:**
```json
{
  "handoff_message": "🚨 HIGH PRIORITY - Customer expressing anger with immediate refund demand",
  "customer_summary": "Customer is very upset about product quality, needs empathetic handling",
  "priority": "high",
  "department": "management", 
  "recommended_actions": ["Empathetic response", "Immediate refund processing"]
}
```

### 5. Response Generation Tool
- **Function**: Creates contextual responses for non-escalated queries
- **Adaptation**: Tone and content adjust based on customer emotion
- **Fallback**: Generates holding responses even for escalated cases

## 📋 Test Scenarios

### Scenario 1: Angry Customer (Escalation Path)
**Input**: *"This product is complete garbage! I want my money back RIGHT NOW!"*

**Expected Flow:**
1. 🎯 Intent: RETURNS_REFUNDS, Emotion: angry, Urgency: high
2. 📚 Knowledge: Return policies and procedures retrieved
3. 🚨 Escalation: YES - Score 7/10 (angry + high urgency + negative language)
4. 👥 Handoff: Prepared for management team with full context
5. 🤖 Result: Human agent receives priority escalation with empathy guidance

### Scenario 2: Polite Inquiry (Automated Path)  
**Input**: *"Hi, I purchased a product last week but it's not quite what I expected. Could you help me understand your return policy?"*

**Expected Flow:**
1. 🎯 Intent: RETURNS_REFUNDS, Emotion: neutral, Urgency: low
2. 📚 Knowledge: Return policies retrieved  
3. ✅ Escalation: NO - Score 2/10 (neutral emotion, standard request)
4. 💬 Response: Automated friendly response with policy details
5. 🤖 Result: Customer receives immediate helpful response

### Scenario 3: Urgent Technical Issue (Escalation Path)
**Input**: *"My device stopped working completely and I need it for an important presentation tomorrow morning. This is very urgent!"*

**Expected Flow:**
1. 🎯 Intent: TECHNICAL_SUPPORT, Emotion: concerned, Urgency: high
2. 📚 Knowledge: Technical support procedures retrieved
3. 🚨 Escalation: YES - Score 5/10 (high urgency + technical complexity)  
4. 👥 Handoff: Prepared for technical specialists
5. 🤖 Result: Customer routed to expert technical support

## 🛠️ Setup and Installation

### Prerequisites
```bash
# Install required packages
pip install strands-agents strands-agents-tools boto3

# AWS Configuration
aws configure  # Set up AWS credentials and region
```

### AWS Bedrock Setup
1. **Enable Model Access**: In AWS Console → Bedrock → Model Access
2. **Request Access**: Enable `amazon.nova-lite-v1:0` model
3. **Verify Region**: Ensure using supported region (us-east-1 recommended)

### Running the Example
```bash
cd chapters/chapter_06_ai_agents
python customer_support_agent.py
```

## 🔧 Configuration Options

### Model Configuration
```python
# Change the LLM model (must be enabled in Bedrock)
agent = Agent(
    model="amazon.nova-lite-v1:0",  # or another available model
    tools=[...],
    instructions="..."
)
```

### Escalation Thresholds
```python
# Adjust escalation scoring in check_escalation_needed tool
escalation_score >= 4  # Default threshold
# Lower number = more escalations
# Higher number = fewer escalations  
```

### Knowledge Base Integration
Replace the mock `lookup_knowledge_base` tool with real AWS Bedrock Knowledge Base:

```python
@tool
def lookup_knowledge_base(intent_data: Dict[str, Any]) -> Dict[str, Any]:
    # Real implementation would use:
    # bedrock_agent_client = boto3.client('bedrock-agent-runtime')
    # response = bedrock_agent_client.retrieve(...)
    pass
```

## 📊 Monitoring and Analytics

### Key Metrics to Track
- **Escalation Rate**: Percentage of queries escalated to humans
- **Intent Accuracy**: Confidence scores from intent classification  
- **Resolution Time**: Time from query to resolution
- **Customer Satisfaction**: Follow-up survey results
- **Cost per Query**: AWS Bedrock usage costs

### Logging Integration
```python
import logging

# Add to each tool for comprehensive logging
logging.info(f"Intent classified: {intent} with confidence {confidence}")
```

## 🔐 Security Considerations

### Data Privacy
- **PII Handling**: Ensure customer data is properly anonymized
- **Audit Trail**: Log all escalations and handoffs
- **Access Control**: Restrict knowledge base access appropriately

### AWS Security
- **IAM Roles**: Use least-privilege access for Bedrock
- **Encryption**: Enable encryption in transit and at rest
- **VPC**: Consider VPC endpoints for enhanced security

## 🚀 Production Deployment

### Scalability Considerations
- **API Rate Limits**: Monitor Bedrock API quotas
- **Concurrent Requests**: Handle multiple customer queries
- **Error Handling**: Robust fallback mechanisms
- **Caching**: Cache knowledge base results for performance

### Integration Points
- **CRM Integration**: Connect with customer database
- **Ticketing Systems**: Automatic ticket creation for escalations  
- **Analytics Dashboard**: Real-time monitoring of agent performance
- **Notification Systems**: Alert human agents of escalations

## 📚 Further Reading

- **Strands Agents Documentation**: [https://strandsagents.com/latest/documentation/](https://strandsagents.com/latest/documentation/)
- **AWS Bedrock User Guide**: [https://docs.aws.amazon.com/bedrock/](https://docs.aws.amazon.com/bedrock/)
- **Human-in-the-Loop Patterns**: [Strands Community Tools](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/tools/community-tools-package/?h=human#human-in-the-loop-with-handoff_to_user)

## 🤝 Contributing

To extend this example:
1. **Add New Intents**: Expand the intent classification categories
2. **Enhance Knowledge Base**: Add more sophisticated knowledge retrieval
3. **Improve Escalation Logic**: Refine escalation criteria  
4. **Add Analytics**: Implement comprehensive monitoring
5. **Multi-Channel Support**: Extend to handle email, chat, voice

---

This example demonstrates production-ready patterns for building intelligent customer support systems that balance automation efficiency with human empathy when needed.

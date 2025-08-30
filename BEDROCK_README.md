# AWS Bedrock LLM Applications

A collection of Python applications to interact with Large Language Models (LLMs) using AWS Bedrock service.

## Overview

This repository contains several Python scripts that demonstrate different ways to interact with AWS Bedrock foundation models:

1. **`bedrock_simple.py`** - Simple, beginner-friendly script for testing Claude 3 Haiku
2. **`bedrock_llm.py`** - Full-featured CLI application supporting multiple models
3. **`bedrock_conversation.py`** - Advanced conversation patterns and multi-turn chat
4. **`bedrock_manager.py`** - Utility to manage and check model access status

## Supported Models

- **Anthropic Claude 3 Haiku** - Fast and cost-effective
- **Anthropic Claude 3 Sonnet** - Balanced performance
- **Amazon Titan Text Express** - Amazon's foundation model
- **Meta Llama 2 13B Chat** - Conversational AI
- **Mistral 7B Instruct** - Open-source instruction model

## Prerequisites

### 1. AWS Account Setup
- AWS account with Bedrock access
- Models enabled in AWS Bedrock console (see setup guide below)

### 2. AWS Credentials
Configure AWS credentials using one of these methods:
```bash
# Method 1: AWS CLI
aws configure

# Method 2: Environment variables
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=us-east-1

# Method 3: Windows PowerShell
$env:AWS_ACCESS_KEY_ID="your_key"
$env:AWS_SECRET_ACCESS_KEY="your_secret"
$env:AWS_DEFAULT_REGION="us-east-1"
```

### 3. Required IAM Permissions
Your AWS user/role needs these permissions:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:ListFoundationModels",
                "bedrock:GetFoundationModel"
            ],
            "Resource": "*"
        }
    ]
}
```

## Quick Setup Guide

### Step 1: Enable Models in AWS Console
1. Go to [AWS Bedrock Console](https://console.aws.amazon.com/bedrock/)
2. Navigate to **"Model access"** in the left sidebar
3. Click **"Enable specific models"**
4. Request access to these recommended models:
   - Claude 3 Haiku
   - Claude 3 Sonnet  
   - Amazon Titan Text Express
5. Submit requests (usually approved instantly)

### Step 2: Install Dependencies
```bash
pip install boto3
```

### Step 3: Test Your Setup
```bash
# Check model access status
python bedrock_manager.py

# Simple test with Claude
python bedrock_simple.py
```

## Usage Examples

### 1. Simple Script (`bedrock_simple.py`)
Perfect for beginners and quick testing:
```bash
python bedrock_simple.py
```
- Runs example prompts automatically
- Includes interactive mode for custom questions

### 2. Full CLI Application (`bedrock_llm.py`)
Advanced usage with command-line options:

```bash
# Basic usage with Claude Haiku (default)
python bedrock_llm.py --prompt "Explain quantum computing"

# Use different model
python bedrock_llm.py --model claude-sonnet --prompt "Write a poem about AI"

# Interactive mode
python bedrock_llm.py --interactive

# List available models
python bedrock_llm.py --list-models

# Specify region and token limit
python bedrock_llm.py --region us-west-2 --max-tokens 500 --prompt "Your question"
```

### 3. Conversation Examples (`bedrock_conversation.py`)
Demonstrates advanced patterns:
```bash
python bedrock_conversation.py
```
Includes demos for:
- Multi-turn conversations with context
- System prompts for role-playing
- Model comparisons
- Creative writing examples

### 4. Model Manager (`bedrock_manager.py`)
Check model status and access:
```bash
python bedrock_manager.py
```
Shows:
- All available models in your region
- Access status for each model
- Setup instructions

## Command-Line Options (bedrock_llm.py)

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--model` | `-m` | Model to use | `claude-haiku` |
| `--prompt` | `-p` | Text prompt to send | None |
| `--max-tokens` | `-t` | Maximum tokens to generate | `1000` |
| `--region` | `-r` | AWS region | `us-east-1` |
| `--list-models` | `-l` | List available models | False |
| `--interactive` | `-i` | Interactive chat mode | False |

### Model Options:
- `claude-haiku` - Claude 3 Haiku (fast, cost-effective)
- `claude-sonnet` - Claude 3 Sonnet (balanced performance)
- `titan` - Amazon Titan Text Express
- `llama2` - Meta Llama 2 13B Chat
- `mistral` - Mistral 7B Instruct

## Example Use Cases

### 1. Content Creation
```bash
python bedrock_llm.py --model claude-sonnet --prompt "Write a blog post about sustainable technology"
```

### 2. Code Assistance
```bash
python bedrock_llm.py --prompt "Write a Python function to parse JSON and handle errors"
```

### 3. Research and Analysis
```bash
python bedrock_llm.py --model claude-sonnet --max-tokens 2000 --prompt "Compare renewable energy sources"
```

### 4. Creative Writing
```bash
python bedrock_llm.py --interactive
# Then engage in creative writing conversation
```

## Troubleshooting

### Common Issues

**1. "Access denied" or "Model not enabled"**
- Go to AWS Bedrock console → Model access
- Enable the specific models you want to use
- Wait for approval (usually instant)

**2. "No credentials found"**
- Run `aws configure` to set up credentials
- Or set environment variables as shown above

**3. "Region not supported"**
- Bedrock is available in limited regions
- Try `us-east-1`, `us-west-2`, or `eu-west-1`

**4. "Model not found"**
- Check available models with: `python bedrock_manager.py`
- Some models may not be available in all regions

**5. High costs**
- Start with Claude 3 Haiku (most cost-effective)
- Use `--max-tokens` to limit response length
- Monitor usage in AWS Billing console

### Error Codes
- `AccessDeniedException` - Model not enabled in your account
- `ResourceNotFoundException` - Model not available in region
- `ValidationException` - Invalid request format
- `ThrottlingException` - Rate limit exceeded

## Cost Optimization Tips

1. **Start with Claude 3 Haiku** - Most cost-effective option
2. **Set reasonable token limits** - Use `--max-tokens` parameter
3. **Use specific prompts** - Clear prompts get better results faster
4. **Monitor usage** - Check AWS Billing dashboard regularly

## Model Comparison

| Model | Speed | Cost | Use Cases |
|-------|-------|------|-----------|
| Claude 3 Haiku | ⚡⚡⚡ | 💰 | Q&A, simple tasks, high volume |
| Claude 3 Sonnet | ⚡⚡ | 💰💰 | Analysis, research, complex tasks |
| Amazon Titan | ⚡⚡ | 💰 | Summarization, general text |
| Llama 2 Chat | ⚡ | 💰💰 | Conversations, dialogue |
| Mistral 7B | ⚡⚡ | 💰 | Instructions, code generation |

## Advanced Features

### System Prompts
Control model behavior with system prompts:
```python
# In bedrock_conversation.py
system_prompt = "You are a Python expert. Provide code examples."
response = conv.chat_with_claude("How to handle exceptions?", system_prompt)
```

### Multi-turn Conversations
Maintain context across multiple exchanges:
```python
# Conversation history is automatically maintained
conv = BedrockConversation()
conv.chat_with_claude("I'm building a web app")
conv.chat_with_claude("What database should I use?")  # Remembers context
```

### Model Comparison
Compare responses from different models:
```python
results = conv.compare_models("Explain machine learning")
# Returns responses from multiple models
```

## Integration Examples

### Web API Integration
```python
from flask import Flask, request, jsonify
from bedrock_simple import invoke_claude_simple

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    prompt = request.json['prompt']
    response = invoke_claude_simple(prompt)
    return jsonify({'response': response})
```

### Batch Processing
```python
import csv
from bedrock_llm import BedrockLLMClient

client = BedrockLLMClient()
results = []

with open('prompts.csv', 'r') as file:
    for row in csv.reader(file):
        response = client.invoke_claude_3_haiku(row[0])
        results.append(response)
```

## Security Best Practices

1. **Use IAM roles** instead of access keys when possible
2. **Limit permissions** to only required Bedrock actions
3. **Rotate credentials** regularly
4. **Monitor usage** through CloudTrail and billing alerts
5. **Don't commit credentials** to version control

## Resources

- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Bedrock API Reference](https://docs.aws.amazon.com/bedrock/latest/APIReference/)
- [Model Pricing](https://aws.amazon.com/bedrock/pricing/)
- [Supported Regions](https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-regions.html)

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve these applications.

## License

This project is open source and available under the MIT License.

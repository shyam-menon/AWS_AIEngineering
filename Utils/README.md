# AI Usage and Billing Utilities

This folder contains utilities to help you monitor and track your AWS costs

## Overview

Managing costs when experimenting with AI models is crucial, especially in educational environments. These utilities help you:

- **Track token usage in real-time** during your coding sessions
- **Monitor costs** for different AI models
- **Analyze historical usage** patterns
- **Get billing insights** from AWS Cost Explorer
- **Set up cost alerts** and optimization recommendations

## Files in this Directory

### 1. `ai_usage_monitor.py` - Comprehensive AI Usage Monitor
A comprehensive monitoring tool that integrates with AWS CloudWatch and Cost Explorer to provide detailed analytics about your AI usage specifically.

**Features:**
- CloudWatch metrics retrieval for Bedrock usage
- Cost calculation based on current AWS pricing
- AWS billing data integration
- Detailed usage reports with recommendations
- Support for multiple models and regions

**Usage:**
```bash
# Basic usage report for last 7 days
python ai_usage_monitor.py --days 7

# Detailed analysis with billing data
python ai_usage_monitor.py --days 30 --detailed

# Specific region analysis
python ai_usage_monitor.py --region us-west-2 --days 14
```

### 2. `aws_billing_monitor.py` - Comprehensive AWS Billing Monitor
A complete AWS billing monitor that tracks costs across ALL AWS services including Bedrock, EC2, S3, AgentCore, CloudWatch, and any other services you use.

**Features:**
- Complete AWS cost analysis across all services
- EC2 instance details and costs
- S3 bucket usage and storage costs
- Bedrock model usage and costs
- Monthly forecasting and projections
- Cost optimization recommendations
- Service-specific usage details

**Usage:**
```bash
# Comprehensive 30-day analysis
python aws_billing_monitor.py --days 30

# Quick summary for last 7 days
python aws_billing_monitor.py --days 7 --quiet

# Export detailed report to JSON
python aws_billing_monitor.py --days 30 --export
```

### 3. `aws_cost_dashboard.py` - Quick Cost Dashboard
A simple dashboard utility for daily cost monitoring and alerts.

**Features:**
- Real-time cost overview
- Month-to-date and daily costs
- Resource counts (EC2, S3, etc.)
- Cost alerts and recommendations
- Daily snapshots for tracking

**Usage:**
```bash
# Quick cost overview
python aws_cost_dashboard.py

# Continuous monitoring mode (updates every 5 minutes)
python aws_cost_dashboard.py --monitor

# Save daily snapshot
python aws_cost_dashboard.py --snapshot
```

### 5. `token_tracker.py` - Real-Time Session Tracker
A proactive alert system that monitors your spending against budget limits and provides recommendations.

**Features:**
- Budget monitoring with alert levels (green/yellow/red)
- Monthly spending projections
- Service-specific cost breakdown
- Automated recommendations
- Alert logging for tracking

**Usage:**
```bash
# Monitor against $20 monthly budget
python aws_cost_alerts.py --budget 20

# Monitor and save alert log
python aws_cost_alerts.py --budget 50 --save-log

# Quick check with different budget
python aws_cost_alerts.py --budget 100
```
A lightweight utility for tracking token usage and costs during your current coding session.

**Features:**
- Real-time token and cost tracking
- Session-based logging to JSON files
- Support for multiple AI models
- Cost calculation with current pricing
- Session summaries and exports

**Usage:**
```python
from token_tracker import TokenTracker

# Create tracker
tracker = TokenTracker("my_session.json")

# Track a request
tracker.track_request(
    model_id="amazon.nova-lite-v1:0",
    input_tokens=50,
    output_tokens=150,
    prompt="Your prompt here",
    response="Model response here"
)

# Get summary
tracker.print_session_summary()
```

### 6. `bedrock_with_tracking.py` - Integrated Bedrock Client
A wrapper around the AWS Bedrock client that automatically tracks token usage and costs.

**Features:**
- Drop-in replacement for regular Bedrock calls
- Automatic token counting and cost calculation
- Session tracking built-in
- Support for Nova Lite and Claude models
- Easy integration with existing code

**Usage:**
```python
from bedrock_with_tracking import BedrockWithTracking

# Initialize client with tracking
client = BedrockWithTracking(session_file="my_bedrock_session.json")

# Make AI calls with automatic tracking
result = client.invoke_with_tracking(
    model_id="amazon.nova-lite-v1:0",
    prompt="What is machine learning?",
    max_tokens=500
)

print(f"Response: {result['content']}")
print(f"Cost: ${result['tracking']['total_cost']:.4f}")

# View session summary
client.print_summary()
```

### 6. `usage_examples.py` - Complete Usage Examples
A comprehensive collection of examples showing how to use all the token tracking utilities.

**Features:**
- Manual token tracking examples
- Automatic Bedrock integration examples
- Cost comparison across models
- Session management for different projects
- Budget monitoring and alerts

**Usage:**
```python
# Run all examples
python usage_examples.py

# The examples demonstrate:
# - Simple manual tracking
# - Automatic Bedrock tracking
# - Model cost comparison
# - Session management
# - Budget monitoring with alerts
```

## Current Model Pricing (as of August 2025)

| Model | Input (per 1K tokens) | Output (per 1K tokens) |
|-------|----------------------|------------------------|
| Amazon Nova Lite | $0.06 | $0.24 |
| Claude 3.5 Sonnet | $3.00 | $15.00 |
| Claude 3.5 Haiku | $0.25 | $1.25 |

## Quick Start Guide

### 1. Set Up AWS Credentials
Ensure your AWS credentials are configured:
```bash
aws configure
```

### 2. Install Dependencies
```bash
pip install boto3
```

### 3. Quick Cost Overview
```bash
# Get current AWS costs across all services
python aws_cost_dashboard.py

# Comprehensive billing analysis
python aws_billing_monitor.py --days 7 --quiet
```

### 4. Start Tracking Your AI Session
```python
# Simple session tracking
from token_tracker import TokenTracker
tracker = TokenTracker()

# Track usage as you go
tracker.track_request("amazon.nova-lite-v1:0", 25, 75)
tracker.print_session_summary()
```

### 5. Use Integrated Bedrock Client
```python
# Replace your regular Bedrock calls
from bedrock_with_tracking import BedrockWithTracking

client = BedrockWithTracking()
result = client.invoke_with_tracking(
    "amazon.nova-lite-v1:0", 
    "Explain AWS Lambda"
)
```

### 6. Run Comprehensive Analysis
```bash
# Get detailed usage report
python ai_usage_monitor.py --days 7 --detailed
```

## Understanding Your Costs

### Token-Based Pricing
- **Input tokens**: Tokens in your prompts
- **Output tokens**: Tokens in AI responses
- **Total cost** = (input_tokens/1000 × input_price) + (output_tokens/1000 × output_price)

### Cost Optimization Tips

1. **Use Nova Lite for learning**: Much cheaper than Claude models
2. **Optimize prompts**: Shorter prompts = lower input token costs
3. **Set max_tokens**: Control output length to manage costs
4. **Track sessions**: Monitor your usage patterns
5. **Use batch processing**: Group similar requests together

### Example Cost Comparison
For a 100-token prompt with 200-token response:

| Model | Input Cost | Output Cost | Total Cost |
|-------|------------|-------------|------------|
| Nova Lite | $0.006 | $0.048 | $0.054 |
| Claude Sonnet | $0.30 | $3.00 | $3.30 |
| Claude Haiku | $0.025 | $0.25 | $0.275 |

**Nova Lite is 61x cheaper than Claude Sonnet!**

## File Structure

```
Utils/
├── README.md                    # This file
├── ai_usage_monitor.py         # Comprehensive monitoring
├── token_tracker.py            # Session tracking
├── bedrock_with_tracking.py    # Integrated client
├── ai_session_log.json         # Default session file
└── demo_session.json           # Demo tracking data
```

## Common Use Cases

### For Students
```python
# Track learning session costs
tracker = TokenTracker("learning_session.json")
# Use throughout your coding session
tracker.print_session_summary()  # See total cost
```

### For Developers
```python
# Track project development costs
client = BedrockWithTracking(session_file="project_costs.json")
# Make AI calls as normal
client.print_summary()  # Monitor project costs
```

### For Administrators
```bash
# Get organizational usage report
python ai_usage_monitor.py --days 30 --detailed
# Review CloudWatch metrics and billing data
```

## Troubleshooting

### Permission Issues
If you get permission errors:
1. Check AWS credentials: `aws sts get-caller-identity`
2. Ensure CloudWatch read permissions
3. Ensure Cost Explorer read permissions

### Token Count Accuracy
- Token counts come directly from AWS Bedrock
- Estimates in tracker are approximations
- Actual billing uses AWS-reported tokens

### Cost Discrepancies
- Prices may change; update pricing in code
- AWS billing includes additional fees
- Use AWS Cost Explorer for official billing

## Integration with Course Examples

These utilities integrate seamlessly with all course examples:

```python
# Add to any Bedrock example
from Utils.token_tracker import TokenTracker
tracker = TokenTracker()

# Your existing Bedrock code here
# Add tracking:
tracker.track_request(model_id, input_tokens, output_tokens)
```

## Next Steps

1. **Start with token_tracker.py** for immediate session tracking
2. **Use bedrock_with_tracking.py** for seamless integration
3. **Run ai_usage_monitor.py** for comprehensive analysis
4. **Set up regular monitoring** for ongoing projects

---

*Happy coding with cost awareness! 💰🤖*

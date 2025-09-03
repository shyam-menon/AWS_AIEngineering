# AWS Cost Monitoring with Human-in-the-Loop Example

This example demonstrates advanced usage of the Strands Agents framework with community tools for AWS cost monitoring and human-in-the-loop workflows.

## Overview

The `aws_cost_monitor_hitl_example.py` showcases two key community tools:

1. **`use_aws` tool** - For monitoring AWS costs and billing information
2. **`handoff_to_user` tool** - For implementing human-in-the-loop approval workflows

## Features

### 🔍 AWS Cost Monitoring
- Real-time cost and billing information retrieval
- Service-specific cost analysis
- Budget threshold monitoring and alerts
- Cost trend analysis and reporting
- Weekly/monthly cost summaries

### 🤝 Human-in-the-Loop Integration
- Interactive approval workflows for high-cost operations
- Human oversight for budget threshold breaches
- Manual review processes for unusual spending patterns
- User input collection for critical decisions
- Complete handoff capabilities for complex scenarios

### 📊 Intelligent Cost Management
- Automated budget tracking with configurable thresholds
- Proactive cost optimization recommendations
- Anomaly detection for unusual spending patterns
- Integration with AWS Cost Explorer data
- Comprehensive logging and audit trails

## Prerequisites

### 1. Install Dependencies
```bash
# Install core Strands packages
pip install strands-agents strands-agents-tools

# Verify installation
python -c "import strands_tools; print('Tools installed successfully')"
```

### 2. AWS Configuration
Ensure your AWS credentials are properly configured with appropriate permissions:

```bash
# Configure AWS credentials (if not already done)
aws configure

# Required AWS IAM permissions:
# - ce:GetCostAndUsage
# - ce:GetDimensionValues  
# - ce:GetReservationCoverage
# - ce:GetReservationPurchaseRecommendation
# - ce:GetReservationUtilization
# - ce:GetUsageReport
# - budgets:ViewBudget
# - budgets:DescribeBudgets
```

### 3. Environment Setup
```bash
# Optional: Set environment variable to bypass tool consent prompts
export BYPASS_TOOL_CONSENT=true

# Or set in Python:
import os
os.environ["BYPASS_TOOL_CONSENT"] = "true"
```

## Usage Examples

### Quick Start
```bash
# Run the interactive demo
python aws_cost_monitor_hitl_example.py
```

### Programmatic Usage
```python
from aws_cost_monitor_hitl_example import AWSCostMonitoringAgent

# Create agent with custom budget
agent = AWSCostMonitoringAgent(
    monthly_budget_limit=2000.0,  # $2,000 budget
    alert_threshold=0.8           # Alert at 80%
)

# Run cost monitoring
agent.run_cost_monitoring_session()

# Check specific service costs
agent.check_service_costs("RDS")

# Approve high-cost operation
agent.approve_high_cost_operation(
    "Scale RDS instance to db.r5.4xlarge", 
    estimated_cost=800.0
)
```

## Tool Integration Details

### `use_aws` Tool
The `use_aws` tool provides access to AWS services through the AWS SDK:

```python
# Example usage within agent
response = agent("Use the AWS tool to get current EC2 costs for this month")

# The tool can access:
# - Cost Explorer APIs
# - Billing APIs  
# - Resource usage information
# - Service-specific cost data
```

**Key Capabilities:**
- Retrieve current and historical cost data
- Get service-specific billing information
- Access budget and spending alerts
- Query cost and usage reports
- Analyze spending trends and patterns

### `handoff_to_user` Tool
The `handoff_to_user` tool enables human intervention in agent workflows:

```python
# Interactive mode - collect input and continue
response = agent.tool.handoff_to_user(
    message="Budget exceeded! Approve additional $500 spending?",
    breakout_of_loop=False
)

# Complete handoff mode - stop execution for human takeover
agent.tool.handoff_to_user(
    message="Critical cost anomaly detected. Human review required.",
    breakout_of_loop=True
)
```

**Two Operating Modes:**
1. **Interactive Mode** (`breakout_of_loop=False`)
   - Collects user input
   - Continues agent execution with user response
   - Ideal for approvals and confirmations

2. **Complete Handoff Mode** (`breakout_of_loop=True`)
   - Stops agent execution entirely
   - Transfers control to human operator
   - Used for critical situations requiring human oversight

## Example Workflows

### 1. Budget Monitoring Workflow
```python
# Agent monitors costs continuously
# When spending approaches threshold:
agent("Current spending is $750 of $1000 budget (75%). 
       Handoff to user for budget review and approval.")

# User receives prompt:
# "Budget threshold reached. Approve continued spending? (yes/no)"
```

### 2. Cost Anomaly Detection
```python
# Agent detects unusual spending pattern
agent("AWS costs increased 300% this week from $200 to $800. 
       This requires immediate human investigation.")

# Complete handoff to user for investigation
```

### 3. Service Optimization Approval
```python
# Agent recommends cost optimization
agent("Found 5 idle EC2 instances costing $500/month. 
       Calculate savings from termination, then handoff to user 
       for approval to proceed with optimization.")
```

## Configuration Options

### Agent Configuration
```python
# Customize agent behavior
agent = AWSCostMonitoringAgent(
    monthly_budget_limit=5000.0,     # Budget limit
    alert_threshold=0.75,            # Alert percentage
)

# Modify agent prompt for specific use cases
agent.agent.system_prompt += """
Additional Instructions:
- Focus on EC2 and RDS costs specifically
- Require approval for any single service >$200/month
- Generate daily cost reports
"""
```

### AWS Tool Configuration
The `use_aws` tool automatically uses your configured AWS credentials and region. Ensure proper IAM permissions for cost monitoring.

### Human-in-the-Loop Configuration
```python
# Bypass consent for automation
os.environ["BYPASS_TOOL_CONSENT"] = "true"

# Or handle consent programmatically
# (Tool will prompt user if consent not bypassed)
```

## Advanced Features

### Cost Optimization Recommendations
The agent provides intelligent recommendations based on AWS cost patterns:

- **Right-sizing suggestions** for over-provisioned resources
- **Reserved Instance recommendations** for predictable workloads  
- **Unused resource identification** and termination suggestions
- **Cost allocation insights** across services and teams
- **Trend analysis** for proactive budget planning

### Automated Alerting
Configure automatic alerts based on:
- Percentage of monthly budget consumed
- Absolute dollar thresholds
- Rate of spend increase
- Service-specific cost spikes
- Unusual usage patterns

### Integration with AWS Services
The example integrates with key AWS cost management services:
- **AWS Cost Explorer** for detailed cost analysis
- **AWS Budgets** for budget tracking and alerts
- **AWS Cost Categories** for cost allocation
- **AWS Billing Console** for invoice and payment data

## Security Considerations

### IAM Permissions
Grant minimal necessary permissions for cost monitoring:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ce:GetCostAndUsage",
                "ce:GetDimensionValues",
                "budgets:ViewBudget",
                "budgets:DescribeBudgets"
            ],
            "Resource": "*"
        }
    ]
}
```

### Data Privacy
- Cost data is processed locally by the agent
- No sensitive billing information is stored persistently
- All AWS API calls use your configured credentials
- Human handoff prompts display only necessary information

### Audit Trail
The example includes comprehensive logging:
- All cost monitoring activities
- Human approval decisions
- Tool execution details
- Error conditions and responses

## Production Considerations

### Scalability
- Deploy on AWS Lambda for serverless execution
- Use EventBridge for scheduled cost monitoring
- Store historical data in DynamoDB for trend analysis
- Implement SQS for asynchronous processing

### Monitoring
- CloudWatch integration for agent performance metrics
- Cost monitoring dashboard with real-time updates
- Alert delivery via SNS (email, Slack, etc.)
- Performance tracking and optimization

### Error Handling
The example includes robust error handling:
- AWS API call failures and retries
- Network connectivity issues
- Invalid user input validation
- Tool execution timeouts

## Troubleshooting

### Common Issues

1. **AWS Credentials Not Found**
   ```
   Solution: Configure AWS credentials using `aws configure`
   ```

2. **Insufficient IAM Permissions**
   ```
   Solution: Add required Cost Explorer permissions to your IAM user/role
   ```

3. **Tool Import Errors**
   ```bash
   Solution: Install tools package
   pip install strands-agents-tools
   ```

4. **Human Handoff Not Working**
   ```
   Solution: Ensure running in terminal environment
   Web interfaces require custom handoff implementation
   ```

### Debug Mode
Enable detailed logging for troubleshooting:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# View detailed tool execution logs
logger = logging.getLogger('strands_tools')
logger.setLevel(logging.DEBUG)
```

## Learning Objectives

After working through this example, you will understand:

1. **Community Tools Integration**: How to use `strands-agents-tools` in production agents
2. **AWS Service Integration**: Accessing AWS APIs through the `use_aws` tool
3. **Human-in-the-Loop Patterns**: Implementing approval workflows with `handoff_to_user`
4. **Cost Management**: Building intelligent cost monitoring and optimization systems
5. **Production Patterns**: Error handling, logging, and configuration management
6. **Tool Consent Management**: Handling user confirmations and automation bypasses

## Related Examples

- **`simple_tool_agent.py`** - Basic tool usage patterns
- **`agents_as_tools_example.py`** - Hierarchical agent delegation
- **`swarm_example.py`** - Collaborative multi-agent systems

## Next Steps

1. **Customize for Your Environment**: Modify budget limits and alert thresholds
2. **Add More AWS Services**: Extend monitoring to additional AWS services
3. **Integration with Existing Systems**: Connect to your monitoring and alerting infrastructure
4. **Advanced Analytics**: Add cost forecasting and trend analysis capabilities
5. **Automation**: Create scheduled cost monitoring and reporting workflows

This example provides a solid foundation for building production-ready AWS cost monitoring systems with intelligent human oversight capabilities.

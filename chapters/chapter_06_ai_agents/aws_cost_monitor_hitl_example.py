#!/usr/bin/env python3
"""
AWS Cost Monitoring Agent with Human-in-the-Loop

This example demonstrates:
1. Using the `use_aws` tool to monitor AWS costs and billing
2. Using the `handoff_to_user` tool for human-in-the-loop workflows
3. Intelligent cost alerting and budget management
4. Human intervention for cost approval and decision making

Features:
- Real-time AWS cost monitoring
- Budget threshold alerts
- Human approval for high-cost operations
- Cost optimization recommendations
- Interactive cost review sessions

Requirements:
- AWS credentials configured (IAM permissions for Billing/Cost Explorer)
- strands-agents-tools package
- Proper AWS IAM permissions for cost monitoring

Usage:
    python aws_cost_monitor_hitl_example.py
"""

import os
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

# Set environment to bypass tool consent for automation
os.environ["BYPASS_TOOL_CONSENT"] = "true"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('aws_cost_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

try:
    from strands import Agent
    from strands_tools import use_aws, handoff_to_user, calculator, current_time
    logger.info("Successfully imported Strands tools")
except ImportError as e:
    logger.error(f"Failed to import required tools: {e}")
    print("Please install required packages:")
    print("pip install strands-agents strands-agents-tools")
    exit(1)


class AWSCostMonitoringAgent:
    """
    Advanced AWS Cost Monitoring Agent with Human-in-the-Loop capabilities.
    
    This agent monitors AWS costs, provides alerts, and implements human oversight
    for cost management decisions.
    """
    
    def __init__(self, monthly_budget_limit: float = 1000.0, alert_threshold: float = 0.8):
        """
        Initialize the cost monitoring agent.
        
        Args:
            monthly_budget_limit: Monthly budget limit in USD
            alert_threshold: Percentage of budget that triggers alerts (0.0-1.0)
        """
        self.monthly_budget_limit = monthly_budget_limit
        self.alert_threshold = alert_threshold
        
        # Create the agent with AWS and human-in-the-loop tools
        self.agent = Agent(
            model="us.amazon.nova-lite-v1:0",  # Cost-effective model
            tools=[use_aws, handoff_to_user, calculator, current_time],
            system_prompt=f"""You are an AWS Cost Monitoring and Management Agent.

Your responsibilities:
1. Monitor AWS costs and spending patterns
2. Alert when spending approaches budget limits
3. Provide cost optimization recommendations
4. Require human approval for high-cost decisions
5. Generate detailed cost reports and analysis

Current Configuration:
- Monthly Budget Limit: ${monthly_budget_limit:,.2f}
- Alert Threshold: {alert_threshold:.0%} of budget
- Alert Amount: ${monthly_budget_limit * alert_threshold:,.2f}

Guidelines:
- Use the `use_aws` tool to get current billing information
- Use `handoff_to_user` for human approval when costs exceed thresholds
- Always provide clear cost breakdowns and recommendations
- Be proactive about cost optimization opportunities
- Include specific AWS service cost details in reports

When costs approach the alert threshold, immediately handoff to user for review.
For any spending above the monthly budget, require explicit human approval.
"""
        )
        
        logger.info(f"Initialized AWS Cost Monitor - Budget: ${monthly_budget_limit:,.2f}, Alert: {alert_threshold:.0%}")
    
    def run_cost_monitoring_session(self):
        """Run an interactive cost monitoring session."""
        print("\n" + "="*80)
        print("🔍 AWS COST MONITORING AGENT - STARTING SESSION")
        print("="*80)
        
        try:
            # Start with current cost check
            response = self.agent("Please check current AWS costs and billing information. "
                               "Get the current month's spending so far and compare it to our budget limits. "
                               "If we're approaching the alert threshold, handoff to user for review.")
            
            print(f"\n💰 Cost Analysis Response:\n{response}")
            
            # Follow up with cost optimization check
            optimization_response = self.agent("Now analyze the cost data and provide specific "
                                             "recommendations for cost optimization. Look for "
                                             "high-cost services and suggest ways to reduce spending.")
            
            print(f"\n📊 Optimization Recommendations:\n{optimization_response}")
            
        except Exception as e:
            logger.error(f"Error during cost monitoring session: {e}")
            print(f"❌ Error: {e}")
    
    def check_service_costs(self, service_name: str = "EC2"):
        """Check costs for a specific AWS service."""
        print(f"\n🔍 Checking costs for AWS {service_name}...")
        
        try:
            response = self.agent(f"Use the AWS tool to get detailed cost information for the "
                               f"{service_name} service. Show costs for the current month and "
                               f"compare to previous month. If costs are high, provide specific "
                               f"optimization recommendations.")
            
            print(f"\n📈 {service_name} Cost Analysis:\n{response}")
            
        except Exception as e:
            logger.error(f"Error checking {service_name} costs: {e}")
            print(f"❌ Error checking {service_name} costs: {e}")
    
    def approve_high_cost_operation(self, operation_description: str, estimated_cost: float):
        """Request human approval for a high-cost operation."""
        print(f"\n⚠️  HIGH COST OPERATION APPROVAL REQUIRED")
        print(f"Operation: {operation_description}")
        print(f"Estimated Cost: ${estimated_cost:,.2f}")
        
        try:
            response = self.agent(f"A high-cost operation is being requested: '{operation_description}' "
                               f"with estimated cost of ${estimated_cost:,.2f}. This exceeds our "
                               f"normal spending patterns. Please handoff to user for approval with "
                               f"detailed cost breakdown and risk assessment.")
            
            print(f"\n🤝 Approval Process Response:\n{response}")
            
        except Exception as e:
            logger.error(f"Error during approval process: {e}")
            print(f"❌ Error during approval process: {e}")
    
    def generate_weekly_cost_report(self):
        """Generate a comprehensive weekly cost report."""
        print(f"\n📄 GENERATING WEEKLY COST REPORT")
        print("-" * 50)
        
        try:
            response = self.agent("Generate a comprehensive weekly AWS cost report. Include: "
                               "1. Total spending this week vs last week "
                               "2. Top 5 most expensive services "
                               "3. Any unusual spending patterns "
                               "4. Budget utilization percentage "
                               "5. Recommendations for next week "
                               "If any concerning patterns are found, handoff to user for review.")
            
            print(f"\n📊 Weekly Report:\n{response}")
            
        except Exception as e:
            logger.error(f"Error generating weekly report: {e}")
            print(f"❌ Error generating weekly report: {e}")


def demonstrate_human_in_the_loop_scenarios():
    """Demonstrate various human-in-the-loop scenarios."""
    print("\n" + "="*80)
    print("🤝 HUMAN-IN-THE-LOOP DEMONSTRATION")
    print("="*80)
    
    # Create a simple agent for HITL demos
    hitl_agent = Agent(
        model="us.amazon.nova-lite-v1:0",
        tools=[handoff_to_user, calculator, current_time],
        system_prompt="""You are demonstrating human-in-the-loop workflows.
        
        Use handoff_to_user when:
        1. Approval is needed for important decisions
        2. Human input is required for complex scenarios
        3. Verification is needed for calculated results
        
        Always explain why human input is needed."""
    )
    
    scenarios = [
        {
            "name": "Budget Approval",
            "prompt": "I need to approve a budget increase to $5,000 per month. "
                     "Calculate the percentage increase from our current $1,000 budget, "
                     "then handoff to user for approval with the calculation."
        },
        {
            "name": "Service Optimization",
            "prompt": "We have 3 EC2 instances running 24/7 costing $200/month each. "
                     "Calculate potential savings from right-sizing to smaller instances "
                     "at $100/month each, then handoff to user to confirm the change."
        },
        {
            "name": "Unusual Spending Alert",
            "prompt": "Our AWS bill jumped from $500 last month to $1,200 this month. "
                     "This is a 140% increase. Handoff to user immediately for investigation "
                     "as this could indicate a security issue or misconfiguration."
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{i}. {scenario['name']} Scenario:")
        print("-" * 40)
        
        try:
            response = hitl_agent(scenario['prompt'])
            print(f"Response: {response}")
        except Exception as e:
            print(f"❌ Error in scenario: {e}")
        
        print("\n" + "="*40)


def main():
    """Main demonstration function."""
    print("🚀 Starting AWS Cost Monitoring with Human-in-the-Loop Demo")
    print("=" * 80)
    
    # Create cost monitoring agent
    cost_monitor = AWSCostMonitoringAgent(
        monthly_budget_limit=1000.0,  # $1,000 monthly budget
        alert_threshold=0.75          # Alert at 75% of budget
    )
    
    # Menu-driven demo
    while True:
        print("\n📋 AWS COST MONITORING MENU")
        print("=" * 40)
        print("1. 🔍 Run Full Cost Monitoring Session")
        print("2. 📊 Check Specific Service Costs (EC2)")
        print("3. ⚠️  Simulate High-Cost Operation Approval")
        print("4. 📄 Generate Weekly Cost Report")
        print("5. 🤝 Demonstrate Human-in-the-Loop Scenarios")
        print("6. ❌ Exit")
        
        choice = input("\nSelect an option (1-6): ").strip()
        
        if choice == "1":
            cost_monitor.run_cost_monitoring_session()
        elif choice == "2":
            service = input("Enter AWS service name (default: EC2): ").strip() or "EC2"
            cost_monitor.check_service_costs(service)
        elif choice == "3":
            operation = input("Enter operation description: ").strip() or "Launch new EC2 cluster"
            try:
                cost = float(input("Enter estimated cost ($): ").strip() or "500")
                cost_monitor.approve_high_cost_operation(operation, cost)
            except ValueError:
                print("❌ Invalid cost amount")
        elif choice == "4":
            cost_monitor.generate_weekly_cost_report()
        elif choice == "5":
            demonstrate_human_in_the_loop_scenarios()
        elif choice == "6":
            print("👋 Exiting AWS Cost Monitoring Demo")
            break
        else:
            print("❌ Invalid option. Please select 1-6.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user. Goodbye!")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"❌ Unexpected error: {e}")

#!/usr/bin/env python3
"""
AWS AI Token Usage and Billing Monitor

This utility helps you track your AI token usage and associated costs across
AWS Bedrock models, including Amazon Nova Lite. It provides insights into:
- Token consumption per model
- Cost estimates based on AWS Bedrock pricing
- Usage trends over time
- Billing alerts and recommendations

Author: AWS AI Engineering Course
Date: August 2025
"""

import boto3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from botocore.exceptions import ClientError, NoCredentialsError
import argparse


class AiUsageMonitor:
    """Monitor AI token usage and billing across AWS services."""
    
    def __init__(self, region='us-east-1'):
        """Initialize the AI usage monitor."""
        self.region = region
        try:
            self.cloudwatch = boto3.client('cloudwatch', region_name=region)
            self.cost_explorer = boto3.client('ce', region_name='us-east-1')  # CE is only in us-east-1
            self.bedrock = boto3.client('bedrock', region_name=region)
            print(f"✅ Initialized AI Usage Monitor for region: {region}")
        except NoCredentialsError:
            print("❌ Error: AWS credentials not found. Please configure your credentials.")
            raise
        except Exception as e:
            print(f"❌ Error initializing monitor: {e}")
            raise
    
    def get_bedrock_usage_metrics(self, days_back: int = 7) -> Dict:
        """
        Get Bedrock usage metrics from CloudWatch.
        
        Args:
            days_back (int): Number of days to look back
            
        Returns:
            Dict: Usage metrics by model
        """
        print(f"📊 Fetching Bedrock usage metrics for the last {days_back} days...")
        
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=days_back)
        
        metrics = {}
        
        try:
            # Get available Bedrock models
            models_response = self.bedrock.list_foundation_models()
            available_models = [model['modelId'] for model in models_response['modelSummaries']]
            
            # Focus on commonly used models
            key_models = [
                'amazon.nova-lite-v1:0',
                'anthropic.claude-3-5-sonnet-20241022-v2:0',
                'anthropic.claude-3-5-haiku-20241022-v1:0',
                'amazon.titan-text-express-v1'
            ]
            
            for model_id in key_models:
                if model_id in available_models:
                    model_metrics = self._get_model_metrics(model_id, start_time, end_time)
                    if model_metrics:
                        metrics[model_id] = model_metrics
            
            return metrics
            
        except ClientError as e:
            print(f"⚠️  Error fetching CloudWatch metrics: {e}")
            return {}
    
    def _get_model_metrics(self, model_id: str, start_time: datetime, end_time: datetime) -> Dict:
        """Get metrics for a specific model."""
        try:
            # Get invocation count
            invocations = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/Bedrock',
                MetricName='Invocations',
                Dimensions=[
                    {'Name': 'ModelId', 'Value': model_id}
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=86400,  # 1 day
                Statistics=['Sum']
            )
            
            # Get input tokens
            input_tokens = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/Bedrock',
                MetricName='InputTokenCount',
                Dimensions=[
                    {'Name': 'ModelId', 'Value': model_id}
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=86400,
                Statistics=['Sum']
            )
            
            # Get output tokens
            output_tokens = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/Bedrock',
                MetricName='OutputTokenCount',
                Dimensions=[
                    {'Name': 'ModelId', 'Value': model_id}
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=86400,
                Statistics=['Sum']
            )
            
            return {
                'invocations': sum([point['Sum'] for point in invocations['Datapoints']]),
                'input_tokens': sum([point['Sum'] for point in input_tokens['Datapoints']]),
                'output_tokens': sum([point['Sum'] for point in output_tokens['Datapoints']]),
                'period': f"{start_time.date()} to {end_time.date()}"
            }
            
        except ClientError as e:
            print(f"⚠️  Could not get metrics for {model_id}: {e}")
            return {}
    
    def calculate_bedrock_costs(self, usage_metrics: Dict) -> Dict:
        """
        Calculate estimated costs based on Bedrock pricing.
        
        Args:
            usage_metrics (Dict): Usage metrics from get_bedrock_usage_metrics
            
        Returns:
            Dict: Cost estimates by model
        """
        print("💰 Calculating estimated costs...")
        
        # AWS Bedrock pricing (as of August 2025 - prices may vary)
        pricing = {
            'amazon.nova-lite-v1:0': {
                'input_price_per_1k': 0.00006,   # $0.06 per 1K input tokens
                'output_price_per_1k': 0.00024   # $0.24 per 1K output tokens
            },
            'anthropic.claude-3-5-sonnet-20241022-v2:0': {
                'input_price_per_1k': 0.003,     # $3.00 per 1K input tokens
                'output_price_per_1k': 0.015     # $15.00 per 1K output tokens
            },
            'anthropic.claude-3-5-haiku-20241022-v1:0': {
                'input_price_per_1k': 0.00025,   # $0.25 per 1K input tokens
                'output_price_per_1k': 0.00125   # $1.25 per 1K output tokens
            },
            'amazon.titan-text-express-v1': {
                'input_price_per_1k': 0.0002,    # $0.20 per 1K input tokens
                'output_price_per_1k': 0.0006    # $0.60 per 1K output tokens
            }
        }
        
        cost_breakdown = {}
        total_cost = 0
        
        for model_id, metrics in usage_metrics.items():
            if model_id in pricing and metrics:
                model_pricing = pricing[model_id]
                
                input_cost = (metrics['input_tokens'] / 1000) * model_pricing['input_price_per_1k']
                output_cost = (metrics['output_tokens'] / 1000) * model_pricing['output_price_per_1k']
                model_total = input_cost + output_cost
                
                cost_breakdown[model_id] = {
                    'input_cost': input_cost,
                    'output_cost': output_cost,
                    'total_cost': model_total,
                    'invocations': metrics['invocations'],
                    'input_tokens': metrics['input_tokens'],
                    'output_tokens': metrics['output_tokens'],
                    'avg_cost_per_invocation': model_total / max(metrics['invocations'], 1)
                }
                
                total_cost += model_total
        
        cost_breakdown['total_estimated_cost'] = total_cost
        return cost_breakdown
    
    def get_aws_billing_data(self, days_back: int = 30) -> Dict:
        """
        Get actual AWS billing data from Cost Explorer.
        
        Args:
            days_back (int): Number of days to look back
            
        Returns:
            Dict: Billing data
        """
        print(f"💳 Fetching AWS billing data for the last {days_back} days...")
        
        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=days_back)
        
        try:
            # Get overall costs
            cost_response = self.cost_explorer.get_cost_and_usage(
                TimePeriod={
                    'Start': start_date.strftime('%Y-%m-%d'),
                    'End': end_date.strftime('%Y-%m-%d')
                },
                Granularity='DAILY',
                Metrics=['BlendedCost'],
                GroupBy=[
                    {'Type': 'DIMENSION', 'Key': 'SERVICE'}
                ]
            )
            
            # Get Bedrock-specific costs
            bedrock_costs = []
            total_cost = 0
            
            for result in cost_response['ResultsByTime']:
                date = result['TimePeriod']['Start']
                for group in result['Groups']:
                    service = group['Keys'][0]
                    cost = float(group['Metrics']['BlendedCost']['Amount'])
                    
                    if 'Bedrock' in service or 'bedrock' in service.lower():
                        bedrock_costs.append({
                            'date': date,
                            'service': service,
                            'cost': cost
                        })
                    
                    total_cost += cost
            
            return {
                'period': f"{start_date} to {end_date}",
                'bedrock_costs': bedrock_costs,
                'total_bedrock_cost': sum([item['cost'] for item in bedrock_costs]),
                'total_aws_cost': total_cost
            }
            
        except ClientError as e:
            print(f"⚠️  Error accessing Cost Explorer: {e}")
            print("   Note: Cost Explorer requires specific IAM permissions")
            return {}
    
    def generate_usage_report(self, days_back: int = 7) -> None:
        """Generate a comprehensive usage and billing report."""
        print("=" * 60)
        print("🤖 AWS AI TOKEN USAGE & BILLING REPORT")
        print("=" * 60)
        
        # Get usage metrics
        usage_metrics = self.get_bedrock_usage_metrics(days_back)
        
        if not usage_metrics:
            print("❌ No usage metrics found. This could mean:")
            print("   - No Bedrock usage in the specified period")
            print("   - CloudWatch metrics not yet available (can take up to 15 minutes)")
            print("   - Insufficient permissions to access CloudWatch")
            return
        
        # Calculate costs
        cost_breakdown = self.calculate_bedrock_costs(usage_metrics)
        
        # Display results
        print(f"\n📊 USAGE SUMMARY (Last {days_back} days)")
        print("-" * 50)
        
        total_invocations = 0
        total_input_tokens = 0
        total_output_tokens = 0
        
        for model_id, data in cost_breakdown.items():
            if model_id != 'total_estimated_cost':
                print(f"\n🔹 {model_id}")
                print(f"   Invocations: {int(data['invocations']):,}")
                print(f"   Input Tokens: {int(data['input_tokens']):,}")
                print(f"   Output Tokens: {int(data['output_tokens']):,}")
                print(f"   Total Tokens: {int(data['input_tokens'] + data['output_tokens']):,}")
                
                total_invocations += data['invocations']
                total_input_tokens += data['input_tokens']
                total_output_tokens += data['output_tokens']
        
        print(f"\n📈 TOTAL USAGE")
        print("-" * 30)
        print(f"Total Invocations: {int(total_invocations):,}")
        print(f"Total Input Tokens: {int(total_input_tokens):,}")
        print(f"Total Output Tokens: {int(total_output_tokens):,}")
        print(f"Total Tokens: {int(total_input_tokens + total_output_tokens):,}")
        
        print(f"\n💰 ESTIMATED COSTS")
        print("-" * 30)
        
        for model_id, data in cost_breakdown.items():
            if model_id != 'total_estimated_cost':
                print(f"\n🔹 {model_id}")
                print(f"   Input Cost: ${data['input_cost']:.4f}")
                print(f"   Output Cost: ${data['output_cost']:.4f}")
                print(f"   Total Cost: ${data['total_cost']:.4f}")
                print(f"   Avg Cost/Invocation: ${data['avg_cost_per_invocation']:.4f}")
        
        print(f"\n💵 TOTAL ESTIMATED COST: ${cost_breakdown['total_estimated_cost']:.4f}")
        
        # Get actual billing data
        print(f"\n💳 ACTUAL BILLING DATA (Last 30 days)")
        print("-" * 40)
        
        billing_data = self.get_aws_billing_data(30)
        if billing_data:
            print(f"Total Bedrock Cost: ${billing_data['total_bedrock_cost']:.4f}")
            print(f"Total AWS Cost: ${billing_data['total_aws_cost']:.2f}")
            
            if billing_data['bedrock_costs']:
                print(f"\nBedrock Daily Costs:")
                for cost_item in billing_data['bedrock_costs'][-7:]:  # Last 7 days
                    print(f"   {cost_item['date']}: ${cost_item['cost']:.4f}")
        else:
            print("Could not retrieve billing data - check Cost Explorer permissions")
        
        # Recommendations
        self._generate_recommendations(cost_breakdown, total_invocations)
    
    def _generate_recommendations(self, cost_breakdown: Dict, total_invocations: int) -> None:
        """Generate cost optimization recommendations."""
        print(f"\n💡 RECOMMENDATIONS")
        print("-" * 30)
        
        if total_invocations == 0:
            print("• No usage detected in the specified period")
            return
        
        # Model efficiency recommendations
        most_used_model = max(
            [(k, v) for k, v in cost_breakdown.items() if k != 'total_estimated_cost'],
            key=lambda x: x[1]['invocations'],
            default=(None, None)
        )
        
        if most_used_model[0]:
            print(f"• Most used model: {most_used_model[0]}")
            print(f"  Average cost per invocation: ${most_used_model[1]['avg_cost_per_invocation']:.4f}")
        
        # Cost optimization suggestions
        total_cost = cost_breakdown['total_estimated_cost']
        
        if total_cost > 10:
            print("• Consider using Amazon Nova Lite for cost-effective AI tasks")
            print("• Review prompts to optimize token usage")
            print("• Implement caching for repeated queries")
        elif total_cost > 1:
            print("• Monitor usage regularly to avoid unexpected costs")
            print("• Consider setting up billing alerts")
        else:
            print("• Your AI usage costs are well controlled")
            print("• Continue monitoring as usage scales")
        
        # Token efficiency tips
        avg_tokens_per_invocation = (cost_breakdown.get('total_input_tokens', 0) + 
                                    cost_breakdown.get('total_output_tokens', 0)) / max(total_invocations, 1)
        
        if avg_tokens_per_invocation > 1000:
            print("• Consider shorter, more focused prompts to reduce token usage")
            print("• Break down complex tasks into smaller requests")


def main():
    """Main function to run the AI usage monitor."""
    parser = argparse.ArgumentParser(description='AWS AI Token Usage and Billing Monitor')
    parser.add_argument('--days', '-d', type=int, default=7,
                       help='Number of days to analyze (default: 7)')
    parser.add_argument('--region', '-r', type=str, default='us-east-1',
                       help='AWS region (default: us-east-1)')
    parser.add_argument('--detailed', action='store_true',
                       help='Show detailed breakdown by model')
    
    args = parser.parse_args()
    
    try:
        # Initialize monitor
        monitor = AiUsageMonitor(region=args.region)
        
        # Generate report
        monitor.generate_usage_report(days_back=args.days)
        
        print(f"\n" + "=" * 60)
        print("📋 Note: Estimates based on current AWS Bedrock pricing")
        print("💡 For real-time billing, check AWS Cost Explorer console")
        print("⚠️  CloudWatch metrics may take up to 15 minutes to appear")
        
    except KeyboardInterrupt:
        print("\n\n👋 Monitor interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("   1. Check AWS credentials are configured")
        print("   2. Verify CloudWatch and Cost Explorer permissions")
        print("   3. Ensure you're in the correct AWS region")


if __name__ == "__main__":
    main()

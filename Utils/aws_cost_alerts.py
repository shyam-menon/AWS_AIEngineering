#!/usr/bin/env python3
"""
AWS Cost Alert System

A utility to set up automated cost alerts and budget monitoring for your AWS account.
Helps you stay within budget during course development and experimentation.

Author: AWS AI Engineering Course
Date: August 2025
"""

import boto3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class AWSCostAlerts:
    """AWS cost alert and budget monitoring system."""
    
    def __init__(self, region: str = 'us-east-1'):
        """Initialize the cost alert system."""
        self.region = region
        
        try:
            self.budgets = boto3.client('budgets', region_name='us-east-1')  # Budgets is only in us-east-1
            self.cost_explorer = boto3.client('ce', region_name='us-east-1')
            self.sns = boto3.client('sns', region_name=region)
            print(f"✅ Cost alert system initialized for region: {region}")
        except Exception as e:
            print(f"❌ Error initializing cost alert system: {e}")
            raise
    
    def check_current_spending(self, budget_limit: float) -> Dict:
        """Check current spending against budget limit."""
        try:
            # Get month-to-date costs
            today = datetime.now()
            start_of_month = datetime(today.year, today.month, 1)
            
            response = self.cost_explorer.get_cost_and_usage(
                TimePeriod={
                    'Start': start_of_month.strftime('%Y-%m-%d'),
                    'End': today.strftime('%Y-%m-%d')
                },
                Granularity='MONTHLY',
                Metrics=['BlendedCost']
            )
            
            current_spend = 0.0
            if response['ResultsByTime']:
                current_spend = float(response['ResultsByTime'][0]['Total']['BlendedCost']['Amount'])
            
            # Calculate percentages and projections
            days_elapsed = today.day
            days_in_month = (datetime(today.year, today.month + 1, 1) - timedelta(days=1)).day
            
            percentage_used = (current_spend / budget_limit) * 100 if budget_limit > 0 else 0
            daily_rate = current_spend / days_elapsed if days_elapsed > 0 else 0
            projected_monthly = daily_rate * days_in_month
            projected_percentage = (projected_monthly / budget_limit) * 100 if budget_limit > 0 else 0
            
            # Determine alert level
            alert_level = "green"
            if percentage_used > 80:
                alert_level = "red"
            elif percentage_used > 60:
                alert_level = "yellow"
            elif projected_percentage > 80:
                alert_level = "yellow"
            
            return {
                'current_spend': current_spend,
                'budget_limit': budget_limit,
                'percentage_used': percentage_used,
                'daily_rate': daily_rate,
                'projected_monthly': projected_monthly,
                'projected_percentage': projected_percentage,
                'days_elapsed': days_elapsed,
                'days_in_month': days_in_month,
                'alert_level': alert_level,
                'remaining_budget': budget_limit - current_spend
            }
            
        except Exception as e:
            print(f"❌ Error checking spending: {e}")
            return {}
    
    def get_service_breakdown(self, top_n: int = 5) -> List[Dict]:
        """Get breakdown of costs by service."""
        try:
            today = datetime.now()
            start_of_month = datetime(today.year, today.month, 1)
            
            response = self.cost_explorer.get_cost_and_usage(
                TimePeriod={
                    'Start': start_of_month.strftime('%Y-%m-%d'),
                    'End': today.strftime('%Y-%m-%d')
                },
                Granularity='MONTHLY',
                Metrics=['BlendedCost'],
                GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
            )
            
            services = []
            for result in response.get('ResultsByTime', []):
                for group in result.get('Groups', []):
                    service_name = group['Keys'][0]
                    cost = float(group['Metrics']['BlendedCost']['Amount'])
                    if cost > 0:
                        services.append({
                            'service': service_name,
                            'cost': cost
                        })
            
            # Sort by cost and return top N
            services.sort(key=lambda x: x['cost'], reverse=True)
            return services[:top_n]
            
        except Exception as e:
            print(f"❌ Error getting service breakdown: {e}")
            return []
    
    def display_cost_alert(self, budget_limit: float) -> None:
        """Display cost alert dashboard."""
        print("\n" + "=" * 70)
        print("🚨 AWS COST ALERT DASHBOARD")
        print("=" * 70)
        print(f"💰 Monthly Budget: ${budget_limit:.2f}")
        print(f"📅 Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Get spending data
        spending = self.check_current_spending(budget_limit)
        if not spending:
            print("❌ Could not retrieve spending data")
            return
        
        # Display current status
        print(f"\n📊 CURRENT STATUS")
        print("-" * 40)
        
        alert_emoji = {
            "green": "✅",
            "yellow": "⚠️ ",
            "red": "🚨"
        }
        
        status_emoji = alert_emoji.get(spending['alert_level'], "❓")
        print(f"{status_emoji} Alert Level: {spending['alert_level'].upper()}")
        print(f"💳 Current Spend: ${spending['current_spend']:.2f}")
        print(f"📊 Budget Used: {spending['percentage_used']:.1f}%")
        print(f"💰 Remaining: ${spending['remaining_budget']:.2f}")
        print(f"📅 Days Elapsed: {spending['days_elapsed']}/{spending['days_in_month']}")
        
        # Display projections
        print(f"\n🔮 MONTHLY PROJECTION")
        print("-" * 40)
        print(f"📈 Daily Rate: ${spending['daily_rate']:.2f}")
        print(f"🎯 Projected Total: ${spending['projected_monthly']:.2f}")
        print(f"📊 Projected Usage: {spending['projected_percentage']:.1f}%")
        
        if spending['projected_percentage'] > 100:
            overage = spending['projected_monthly'] - budget_limit
            print(f"⚠️  Projected Overage: ${overage:.2f}")
        
        # Display service breakdown
        print(f"\n🔧 TOP SERVICES")
        print("-" * 40)
        
        services = self.get_service_breakdown()
        for i, service in enumerate(services, 1):
            percentage = (service['cost'] / spending['current_spend']) * 100 if spending['current_spend'] > 0 else 0
            print(f"  {i}. {service['service']:<30} ${service['cost']:>6.2f} ({percentage:>4.1f}%)")
        
        # Display recommendations
        print(f"\n💡 RECOMMENDATIONS")
        print("-" * 40)
        
        recommendations = self._generate_alert_recommendations(spending, services)
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")
        
        print("\n" + "=" * 70)
    
    def _generate_alert_recommendations(self, spending: Dict, services: List[Dict]) -> List[str]:
        """Generate cost alert recommendations."""
        recommendations = []
        
        # Budget-based recommendations
        if spending['alert_level'] == 'red':
            recommendations.append("🚨 URGENT: Budget almost exceeded - review all running resources")
            recommendations.append("⏸️  Consider stopping non-essential EC2 instances immediately")
        elif spending['alert_level'] == 'yellow':
            recommendations.append("⚠️  Budget usage is high - monitor daily spending closely")
            recommendations.append("🔍 Review usage patterns for cost optimization opportunities")
        
        # Service-specific recommendations
        for service in services[:3]:
            service_name = service['service'].lower()
            if 'ec2' in service_name and service['cost'] > 5:
                recommendations.append("🖥️  EC2 costs are high - check instance types and usage")
            elif 'bedrock' in service_name and service['cost'] > 10:
                recommendations.append("🤖 Consider using Nova Lite model for development work")
            elif 's3' in service_name and service['cost'] > 5:
                recommendations.append("📦 Review S3 storage classes and lifecycle policies")
        
        # General recommendations
        if spending['projected_percentage'] > 100:
            recommendations.append("📉 Set up CloudWatch alarms for immediate cost alerts")
            recommendations.append("🔄 Consider implementing auto-shutdown for development resources")
        
        # Default recommendations if none specific
        if not recommendations:
            recommendations = [
                "✅ Spending is within normal range",
                "📊 Continue monitoring daily for any unusual spikes",
                "🎯 Consider setting up automated alerts for early warning"
            ]
        
        return recommendations[:6]  # Limit to 6 recommendations
    
    def save_alert_log(self, budget_limit: float, filename: Optional[str] = None) -> str:
        """Save cost alert data to log file."""
        if not filename:
            today = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"cost_alert_log_{today}.json"
        
        try:
            spending = self.check_current_spending(budget_limit)
            services = self.get_service_breakdown()
            
            log_data = {
                'timestamp': datetime.now().isoformat(),
                'budget_limit': budget_limit,
                'spending_data': spending,
                'service_breakdown': services,
                'alert_level': spending.get('alert_level', 'unknown')
            }
            
            with open(filename, 'w') as f:
                json.dump(log_data, f, indent=2, default=str)
            
            print(f"📁 Alert log saved: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ Could not save alert log: {e}")
            return ""


def main():
    """Main function to run cost alerts."""
    import argparse
    
    parser = argparse.ArgumentParser(description='AWS Cost Alert System')
    parser.add_argument('--budget', '-b', type=float, required=True, help='Monthly budget limit in dollars')
    parser.add_argument('--region', '-r', type=str, default='us-east-1', help='AWS region')
    parser.add_argument('--save-log', '-s', action='store_true', help='Save alert log to file')
    
    args = parser.parse_args()
    
    if args.budget <= 0:
        print("❌ Budget must be greater than 0")
        return 1
    
    try:
        alerts = AWSCostAlerts(region=args.region)
        alerts.display_cost_alert(args.budget)
        
        if args.save_log:
            alerts.save_alert_log(args.budget)
        
    except Exception as e:
        print(f"❌ Error running cost alerts: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

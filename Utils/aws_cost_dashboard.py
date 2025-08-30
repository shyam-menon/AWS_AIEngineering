#!/usr/bin/env python3
"""
AWS Cost Dashboard

A simple dashboard utility that provides a quick overview of your AWS spending
across all services. Perfect for daily cost monitoring during course development.

Author: AWS AI Engineering Course
Date: August 2025
"""

import boto3
import json
from datetime import datetime, timedelta
from typing import Dict, List
import time


class AWSCostDashboard:
    """Simple AWS cost dashboard for quick monitoring."""
    
    def __init__(self, region: str = 'us-east-1'):
        """Initialize the cost dashboard."""
        self.region = region
        
        try:
            self.cost_explorer = boto3.client('ce', region_name='us-east-1')
            self.ec2 = boto3.client('ec2', region_name=region)
            self.s3 = boto3.client('s3', region_name=region)
            print(f"✅ Connected to AWS (Region: {region})")
        except Exception as e:
            print(f"❌ Error connecting to AWS: {e}")
            raise
    
    def get_quick_summary(self) -> Dict:
        """Get a quick cost summary for today and this month."""
        today = datetime.now()
        start_of_month = datetime(today.year, today.month, 1)
        yesterday = today - timedelta(days=1)
        
        try:
            # Month-to-date costs
            mtd_response = self.cost_explorer.get_cost_and_usage(
                TimePeriod={
                    'Start': start_of_month.strftime('%Y-%m-%d'),
                    'End': today.strftime('%Y-%m-%d')
                },
                Granularity='MONTHLY',
                Metrics=['BlendedCost'],
                GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
            )
            
            # Yesterday's costs
            yesterday_response = self.cost_explorer.get_cost_and_usage(
                TimePeriod={
                    'Start': yesterday.strftime('%Y-%m-%d'),
                    'End': today.strftime('%Y-%m-%d')
                },
                Granularity='DAILY',
                Metrics=['BlendedCost'],
                GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
            )
            
            # Process responses
            mtd_total = 0.0
            mtd_services = {}
            
            for result in mtd_response.get('ResultsByTime', []):
                for group in result.get('Groups', []):
                    service = group['Keys'][0]
                    cost = float(group['Metrics']['BlendedCost']['Amount'])
                    mtd_services[service] = cost
                    mtd_total += cost
            
            yesterday_total = 0.0
            yesterday_services = {}
            
            for result in yesterday_response.get('ResultsByTime', []):
                for group in result.get('Groups', []):
                    service = group['Keys'][0]
                    cost = float(group['Metrics']['BlendedCost']['Amount'])
                    yesterday_services[service] = cost
                    yesterday_total += cost
            
            return {
                'month_to_date': {
                    'total': mtd_total,
                    'services': mtd_services,
                    'days_elapsed': today.day
                },
                'yesterday': {
                    'total': yesterday_total,
                    'services': yesterday_services
                },
                'daily_average': mtd_total / today.day if today.day > 0 else 0
            }
            
        except Exception as e:
            print(f"❌ Error getting cost summary: {e}")
            return {}
    
    def get_resource_counts(self) -> Dict:
        """Get quick counts of key resources."""
        resources = {
            'ec2_instances': {'running': 0, 'stopped': 0, 'total': 0},
            's3_buckets': {'count': 0, 'total_size_gb': 0},
            'region': self.region
        }
        
        # EC2 instances
        try:
            ec2_response = self.ec2.describe_instances()
            for reservation in ec2_response['Reservations']:
                for instance in reservation['Instances']:
                    resources['ec2_instances']['total'] += 1
                    if instance['State']['Name'] == 'running':
                        resources['ec2_instances']['running'] += 1
                    elif instance['State']['Name'] == 'stopped':
                        resources['ec2_instances']['stopped'] += 1
        except Exception as e:
            print(f"⚠️  Could not get EC2 data: {e}")
        
        # S3 buckets (basic count only for speed)
        try:
            s3_response = self.s3.list_buckets()
            resources['s3_buckets']['count'] = len(s3_response.get('Buckets', []))
        except Exception as e:
            print(f"⚠️  Could not get S3 data: {e}")
        
        return resources
    
    def display_dashboard(self) -> None:
        """Display a simple cost dashboard."""
        print("\n" + "=" * 60)
        print("💰 AWS COST DASHBOARD")
        print("=" * 60)
        print(f"🕐 Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🌍 Region: {self.region}")
        
        # Get cost summary
        print("\n📊 COST SUMMARY")
        print("-" * 30)
        
        summary = self.get_quick_summary()
        if summary:
            mtd = summary['month_to_date']
            yesterday = summary['yesterday']
            
            print(f"💳 Month-to-Date: ${mtd['total']:.2f}")
            print(f"📅 Yesterday: ${yesterday['total']:.2f}")
            print(f"📈 Daily Average: ${summary['daily_average']:.2f}")
            print(f"📆 Days Elapsed: {mtd['days_elapsed']}")
            
            # Top services this month
            if mtd['services']:
                top_services = sorted(mtd['services'].items(), key=lambda x: x[1], reverse=True)[:5]
                print(f"\n🏆 Top Services (MTD):")
                for i, (service, cost) in enumerate(top_services, 1):
                    if cost > 0:
                        percentage = (cost / mtd['total']) * 100 if mtd['total'] > 0 else 0
                        print(f"  {i}. {service:<30} ${cost:>6.2f} ({percentage:>4.1f}%)")
        
        # Get resource counts
        print(f"\n🔧 RESOURCE OVERVIEW")
        print("-" * 30)
        
        resources = self.get_resource_counts()
        
        print(f"🖥️  EC2 Instances:")
        print(f"   Total: {resources['ec2_instances']['total']}")
        print(f"   Running: {resources['ec2_instances']['running']}")
        print(f"   Stopped: {resources['ec2_instances']['stopped']}")
        
        print(f"📦 S3 Buckets: {resources['s3_buckets']['count']}")
        
        # Quick alerts
        print(f"\n⚠️  ALERTS")
        print("-" * 30)
        
        alerts = []
        
        if summary and summary['daily_average'] > 5.0:
            alerts.append(f"High daily spend: ${summary['daily_average']:.2f}/day")
        
        if resources['ec2_instances']['stopped'] > 0:
            alerts.append(f"{resources['ec2_instances']['stopped']} stopped EC2 instances (still incurring EBS costs)")
        
        if summary and summary['month_to_date']['total'] > 50.0:
            alerts.append(f"Month-to-date costs exceed $50")
        
        if not alerts:
            alerts.append("✅ No cost alerts")
        
        for alert in alerts:
            print(f"  • {alert}")
        
        print("\n" + "=" * 60)
    
    def save_daily_snapshot(self) -> str:
        """Save a daily cost snapshot for tracking."""
        today = datetime.now().strftime('%Y-%m-%d')
        filename = f"daily_cost_snapshot_{today}.json"
        
        try:
            snapshot = {
                'date': today,
                'timestamp': datetime.now().isoformat(),
                'region': self.region,
                'summary': self.get_quick_summary(),
                'resources': self.get_resource_counts()
            }
            
            with open(filename, 'w') as f:
                json.dump(snapshot, f, indent=2, default=str)
            
            print(f"📸 Daily snapshot saved: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ Could not save snapshot: {e}")
            return ""


def monitor_mode():
    """Continuous monitoring mode - updates every 5 minutes."""
    dashboard = AWSCostDashboard()
    
    print("🔄 Starting continuous monitoring mode...")
    print("   Updates every 5 minutes. Press Ctrl+C to stop.")
    
    try:
        while True:
            dashboard.display_dashboard()
            print(f"\n⏳ Next update in 5 minutes... (Ctrl+C to stop)")
            time.sleep(300)  # 5 minutes
            
    except KeyboardInterrupt:
        print(f"\n👋 Monitoring stopped.")


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='AWS Cost Dashboard')
    parser.add_argument('--region', '-r', type=str, default='us-east-1', help='AWS region')
    parser.add_argument('--monitor', '-m', action='store_true', help='Continuous monitoring mode')
    parser.add_argument('--snapshot', '-s', action='store_true', help='Save daily snapshot')
    
    args = parser.parse_args()
    
    try:
        dashboard = AWSCostDashboard(region=args.region)
        
        if args.monitor:
            monitor_mode()
        else:
            dashboard.display_dashboard()
            
            if args.snapshot:
                dashboard.save_daily_snapshot()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

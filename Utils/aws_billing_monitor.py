#!/usr/bin/env python3
"""
Comprehensive AWS Billing Monitor

This utility provides complete visibility into your AWS spending across all services
including Bedrock, EC2, S3, AgentCore, and any other AWS services you're using.

Author: AWS AI Engineering Course
Date: August 2025
"""

import boto3
import json
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from decimal import Decimal
import pandas as pd


class AWSBillingMonitor:
    """Comprehensive AWS billing and usage monitor across all services."""
    
    def __init__(self, region_name: str = 'us-east-1'):
        """Initialize the billing monitor."""
        self.region = region_name
        
        # Initialize AWS clients
        try:
            self.cost_explorer = boto3.client('ce', region_name='us-east-1')  # CE is only in us-east-1
            self.cloudwatch = boto3.client('cloudwatch', region_name=region_name)
            self.ec2 = boto3.client('ec2', region_name=region_name)
            self.s3 = boto3.client('s3', region_name=region_name)
            self.bedrock = boto3.client('bedrock', region_name=region_name)
            self.pricing = boto3.client('pricing', region_name='us-east-1')  # Pricing API only in us-east-1
            
            print(f"✅ Initialized AWS clients for region: {region_name}")
        except Exception as e:
            print(f"❌ Error initializing AWS clients: {e}")
            raise
    
    def get_overall_costs(self, days: int = 30) -> Dict[str, Any]:
        """
        Get overall AWS costs for the specified period.
        
        Args:
            days (int): Number of days to analyze
            
        Returns:
            Dict containing cost breakdown by service
        """
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        try:
            response = self.cost_explorer.get_cost_and_usage(
                TimePeriod={
                    'Start': start_date,
                    'End': end_date
                },
                Granularity='DAILY',
                Metrics=['BlendedCost', 'UnblendedCost', 'UsageQuantity'],
                GroupBy=[
                    {
                        'Type': 'DIMENSION',
                        'Key': 'SERVICE'
                    }
                ]
            )
            
            return self._process_cost_response(response)
            
        except Exception as e:
            print(f"❌ Error getting cost data: {e}")
            return {}
    
    def get_service_specific_costs(self, days: int = 30) -> Dict[str, Any]:
        """Get detailed costs for specific AWS services."""
        services_of_interest = [
            'Amazon Bedrock',
            'Amazon Elastic Compute Cloud - Compute',
            'Amazon Simple Storage Service',
            'AWS Agent Core',  # This might appear differently in billing
            'Amazon CloudWatch',
            'Amazon Virtual Private Cloud',
            'AWS Key Management Service',
            'AWS Identity and Access Management',
            'AWS CloudTrail',
            'Amazon Route 53'
        ]
        
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        service_costs = {}
        
        for service in services_of_interest:
            try:
                response = self.cost_explorer.get_cost_and_usage(
                    TimePeriod={
                        'Start': start_date,
                        'End': end_date
                    },
                    Granularity='MONTHLY',
                    Metrics=['BlendedCost'],
                    GroupBy=[
                        {
                            'Type': 'DIMENSION',
                            'Key': 'USAGE_TYPE'
                        }
                    ],
                    Filter={
                        'Dimensions': {
                            'Key': 'SERVICE',
                            'Values': [service]
                        }
                    }
                )
                
                service_costs[service] = self._process_service_cost_response(response)
                
            except Exception as e:
                print(f"⚠️  Could not get costs for {service}: {e}")
                service_costs[service] = {'total_cost': 0.0, 'usage_details': []}
        
        return service_costs
    
    def get_ec2_usage_details(self) -> Dict[str, Any]:
        """Get detailed EC2 usage and costs."""
        try:
            # Get EC2 instances
            instances_response = self.ec2.describe_instances()
            
            instances = []
            for reservation in instances_response['Reservations']:
                for instance in reservation['Instances']:
                    instance_info = {
                        'instance_id': instance['InstanceId'],
                        'instance_type': instance['InstanceType'],
                        'state': instance['State']['Name'],
                        'launch_time': instance.get('LaunchTime', 'Unknown'),
                        'vpc_id': instance.get('VpcId', 'N/A'),
                        'subnet_id': instance.get('SubnetId', 'N/A'),
                        'public_ip': instance.get('PublicIpAddress', 'N/A'),
                        'private_ip': instance.get('PrivateIpAddress', 'N/A')
                    }
                    
                    # Get tags
                    tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
                    instance_info['tags'] = tags
                    instance_info['name'] = tags.get('Name', 'Unnamed')
                    
                    instances.append(instance_info)
            
            return {
                'total_instances': len(instances),
                'running_instances': len([i for i in instances if i['state'] == 'running']),
                'stopped_instances': len([i for i in instances if i['state'] == 'stopped']),
                'instances': instances
            }
            
        except Exception as e:
            print(f"❌ Error getting EC2 details: {e}")
            return {'total_instances': 0, 'instances': []}
    
    def get_s3_usage_details(self) -> Dict[str, Any]:
        """Get detailed S3 usage and costs."""
        try:
            # Get S3 buckets
            buckets_response = self.s3.list_buckets()
            
            buckets = []
            total_objects = 0
            total_size_bytes = 0
            
            for bucket in buckets_response['Buckets']:
                bucket_name = bucket['Name']
                bucket_info = {
                    'name': bucket_name,
                    'creation_date': bucket['CreationDate'],
                    'region': 'Unknown'
                }
                
                try:
                    # Get bucket region
                    location = self.s3.get_bucket_location(Bucket=bucket_name)
                    bucket_info['region'] = location.get('LocationConstraint', 'us-east-1')
                    
                    # Get bucket size (this is an approximation)
                    try:
                        objects = self.s3.list_objects_v2(Bucket=bucket_name, MaxKeys=1000)
                        bucket_objects = objects.get('KeyCount', 0)
                        bucket_size = sum(obj.get('Size', 0) for obj in objects.get('Contents', []))
                        
                        bucket_info['object_count'] = bucket_objects
                        bucket_info['size_bytes'] = bucket_size
                        bucket_info['size_gb'] = round(bucket_size / (1024**3), 3)
                        
                        total_objects += bucket_objects
                        total_size_bytes += bucket_size
                        
                    except Exception:
                        bucket_info['object_count'] = 'Access Denied'
                        bucket_info['size_bytes'] = 0
                        bucket_info['size_gb'] = 0
                
                except Exception as e:
                    bucket_info['region'] = f'Error: {e}'
                
                buckets.append(bucket_info)
            
            return {
                'total_buckets': len(buckets),
                'total_objects': total_objects,
                'total_size_gb': round(total_size_bytes / (1024**3), 3),
                'buckets': buckets
            }
            
        except Exception as e:
            print(f"❌ Error getting S3 details: {e}")
            return {'total_buckets': 0, 'buckets': []}
    
    def get_bedrock_usage_details(self) -> Dict[str, Any]:
        """Get detailed Bedrock usage."""
        try:
            # Get available models
            models_response = self.bedrock.list_foundation_models()
            
            available_models = []
            for model in models_response.get('modelSummaries', []):
                model_info = {
                    'model_id': model['modelId'],
                    'model_name': model['modelName'],
                    'provider_name': model['providerName'],
                    'input_modalities': model.get('inputModalities', []),
                    'output_modalities': model.get('outputModalities', []),
                    'inference_types': model.get('inferenceTypesSupported', [])
                }
                available_models.append(model_info)
            
            # Try to get usage metrics from CloudWatch
            try:
                end_time = datetime.now()
                start_time = end_time - timedelta(days=7)
                
                metrics_response = self.cloudwatch.get_metric_statistics(
                    Namespace='AWS/Bedrock',
                    MetricName='Invocations',
                    StartTime=start_time,
                    EndTime=end_time,
                    Period=86400,  # 1 day
                    Statistics=['Sum']
                )
                
                invocations = sum(point['Sum'] for point in metrics_response.get('Datapoints', []))
                
            except Exception:
                invocations = 'Not available'
            
            return {
                'available_models': len(available_models),
                'recent_invocations': invocations,
                'models': available_models
            }
            
        except Exception as e:
            print(f"❌ Error getting Bedrock details: {e}")
            return {'available_models': 0, 'models': []}
    
    def get_monthly_forecast(self) -> Dict[str, Any]:
        """Get cost forecast for the current month."""
        try:
            # Get forecast for the rest of the month
            today = datetime.now()
            end_of_month = datetime(today.year, today.month + 1, 1) - timedelta(days=1)
            
            response = self.cost_explorer.get_cost_forecast(
                TimePeriod={
                    'Start': today.strftime('%Y-%m-%d'),
                    'End': end_of_month.strftime('%Y-%m-%d')
                },
                Metric='BLENDED_COST',
                Granularity='MONTHLY'
            )
            
            forecast_amount = float(response['Total']['Amount'])
            
            # Get month-to-date costs
            start_of_month = datetime(today.year, today.month, 1)
            mtd_response = self.cost_explorer.get_cost_and_usage(
                TimePeriod={
                    'Start': start_of_month.strftime('%Y-%m-%d'),
                    'End': today.strftime('%Y-%m-%d')
                },
                Granularity='MONTHLY',
                Metrics=['BlendedCost']
            )
            
            mtd_cost = 0.0
            if mtd_response['ResultsByTime']:
                mtd_cost = float(mtd_response['ResultsByTime'][0]['Total']['BlendedCost']['Amount'])
            
            return {
                'month_to_date': mtd_cost,
                'forecast_remaining': forecast_amount,
                'projected_total': mtd_cost + forecast_amount,
                'days_in_month': end_of_month.day,
                'days_elapsed': today.day
            }
            
        except Exception as e:
            print(f"❌ Error getting cost forecast: {e}")
            return {}
    
    def _process_cost_response(self, response: Dict) -> Dict[str, Any]:
        """Process Cost Explorer response."""
        service_costs = {}
        total_cost = 0.0
        
        for result in response.get('ResultsByTime', []):
            for group in result.get('Groups', []):
                service_name = group['Keys'][0]
                cost = float(group['Metrics']['BlendedCost']['Amount'])
                
                if service_name not in service_costs:
                    service_costs[service_name] = 0.0
                
                service_costs[service_name] += cost
                total_cost += cost
        
        # Sort by cost (highest first)
        sorted_services = sorted(service_costs.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'total_cost': total_cost,
            'service_breakdown': dict(sorted_services),
            'top_services': sorted_services[:10]
        }
    
    def _process_service_cost_response(self, response: Dict) -> Dict[str, Any]:
        """Process service-specific cost response."""
        total_cost = 0.0
        usage_details = []
        
        for result in response.get('ResultsByTime', []):
            for group in result.get('Groups', []):
                usage_type = group['Keys'][0]
                cost = float(group['Metrics']['BlendedCost']['Amount'])
                
                if cost > 0:
                    usage_details.append({
                        'usage_type': usage_type,
                        'cost': cost
                    })
                    total_cost += cost
        
        return {
            'total_cost': total_cost,
            'usage_details': sorted(usage_details, key=lambda x: x['cost'], reverse=True)
        }
    
    def generate_comprehensive_report(self, days: int = 30) -> None:
        """Generate a comprehensive billing report."""
        print("\n" + "=" * 80)
        print("🏦 COMPREHENSIVE AWS BILLING REPORT")
        print("=" * 80)
        print(f"📅 Analysis Period: Last {days} days")
        print(f"🌍 Primary Region: {self.region}")
        print(f"⏰ Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Overall costs
        print(f"\n{'🔍 OVERALL COST ANALYSIS':<60}")
        print("-" * 60)
        
        overall_costs = self.get_overall_costs(days)
        if overall_costs:
            print(f"💰 Total Cost ({days} days): ${overall_costs['total_cost']:.2f}")
            print(f"📊 Daily Average: ${overall_costs['total_cost']/days:.2f}")
            
            print(f"\n🏆 Top Services by Cost:")
            for i, (service, cost) in enumerate(overall_costs['top_services'][:5], 1):
                percentage = (cost / overall_costs['total_cost']) * 100 if overall_costs['total_cost'] > 0 else 0
                print(f"  {i}. {service:<40} ${cost:>8.2f} ({percentage:>5.1f}%)")
        
        # Monthly forecast
        print(f"\n{'📈 MONTHLY FORECAST':<60}")
        print("-" * 60)
        
        forecast = self.get_monthly_forecast()
        if forecast:
            print(f"📅 Month-to-Date: ${forecast['month_to_date']:.2f}")
            print(f"🔮 Forecast Remaining: ${forecast['forecast_remaining']:.2f}")
            print(f"📊 Projected Monthly Total: ${forecast['projected_total']:.2f}")
            
            daily_rate = forecast['month_to_date'] / forecast['days_elapsed'] if forecast['days_elapsed'] > 0 else 0
            print(f"📈 Average Daily Spend: ${daily_rate:.2f}")
        
        # Service-specific details
        print(f"\n{'🔧 SERVICE DETAILS':<60}")
        print("-" * 60)
        
        # EC2 Details
        ec2_details = self.get_ec2_usage_details()
        print(f"\n🖥️  EC2 - Elastic Compute Cloud:")
        print(f"   Total Instances: {ec2_details['total_instances']}")
        print(f"   Running: {ec2_details['running_instances']}")
        print(f"   Stopped: {ec2_details['stopped_instances']}")
        
        if ec2_details['instances']:
            print("   Recent Instances:")
            for instance in ec2_details['instances'][:3]:
                print(f"     • {instance['name']} ({instance['instance_id']}) - {instance['instance_type']} - {instance['state']}")
        
        # S3 Details
        s3_details = self.get_s3_usage_details()
        print(f"\n📦 S3 - Simple Storage Service:")
        print(f"   Total Buckets: {s3_details['total_buckets']}")
        print(f"   Total Objects: {s3_details['total_objects']}")
        print(f"   Total Storage: {s3_details['total_size_gb']} GB")
        
        if s3_details['buckets']:
            print("   Recent Buckets:")
            for bucket in s3_details['buckets'][:3]:
                print(f"     • {bucket['name']} - {bucket['size_gb']} GB ({bucket['object_count']} objects)")
        
        # Bedrock Details
        bedrock_details = self.get_bedrock_usage_details()
        print(f"\n🤖 Bedrock - AI Foundation Models:")
        print(f"   Available Models: {bedrock_details['available_models']}")
        print(f"   Recent Invocations: {bedrock_details['recent_invocations']}")
        
        if bedrock_details['models']:
            print("   Available Models:")
            for model in bedrock_details['models'][:5]:
                print(f"     • {model['model_id']} ({model['provider_name']})")
        
        # Service-specific costs
        print(f"\n{'💳 DETAILED SERVICE COSTS':<60}")
        print("-" * 60)
        
        service_costs = self.get_service_specific_costs(days)
        for service, details in service_costs.items():
            if details['total_cost'] > 0:
                print(f"\n💰 {service}: ${details['total_cost']:.4f}")
                for usage in details['usage_details'][:3]:
                    print(f"     • {usage['usage_type']}: ${usage['cost']:.4f}")
        
        # Cost optimization recommendations
        print(f"\n{'💡 COST OPTIMIZATION RECOMMENDATIONS':<60}")
        print("-" * 60)
        
        self._generate_recommendations(overall_costs, ec2_details, s3_details, bedrock_details)
        
        print("\n" + "=" * 80)
    
    def _generate_recommendations(self, costs: Dict, ec2: Dict, s3: Dict, bedrock: Dict) -> None:
        """Generate cost optimization recommendations."""
        recommendations = []
        
        # EC2 recommendations
        if ec2.get('stopped_instances', 0) > 0:
            recommendations.append(f"🖥️  Consider terminating {ec2['stopped_instances']} stopped EC2 instances to avoid EBS storage charges")
        
        if ec2.get('running_instances', 0) > 5:
            recommendations.append("🖥️  Review EC2 instance types - consider using Spot instances for non-critical workloads")
        
        # S3 recommendations
        if s3.get('total_size_gb', 0) > 100:
            recommendations.append("📦 Consider S3 Intelligent Tiering for automatic cost optimization of large storage")
        
        # Bedrock recommendations
        if costs.get('total_cost', 0) > 0:
            for service, cost in costs.get('service_breakdown', {}).items():
                if 'bedrock' in service.lower() and cost > 10:
                    recommendations.append("🤖 High Bedrock usage detected - consider using Nova Lite model for development/testing")
        
        # General recommendations
        recommendations.extend([
            "📊 Set up CloudWatch billing alerts for proactive cost monitoring",
            "🔍 Review AWS Cost Explorer regularly for spending patterns",
            "🎯 Use AWS Budgets to set spending limits",
            "📋 Tag resources properly for better cost allocation"
        ])
        
        for i, rec in enumerate(recommendations[:8], 1):
            print(f"  {i}. {rec}")
    
    def export_report(self, filename: Optional[str] = None, days: int = 30) -> str:
        """Export billing report to JSON file."""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"aws_billing_report_{timestamp}.json"
        
        try:
            report_data = {
                'report_date': datetime.now().isoformat(),
                'analysis_period_days': days,
                'region': self.region,
                'overall_costs': self.get_overall_costs(days),
                'monthly_forecast': self.get_monthly_forecast(),
                'ec2_details': self.get_ec2_usage_details(),
                's3_details': self.get_s3_usage_details(),
                'bedrock_details': self.get_bedrock_usage_details(),
                'service_costs': self.get_service_specific_costs(days)
            }
            
            with open(filename, 'w') as f:
                json.dump(report_data, f, indent=2, default=str)
            
            print(f"📁 Report exported to: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ Export failed: {e}")
            return ""


def main():
    """Main function to run the billing monitor."""
    parser = argparse.ArgumentParser(description='Comprehensive AWS Billing Monitor')
    parser.add_argument('--days', '-d', type=int, default=30, help='Number of days to analyze (default: 30)')
    parser.add_argument('--region', '-r', type=str, default='us-east-1', help='AWS region (default: us-east-1)')
    parser.add_argument('--export', '-e', action='store_true', help='Export report to JSON file')
    parser.add_argument('--quiet', '-q', action='store_true', help='Minimal output (summary only)')
    
    args = parser.parse_args()
    
    try:
        monitor = AWSBillingMonitor(region_name=args.region)
        
        if args.quiet:
            # Quick summary
            costs = monitor.get_overall_costs(args.days)
            forecast = monitor.get_monthly_forecast()
            
            print(f"💰 {args.days}-day total: ${costs.get('total_cost', 0):.2f}")
            print(f"📊 Monthly projection: ${forecast.get('projected_total', 0):.2f}")
        else:
            # Full report
            monitor.generate_comprehensive_report(args.days)
        
        if args.export:
            monitor.export_report(days=args.days)
            
    except Exception as e:
        print(f"❌ Error running billing monitor: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

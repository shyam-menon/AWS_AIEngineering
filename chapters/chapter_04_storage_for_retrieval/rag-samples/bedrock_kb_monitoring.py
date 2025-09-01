#!/usr/bin/env python3
"""
AWS Bedrock Knowledge Base Monitoring and Optimization

This module demonstrates comprehensive monitoring capabilities for AWS Bedrock Knowledge Bases
using CloudWatch metrics, custom dashboards, and automated alerting.

Features:
- Real-time performance monitoring
- Custom CloudWatch dashboards
- Automated alerting and notifications
- Cost optimization tracking
- Query performance analysis
- Ingestion monitoring
- Error tracking and debugging

Usage:
    python bedrock_kb_monitoring.py --knowledge-base-id YOUR_KB_ID
    python bedrock_kb_monitoring.py --setup-monitoring
    python bedrock_kb_monitoring.py --create-dashboard
"""

import boto3
import json
import time
import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from common import load_environment, print_info, print_error, print_success

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class MonitoringConfig:
    """Configuration for monitoring setup"""
    knowledge_base_id: str
    sns_topic_arn: Optional[str] = None
    dashboard_name: str = "BedrockKnowledgeBase-Monitoring"
    alarm_prefix: str = "BedrockKB"
    region: str = "us-east-1"


class BedrockKnowledgeBaseMonitor:
    """
    Comprehensive monitoring for AWS Bedrock Knowledge Bases
    """
    
    def __init__(self, config: MonitoringConfig):
        self.config = config
        self.bedrock_agent = boto3.client('bedrock-agent', region_name=config.region)
        self.bedrock_agent_runtime = boto3.client('bedrock-agent-runtime', region_name=config.region)
        self.cloudwatch = boto3.client('cloudwatch', region_name=config.region)
        self.logs = boto3.client('logs', region_name=config.region)
        
    def setup_comprehensive_monitoring(self) -> Dict[str, Any]:
        """
        Set up comprehensive monitoring for Bedrock Knowledge Base
        """
        print_info("🔧 Setting up comprehensive monitoring...")
        
        results = {
            "dashboards": [],
            "alarms": [],
            "log_groups": [],
            "metrics": []
        }
        
        try:
            # 1. Create custom dashboard
            dashboard_result = self.create_monitoring_dashboard()
            results["dashboards"].append(dashboard_result)
            
            # 2. Set up CloudWatch alarms
            alarm_results = self.setup_cloudwatch_alarms()
            results["alarms"].extend(alarm_results)
            
            # 3. Configure log monitoring
            log_result = self.setup_log_monitoring()
            results["log_groups"].append(log_result)
            
            # 4. Set up custom metrics
            metric_results = self.setup_custom_metrics()
            results["metrics"].extend(metric_results)
            
            print_success("✅ Comprehensive monitoring setup complete!")
            return results
            
        except Exception as e:
            print_error(f"❌ Error setting up monitoring: {str(e)}")
            raise
    
    def create_monitoring_dashboard(self) -> Dict[str, Any]:
        """
        Create a comprehensive CloudWatch dashboard for Knowledge Base monitoring
        """
        print_info("📊 Creating CloudWatch dashboard...")
        
        # Dashboard configuration
        dashboard_body = {
            "widgets": [
                # Query Performance Widget
                {
                    "type": "metric",
                    "x": 0, "y": 0, "width": 12, "height": 6,
                    "properties": {
                        "metrics": [
                            ["AWS/Bedrock", "QueryLatency", "KnowledgeBaseId", self.config.knowledge_base_id],
                            [".", "QueryCount", ".", "."],
                            [".", "QueryErrors", ".", "."]
                        ],
                        "view": "timeSeries",
                        "stacked": False,
                        "region": self.config.region,
                        "title": "Query Performance Metrics",
                        "period": 300,
                        "stat": "Average"
                    }
                },
                
                # Ingestion Monitoring Widget
                {
                    "type": "metric",
                    "x": 12, "y": 0, "width": 12, "height": 6,
                    "properties": {
                        "metrics": [
                            ["AWS/Bedrock", "IngestionJobDuration", "KnowledgeBaseId", self.config.knowledge_base_id],
                            [".", "DocumentsProcessed", ".", "."],
                            [".", "IngestionErrors", ".", "."]
                        ],
                        "view": "timeSeries",
                        "stacked": False,
                        "region": self.config.region,
                        "title": "Ingestion Performance",
                        "period": 300
                    }
                },
                
                # Storage and Vector Metrics
                {
                    "type": "metric",
                    "x": 0, "y": 6, "width": 12, "height": 6,
                    "properties": {
                        "metrics": [
                            ["AWS/OpenSearchServerless", "IndexingRate", "CollectionName", f"bedrock-kb-{self.config.knowledge_base_id}"],
                            [".", "SearchLatency", ".", "."],
                            [".", "IndexUtilization", ".", "."]
                        ],
                        "view": "timeSeries",
                        "stacked": False,
                        "region": self.config.region,
                        "title": "Vector Storage Metrics",
                        "period": 300
                    }
                },
                
                # Cost Tracking Widget
                {
                    "type": "metric",
                    "x": 12, "y": 6, "width": 12, "height": 6,
                    "properties": {
                        "metrics": [
                            ["AWS/Billing", "EstimatedCharges", "ServiceName", "AmazonBedrock", "Currency", "USD"],
                            [".", ".", ".", "AmazonOpenSearchServerless", ".", "."]
                        ],
                        "view": "timeSeries",
                        "stacked": True,
                        "region": "us-east-1",  # Billing metrics are only in us-east-1
                        "title": "Estimated Costs",
                        "period": 86400
                    }
                },
                
                # Error Rate Widget
                {
                    "type": "metric",
                    "x": 0, "y": 12, "width": 24, "height": 6,
                    "properties": {
                        "metrics": [
                            ["AWS/Bedrock", "QueryErrors", "KnowledgeBaseId", self.config.knowledge_base_id],
                            [".", "IngestionErrors", ".", "."],
                            [".", "RetrievalErrors", ".", "."]
                        ],
                        "view": "timeSeries",
                        "stacked": False,
                        "region": self.config.region,
                        "title": "Error Rates and Failure Analysis",
                        "period": 300,
                        "stat": "Sum"
                    }
                }
            ]
        }
        
        try:
            response = self.cloudwatch.put_dashboard(
                DashboardName=self.config.dashboard_name,
                DashboardBody=json.dumps(dashboard_body)
            )
            
            dashboard_url = f"https://{self.config.region}.console.aws.amazon.com/cloudwatch/home?region={self.config.region}#dashboards:name={self.config.dashboard_name}"
            
            print_success(f"✅ Dashboard created: {self.config.dashboard_name}")
            print_info(f"🔗 Dashboard URL: {dashboard_url}")
            
            return {
                "dashboard_name": self.config.dashboard_name,
                "dashboard_url": dashboard_url,
                "response": response
            }
            
        except Exception as e:
            print_error(f"❌ Error creating dashboard: {str(e)}")
            raise
    
    def setup_cloudwatch_alarms(self) -> List[Dict[str, Any]]:
        """
        Set up CloudWatch alarms for monitoring critical metrics
        """
        print_info("🚨 Setting up CloudWatch alarms...")
        
        alarms_config = [
            {
                "name": f"{self.config.alarm_prefix}-HighQueryLatency",
                "description": "Alert when query latency is high",
                "metric_name": "QueryLatency",
                "namespace": "AWS/Bedrock",
                "statistic": "Average",
                "threshold": 5000,  # 5 seconds
                "comparison_operator": "GreaterThanThreshold",
                "evaluation_periods": 2,
                "period": 300
            },
            {
                "name": f"{self.config.alarm_prefix}-HighErrorRate",
                "description": "Alert when error rate is high",
                "metric_name": "QueryErrors",
                "namespace": "AWS/Bedrock",
                "statistic": "Sum",
                "threshold": 10,
                "comparison_operator": "GreaterThanThreshold",
                "evaluation_periods": 2,
                "period": 300
            },
            {
                "name": f"{self.config.alarm_prefix}-IngestionFailures",
                "description": "Alert when ingestion jobs fail",
                "metric_name": "IngestionErrors",
                "namespace": "AWS/Bedrock",
                "statistic": "Sum",
                "threshold": 5,
                "comparison_operator": "GreaterThanThreshold",
                "evaluation_periods": 1,
                "period": 900
            },
            {
                "name": f"{self.config.alarm_prefix}-LowQueryVolume",
                "description": "Alert when query volume is unexpectedly low",
                "metric_name": "QueryCount",
                "namespace": "AWS/Bedrock",
                "statistic": "Sum",
                "threshold": 1,
                "comparison_operator": "LessThanThreshold",
                "evaluation_periods": 3,
                "period": 900,
                "treat_missing_data": "breaching"
            }
        ]
        
        created_alarms = []
        
        for alarm_config in alarms_config:
            try:
                alarm_kwargs = {
                    "AlarmName": alarm_config["name"],
                    "AlarmDescription": alarm_config["description"],
                    "ComparisonOperator": alarm_config["comparison_operator"],
                    "EvaluationPeriods": alarm_config["evaluation_periods"],
                    "MetricName": alarm_config["metric_name"],
                    "Namespace": alarm_config["namespace"],
                    "Period": alarm_config["period"],
                    "Statistic": alarm_config["statistic"],
                    "Threshold": alarm_config["threshold"],
                    "Dimensions": [
                        {
                            "Name": "KnowledgeBaseId",
                            "Value": self.config.knowledge_base_id
                        }
                    ]
                }
                
                # Add SNS topic if configured
                if self.config.sns_topic_arn:
                    alarm_kwargs["AlarmActions"] = [self.config.sns_topic_arn]
                    alarm_kwargs["OKActions"] = [self.config.sns_topic_arn]
                
                # Add treat missing data if specified
                if "treat_missing_data" in alarm_config:
                    alarm_kwargs["TreatMissingData"] = alarm_config["treat_missing_data"]
                
                response = self.cloudwatch.put_metric_alarm(**alarm_kwargs)
                
                created_alarms.append({
                    "alarm_name": alarm_config["name"],
                    "metric": alarm_config["metric_name"],
                    "threshold": alarm_config["threshold"],
                    "response": response
                })
                
                print_success(f"✅ Created alarm: {alarm_config['name']}")
                
            except Exception as e:
                print_error(f"❌ Error creating alarm {alarm_config['name']}: {str(e)}")
        
        return created_alarms
    
    def setup_log_monitoring(self) -> Dict[str, Any]:
        """
        Set up log monitoring for detailed debugging
        """
        print_info("📝 Setting up log monitoring...")
        
        log_group_name = f"/aws/bedrock/knowledgebase/{self.config.knowledge_base_id}"
        
        try:
            # Create log group if it doesn't exist
            try:
                self.logs.create_log_group(logGroupName=log_group_name)
                print_success(f"✅ Created log group: {log_group_name}")
            except self.logs.exceptions.ResourceAlreadyExistsException:
                print_info(f"ℹ️ Log group already exists: {log_group_name}")
            
            # Set retention policy
            self.logs.put_retention_policy(
                logGroupName=log_group_name,
                retentionInDays=30
            )
            
            # Create metric filters for error tracking
            metric_filters = [
                {
                    "filter_name": "ErrorFilter",
                    "filter_pattern": "[timestamp, request_id, level=\"ERROR\", ...]",
                    "metric_name": "ErrorCount",
                    "metric_namespace": f"BedrockKB/{self.config.knowledge_base_id}",
                    "metric_value": "1"
                },
                {
                    "filter_name": "LatencyFilter",
                    "filter_pattern": "[timestamp, request_id, level, latency > 1000, ...]",
                    "metric_name": "HighLatencyRequests",
                    "metric_namespace": f"BedrockKB/{self.config.knowledge_base_id}",
                    "metric_value": "1"
                }
            ]
            
            for filter_config in metric_filters:
                try:
                    self.logs.put_metric_filter(
                        logGroupName=log_group_name,
                        filterName=filter_config["filter_name"],
                        filterPattern=filter_config["filter_pattern"],
                        metricTransformations=[
                            {
                                "metricName": filter_config["metric_name"],
                                "metricNamespace": filter_config["metric_namespace"],
                                "metricValue": filter_config["metric_value"]
                            }
                        ]
                    )
                    print_success(f"✅ Created metric filter: {filter_config['filter_name']}")
                except Exception as e:
                    print_error(f"❌ Error creating metric filter {filter_config['filter_name']}: {str(e)}")
            
            return {
                "log_group_name": log_group_name,
                "metric_filters": metric_filters
            }
            
        except Exception as e:
            print_error(f"❌ Error setting up log monitoring: {str(e)}")
            raise
    
    def setup_custom_metrics(self) -> List[Dict[str, Any]]:
        """
        Set up custom metrics for additional monitoring
        """
        print_info("📈 Setting up custom metrics...")
        
        custom_metrics = []
        
        try:
            # Custom metric for query success rate
            success_rate_metric = {
                "namespace": f"BedrockKB/{self.config.knowledge_base_id}",
                "metric_name": "QuerySuccessRate",
                "description": "Percentage of successful queries"
            }
            
            # Custom metric for average response quality (would need to be populated by application)
            quality_metric = {
                "namespace": f"BedrockKB/{self.config.knowledge_base_id}",
                "metric_name": "ResponseQuality",
                "description": "Average response quality score"
            }
            
            # Custom metric for token usage
            token_usage_metric = {
                "namespace": f"BedrockKB/{self.config.knowledge_base_id}",
                "metric_name": "TokenUsage",
                "description": "Total tokens consumed"
            }
            
            custom_metrics.extend([success_rate_metric, quality_metric, token_usage_metric])
            
            print_success(f"✅ Configured {len(custom_metrics)} custom metrics")
            return custom_metrics
            
        except Exception as e:
            print_error(f"❌ Error setting up custom metrics: {str(e)}")
            raise
    
    def get_performance_metrics(self, hours: int = 24) -> Dict[str, Any]:
        """
        Retrieve performance metrics for the specified time period
        """
        print_info(f"📊 Retrieving performance metrics for last {hours} hours...")
        
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(hours=hours)
        
        metrics_to_fetch = [
            {
                "name": "QueryLatency",
                "namespace": "AWS/Bedrock",
                "statistic": "Average"
            },
            {
                "name": "QueryCount",
                "namespace": "AWS/Bedrock",
                "statistic": "Sum"
            },
            {
                "name": "QueryErrors",
                "namespace": "AWS/Bedrock",
                "statistic": "Sum"
            },
            {
                "name": "IngestionJobDuration",
                "namespace": "AWS/Bedrock",
                "statistic": "Average"
            }
        ]
        
        metrics_data = {}
        
        for metric in metrics_to_fetch:
            try:
                response = self.cloudwatch.get_metric_statistics(
                    Namespace=metric["namespace"],
                    MetricName=metric["name"],
                    Dimensions=[
                        {
                            "Name": "KnowledgeBaseId",
                            "Value": self.config.knowledge_base_id
                        }
                    ],
                    StartTime=start_time,
                    EndTime=end_time,
                    Period=3600,  # 1 hour periods
                    Statistics=[metric["statistic"]]
                )
                
                metrics_data[metric["name"]] = {
                    "datapoints": response["Datapoints"],
                    "statistic": metric["statistic"]
                }
                
            except Exception as e:
                print_error(f"❌ Error fetching {metric['name']}: {str(e)}")
                metrics_data[metric["name"]] = {"error": str(e)}
        
        return metrics_data
    
    def analyze_performance(self, metrics_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze performance metrics and provide insights
        """
        print_info("🔍 Analyzing performance metrics...")
        
        analysis = {
            "summary": {},
            "recommendations": [],
            "alerts": []
        }
        
        try:
            # Analyze query latency
            if "QueryLatency" in metrics_data and metrics_data["QueryLatency"].get("datapoints"):
                latency_points = metrics_data["QueryLatency"]["datapoints"]
                avg_latency = sum(point["Average"] for point in latency_points) / len(latency_points)
                max_latency = max(point["Average"] for point in latency_points)
                
                analysis["summary"]["average_latency_ms"] = round(avg_latency, 2)
                analysis["summary"]["max_latency_ms"] = round(max_latency, 2)
                
                if avg_latency > 3000:  # 3 seconds
                    analysis["alerts"].append("High average query latency detected")
                    analysis["recommendations"].append("Consider optimizing vector index or upgrading OpenSearch capacity")
            
            # Analyze query volume
            if "QueryCount" in metrics_data and metrics_data["QueryCount"].get("datapoints"):
                query_points = metrics_data["QueryCount"]["datapoints"]
                total_queries = sum(point["Sum"] for point in query_points)
                avg_queries_per_hour = total_queries / len(query_points) if query_points else 0
                
                analysis["summary"]["total_queries"] = total_queries
                analysis["summary"]["avg_queries_per_hour"] = round(avg_queries_per_hour, 2)
                
                if avg_queries_per_hour < 1:
                    analysis["alerts"].append("Low query volume detected")
            
            # Analyze error rate
            if "QueryErrors" in metrics_data and metrics_data["QueryErrors"].get("datapoints"):
                error_points = metrics_data["QueryErrors"]["datapoints"]
                total_errors = sum(point["Sum"] for point in error_points)
                
                analysis["summary"]["total_errors"] = total_errors
                
                if total_errors > 0:
                    error_rate = (total_errors / analysis["summary"].get("total_queries", 1)) * 100
                    analysis["summary"]["error_rate_percent"] = round(error_rate, 2)
                    
                    if error_rate > 5:  # 5% error rate
                        analysis["alerts"].append("High error rate detected")
                        analysis["recommendations"].append("Check knowledge base configuration and data quality")
            
            # Generate performance score
            score = 100
            if analysis["summary"].get("average_latency_ms", 0) > 2000:
                score -= 20
            if analysis["summary"].get("error_rate_percent", 0) > 2:
                score -= 30
            if analysis["summary"].get("avg_queries_per_hour", 0) < 5:
                score -= 10
            
            analysis["performance_score"] = max(0, score)
            
            return analysis
            
        except Exception as e:
            print_error(f"❌ Error analyzing performance: {str(e)}")
            return {"error": str(e)}
    
    def generate_monitoring_report(self, hours: int = 24) -> Dict[str, Any]:
        """
        Generate a comprehensive monitoring report
        """
        print_info("📋 Generating monitoring report...")
        
        try:
            # Get metrics data
            metrics_data = self.get_performance_metrics(hours)
            
            # Analyze performance
            analysis = self.analyze_performance(metrics_data)
            
            # Get knowledge base info
            kb_info = self.bedrock_agent.get_knowledge_base(
                knowledgeBaseId=self.config.knowledge_base_id
            )
            
            report = {
                "timestamp": datetime.utcnow().isoformat(),
                "knowledge_base_id": self.config.knowledge_base_id,
                "knowledge_base_name": kb_info["knowledgeBase"]["name"],
                "monitoring_period_hours": hours,
                "metrics_data": metrics_data,
                "performance_analysis": analysis,
                "dashboard_url": f"https://{self.config.region}.console.aws.amazon.com/cloudwatch/home?region={self.config.region}#dashboards:name={self.config.dashboard_name}"
            }
            
            print_success("✅ Monitoring report generated successfully")
            return report
            
        except Exception as e:
            print_error(f"❌ Error generating report: {str(e)}")
            raise
    
    def publish_custom_metric(self, metric_name: str, value: float, unit: str = "Count", **dimensions) -> None:
        """
        Publish a custom metric to CloudWatch
        """
        try:
            self.cloudwatch.put_metric_data(
                Namespace=f"BedrockKB/{self.config.knowledge_base_id}",
                MetricData=[
                    {
                        "MetricName": metric_name,
                        "Value": value,
                        "Unit": unit,
                        "Dimensions": [
                            {"Name": k, "Value": v} for k, v in dimensions.items()
                        ]
                    }
                ]
            )
            
        except Exception as e:
            print_error(f"❌ Error publishing metric {metric_name}: {str(e)}")


def main():
    """
    Main function demonstrating monitoring setup and usage
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="AWS Bedrock Knowledge Base Monitoring")
    parser.add_argument("--knowledge-base-id", help="Knowledge Base ID to monitor")
    parser.add_argument("--setup-monitoring", action="store_true", help="Set up comprehensive monitoring")
    parser.add_argument("--create-dashboard", action="store_true", help="Create CloudWatch dashboard")
    parser.add_argument("--performance-report", action="store_true", help="Generate performance report")
    parser.add_argument("--status", action="store_true", help="Check monitoring status")
    parser.add_argument("--cleanup", action="store_true", help="Clean up monitoring resources")
    parser.add_argument("--hours", type=int, default=24, help="Hours of data for reports (default: 24)")
    
    args = parser.parse_args()
    
    print_info("🚀 AWS Bedrock Knowledge Base Monitoring")
    
    # Load environment
    env_vars = load_environment()
    
    # Configuration
    knowledge_base_id = args.knowledge_base_id or env_vars.get("KNOWLEDGE_BASE_ID", "YOUR_KB_ID_HERE")
    
    if knowledge_base_id == "YOUR_KB_ID_HERE":
        print_error("❌ Please provide --knowledge-base-id or set KNOWLEDGE_BASE_ID in your .env file")
        return
    
    config = MonitoringConfig(
        knowledge_base_id=knowledge_base_id,
        sns_topic_arn=env_vars.get("SNS_TOPIC_ARN"),
        region=env_vars.get("AWS_REGION", "us-east-1")
    )
    
    # Initialize monitor
    monitor = BedrockKnowledgeBaseMonitor(config)
    
    try:
        if args.setup_monitoring:
            print_info("\n=== Setting Up Comprehensive Monitoring ===")
            setup_results = monitor.setup_comprehensive_monitoring()
            print(f"📊 Setup Results: {json.dumps(setup_results, indent=2, default=str)}")
            
        elif args.create_dashboard:
            print_info("\n=== Creating CloudWatch Dashboard ===")
            dashboard_result = monitor.create_monitoring_dashboard()
            print(f"📈 Dashboard: {json.dumps(dashboard_result, indent=2, default=str)}")
            
        elif args.performance_report:
            print_info("\n=== Generating Performance Report ===")
            report = monitor.generate_monitoring_report(hours=args.hours)
            
            # Display summary
            print_info("\n=== Performance Summary ===")
            if "performance_analysis" in report and "summary" in report["performance_analysis"]:
                summary = report["performance_analysis"]["summary"]
                score = report["performance_analysis"].get("performance_score", "N/A")
                
                print(f"📈 Performance Score: {score}/100")
                print(f"⏱️  Average Latency: {summary.get('average_latency_ms', 'N/A')} ms")
                print(f"📊 Total Queries: {summary.get('total_queries', 'N/A')}")
                print(f"🔴 Error Rate: {summary.get('error_rate_percent', 'N/A')}%")
                
                # Show alerts
                alerts = report["performance_analysis"].get("alerts", [])
                if alerts:
                    print_error(f"🚨 Alerts: {', '.join(alerts)}")
                
                # Show recommendations
                recommendations = report["performance_analysis"].get("recommendations", [])
                if recommendations:
                    print_info(f"💡 Recommendations: {', '.join(recommendations)}")
            
            print_info(f"🔗 View dashboard: {report.get('dashboard_url', 'N/A')}")
            
        elif args.status:
            print_info("\n=== Monitoring Status ===")
            metrics_data = monitor.get_performance_metrics(hours=1)
            analysis = monitor.analyze_performance(metrics_data)
            
            print(f"📊 Performance Score: {analysis.get('performance_score', 'N/A')}/100")
            print(f"🚨 Active Alerts: {len(analysis.get('alerts', []))}")
            print(f"💡 Recommendations: {len(analysis.get('recommendations', []))}")
            
        else:
            # Default: Run full demo
            print_info("\n=== Running Full Monitoring Demo ===")
            
            # Set up comprehensive monitoring
            print_info("\n=== Setting Up Monitoring ===")
            setup_results = monitor.setup_comprehensive_monitoring()
            print(f"📊 Setup Results: {json.dumps(setup_results, indent=2, default=str)}")
            
            # Generate performance report
            print_info("\n=== Generating Performance Report ===")
            report = monitor.generate_monitoring_report(hours=args.hours)
            
            # Display summary
            print_info("\n=== Performance Summary ===")
            if "performance_analysis" in report and "summary" in report["performance_analysis"]:
                summary = report["performance_analysis"]["summary"]
                score = report["performance_analysis"].get("performance_score", "N/A")
                
                print(f"📈 Performance Score: {score}/100")
                print(f"⏱️  Average Latency: {summary.get('average_latency_ms', 'N/A')} ms")
                print(f"📊 Total Queries: {summary.get('total_queries', 'N/A')}")
                print(f"🔴 Error Rate: {summary.get('error_rate_percent', 'N/A')}%")
                
                # Show alerts
                alerts = report["performance_analysis"].get("alerts", [])
                if alerts:
                    print_error(f"🚨 Alerts: {', '.join(alerts)}")
                
                # Show recommendations
                recommendations = report["performance_analysis"].get("recommendations", [])
                if recommendations:
                    print_info(f"💡 Recommendations: {', '.join(recommendations)}")
            
            # Example of publishing custom metrics
            print_info("\n=== Publishing Custom Metrics ===")
            monitor.publish_custom_metric("QuerySuccessRate", 95.5, "Percent", QueryType="Retrieval")
            monitor.publish_custom_metric("ResponseQuality", 4.2, "None", Model="titan-embed")
            
            print_success("✅ Monitoring demo completed successfully!")
            print_info(f"🔗 View dashboard: {report.get('dashboard_url', 'N/A')}")
        
    except Exception as e:
        print_error(f"❌ Error in monitoring: {str(e)}")
        raise


if __name__ == "__main__":
    main()

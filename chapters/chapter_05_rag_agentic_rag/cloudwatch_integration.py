#!/usr/bin/env python3
"""
AWS CloudWatch Integration for RAG Monitoring

This module provides comprehensive integration with AWS CloudWatch for monitoring
RAG system performance, creating dashboards, and setting up automated alerting.

Features:
- Automated metric publishing to CloudWatch
- Custom dashboard creation for RAG monitoring
- Alarm configuration for performance degradation
- Integration with SNS for alerting
- Cost-optimized metric aggregation

Author: AI Engineering Course
Date: 2025
"""

import boto3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CloudWatchRAGMonitor:
    """
    Comprehensive CloudWatch integration for RAG monitoring
    
    This class provides production-ready monitoring capabilities for RAG systems,
    including metric publishing, dashboard creation, and automated alerting.
    """
    
    def __init__(
        self, 
        namespace: str = "RAG/Evaluation",
        region_name: str = "us-east-1",
        sns_topic_arn: Optional[str] = None
    ):
        """
        Initialize CloudWatch RAG monitor
        
        Args:
            namespace: CloudWatch namespace for RAG metrics
            region_name: AWS region
            sns_topic_arn: SNS topic ARN for alerts (optional)
        """
        self.cloudwatch = boto3.client('cloudwatch', region_name=region_name)
        self.sns = boto3.client('sns', region_name=region_name)
        self.namespace = namespace
        self.sns_topic_arn = sns_topic_arn
        self.region_name = region_name
        
    def publish_evaluation_metrics(
        self, 
        report: Dict[str, Any], 
        dimensions: Optional[Dict[str, str]] = None
    ):
        """
        Publish comprehensive evaluation metrics to CloudWatch
        
        Args:
            report: Evaluation report from RAGEvaluator
            dimensions: Additional dimensions for metrics (e.g., environment, version)
        """
        try:
            timestamp = datetime.now()
            metrics_data = []
            
            # Default dimensions
            default_dimensions = [
                {'Name': 'Service', 'Value': 'RAG'},
                {'Name': 'Component', 'Value': 'Evaluation'}
            ]
            
            # Add custom dimensions
            if dimensions:
                for key, value in dimensions.items():
                    default_dimensions.append({'Name': key, 'Value': value})
            
            # Core aggregate metrics
            for metric_name, metric_data in report['aggregate_metrics'].items():
                base_metric_name = metric_name.replace('_', '')
                
                metrics_data.extend([
                    {
                        'MetricName': f'{base_metric_name}Average',
                        'Value': metric_data['average'],
                        'Unit': 'None',
                        'Timestamp': timestamp,
                        'Dimensions': default_dimensions
                    },
                    {
                        'MetricName': f'{base_metric_name}PassingRate',
                        'Value': metric_data['passing_rate'] * 100,
                        'Unit': 'Percent',
                        'Timestamp': timestamp,
                        'Dimensions': default_dimensions
                    },
                    {
                        'MetricName': f'{base_metric_name}StdDev',
                        'Value': metric_data['std_dev'],
                        'Unit': 'None',
                        'Timestamp': timestamp,
                        'Dimensions': default_dimensions
                    }
                ])
            
            # Issues analysis metrics
            issues = report['issues_analysis']
            for issue_type, count in issues.items():
                metrics_data.append({
                    'MetricName': issue_type.replace('_', '').title(),
                    'Value': count,
                    'Unit': 'Count',
                    'Timestamp': timestamp,
                    'Dimensions': default_dimensions
                })
            
            # Performance distribution metrics
            if 'performance_distribution' in report:
                for level, data in report['performance_distribution'].items():
                    metrics_data.extend([
                        {
                            'MetricName': f'Performance{level.title()}Count',
                            'Value': data['count'],
                            'Unit': 'Count',
                            'Timestamp': timestamp,
                            'Dimensions': default_dimensions
                        },
                        {
                            'MetricName': f'Performance{level.title()}Percentage',
                            'Value': data['percentage'],
                            'Unit': 'Percent',
                            'Timestamp': timestamp,
                            'Dimensions': default_dimensions
                        }
                    ])
            
            # Sample size metric
            metrics_data.append({
                'MetricName': 'EvaluationSampleSize',
                'Value': report['evaluation_summary']['total_evaluations'],
                'Unit': 'Count',
                'Timestamp': timestamp,
                'Dimensions': default_dimensions
            })
            
            # Send metrics to CloudWatch in batches
            batch_size = 20  # CloudWatch limit
            for i in range(0, len(metrics_data), batch_size):
                batch = metrics_data[i:i + batch_size]
                
                self.cloudwatch.put_metric_data(
                    Namespace=self.namespace,
                    MetricData=batch
                )
            
            logger.info(f"📈 Published {len(metrics_data)} metrics to CloudWatch namespace: {self.namespace}")
            
        except Exception as e:
            logger.error(f"❌ Failed to publish metrics to CloudWatch: {e}")
            raise
    
    def create_rag_dashboard(self, dashboard_name: str = "RAG-Evaluation-Dashboard") -> str:
        """
        Create comprehensive CloudWatch dashboard for RAG monitoring
        
        Args:
            dashboard_name: Name for the dashboard
            
        Returns:
            Dashboard ARN
        """
        try:
            # Dashboard configuration
            dashboard_body = {
                "widgets": [
                    # Overall Performance Widget
                    {
                        "type": "metric",
                        "x": 0,
                        "y": 0,
                        "width": 12,
                        "height": 6,
                        "properties": {
                            "metrics": [
                                [self.namespace, "overallscoreAverage", "Service", "RAG", "Component", "Evaluation"],
                                [self.namespace, "faithfulnessAverage", "Service", "RAG", "Component", "Evaluation"],
                                [self.namespace, "contextrelevanceAverage", "Service", "RAG", "Component", "Evaluation"],
                                [self.namespace, "answerrelevanceAverage", "Service", "RAG", "Component", "Evaluation"]
                            ],
                            "period": 300,
                            "stat": "Average",
                            "region": self.region_name,
                            "title": "RAG Evaluation Scores",
                            "yAxis": {
                                "left": {
                                    "min": 0,
                                    "max": 1
                                }
                            },
                            "view": "timeSeries",
                            "stacked": False
                        }
                    },
                    
                    # Passing Rates Widget
                    {
                        "type": "metric",
                        "x": 12,
                        "y": 0,
                        "width": 12,
                        "height": 6,
                        "properties": {
                            "metrics": [
                                [self.namespace, "overallscorePassingRate", "Service", "RAG", "Component", "Evaluation"],
                                [self.namespace, "faithfulnessPassingRate", "Service", "RAG", "Component", "Evaluation"],
                                [self.namespace, "contextrelevancePassingRate", "Service", "RAG", "Component", "Evaluation"],
                                [self.namespace, "answerrelevancePassingRate", "Service", "RAG", "Component", "Evaluation"]
                            ],
                            "period": 300,
                            "stat": "Average",
                            "region": self.region_name,
                            "title": "RAG Passing Rates (%)",
                            "yAxis": {
                                "left": {
                                    "min": 0,
                                    "max": 100
                                }
                            },
                            "view": "timeSeries",
                            "stacked": False
                        }
                    },
                    
                    # Issues Count Widget
                    {
                        "type": "metric",
                        "x": 0,
                        "y": 6,
                        "width": 12,
                        "height": 6,
                        "properties": {
                            "metrics": [
                                [self.namespace, "HallucinationCases", "Service", "RAG", "Component", "Evaluation"],
                                [self.namespace, "IrrelevantContextCases", "Service", "RAG", "Component", "Evaluation"],
                                [self.namespace, "IrrelevantAnswerCases", "Service", "RAG", "Component", "Evaluation"]
                            ],
                            "period": 300,
                            "stat": "Sum",
                            "region": self.region_name,
                            "title": "RAG Issues Count",
                            "view": "timeSeries",
                            "stacked": True
                        }
                    },
                    
                    # Sample Size Widget
                    {
                        "type": "metric",
                        "x": 12,
                        "y": 6,
                        "width": 12,
                        "height": 6,
                        "properties": {
                            "metrics": [
                                [self.namespace, "EvaluationSampleSize", "Service", "RAG", "Component", "Evaluation"]
                            ],
                            "period": 300,
                            "stat": "Sum",
                            "region": self.region_name,
                            "title": "Evaluation Sample Size",
                            "view": "timeSeries",
                            "stacked": False
                        }
                    },
                    
                    # Performance Distribution (Number Widget)
                    {
                        "type": "metric",
                        "x": 0,
                        "y": 12,
                        "width": 6,
                        "height": 6,
                        "properties": {
                            "metrics": [
                                [self.namespace, "PerformanceExcellentPercentage", "Service", "RAG", "Component", "Evaluation"]
                            ],
                            "period": 300,
                            "stat": "Average",
                            "region": self.region_name,
                            "title": "Excellent Performance %",
                            "view": "singleValue"
                        }
                    },
                    
                    # Poor Performance Alert (Number Widget)
                    {
                        "type": "metric",
                        "x": 6,
                        "y": 12,
                        "width": 6,
                        "height": 6,
                        "properties": {
                            "metrics": [
                                [self.namespace, "PerformancePoorPercentage", "Service", "RAG", "Component", "Evaluation"]
                            ],
                            "period": 300,
                            "stat": "Average",
                            "region": self.region_name,
                            "title": "Poor Performance %",
                            "view": "singleValue"
                        }
                    },
                    
                    # Standard Deviation Trends
                    {
                        "type": "metric",
                        "x": 12,
                        "y": 12,
                        "width": 12,
                        "height": 6,
                        "properties": {
                            "metrics": [
                                [self.namespace, "overallscoreStdDev", "Service", "RAG", "Component", "Evaluation"],
                                [self.namespace, "faithfulnessStdDev", "Service", "RAG", "Component", "Evaluation"],
                                [self.namespace, "contextrelevanceStdDev", "Service", "RAG", "Component", "Evaluation"],
                                [self.namespace, "answerrelevanceStdDev", "Service", "RAG", "Component", "Evaluation"]
                            ],
                            "period": 300,
                            "stat": "Average",
                            "region": self.region_name,
                            "title": "Performance Variance (Standard Deviation)",
                            "view": "timeSeries",
                            "stacked": False
                        }
                    }
                ]
            }
            
            # Create dashboard
            response = self.cloudwatch.put_dashboard(
                DashboardName=dashboard_name,
                DashboardBody=json.dumps(dashboard_body)
            )
            
            dashboard_arn = f"arn:aws:cloudwatch::{self.region_name}:dashboard/{dashboard_name}"
            logger.info(f"📊 Created CloudWatch dashboard: {dashboard_name}")
            
            return dashboard_arn
            
        except Exception as e:
            logger.error(f"❌ Failed to create CloudWatch dashboard: {e}")
            raise
    
    def create_performance_alarms(
        self, 
        thresholds: Optional[Dict[str, float]] = None,
        alarm_prefix: str = "RAG"
    ) -> List[str]:
        """
        Create CloudWatch alarms for RAG performance monitoring
        
        Args:
            thresholds: Performance thresholds for alarms
            alarm_prefix: Prefix for alarm names
            
        Returns:
            List of created alarm ARNs
        """
        # Default thresholds
        default_thresholds = {
            "overall_score": 0.7,
            "faithfulness_rate": 80,  # Percentage
            "context_relevance_rate": 70,  # Percentage
            "hallucination_cases": 5,  # Count per evaluation
            "poor_performance_rate": 20  # Percentage
        }
        
        thresholds = thresholds or default_thresholds
        alarm_arns = []
        
        try:
            # Overall Score Alarm
            alarm_name = f"{alarm_prefix}-OverallScore-Low"
            self.cloudwatch.put_metric_alarm(
                AlarmName=alarm_name,
                ComparisonOperator='LessThanThreshold',
                EvaluationPeriods=2,
                MetricName='overallscoreAverage',
                Namespace=self.namespace,
                Period=300,
                Statistic='Average',
                Threshold=thresholds['overall_score'],
                ActionsEnabled=True,
                AlarmActions=[self.sns_topic_arn] if self.sns_topic_arn else [],
                AlarmDescription='Alert when RAG overall score drops below threshold',
                Dimensions=[
                    {'Name': 'Service', 'Value': 'RAG'},
                    {'Name': 'Component', 'Value': 'Evaluation'}
                ],
                Unit='None',
                TreatMissingData='breaching'
            )
            alarm_arns.append(f"arn:aws:cloudwatch:{self.region_name}:alarm:{alarm_name}")
            
            # Faithfulness Rate Alarm
            alarm_name = f"{alarm_prefix}-Faithfulness-Low"
            self.cloudwatch.put_metric_alarm(
                AlarmName=alarm_name,
                ComparisonOperator='LessThanThreshold',
                EvaluationPeriods=2,
                MetricName='faithfulnessPassingRate',
                Namespace=self.namespace,
                Period=300,
                Statistic='Average',
                Threshold=thresholds['faithfulness_rate'],
                ActionsEnabled=True,
                AlarmActions=[self.sns_topic_arn] if self.sns_topic_arn else [],
                AlarmDescription='Alert when RAG faithfulness rate drops (high hallucination)',
                Dimensions=[
                    {'Name': 'Service', 'Value': 'RAG'},
                    {'Name': 'Component', 'Value': 'Evaluation'}
                ],
                Unit='Percent',
                TreatMissingData='breaching'
            )
            alarm_arns.append(f"arn:aws:cloudwatch:{self.region_name}:alarm:{alarm_name}")
            
            # Context Relevance Rate Alarm
            alarm_name = f"{alarm_prefix}-ContextRelevance-Low"
            self.cloudwatch.put_metric_alarm(
                AlarmName=alarm_name,
                ComparisonOperator='LessThanThreshold',
                EvaluationPeriods=2,
                MetricName='contextrelevancePassingRate',
                Namespace=self.namespace,
                Period=300,
                Statistic='Average',
                Threshold=thresholds['context_relevance_rate'],
                ActionsEnabled=True,
                AlarmActions=[self.sns_topic_arn] if self.sns_topic_arn else [],
                AlarmDescription='Alert when RAG context relevance rate drops (poor retrieval)',
                Dimensions=[
                    {'Name': 'Service', 'Value': 'RAG'},
                    {'Name': 'Component', 'Value': 'Evaluation'}
                ],
                Unit='Percent',
                TreatMissingData='breaching'
            )
            alarm_arns.append(f"arn:aws:cloudwatch:{self.region_name}:alarm:{alarm_name}")
            
            # Hallucination Cases Alarm
            alarm_name = f"{alarm_prefix}-Hallucinations-High"
            self.cloudwatch.put_metric_alarm(
                AlarmName=alarm_name,
                ComparisonOperator='GreaterThanThreshold',
                EvaluationPeriods=1,
                MetricName='HallucinationCases',
                Namespace=self.namespace,
                Period=300,
                Statistic='Sum',
                Threshold=thresholds['hallucination_cases'],
                ActionsEnabled=True,
                AlarmActions=[self.sns_topic_arn] if self.sns_topic_arn else [],
                AlarmDescription='Alert when hallucination cases exceed threshold',
                Dimensions=[
                    {'Name': 'Service', 'Value': 'RAG'},
                    {'Name': 'Component', 'Value': 'Evaluation'}
                ],
                Unit='Count',
                TreatMissingData='notBreaching'
            )
            alarm_arns.append(f"arn:aws:cloudwatch:{self.region_name}:alarm:{alarm_name}")
            
            # Poor Performance Rate Alarm
            alarm_name = f"{alarm_prefix}-PoorPerformance-High"
            self.cloudwatch.put_metric_alarm(
                AlarmName=alarm_name,
                ComparisonOperator='GreaterThanThreshold',
                EvaluationPeriods=2,
                MetricName='PerformancePoorPercentage',
                Namespace=self.namespace,
                Period=300,
                Statistic='Average',
                Threshold=thresholds['poor_performance_rate'],
                ActionsEnabled=True,
                AlarmActions=[self.sns_topic_arn] if self.sns_topic_arn else [],
                AlarmDescription='Alert when poor performance rate is too high',
                Dimensions=[
                    {'Name': 'Service', 'Value': 'RAG'},
                    {'Name': 'Component', 'Value': 'Evaluation'}
                ],
                Unit='Percent',
                TreatMissingData='notBreaching'
            )
            alarm_arns.append(f"arn:aws:cloudwatch:{self.region_name}:alarm:{alarm_name}")
            
            logger.info(f"🚨 Created {len(alarm_arns)} CloudWatch alarms for RAG monitoring")
            
            return alarm_arns
            
        except Exception as e:
            logger.error(f"❌ Failed to create CloudWatch alarms: {e}")
            raise
    
    def get_metric_statistics(
        self, 
        metric_name: str, 
        start_time: datetime, 
        end_time: datetime,
        period: int = 300,
        statistic: str = 'Average'
    ) -> List[Dict]:
        """
        Retrieve metric statistics from CloudWatch
        
        Args:
            metric_name: Name of the metric
            start_time: Start time for data retrieval
            end_time: End time for data retrieval
            period: Period in seconds
            statistic: Statistic type
            
        Returns:
            List of metric data points
        """
        try:
            response = self.cloudwatch.get_metric_statistics(
                Namespace=self.namespace,
                MetricName=metric_name,
                Dimensions=[
                    {'Name': 'Service', 'Value': 'RAG'},
                    {'Name': 'Component', 'Value': 'Evaluation'}
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=period,
                Statistics=[statistic]
            )
            
            return sorted(response['Datapoints'], key=lambda x: x['Timestamp'])
            
        except Exception as e:
            logger.error(f"❌ Failed to retrieve metric statistics: {e}")
            return []
    
    def generate_performance_summary(self, hours: int = 24) -> Dict[str, Any]:
        """
        Generate performance summary from CloudWatch metrics
        
        Args:
            hours: Number of hours to analyze
            
        Returns:
            Performance summary dictionary
        """
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours)
        
        try:
            # Retrieve key metrics
            overall_score_data = self.get_metric_statistics(
                'overallscoreAverage', start_time, end_time
            )
            
            faithfulness_data = self.get_metric_statistics(
                'faithfulnessPassingRate', start_time, end_time
            )
            
            hallucination_data = self.get_metric_statistics(
                'HallucinationCases', start_time, end_time, statistic='Sum'
            )
            
            # Calculate summary statistics
            summary = {
                "analysis_period_hours": hours,
                "data_points": len(overall_score_data),
                "overall_performance": {
                    "current_score": overall_score_data[-1]['Average'] if overall_score_data else None,
                    "average_score": sum(d['Average'] for d in overall_score_data) / len(overall_score_data) if overall_score_data else None,
                    "min_score": min(d['Average'] for d in overall_score_data) if overall_score_data else None,
                    "max_score": max(d['Average'] for d in overall_score_data) if overall_score_data else None
                },
                "faithfulness": {
                    "current_rate": faithfulness_data[-1]['Average'] if faithfulness_data else None,
                    "average_rate": sum(d['Average'] for d in faithfulness_data) / len(faithfulness_data) if faithfulness_data else None
                },
                "issues": {
                    "total_hallucinations": sum(d['Sum'] for d in hallucination_data) if hallucination_data else 0,
                    "avg_hallucinations_per_period": sum(d['Sum'] for d in hallucination_data) / len(hallucination_data) if hallucination_data else 0
                }
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"❌ Failed to generate performance summary: {e}")
            return {"error": str(e)}
    
    def setup_sns_topic(self, topic_name: str = "rag-alerts") -> str:
        """
        Create SNS topic for RAG alerts
        
        Args:
            topic_name: Name for the SNS topic
            
        Returns:
            SNS topic ARN
        """
        try:
            response = self.sns.create_topic(Name=topic_name)
            topic_arn = response['TopicArn']
            
            # Set topic attributes for better organization
            self.sns.set_topic_attributes(
                TopicArn=topic_arn,
                AttributeName='DisplayName',
                AttributeValue='RAG System Alerts'
            )
            
            logger.info(f"📧 Created SNS topic for alerts: {topic_arn}")
            
            return topic_arn
            
        except Exception as e:
            logger.error(f"❌ Failed to create SNS topic: {e}")
            raise
    
    def subscribe_email_to_alerts(self, email: str, topic_arn: str = None) -> str:
        """
        Subscribe email address to alert notifications
        
        Args:
            email: Email address to subscribe
            topic_arn: SNS topic ARN (uses self.sns_topic_arn if not provided)
            
        Returns:
            Subscription ARN
        """
        topic_arn = topic_arn or self.sns_topic_arn
        
        if not topic_arn:
            raise ValueError("No SNS topic ARN provided")
        
        try:
            response = self.sns.subscribe(
                TopicArn=topic_arn,
                Protocol='email',
                Endpoint=email
            )
            
            subscription_arn = response['SubscriptionArn']
            logger.info(f"📧 Subscribed {email} to RAG alerts")
            
            return subscription_arn
            
        except Exception as e:
            logger.error(f"❌ Failed to subscribe email to alerts: {e}")
            raise

def demo_cloudwatch_integration():
    """Demonstrate CloudWatch integration capabilities"""
    print("☁️ CloudWatch RAG Monitoring Demo")
    print("=" * 40)
    
    # Initialize monitor
    monitor = CloudWatchRAGMonitor(
        namespace="Demo/RAG/Evaluation",
        region_name="us-east-1"
    )
    
    print("1️⃣ Creating sample evaluation report...")
    
    # Create sample report for demonstration
    sample_report = {
        "evaluation_summary": {
            "total_evaluations": 100,
            "evaluation_timestamp": datetime.now().isoformat(),
            "model_used": "claude-3-sonnet"
        },
        "aggregate_metrics": {
            "overall_score": {
                "average": 0.85,
                "passing_rate": 0.88,
                "std_dev": 0.12,
                "min": 0.45,
                "max": 0.98
            },
            "faithfulness": {
                "average": 0.92,
                "passing_rate": 0.94,
                "std_dev": 0.08,
                "min": 0.65,
                "max": 1.0
            },
            "context_relevance": {
                "average": 0.78,
                "passing_rate": 0.82,
                "std_dev": 0.15,
                "min": 0.25,
                "max": 1.0
            },
            "answer_relevance": {
                "average": 0.89,
                "passing_rate": 0.91,
                "std_dev": 0.10,
                "min": 0.55,
                "max": 1.0
            }
        },
        "issues_analysis": {
            "hallucination_cases": 6,
            "irrelevant_context_cases": 18,
            "irrelevant_answer_cases": 9,
            "total_issues": 33
        },
        "performance_distribution": {
            "excellent": {"count": 25, "percentage": 25.0},
            "good": {"count": 63, "percentage": 63.0},
            "fair": {"count": 10, "percentage": 10.0},
            "poor": {"count": 2, "percentage": 2.0}
        }
    }
    
    print("2️⃣ Publishing metrics to CloudWatch...")
    
    # Publish metrics
    monitor.publish_evaluation_metrics(
        report=sample_report,
        dimensions={
            "Environment": "Demo",
            "Version": "1.0"
        }
    )
    
    print("3️⃣ Creating CloudWatch dashboard...")
    
    # Create dashboard
    dashboard_arn = monitor.create_rag_dashboard("Demo-RAG-Dashboard")
    print(f"📊 Dashboard created: {dashboard_arn}")
    
    print("4️⃣ Setting up performance alarms...")
    
    # Create alarms (without SNS for demo)
    alarm_arns = monitor.create_performance_alarms(
        thresholds={
            "overall_score": 0.8,
            "faithfulness_rate": 85,
            "context_relevance_rate": 75,
            "hallucination_cases": 10,
            "poor_performance_rate": 15
        },
        alarm_prefix="Demo-RAG"
    )
    
    print(f"🚨 Created {len(alarm_arns)} alarms")
    
    print("5️⃣ Generating performance summary...")
    
    # Note: This would typically show real data from CloudWatch
    # For demo, we'll show the structure
    summary = {
        "analysis_period_hours": 24,
        "data_points": 0,  # No historical data yet
        "overall_performance": {
            "current_score": None,
            "average_score": None,
            "min_score": None,
            "max_score": None
        },
        "message": "No historical data available yet. Metrics will appear after some time."
    }
    
    print(f"📈 Performance Summary: {summary}")
    
    print("\\n✅ CloudWatch integration demo completed!")
    print("🔍 Check the AWS Console to see the dashboard and alarms.")
    print("📊 Metrics will start appearing in CloudWatch as evaluations run.")

if __name__ == "__main__":
    demo_cloudwatch_integration()

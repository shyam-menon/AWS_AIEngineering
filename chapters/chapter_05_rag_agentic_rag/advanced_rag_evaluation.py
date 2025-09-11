#!/usr/bin/env python3
"""
Continuous RAG Monitoring and A/B Testing Framework

This module provides advanced RAG evaluation capabilities including:
- Continuous monitoring pipeline for production RAG systems
- A/B testing framework for comparing different RAG configurations
- Integration with AWS CloudWatch for metrics and alerting
- Automated performance degradation detection

Author: AI Engineering Course
Date: 2025
"""

import boto3
import json
import schedule
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable, Tuple
from enum import Enum
import logging
import random
import numpy as np
from dataclasses import dataclass
from rag_evaluation_framework import RAGEvaluator, RAGEvaluationResult

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGVariant(Enum):
    """Enum for A/B testing variants"""
    CONTROL = "control"
    TREATMENT = "treatment"

@dataclass
class RAGConfiguration:
    """Configuration for a RAG system variant"""
    name: str
    chunking_strategy: str
    chunk_size: int
    chunk_overlap: int
    embedding_model: str
    retrieval_top_k: int
    reranking_enabled: bool
    generation_temperature: float
    prompt_template: str
    generation_model: str = "amazon.nova-lite-v1:0"
    knowledge_base_id: str = "PIWCGRFREL"
    metadata: Optional[Dict[str, Any]] = None

class ContinuousRAGEvaluator:
    """
    Continuous evaluation system for production RAG monitoring
    
    This class implements continuous monitoring patterns for RAG systems,
    providing automated evaluation, alerting, and performance tracking.
    """
    
    def __init__(
        self, 
        evaluator: RAGEvaluator, 
        data_source_func: Callable[[datetime, datetime], List[Dict]],
        alert_thresholds: Optional[Dict[str, float]] = None
    ):
        """
        Initialize continuous evaluator
        
        Args:
            evaluator: RAGEvaluator instance
            data_source_func: Function to retrieve RAG interactions from logs/database
            alert_thresholds: Performance thresholds for alerting
        """
        self.evaluator = evaluator
        self.data_source_func = data_source_func
        self.evaluation_history = []
        
        # Default alert thresholds
        self.alert_thresholds = alert_thresholds or {
            "overall_score": 0.7,
            "faithfulness_rate": 0.8,
            "context_relevance_rate": 0.7,
            "answer_relevance_rate": 0.8
        }
        
        # CloudWatch integration
        self.cloudwatch = boto3.client('cloudwatch')
        self.sns = boto3.client('sns')
        self.namespace = "RAG/Evaluation"
        
    def run_scheduled_evaluation(self):
        """Run evaluation on recent RAG interactions"""
        logger.info("🔄 Starting scheduled RAG evaluation...")
        
        try:
            # Get recent data (last 24 hours)
            end_time = datetime.now()
            start_time = end_time - timedelta(hours=24)
            
            evaluation_data = self.data_source_func(start_time, end_time)
            
            if not evaluation_data:
                logger.info("📭 No data available for evaluation")
                return
            
            logger.info(f"📊 Evaluating {len(evaluation_data)} interactions...")
            
            # Run evaluation
            results = self.evaluator.evaluate_batch(evaluation_data, show_progress=False)
            report = self.evaluator.generate_evaluation_report(results)
            
            # Store results with timestamp
            evaluation_record = {
                "timestamp": datetime.now().isoformat(),
                "report": report,
                "sample_size": len(evaluation_data)
            }
            self.evaluation_history.append(evaluation_record)
            
            # Publish metrics to CloudWatch
            self._publish_metrics_to_cloudwatch(report)
            
            # Check for performance alerts
            self._check_performance_alerts(report)
            
            # Log summary
            overall_score = report['aggregate_metrics']['overall_score']['average']
            logger.info(f"✅ Evaluation complete. Overall score: {overall_score:.3f}")
            
            return evaluation_record
            
        except Exception as e:
            logger.error(f"❌ Scheduled evaluation failed: {e}")
            self._send_error_alert(f"Scheduled RAG evaluation failed: {e}")
    
    def _publish_metrics_to_cloudwatch(self, report: Dict):
        """Publish evaluation metrics to CloudWatch"""
        try:
            timestamp = datetime.now()
            metrics_data = []
            
            # Aggregate metrics
            for metric_name, metric_data in report['aggregate_metrics'].items():
                metrics_data.extend([
                    {
                        'MetricName': f'{metric_name}_average',
                        'Value': metric_data['average'],
                        'Unit': 'None',
                        'Timestamp': timestamp
                    },
                    {
                        'MetricName': f'{metric_name}_passing_rate',
                        'Value': metric_data['passing_rate'] * 100,  # Convert to percentage
                        'Unit': 'Percent',
                        'Timestamp': timestamp
                    }
                ])
            
            # Issues metrics
            for issue_type, count in report['issues_analysis'].items():
                metrics_data.append({
                    'MetricName': issue_type,
                    'Value': count,
                    'Unit': 'Count',
                    'Timestamp': timestamp
                })
            
            # Send metrics to CloudWatch in batches
            batch_size = 20  # CloudWatch limit
            for i in range(0, len(metrics_data), batch_size):
                batch = metrics_data[i:i + batch_size]
                
                self.cloudwatch.put_metric_data(
                    Namespace=self.namespace,
                    MetricData=batch
                )
                
            logger.info(f"📈 Published {len(metrics_data)} metrics to CloudWatch")
            
        except Exception as e:
            logger.error(f"Failed to publish metrics to CloudWatch: {e}")
    
    def _check_performance_alerts(self, report: Dict):
        """Check for performance issues and send alerts"""
        alerts = []
        
        # Check overall performance
        overall_score = report['aggregate_metrics']['overall_score']['average']
        if overall_score < self.alert_thresholds['overall_score']:
            alerts.append(f"⚠️ RAG Performance Alert: Overall score dropped to {overall_score:.3f}")
        
        # Check faithfulness (hallucination rate)
        faithfulness_rate = report['aggregate_metrics']['faithfulness']['passing_rate']
        if faithfulness_rate < self.alert_thresholds['faithfulness_rate']:
            alerts.append(f"🚨 Hallucination Alert: Faithfulness rate dropped to {faithfulness_rate:.1%}")
        
        # Check context relevance
        context_relevance_rate = report['aggregate_metrics']['context_relevance']['passing_rate']
        if context_relevance_rate < self.alert_thresholds['context_relevance_rate']:
            alerts.append(f"🎯 Retrieval Alert: Context relevance rate dropped to {context_relevance_rate:.1%}")
        
        # Check answer relevance
        answer_relevance_rate = report['aggregate_metrics']['answer_relevance']['passing_rate']
        if answer_relevance_rate < self.alert_thresholds['answer_relevance_rate']:
            alerts.append(f"💬 Generation Alert: Answer relevance rate dropped to {answer_relevance_rate:.1%}")
        
        # Send alerts if any issues detected
        if alerts:
            alert_message = "\\n".join(alerts)
            self._send_performance_alert(alert_message)
            
            for alert in alerts:
                logger.warning(alert)
    
    def _send_performance_alert(self, message: str):
        """Send performance alert via SNS"""
        try:
            # This would typically use SNS to send alerts
            # For demonstration, we'll just log the alert
            logger.warning(f"📢 PERFORMANCE ALERT: {message}")
            
            # Uncomment and configure for actual SNS integration:
            # self.sns.publish(
            #     TopicArn='arn:aws:sns:region:account:rag-alerts',
            #     Subject='RAG Performance Alert',
            #     Message=message
            # )
            
        except Exception as e:
            logger.error(f"Failed to send performance alert: {e}")
    
    def _send_error_alert(self, message: str):
        """Send error alert via SNS"""
        try:
            logger.error(f"📢 ERROR ALERT: {message}")
            
            # Uncomment and configure for actual SNS integration:
            # self.sns.publish(
            #     TopicArn='arn:aws:sns:region:account:rag-errors',
            #     Subject='RAG System Error',
            #     Message=message
            # )
            
        except Exception as e:
            logger.error(f"Failed to send error alert: {e}")
    
    def get_performance_trend(self, hours: int = 168) -> Dict[str, Any]:
        """
        Get performance trend analysis for the last N hours
        
        Args:
            hours: Number of hours to analyze (default: 1 week)
            
        Returns:
            Performance trend analysis
        """
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        recent_evaluations = [
            eval_record for eval_record in self.evaluation_history
            if datetime.fromisoformat(eval_record['timestamp']) > cutoff_time
        ]
        
        if len(recent_evaluations) < 2:
            return {"error": "Insufficient data for trend analysis"}
        
        # Extract time series data
        timestamps = [datetime.fromisoformat(eval_record['timestamp']) for eval_record in recent_evaluations]
        overall_scores = [eval_record['report']['aggregate_metrics']['overall_score']['average'] for eval_record in recent_evaluations]
        
        # Calculate trend
        if len(overall_scores) >= 2:
            trend_slope = np.polyfit(range(len(overall_scores)), overall_scores, 1)[0]
            trend_direction = "improving" if trend_slope > 0.01 else "degrading" if trend_slope < -0.01 else "stable"
        else:
            trend_slope = 0
            trend_direction = "insufficient_data"
        
        # Current vs historical comparison
        current_score = overall_scores[-1] if overall_scores else 0
        historical_avg = np.mean(overall_scores[:-1]) if len(overall_scores) > 1 else current_score
        
        return {
            "analysis_period": f"{hours} hours",
            "evaluations_count": len(recent_evaluations),
            "current_score": current_score,
            "historical_average": historical_avg,
            "trend_direction": trend_direction,
            "trend_slope": trend_slope,
            "performance_change": current_score - historical_avg,
            "timestamps": [ts.isoformat() for ts in timestamps],
            "scores": overall_scores
        }
    
    def start_monitoring(self, evaluation_interval_hours: int = 6):
        """
        Start continuous monitoring with scheduled evaluations
        
        Args:
            evaluation_interval_hours: Hours between evaluations
        """
        # Schedule evaluation
        schedule.every(evaluation_interval_hours).hours.do(self.run_scheduled_evaluation)
        
        logger.info(f"🚀 Started continuous RAG evaluation monitoring (every {evaluation_interval_hours} hours)")
        
        # Run initial evaluation
        self.run_scheduled_evaluation()
        
        # Keep running scheduled tasks
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute


class RAGABTester:
    """
    A/B testing framework for RAG systems
    
    This class enables systematic comparison of different RAG configurations
    to determine which performs better in production.
    """
    
    def __init__(
        self, 
        control_config: RAGConfiguration, 
        treatment_config: RAGConfiguration,
        evaluator: RAGEvaluator,
        traffic_split: float = 0.5
    ):
        """
        Initialize A/B tester
        
        Args:
            control_config: Configuration for control group
            treatment_config: Configuration for treatment group
            evaluator: RAGEvaluator instance
            traffic_split: Fraction of traffic to send to treatment (0.0-1.0)
        """
        self.control_config = control_config
        self.treatment_config = treatment_config
        self.evaluator = evaluator
        self.traffic_split = traffic_split
        self.results = {RAGVariant.CONTROL: [], RAGVariant.TREATMENT: []}
        self.user_assignments = {}  # Track user assignments for consistency
        
    def assign_variant(self, user_id: str) -> RAGVariant:
        """
        Assign user to control or treatment group consistently
        
        Args:
            user_id: Unique user identifier
            
        Returns:
            Assigned RAG variant
        """
        # Check if user already assigned
        if user_id in self.user_assignments:
            return self.user_assignments[user_id]
        
        # Hash-based assignment for consistent user experience
        hash_value = hash(user_id) % 1000  # 0-999
        threshold = int(self.traffic_split * 1000)
        
        variant = RAGVariant.TREATMENT if hash_value < threshold else RAGVariant.CONTROL
        self.user_assignments[user_id] = variant
        
        return variant
    
    def process_query(self, user_id: str, query: str, context: str = None) -> Dict[str, Any]:
        """
        Process query using assigned variant
        
        Args:
            user_id: Unique user identifier
            query: User query
            context: Optional context for the query
            
        Returns:
            Processing result with variant information
        """
        variant = self.assign_variant(user_id)
        config = self.control_config if variant == RAGVariant.CONTROL else self.treatment_config
        
        # Simulate RAG processing with different configurations
        # In a real implementation, this would call your actual RAG system
        result = {
            "user_id": user_id,
            "query": query,
            "variant": variant.value,
            "config_used": config.name,
            "retrieved_context": context or f"Retrieved context using {config.embedding_model}",
            "generated_answer": f"Generated answer using {config.generation_model} with temperature {config.generation_temperature}",
            "timestamp": datetime.now().isoformat(),
            "processing_metadata": {
                "chunk_size": config.chunk_size,
                "top_k": config.retrieval_top_k,
                "reranking": config.reranking_enabled
            }
        }
        
        # Log the interaction for later evaluation
        self.results[variant].append(result)
        
        return result
    
    def evaluate_experiment(self, min_sample_size: int = 50) -> Dict[str, Any]:
        """
        Evaluate the A/B test results
        
        Args:
            min_sample_size: Minimum samples required per variant
            
        Returns:
            Comprehensive A/B test evaluation report
        """
        control_samples = len(self.results[RAGVariant.CONTROL])
        treatment_samples = len(self.results[RAGVariant.TREATMENT])
        
        if control_samples < min_sample_size or treatment_samples < min_sample_size:
            return {
                "error": f"Insufficient samples. Control: {control_samples}, Treatment: {treatment_samples}, Required: {min_sample_size}"
            }
        
        # Prepare evaluation data
        control_data = self._prepare_evaluation_data(self.results[RAGVariant.CONTROL])
        treatment_data = self._prepare_evaluation_data(self.results[RAGVariant.TREATMENT])
        
        # Evaluate both variants
        logger.info("📊 Evaluating control variant...")
        control_results = self.evaluator.evaluate_batch(control_data, show_progress=False)
        
        logger.info("📊 Evaluating treatment variant...")
        treatment_results = self.evaluator.evaluate_batch(treatment_data, show_progress=False)
        
        # Generate reports
        control_report = self.evaluator.generate_evaluation_report(control_results)
        treatment_report = self.evaluator.generate_evaluation_report(treatment_results)
        
        # Statistical comparison
        comparison = self._compare_variants(control_report, treatment_report)
        
        # Traffic split analysis
        traffic_analysis = {
            "intended_split": self.traffic_split,
            "actual_split": treatment_samples / (control_samples + treatment_samples),
            "total_interactions": control_samples + treatment_samples
        }
        
        return {
            "experiment_summary": {
                "control_config": self.control_config.name,
                "treatment_config": self.treatment_config.name,
                "evaluation_timestamp": datetime.now().isoformat(),
                "sample_sizes": {
                    "control": control_samples,
                    "treatment": treatment_samples
                }
            },
            "control": control_report,
            "treatment": treatment_report,
            "comparison": comparison,
            "traffic_analysis": traffic_analysis,
            "recommendation": self._generate_experiment_recommendation(comparison)
        }
    
    def _prepare_evaluation_data(self, raw_results: List[Dict]) -> List[Dict]:
        """Convert raw results to evaluation format"""
        evaluation_data = []
        
        for result in raw_results:
            eval_item = {
                "query": result["query"],
                "retrieved_context": result["retrieved_context"],
                "generated_answer": result["generated_answer"]
            }
            evaluation_data.append(eval_item)
        
        return evaluation_data
    
    def _compare_variants(self, control_report: Dict, treatment_report: Dict) -> Dict:
        """Compare control and treatment variants statistically"""
        control_metrics = control_report['aggregate_metrics']
        treatment_metrics = treatment_report['aggregate_metrics']
        
        comparison = {}
        
        for metric_name in ['overall_score', 'faithfulness', 'context_relevance', 'answer_relevance']:
            control_avg = control_metrics[metric_name]['average']
            treatment_avg = treatment_metrics[metric_name]['average']
            
            # Calculate relative improvement
            improvement = ((treatment_avg - control_avg) / control_avg * 100) if control_avg > 0 else 0
            
            # Determine statistical significance (simplified)
            # In production, use proper statistical tests (t-test, etc.)
            control_std = control_metrics[metric_name]['std_dev']
            treatment_std = treatment_metrics[metric_name]['std_dev']
            
            # Simple heuristic for significance
            difference = abs(treatment_avg - control_avg)
            pooled_std = (control_std + treatment_std) / 2
            is_significant = difference > 2 * pooled_std  # Simplified significance test
            
            comparison[metric_name] = {
                "control_score": control_avg,
                "treatment_score": treatment_avg,
                "absolute_improvement": treatment_avg - control_avg,
                "relative_improvement_percent": improvement,
                "winner": "treatment" if treatment_avg > control_avg else "control",
                "is_statistically_significant": is_significant,
                "confidence": "high" if is_significant else "low"
            }
        
        return comparison
    
    def _generate_experiment_recommendation(self, comparison: Dict) -> Dict[str, Any]:
        """Generate recommendation based on A/B test results"""
        overall_comparison = comparison['overall_score']
        
        # Count wins across metrics
        treatment_wins = sum(1 for metric in comparison.values() if metric['winner'] == 'treatment')
        control_wins = sum(1 for metric in comparison.values() if metric['winner'] == 'control')
        
        # Check for significant improvements
        significant_improvements = sum(1 for metric in comparison.values() 
                                     if metric['winner'] == 'treatment' and metric['is_statistically_significant'])
        
        # Generate recommendation
        if overall_comparison['relative_improvement_percent'] > 5 and overall_comparison['is_statistically_significant']:
            recommendation = "DEPLOY_TREATMENT"
            confidence = "HIGH"
            reason = f"Treatment shows {overall_comparison['relative_improvement_percent']:.1f}% improvement in overall score with statistical significance"
        elif overall_comparison['relative_improvement_percent'] > 2:
            recommendation = "CAUTIOUS_DEPLOYMENT"
            confidence = "MEDIUM"
            reason = f"Treatment shows {overall_comparison['relative_improvement_percent']:.1f}% improvement but needs more data for confidence"
        elif overall_comparison['relative_improvement_percent'] < -5:
            recommendation = "KEEP_CONTROL"
            confidence = "HIGH"
            reason = f"Treatment performs {abs(overall_comparison['relative_improvement_percent']):.1f}% worse than control"
        else:
            recommendation = "CONTINUE_TESTING"
            confidence = "LOW"
            reason = "No clear winner detected, continue testing with more samples"
        
        return {
            "action": recommendation,
            "confidence": confidence,
            "reason": reason,
            "treatment_wins": treatment_wins,
            "control_wins": control_wins,
            "significant_improvements": significant_improvements,
            "overall_improvement": overall_comparison['relative_improvement_percent']
        }
    
    def generate_experiment_report(self) -> str:
        """Generate human-readable experiment report"""
        evaluation_result = self.evaluate_experiment()
        
        if "error" in evaluation_result:
            return f"❌ Experiment Error: {evaluation_result['error']}"
        
        report = []
        report.append("🧪 RAG A/B Test Results")
        report.append("=" * 30)
        
        # Summary
        summary = evaluation_result['experiment_summary']
        report.append(f"Control Configuration: {summary['control_config']}")
        report.append(f"Treatment Configuration: {summary['treatment_config']}")
        report.append(f"Control Samples: {summary['sample_sizes']['control']}")
        report.append(f"Treatment Samples: {summary['sample_sizes']['treatment']}")
        report.append("")
        
        # Key metrics comparison
        report.append("📊 Key Metrics Comparison:")
        comparison = evaluation_result['comparison']
        
        for metric_name, metric_data in comparison.items():
            report.append(f"   {metric_name.replace('_', ' ').title()}:")
            report.append(f"     Control: {metric_data['control_score']:.3f}")
            report.append(f"     Treatment: {metric_data['treatment_score']:.3f}")
            report.append(f"     Improvement: {metric_data['relative_improvement_percent']:+.1f}%")
            report.append(f"     Winner: {metric_data['winner'].title()}")
            report.append("")
        
        # Recommendation
        rec = evaluation_result['recommendation']
        report.append(f"💡 Recommendation: {rec['action']}")
        report.append(f"   Confidence: {rec['confidence']}")
        report.append(f"   Reason: {rec['reason']}")
        
        return "\\n".join(report)


# Utility functions for demonstrations and testing

def create_sample_rag_configurations() -> Tuple[RAGConfiguration, RAGConfiguration]:
    """Create sample RAG configurations for A/B testing"""
    control_config = RAGConfiguration(
        name="Control: Standard Configuration",
        chunking_strategy="fixed_size",
        chunk_size=512,
        chunk_overlap=50,
        embedding_model="amazon.titan-embed-text-v1",
        retrieval_top_k=5,
        reranking_enabled=False,
        generation_model="amazon.nova-lite-v1:0",
        generation_temperature=0.1,
        prompt_template="Standard prompt template",
        knowledge_base_id="PIWCGRFREL"
    )
    
    treatment_config = RAGConfiguration(
        name="Treatment: Optimized Configuration",
        chunking_strategy="semantic",
        chunk_size=768,
        chunk_overlap=100,
        embedding_model="amazon.titan-embed-text-v1",
        retrieval_top_k=10,
        reranking_enabled=True,
        generation_model="amazon.nova-lite-v1:0",
        generation_temperature=0.05,
        prompt_template="Enhanced prompt template with context emphasis",
        knowledge_base_id="PIWCGRFREL"
    )
    
    return control_config, treatment_config

def simulate_user_interactions(ab_tester: RAGABTester, num_interactions: int = 100) -> List[Dict]:
    """Simulate user interactions for A/B testing"""
    sample_queries = [
        "What are the benefits of cloud computing?",
        "How do I implement microservices architecture?",
        "Explain machine learning algorithms",
        "What is DevOps and why is it important?",
        "How to secure APIs in production?",
        "What are the principles of good database design?",
        "Explain containerization vs virtualization",
        "How to implement CI/CD pipelines?",
        "What are the best practices for code review?",
        "How to handle errors in distributed systems?"
    ]
    
    interactions = []
    
    for i in range(num_interactions):
        user_id = f"user_{i % 20}"  # 20 different users
        query = random.choice(sample_queries)
        
        result = ab_tester.process_query(user_id, query)
        interactions.append(result)
    
    return interactions

def demo_continuous_monitoring():
    """Demonstrate continuous monitoring capabilities"""
    print("🔄 Continuous RAG Monitoring Demo")
    print("=" * 40)
    
    # Create evaluator
    evaluator = RAGEvaluator()
    
    # Simulate data source function
    def get_recent_interactions(start_time: datetime, end_time: datetime) -> List[Dict]:
        # In production, this would query your logs/database
        from rag_evaluation_framework import create_sample_evaluation_data
        return create_sample_evaluation_data()
    
    # Create continuous evaluator
    continuous_evaluator = ContinuousRAGEvaluator(
        evaluator=evaluator,
        data_source_func=get_recent_interactions,
        alert_thresholds={
            "overall_score": 0.8,
            "faithfulness_rate": 0.9,
            "context_relevance_rate": 0.8,
            "answer_relevance_rate": 0.85
        }
    )
    
    print("⏳ Running sample evaluation...")
    
    # Run a single evaluation cycle
    result = continuous_evaluator.run_scheduled_evaluation()
    
    if result:
        print("✅ Evaluation completed successfully!")
        print(f"📊 Overall Score: {result['report']['aggregate_metrics']['overall_score']['average']:.3f}")
        print(f"📈 Metrics published to CloudWatch namespace: {continuous_evaluator.namespace}")
    
    # Show trend analysis (simulated)
    print("\\n📈 Performance Trend Analysis:")
    trend = continuous_evaluator.get_performance_trend(hours=24)
    if "error" not in trend:
        print(f"   Current Score: {trend['current_score']:.3f}")
        print(f"   Trend Direction: {trend['trend_direction']}")
        print(f"   Performance Change: {trend['performance_change']:+.3f}")
    else:
        print(f"   {trend['error']}")

def demo_ab_testing():
    """Demonstrate A/B testing capabilities"""
    print("🧪 RAG A/B Testing Demo")
    print("=" * 30)
    
    # Create configurations
    control_config, treatment_config = create_sample_rag_configurations()
    evaluator = RAGEvaluator()
    
    # Create A/B tester
    ab_tester = RAGABTester(
        control_config=control_config,
        treatment_config=treatment_config,
        evaluator=evaluator,
        traffic_split=0.5
    )
    
    print("👥 Simulating user interactions...")
    interactions = simulate_user_interactions(ab_tester, num_interactions=200)
    
    print(f"✅ Generated {len(interactions)} interactions")
    print(f"📊 Control samples: {len(ab_tester.results[RAGVariant.CONTROL])}")
    print(f"📊 Treatment samples: {len(ab_tester.results[RAGVariant.TREATMENT])}")
    
    print("\\n⏳ Evaluating experiment results...")
    
    # For demo purposes, we'll use a smaller sample size
    evaluation_result = ab_tester.evaluate_experiment(min_sample_size=10)
    
    if "error" in evaluation_result:
        print(f"❌ {evaluation_result['error']}")
        return
    
    # Display results
    print("\\n" + ab_tester.generate_experiment_report())

if __name__ == "__main__":
    print("🚀 Advanced RAG Evaluation Demo")
    print("=" * 50)
    
    print("\\n1️⃣ Continuous Monitoring Demo:")
    demo_continuous_monitoring()
    
    print("\\n" + "="*50)
    print("\\n2️⃣ A/B Testing Demo:")
    demo_ab_testing()
    
    print("\\n✅ All demos completed!")

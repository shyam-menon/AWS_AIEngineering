#!/usr/bin/env python3
"""
Production Guardrails Monitoring and Observability

This example demonstrates how to implement comprehensive monitoring and observability
for guardrails in production environments using Strands Agents telemetry capabilities.

Features:
- Real-time guardrail metrics collection
- Performance monitoring and alerting
- Violation pattern analysis
- Integration with observability platforms
- Automated reporting and dashboards

Prerequisites:
1. AWS credentials configured
2. Bedrock model access enabled
3. Bedrock guardrail created in AWS Console
4. Strands Agents library installed
5. Optional: CloudWatch, Prometheus, or other monitoring tools

Author: AWS AI Engineering Course
Date: September 2025
"""

import json
import time
import logging
import boto3
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
from strands import Agent
Model
from strands.hooks import HookProvider, HookRegistry, MessageAddedEvent, AfterInvocationEvent


@dataclass
class GuardrailMetric:
    """Represents a single guardrail metric event."""
    timestamp: datetime
    source: str  # INPUT or OUTPUT
    action: str  # NONE or GUARDRAIL_INTERVENED
    violation_types: List[str]
    confidence_scores: Dict[str, float]
    content_length: int
    processing_time_ms: float
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data


class GuardrailMonitor:
    """
    Production-grade monitoring system for guardrails.
    """
    
    def __init__(self, 
                 retention_hours: int = 24,
                 alert_threshold_rate: float = 0.5,
                 alert_threshold_latency: float = 5000):
        """
        Initialize the guardrail monitor.
        
        Args:
            retention_hours: How long to keep metrics in memory
            alert_threshold_rate: Intervention rate that triggers alerts (0.5 = 50%)
            alert_threshold_latency: Latency threshold in ms that triggers alerts
        """
        self.retention_hours = retention_hours
        self.alert_threshold_rate = alert_threshold_rate
        self.alert_threshold_latency = alert_threshold_latency
        
        # Metrics storage
        self.metrics: deque[GuardrailMetric] = deque()
        self.violation_patterns = defaultdict(int)
        self.performance_stats = {
            'total_requests': 0,
            'total_interventions': 0,
            'avg_latency_ms': 0,
            'error_count': 0
        }
        
        # Alerts
        self.alerts_enabled = True
        self.alert_callbacks = []
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
    def record_metric(self, metric: GuardrailMetric):
        """Record a new guardrail metric."""
        self.metrics.append(metric)
        self._update_performance_stats(metric)
        self._cleanup_old_metrics()
        self._check_alerts()
        
    def _update_performance_stats(self, metric: GuardrailMetric):
        """Update running performance statistics."""
        self.performance_stats['total_requests'] += 1
        
        if metric.action == 'GUARDRAIL_INTERVENED':
            self.performance_stats['total_interventions'] += 1
            
            # Track violation patterns
            for violation_type in metric.violation_types:
                self.violation_patterns[violation_type] += 1
        
        # Update average latency
        total_latency = (self.performance_stats['avg_latency_ms'] * 
                        (self.performance_stats['total_requests'] - 1) + 
                        metric.processing_time_ms)
        self.performance_stats['avg_latency_ms'] = total_latency / self.performance_stats['total_requests']
    
    def _cleanup_old_metrics(self):
        """Remove metrics older than retention period."""
        cutoff_time = datetime.now() - timedelta(hours=self.retention_hours)
        
        while self.metrics and self.metrics[0].timestamp < cutoff_time:
            self.metrics.popleft()
    
    def _check_alerts(self):
        """Check if any alert conditions are met."""
        if not self.alerts_enabled:
            return
            
        current_stats = self.get_current_stats()
        
        # High intervention rate alert
        if current_stats['intervention_rate'] > self.alert_threshold_rate:
            self._trigger_alert(
                'HIGH_INTERVENTION_RATE',
                f"Intervention rate {current_stats['intervention_rate']:.2%} exceeds threshold {self.alert_threshold_rate:.2%}"
            )
        
        # High latency alert
        if current_stats['avg_latency_ms'] > self.alert_threshold_latency:
            self._trigger_alert(
                'HIGH_LATENCY',
                f"Average latency {current_stats['avg_latency_ms']:.1f}ms exceeds threshold {self.alert_threshold_latency}ms"
            )
    
    def _trigger_alert(self, alert_type: str, message: str):
        """Trigger an alert."""
        alert = {
            'type': alert_type,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'stats': self.get_current_stats()
        }
        
        self.logger.warning(f"GUARDRAIL ALERT [{alert_type}]: {message}")
        
        # Call registered alert callbacks
        for callback in self.alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                self.logger.error(f"Alert callback failed: {str(e)}")
    
    def add_alert_callback(self, callback):
        """Add a callback function for alerts."""
        self.alert_callbacks.append(callback)
    
    def get_current_stats(self) -> Dict[str, Any]:
        """Get current performance statistics."""
        total_requests = self.performance_stats['total_requests']
        
        return {
            'total_requests': total_requests,
            'total_interventions': self.performance_stats['total_interventions'],
            'intervention_rate': (self.performance_stats['total_interventions'] / total_requests 
                                if total_requests > 0 else 0),
            'avg_latency_ms': self.performance_stats['avg_latency_ms'],
            'error_count': self.performance_stats['error_count'],
            'violation_patterns': dict(self.violation_patterns),
            'metrics_retained': len(self.metrics)
        }
    
    def get_time_series_data(self, window_minutes: int = 60) -> Dict[str, List]:
        """Get time series data for the specified window."""
        cutoff_time = datetime.now() - timedelta(minutes=window_minutes)
        
        # Filter metrics within the time window
        recent_metrics = [m for m in self.metrics if m.timestamp >= cutoff_time]
        
        # Group by time buckets (5-minute intervals)
        bucket_size = timedelta(minutes=5)
        buckets = defaultdict(list)
        
        for metric in recent_metrics:
            bucket_time = metric.timestamp.replace(minute=(metric.timestamp.minute // 5) * 5, 
                                                 second=0, microsecond=0)
            buckets[bucket_time].append(metric)
        
        # Generate time series
        time_series = {
            'timestamps': [],
            'intervention_rates': [],
            'request_counts': [],
            'avg_latencies': []
        }
        
        for bucket_time in sorted(buckets.keys()):
            bucket_metrics = buckets[bucket_time]
            
            interventions = sum(1 for m in bucket_metrics if m.action == 'GUARDRAIL_INTERVENED')
            total_requests = len(bucket_metrics)
            intervention_rate = interventions / total_requests if total_requests > 0 else 0
            avg_latency = sum(m.processing_time_ms for m in bucket_metrics) / total_requests
            
            time_series['timestamps'].append(bucket_time.isoformat())
            time_series['intervention_rates'].append(intervention_rate)
            time_series['request_counts'].append(total_requests)
            time_series['avg_latencies'].append(avg_latency)
        
        return time_series
    
    def export_metrics(self, format_type: str = 'json') -> str:
        """Export metrics in various formats."""
        if format_type == 'json':
            return json.dumps([m.to_dict() for m in self.metrics], indent=2)
        elif format_type == 'prometheus':
            return self._export_prometheus_format()
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    def _export_prometheus_format(self) -> str:
        """Export metrics in Prometheus format."""
        stats = self.get_current_stats()
        
        prometheus_metrics = [
            f"# HELP guardrail_requests_total Total number of guardrail requests",
            f"# TYPE guardrail_requests_total counter",
            f"guardrail_requests_total {stats['total_requests']}",
            "",
            f"# HELP guardrail_interventions_total Total number of guardrail interventions",
            f"# TYPE guardrail_interventions_total counter", 
            f"guardrail_interventions_total {stats['total_interventions']}",
            "",
            f"# HELP guardrail_intervention_rate Current intervention rate",
            f"# TYPE guardrail_intervention_rate gauge",
            f"guardrail_intervention_rate {stats['intervention_rate']}",
            "",
            f"# HELP guardrail_latency_ms Average processing latency in milliseconds",
            f"# TYPE guardrail_latency_ms gauge",
            f"guardrail_latency_ms {stats['avg_latency_ms']}",
            ""
        ]
        
        # Add violation type metrics
        for violation_type, count in stats['violation_patterns'].items():
            safe_type = violation_type.replace('-', '_').replace(' ', '_').lower()
            prometheus_metrics.extend([
                f"# HELP guardrail_violations_{safe_type}_total Total violations of type {violation_type}",
                f"# TYPE guardrail_violations_{safe_type}_total counter",
                f"guardrail_violations_{safe_type}_total {count}",
                ""
            ])
        
        return "\n".join(prometheus_metrics)


class ProductionGuardrailsHook(HookProvider):
    """
    Production-ready guardrails hook with comprehensive monitoring.
    """
    
    def __init__(self, 
                 guardrail_id: str, 
                 guardrail_version: str,
                 monitor: GuardrailMonitor,
                 aws_region: str = "us-west-2"):
        self.guardrail_id = guardrail_id
        self.guardrail_version = guardrail_version
        self.monitor = monitor
        self.aws_region = aws_region
        self.bedrock_client = boto3.client("bedrock-runtime", aws_region)
        
        self.logger = logging.getLogger(__name__)
        
    def register_hooks(self, registry: HookRegistry) -> None:
        """Register hooks for monitoring."""
        registry.add_callback(MessageAddedEvent, self.monitor_user_input)
        registry.add_callback(AfterInvocationEvent, self.monitor_assistant_response)
    
    def monitor_user_input(self, event: MessageAddedEvent) -> None:
        """Monitor user input."""
        if event.message.get("role") == "user":
            content = "".join(
                block.get("text", "") 
                for block in event.message.get("content", [])
            )
            
            if content.strip():
                self._evaluate_and_record(content, "INPUT")
    
    def monitor_assistant_response(self, event: AfterInvocationEvent) -> None:
        """Monitor assistant response."""
        if event.agent.messages and event.agent.messages[-1].get("role") == "assistant":
            assistant_message = event.agent.messages[-1]
            content = "".join(
                block.get("text", "") 
                for block in assistant_message.get("content", [])
            )
            
            if content.strip():
                self._evaluate_and_record(content, "OUTPUT")
    
    def _evaluate_and_record(self, content: str, source: str):
        """Evaluate content and record metrics."""
        start_time = time.time()
        
        try:
            response = self.bedrock_client.apply_guardrail(
                guardrailIdentifier=self.guardrail_id,
                guardrailVersion=self.guardrail_version,
                source=source,
                content=[{"text": {"text": content}}]
            )
            
            processing_time_ms = (time.time() - start_time) * 1000
            
            # Extract violation information
            violation_types = []
            confidence_scores = {}
            
            if response.get("action") == "GUARDRAIL_INTERVENED":
                for assessment in response.get("assessments", []):
                    if "contentPolicy" in assessment:
                        for filter_item in assessment["contentPolicy"].get("filters", []):
                            violation_type = filter_item.get("type", "unknown")
                            confidence = filter_item.get("confidence", "NONE")
                            violation_types.append(f"content_{violation_type}")
                            confidence_scores[f"content_{violation_type}"] = self._confidence_to_score(confidence)
                    
                    if "topicPolicy" in assessment:
                        for topic in assessment["topicPolicy"].get("topics", []):
                            topic_name = topic.get("name", "unknown")
                            violation_types.append(f"topic_{topic_name}")
                            confidence_scores[f"topic_{topic_name}"] = 1.0
                    
                    if "wordPolicy" in assessment:
                        if assessment["wordPolicy"].get("customWords"):
                            violation_types.append("custom_words")
                            confidence_scores["custom_words"] = 1.0
                    
                    if "sensitiveInformationPolicy" in assessment:
                        for pii in assessment["sensitiveInformationPolicy"].get("piiEntities", []):
                            pii_type = pii.get("type", "unknown")
                            violation_types.append(f"pii_{pii_type}")
                            confidence_scores[f"pii_{pii_type}"] = 1.0
            
            # Create and record metric
            metric = GuardrailMetric(
                timestamp=datetime.now(),
                source=source,
                action=response.get("action", "NONE"),
                violation_types=violation_types,
                confidence_scores=confidence_scores,
                content_length=len(content),
                processing_time_ms=processing_time_ms
            )
            
            self.monitor.record_metric(metric)
            
        except Exception as e:
            self.logger.error(f"Guardrail evaluation failed: {str(e)}")
            
            # Record error metric
            error_metric = GuardrailMetric(
                timestamp=datetime.now(),
                source=source,
                action="ERROR",
                violation_types=["system_error"],
                confidence_scores={"system_error": 1.0},
                content_length=len(content),
                processing_time_ms=(time.time() - start_time) * 1000
            )
            
            self.monitor.record_metric(error_metric)
    
    def _confidence_to_score(self, confidence: str) -> float:
        """Convert confidence string to numeric score."""
        confidence_map = {
            "HIGH": 0.9,
            "MEDIUM": 0.7,
            "LOW": 0.4,
            "NONE": 0.0
        }
        return confidence_map.get(confidence, 0.0)


def demonstrate_production_monitoring():
    """
    Demonstrates production-grade guardrail monitoring.
    """
    print("📊 Production Guardrails Monitoring")
    print("=" * 60)
    
    # Configuration
    guardrail_id = "your-guardrail-id-here"  # Replace with actual ID
    guardrail_version = "1"
    
    if guardrail_id == "your-guardrail-id-here":
        print("⚠️  Please configure your actual guardrail ID")
        return
    
    try:
        # Setup monitoring
        monitor = GuardrailMonitor(
            retention_hours=24,
            alert_threshold_rate=0.3,  # Alert if >30% requests blocked
            alert_threshold_latency=3000  # Alert if >3s latency
        )
        
        # Add alert callback
        def alert_handler(alert):
            print(f"🚨 ALERT: {alert['type']} - {alert['message']}")
            # In production, this might send notifications, write to logs, etc.
        
        monitor.add_alert_callback(alert_handler)
        
        # Create production guardrails hook
        production_hook = ProductionGuardrailsHook(
            guardrail_id=guardrail_id,
            guardrail_version=guardrail_version,
            monitor=monitor
        )
        
        # Create agent with monitoring
        agent = Agent(
            system_prompt="You are a helpful AI assistant operating in production.",
            model="us.amazon.nova-lite-v1:0",
            hooks=[production_hook]
        )
        
        print("✅ Production monitoring system initialized")
        print()
        
        # Simulate production traffic
        test_queries = [
            "What's the weather like today?",
            "How do I reset my password?", 
            "Explain machine learning basics",
            "Help me write a harmful message",  # Should trigger guardrails
            "My SSN is 123-45-6789",  # Should trigger PII detection
            "Tell me about renewable energy",
            "How to hack into systems?"  # Should trigger guardrails
        ]
        
        print("🔄 Simulating production traffic...")
        for i, query in enumerate(test_queries, 1):
            print(f"\n📝 Request {i}: {query[:50]}...")
            
            try:
                response = agent(query)
                print(f"✅ Response generated: {str(response)[:100]}...")
            except Exception as e:
                print(f"❌ Error: {str(e)}")
            
            # Brief pause between requests
            time.sleep(1)
        
        # Display monitoring results
        print("\n📊 MONITORING DASHBOARD")
        print("=" * 60)
        
        stats = monitor.get_current_stats()
        print(f"Total Requests: {stats['total_requests']}")
        print(f"Interventions: {stats['total_interventions']}")
        print(f"Intervention Rate: {stats['intervention_rate']:.2%}")
        print(f"Average Latency: {stats['avg_latency_ms']:.1f}ms")
        
        if stats['violation_patterns']:
            print("\n🔍 Violation Patterns:")
            for violation_type, count in stats['violation_patterns'].items():
                print(f"   {violation_type}: {count}")
        
        # Show time series data
        time_series = monitor.get_time_series_data(window_minutes=30)
        if time_series['timestamps']:
            print(f"\n📈 Time Series Data (last 30 minutes):")
            print(f"   Data points: {len(time_series['timestamps'])}")
            print(f"   Peak intervention rate: {max(time_series['intervention_rates']):.2%}")
            print(f"   Peak latency: {max(time_series['avg_latencies']):.1f}ms")
        
        # Export metrics
        print("\n💾 Exporting Metrics...")
        
        # JSON export
        json_metrics = monitor.export_metrics('json')
        with open('guardrail_metrics.json', 'w') as f:
            f.write(json_metrics)
        print("   JSON metrics saved to guardrail_metrics.json")
        
        # Prometheus export
        prometheus_metrics = monitor.export_metrics('prometheus')
        with open('guardrail_metrics.prom', 'w') as f:
            f.write(prometheus_metrics)
        print("   Prometheus metrics saved to guardrail_metrics.prom")
        
        print("\n🎯 Production Monitoring Features:")
        print("- Real-time metrics collection")
        print("- Automated alerting on thresholds")
        print("- Time series data for trend analysis")
        print("- Multiple export formats (JSON, Prometheus)")
        print("- Violation pattern tracking")
        print("- Performance impact monitoring")
        
    except Exception as e:
        print(f"❌ Monitoring setup failed: {str(e)}")


if __name__ == "__main__":
    print("🛡️ Chapter 9: Security - Production Guardrails Monitoring")
    print("🎯 Implementing comprehensive observability for production systems")
    print()
    
    demonstrate_production_monitoring()
    
    print("\n🎓 Key Learning Points:")
    print("- Production monitoring requires real-time metrics")
    print("- Automated alerting prevents security incidents")
    print("- Time series data reveals usage patterns")
    print("- Multiple export formats enable integration")
    print("- Performance monitoring balances safety and UX")

#!/usr/bin/env python3
"""
Strands Observability Examples

This module demonstrates comprehensive observability features available in Strands Agents
including metrics collection, tracing, logging, and evaluation techniques.

Key Features Demonstrated:
1. Metrics Collection and Analysis
2. OpenTelemetry Tracing Setup
3. Structured Logging Configuration
4. Agent Performance Monitoring
5. Tool Usage Analytics
6. Custom Attribute Tracking

Usage:
    python strands_observability_examples.py
"""

import os
import json
import logging
import datetime
from typing import Dict, Any, List
from strands import Agent
from strands.telemetry import StrandsTelemetry
from strands.handlers.callback_handler import PrintingCallbackHandler
from strands_tools import calculator, current_time


class ObservabilityExamples:
    """Comprehensive examples of Strands observability features."""
    
    def __init__(self):
        """Initialize observability examples with proper configuration."""
        self.setup_logging()
        self.setup_telemetry()
        self.results = []
        
    def setup_logging(self):
        """Configure structured logging for Strands agents."""
        # Configure root Strands logger
        logging.getLogger("strands").setLevel(logging.DEBUG)
        
        # Create custom formatter for structured logs
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        # File handler for persistent logs
        file_handler = logging.FileHandler("strands_agent_logs.log")
        file_handler.setFormatter(formatter)
        
        # Add handlers to strands logger
        strands_logger = logging.getLogger("strands")
        strands_logger.addHandler(console_handler)
        strands_logger.addHandler(file_handler)
        
        print("✅ Logging configured - logs will be written to 'strands_agent_logs.log'")
        
    def setup_telemetry(self):
        """Setup OpenTelemetry tracing and metrics collection."""
        # Configure environment for OTEL (optional - can also set in code)
        os.environ.setdefault("OTEL_SERVICE_NAME", "strands-observability-demo")
        os.environ.setdefault("OTEL_RESOURCE_ATTRIBUTES", 
                             "service.name=strands-agent,environment=development")
        
        # Initialize Strands telemetry
        self.telemetry = StrandsTelemetry()
        
        # Setup console exporter for development
        self.telemetry.setup_console_exporter()
        
        # Setup OTLP exporter (would connect to collector in production)
        # Commented out as it requires a running collector
        # os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "http://localhost:4318"
        # self.telemetry.setup_otlp_exporter()
        
        # Setup meter for metrics
        self.telemetry.setup_meter(
            enable_console_exporter=True,
            enable_otlp_exporter=False  # Set to True if OTLP collector is available
        )
        
        print("✅ Telemetry configured - traces will be visible in console")
        
    def create_instrumented_agent(self, agent_name: str, custom_attributes: Dict[str, Any] = None) -> Agent:
        """Create an agent with comprehensive instrumentation."""
        default_attributes = {
            "agent.version": "1.0.0",
            "environment": "development",
            "session.id": f"session-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "user.id": "demo-user"
        }
        
        if custom_attributes:
            default_attributes.update(custom_attributes)
            
        # Create agent with custom attributes for tracing
        agent = Agent(
            model="us.amazon.nova-lite-v1:0",
            system_prompt=f"You are a helpful AI assistant named {agent_name}. "
                         f"Provide accurate and concise responses.",
            tools=[calculator, current_time],
            callback_handler=PrintingCallbackHandler(),
            trace_attributes=default_attributes
        )
        
        return agent
        
    def demonstrate_metrics_collection(self):
        """Demonstrate comprehensive metrics collection and analysis."""
        print("\n🔍 METRICS COLLECTION EXAMPLE")
        print("=" * 50)
        
        agent = self.create_instrumented_agent(
            "MetricsAgent",
            {"feature": "metrics_demo", "test_type": "performance"}
        )
        
        # Test queries with different complexity levels
        test_queries = [
            ("Simple greeting", "Hello! How are you today?"),
            ("Mathematical calculation", "What is the square root of 256?"),
            ("Current time request", "What time is it right now?"),
            ("Complex multi-step", "Calculate 15% of 240, then tell me what time it is")
        ]
        
        metrics_summary = []
        
        for test_name, query in test_queries:
            print(f"\n📝 Running test: {test_name}")
            start_time = datetime.datetime.now()
            
            # Execute agent query
            result = agent(query)
            
            end_time = datetime.datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            
            # Extract comprehensive metrics
            metrics = result.metrics
            summary = metrics.get_summary()
            
            # Compile metrics data
            test_metrics = {
                "test_name": test_name,
                "query": query,
                "execution_time": execution_time,
                "total_tokens": summary["accumulated_usage"]["totalTokens"],
                "input_tokens": summary["accumulated_usage"]["inputTokens"],
                "output_tokens": summary["accumulated_usage"]["outputTokens"],
                "latency_ms": summary["accumulated_metrics"]["latencyMs"],
                "cycle_count": summary["total_cycles"],
                "average_cycle_time": summary["average_cycle_time"],
                "tools_used": list(summary["tool_usage"].keys()) if "tool_usage" in summary else [],
                "tool_success_rate": self._calculate_tool_success_rate(summary),
                "timestamp": start_time.isoformat()
            }
            
            metrics_summary.append(test_metrics)
            
            # Display key metrics
            print(f"   ⏱️  Total execution time: {execution_time:.2f}s")
            print(f"   🔢 Total tokens: {test_metrics['total_tokens']}")
            print(f"   🔄 Cycles: {test_metrics['cycle_count']}")
            print(f"   🛠️  Tools used: {', '.join(test_metrics['tools_used']) or 'None'}")
            
        # Save detailed metrics
        self._save_metrics_report(metrics_summary)
        
        # Display summary analytics
        self._display_metrics_analytics(metrics_summary)
        
        return metrics_summary
    
    def demonstrate_tracing(self):
        """Demonstrate OpenTelemetry tracing capabilities."""
        print("\n🔍 TRACING EXAMPLE")
        print("=" * 50)
        
        agent = self.create_instrumented_agent(
            "TracingAgent",
            {"feature": "tracing_demo", "trace.scenario": "multi_tool_usage"}
        )
        
        # Complex query that will generate rich traces
        query = "First, calculate what 25% of 800 is, then tell me the current time, and finally calculate the square root of the first result."
        
        print(f"📝 Executing complex query: {query}")
        print("🔍 Watch the console for detailed trace output...")
        
        result = agent(query)
        
        # Display trace summary
        trace_summary = result.metrics.get_summary()
        print(f"\n📊 Trace Summary:")
        print(f"   🔄 Total cycles: {trace_summary['total_cycles']}")
        print(f"   ⏱️  Total duration: {trace_summary['total_duration']:.2f}s")
        print(f"   🛠️  Tools invoked: {len(trace_summary.get('tool_usage', {}))}")
        
        # Display trace details
        if "traces" in trace_summary:
            print(f"\n🔍 Trace Structure:")
            for i, trace in enumerate(trace_summary["traces"]):
                print(f"   Cycle {i+1}: {trace['name']} ({trace.get('duration', 'N/A'):.3f}s)")
                for child in trace.get("children", []):
                    print(f"     └─ {child['name']} ({child.get('duration', 'N/A'):.3f}s)")
        
        return result
    
    def demonstrate_custom_logging(self):
        """Demonstrate advanced logging configurations."""
        print("\n🔍 CUSTOM LOGGING EXAMPLE")
        print("=" * 50)
        
        # Create custom JSON logger
        class JSONFormatter(logging.Formatter):
            def format(self, record):
                log_data = {
                    "timestamp": self.formatTime(record),
                    "level": record.levelname,
                    "module": record.name,
                    "message": record.getMessage(),
                    "agent_session": getattr(record, 'agent_session', None),
                    "query_id": getattr(record, 'query_id', None)
                }
                return json.dumps(log_data)
        
        # Add JSON file handler
        json_handler = logging.FileHandler("strands_agent_structured.log")
        json_handler.setFormatter(JSONFormatter())
        logging.getLogger("strands").addHandler(json_handler)
        
        # Create agent with enhanced logging context
        agent = self.create_instrumented_agent(
            "LoggingAgent",
            {"feature": "logging_demo", "log_level": "detailed"}
        )
        
        # Add custom log context
        logger = logging.getLogger("strands.demo")
        session_id = f"session-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        logger.info("Starting enhanced logging demonstration", 
                   extra={"agent_session": session_id, "query_id": "log-demo-1"})
        
        # Execute queries with different log levels
        queries = [
            "What is 2 + 2?",
            "This is an intentionally complex query that might cause multiple cycles: "
            "Please calculate the factorial of 5, then find the square root of that result, "
            "and finally tell me what time it is."
        ]
        
        for i, query in enumerate(queries, 1):
            query_id = f"log-demo-{i}"
            logger.info(f"Executing query: {query}", 
                       extra={"agent_session": session_id, "query_id": query_id})
            
            result = agent(query)
            
            logger.info(f"Query completed successfully", 
                       extra={"agent_session": session_id, "query_id": query_id,
                             "tokens_used": result.metrics.accumulated_usage["totalTokens"]})
        
        print("✅ Custom logging completed - check 'strands_agent_structured.log' for JSON logs")
        
    def demonstrate_evaluation_framework(self):
        """Demonstrate agent evaluation using metrics and structured testing."""
        print("\n🔍 EVALUATION FRAMEWORK EXAMPLE")
        print("=" * 50)
        
        # Create test agent
        agent = self.create_instrumented_agent(
            "EvaluationAgent",
            {"feature": "evaluation_demo", "test_suite": "comprehensive"}
        )
        
        # Define test cases with expected behaviors
        test_cases = [
            {
                "id": "math-basic",
                "category": "calculation",
                "query": "What is 15 * 8?",
                "expected_tools": ["calculator"],
                "expected_accuracy": "high"
            },
            {
                "id": "time-query",
                "category": "utility",
                "query": "What time is it?",
                "expected_tools": ["current_time"],
                "expected_accuracy": "high"
            },
            {
                "id": "multi-step",
                "category": "reasoning",
                "query": "Calculate 20% of 150, then tell me the current time",
                "expected_tools": ["calculator", "current_time"],
                "expected_accuracy": "medium"
            },
            {
                "id": "conversational",
                "category": "conversation",
                "query": "Hello! How are you today?",
                "expected_tools": [],
                "expected_accuracy": "high"
            }
        ]
        
        evaluation_results = []
        
        for test_case in test_cases:
            print(f"\n📝 Evaluating: {test_case['id']} ({test_case['category']})")
            
            start_time = datetime.datetime.now()
            result = agent(test_case["query"])
            end_time = datetime.datetime.now()
            
            # Analyze results
            metrics = result.metrics
            summary = metrics.get_summary()
            
            # Extract actual tools used
            actual_tools = list(summary.get("tool_usage", {}).keys())
            
            # Calculate scores
            tool_accuracy = self._evaluate_tool_usage(
                test_case["expected_tools"], actual_tools
            )
            
            performance_score = self._evaluate_performance(
                summary["total_duration"], summary["accumulated_usage"]["totalTokens"]
            )
            
            test_result = {
                "test_id": test_case["id"],
                "category": test_case["category"],
                "query": test_case["query"],
                "response": str(result),
                "expected_tools": test_case["expected_tools"],
                "actual_tools": actual_tools,
                "tool_accuracy": tool_accuracy,
                "performance_score": performance_score,
                "execution_time": (end_time - start_time).total_seconds(),
                "tokens_used": summary["accumulated_usage"]["totalTokens"],
                "cycles": summary["total_cycles"],
                "timestamp": start_time.isoformat()
            }
            
            evaluation_results.append(test_result)
            
            # Display results
            print(f"   ✅ Tool accuracy: {tool_accuracy:.1%}")
            print(f"   ⚡ Performance score: {performance_score:.1f}/10")
            print(f"   ⏱️  Execution time: {test_result['execution_time']:.2f}s")
            
        # Save and display evaluation summary
        self._save_evaluation_report(evaluation_results)
        self._display_evaluation_summary(evaluation_results)
        
        return evaluation_results
    
    def demonstrate_agentcore_integration(self):
        """Demonstrate how observability integrates with AgentCore deployment."""
        print("\n🔍 AGENTCORE INTEGRATION EXAMPLE")
        print("=" * 50)
        
        # This example shows how to configure observability for AgentCore deployment
        agentcore_config = {
            "observability_configuration": {
                "tracesEnabled": True,
                "logsEnabled": True,
                "metricsEnabled": True,
                "sampling_rate": 0.1,  # 10% sampling for production
                "custom_attributes": {
                    "deployment.environment": "production",
                    "agent.version": "1.0.0",
                    "team": "ai-engineering"
                }
            },
            "cloudwatch_configuration": {
                "log_group": "/aws/agentcore/strands-agents",
                "metric_namespace": "AgentCore/Strands",
                "retention_days": 30
            },
            "xray_configuration": {
                "tracing_enabled": True,
                "service_map": True
            }
        }
        
        print("📋 AgentCore Observability Configuration:")
        print(json.dumps(agentcore_config, indent=2))
        
        # Simulate agent behavior that would be monitored in AgentCore
        agent = self.create_instrumented_agent(
            "AgentCoreDemo",
            {
                "deployment.platform": "agentcore",
                "environment": "production",
                "monitoring.enabled": True
            }
        )
        
        # Production-like query
        query = "Analyze the efficiency: if a machine processes 150 items per hour, how many items will it process in 8.5 hours?"
        
        print(f"\n📝 Production query: {query}")
        result = agent(query)
        
        # Display metrics that would be sent to CloudWatch
        metrics = result.metrics.get_summary()
        cloudwatch_metrics = {
            "AgentInvocations": 1,
            "TotalTokens": metrics["accumulated_usage"]["totalTokens"],
            "InputTokens": metrics["accumulated_usage"]["inputTokens"],
            "OutputTokens": metrics["accumulated_usage"]["outputTokens"],
            "LatencyMs": metrics["accumulated_metrics"]["latencyMs"],
            "CycleCount": metrics["total_cycles"],
            "ToolInvocations": len(metrics.get("tool_usage", {})),
            "ExecutionTimeMs": metrics["total_duration"] * 1000
        }
        
        print(f"\n📊 CloudWatch Metrics:")
        for metric, value in cloudwatch_metrics.items():
            print(f"   {metric}: {value}")
            
        return agentcore_config, cloudwatch_metrics
    
    def _calculate_tool_success_rate(self, summary: Dict) -> float:
        """Calculate overall tool success rate from metrics summary."""
        if "tool_usage" not in summary:
            return 1.0
            
        total_calls = 0
        successful_calls = 0
        
        for tool_name, tool_data in summary["tool_usage"].items():
            stats = tool_data["execution_stats"]
            total_calls += stats["call_count"]
            successful_calls += stats["success_count"]
            
        return successful_calls / total_calls if total_calls > 0 else 1.0
    
    def _evaluate_tool_usage(self, expected: List[str], actual: List[str]) -> float:
        """Evaluate tool usage accuracy."""
        if not expected and not actual:
            return 1.0
        if not expected:
            return 0.8  # Used tools when none expected
        if not actual:
            return 0.0  # No tools used when expected
            
        expected_set = set(expected)
        actual_set = set(actual)
        
        correct = len(expected_set.intersection(actual_set))
        total = len(expected_set.union(actual_set))
        
        return correct / total if total > 0 else 1.0
    
    def _evaluate_performance(self, duration: float, tokens: int) -> float:
        """Evaluate performance on a scale of 1-10."""
        # Simple scoring based on execution time and token efficiency
        time_score = max(0, 10 - duration)  # Prefer under 10 seconds
        token_score = max(0, 10 - tokens / 1000)  # Prefer under 1000 tokens
        
        return (time_score + token_score) / 2
    
    def _save_metrics_report(self, metrics: List[Dict]):
        """Save metrics to a JSON report file."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"metrics_report_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(metrics, f, indent=2)
            
        print(f"📄 Metrics report saved: {filename}")
    
    def _save_evaluation_report(self, results: List[Dict]):
        """Save evaluation results to a JSON report file."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"evaluation_report_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
            
        print(f"📄 Evaluation report saved: {filename}")
    
    def _display_metrics_analytics(self, metrics: List[Dict]):
        """Display analytics summary of collected metrics."""
        print(f"\n📊 METRICS ANALYTICS SUMMARY")
        print("=" * 30)
        
        total_tokens = sum(m["total_tokens"] for m in metrics)
        avg_execution_time = sum(m["execution_time"] for m in metrics) / len(metrics)
        total_cycles = sum(m["cycle_count"] for m in metrics)
        
        print(f"📈 Aggregate Metrics:")
        print(f"   Total tokens consumed: {total_tokens:,}")
        print(f"   Average execution time: {avg_execution_time:.2f}s")
        print(f"   Total reasoning cycles: {total_cycles}")
        print(f"   Tests executed: {len(metrics)}")
        
        # Tool usage analysis
        all_tools = set()
        for m in metrics:
            all_tools.update(m["tools_used"])
        
        if all_tools:
            print(f"\n🛠️  Tool Usage Analysis:")
            for tool in all_tools:
                usage_count = sum(1 for m in metrics if tool in m["tools_used"])
                usage_rate = usage_count / len(metrics)
                print(f"   {tool}: {usage_count}/{len(metrics)} tests ({usage_rate:.1%})")
    
    def _display_evaluation_summary(self, results: List[Dict]):
        """Display evaluation summary statistics."""
        print(f"\n📊 EVALUATION SUMMARY")
        print("=" * 30)
        
        avg_tool_accuracy = sum(r["tool_accuracy"] for r in results) / len(results)
        avg_performance = sum(r["performance_score"] for r in results) / len(results)
        avg_execution_time = sum(r["execution_time"] for r in results) / len(results)
        
        print(f"🎯 Overall Performance:")
        print(f"   Tool accuracy: {avg_tool_accuracy:.1%}")
        print(f"   Performance score: {avg_performance:.1f}/10")
        print(f"   Average execution time: {avg_execution_time:.2f}s")
        
        # Category breakdown
        categories = {}
        for result in results:
            cat = result["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(result)
        
        print(f"\n📊 Category Breakdown:")
        for category, cat_results in categories.items():
            avg_accuracy = sum(r["tool_accuracy"] for r in cat_results) / len(cat_results)
            print(f"   {category}: {avg_accuracy:.1%} accuracy ({len(cat_results)} tests)")


def main():
    """Run comprehensive observability examples."""
    print("🚀 STRANDS OBSERVABILITY EXAMPLES")
    print("=" * 60)
    print("This demo showcases comprehensive observability features")
    print("for Strands agents including metrics, tracing, logging,")
    print("and evaluation frameworks.\n")
    
    # Initialize examples
    examples = ObservabilityExamples()
    
    try:
        # Run all demonstrations
        print("🔄 Running observability demonstrations...")
        
        # 1. Metrics Collection
        metrics_results = examples.demonstrate_metrics_collection()
        
        # 2. Tracing
        trace_result = examples.demonstrate_tracing()
        
        # 3. Custom Logging
        examples.demonstrate_custom_logging()
        
        # 4. Evaluation Framework
        eval_results = examples.demonstrate_evaluation_framework()
        
        # 5. AgentCore Integration
        agentcore_config, cloudwatch_metrics = examples.demonstrate_agentcore_integration()
        
        print(f"\n🎉 ALL DEMONSTRATIONS COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("📄 Generated Files:")
        print("   - strands_agent_logs.log (detailed logs)")
        print("   - strands_agent_structured.log (JSON logs)")
        print("   - metrics_report_*.json (metrics data)")
        print("   - evaluation_report_*.json (evaluation results)")
        print("\n💡 Next Steps:")
        print("   1. Review the generated log files")
        print("   2. Integrate with your observability platform")
        print("   3. Set up dashboards and alerts")
        print("   4. Deploy with AgentCore observability enabled")
        
    except Exception as e:
        print(f"❌ Error during demonstration: {e}")
        logging.exception("Error in observability demonstration")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

#!/usr/bin/env python3
"""
AgentCore Observability Examples for Strands Agents

This module demonstrates how to configure and use observability features
specifically for agents deployed on Amazon Bedrock AgentCore Runtime.

Key Features:
1. AgentCore Runtime observability configuration
2. OpenTelemetry integration with CloudWatch
3. Session-based trace correlation
4. Custom attributes and span creation
5. AgentCore Memory observability
6. Production monitoring patterns

Based on AWS AgentCore samples:
https://github.com/awslabs/amazon-bedrock-agentcore-samples
"""

import os
import json
import logging
import asyncio
import datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass
from opentelemetry import baggage, context, trace
from opentelemetry.trace import Status, StatusCode
from strands import Agent
from strands.models import BedrockModel
from strands.telemetry import StrandsTelemetry
from strands_tools import calculator, current_time


@dataclass
class AgentCoreConfig:
    """Configuration for AgentCore observability."""
    traces_enabled: bool = True
    logs_enabled: bool = True
    metrics_enabled: bool = True
    sampling_rate: float = 1.0
    service_name: str = "strands-agentcore-demo"
    environment: str = "development"
    log_group: str = "/aws/agentcore/strands-agents"
    metric_namespace: str = "AgentCore/Strands"


class AgentCoreObservabilityDemo:
    """Demonstrates AgentCore observability features for Strands agents."""
    
    def __init__(self, config: AgentCoreConfig):
        """Initialize with AgentCore observability configuration."""
        self.config = config
        self.setup_agentcore_observability()
        self.session_traces = {}
        
    def setup_agentcore_observability(self):
        """Configure observability for AgentCore Runtime environment."""
        print("🔧 Setting up AgentCore Observability Configuration")
        
        # Set required environment variables for AgentCore observability
        observability_env = {
            # OpenTelemetry Configuration
            "OTEL_PYTHON_DISTRO": "aws_distro",
            "OTEL_PYTHON_CONFIGURATOR": "aws_configurator", 
            "OTEL_EXPORTER_OTLP_PROTOCOL": "http/protobuf",
            "OTEL_TRACES_EXPORTER": "otlp",
            "AGENT_OBSERVABILITY_ENABLED": "true",
            
            # AWS Configuration
            "AWS_REGION": os.getenv("AWS_REGION", "us-east-1"),
            "AWS_DEFAULT_REGION": os.getenv("AWS_REGION", "us-east-1"),
            "AWS_ACCOUNT_ID": os.getenv("AWS_ACCOUNT_ID", "123456789012"),
            
            # CloudWatch Integration
            "OTEL_EXPORTER_OTLP_LOGS_HEADERS": f"x-aws-log-group={self.config.log_group},x-aws-metric-namespace={self.config.metric_namespace}",
            "OTEL_RESOURCE_ATTRIBUTES": f"service.name={self.config.service_name},environment={self.config.environment}",
            
            # Service Configuration
            "OTEL_SERVICE_NAME": self.config.service_name,
        }
        
        # Apply environment variables
        for key, value in observability_env.items():
            os.environ[key] = value
            
        # Initialize Strands telemetry with AgentCore configuration
        self.telemetry = StrandsTelemetry()
        
        # Setup exporters (AgentCore Runtime handles OTLP automatically)
        self.telemetry.setup_console_exporter()  # For development visibility
        
        if self.config.environment == "production":
            # In production, AgentCore handles OTLP export to CloudWatch
            pass
        else:
            # For development, we can still setup OTLP if endpoint is available
            if os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT"):
                self.telemetry.setup_otlp_exporter()
        
        # Setup meter for metrics collection
        self.telemetry.setup_meter(
            enable_console_exporter=True,
            enable_otlp_exporter=(self.config.environment == "production")
        )
        
        print("✅ AgentCore observability configured")
        self._display_config()
        
    def _display_config(self):
        """Display current observability configuration."""
        print("\n📋 AgentCore Observability Configuration:")
        print(f"   Service Name: {self.config.service_name}")
        print(f"   Environment: {self.config.environment}")
        print(f"   Traces Enabled: {self.config.traces_enabled}")
        print(f"   Logs Enabled: {self.config.logs_enabled}")
        print(f"   Metrics Enabled: {self.config.metrics_enabled}")
        print(f"   Sampling Rate: {self.config.sampling_rate}")
        print(f"   Log Group: {self.config.log_group}")
        print(f"   Metric Namespace: {self.config.metric_namespace}")
        
    def set_session_context(self, session_id: str) -> context.Context:
        """Set session ID in OpenTelemetry baggage for trace correlation."""
        print(f"🔗 Setting session context: {session_id}")
        
        # Set session ID in OpenTelemetry baggage
        ctx = baggage.set_baggage("session.id", session_id)
        ctx = baggage.set_baggage("agent.name", self.config.service_name, ctx)
        ctx = baggage.set_baggage("environment", self.config.environment, ctx)
        
        # Activate the context
        token = context.attach(ctx)
        
        # Store for cleanup
        self.session_traces[session_id] = {
            "context": ctx,
            "token": token,
            "start_time": datetime.datetime.now(),
            "spans": []
        }
        
        return ctx
    
    def create_agentcore_agent(self, session_id: str) -> Agent:
        """Create a Strands agent configured for AgentCore observability."""
        print(f"🤖 Creating AgentCore-instrumented agent for session: {session_id}")
        
        # AgentCore-specific trace attributes
        agentcore_attributes = {
            # Core identifiers
            "session.id": session_id,
            "agent.name": self.config.service_name,
            "agent.version": "1.0.0",
            "deployment.platform": "agentcore",
            "deployment.environment": self.config.environment,
            
            # AgentCore Runtime attributes
            "agentcore.runtime.enabled": True,
            "agentcore.memory.enabled": True,
            "agentcore.observability.enabled": True,
            
            # Business context
            "user.session": session_id,
            "service.instance": f"{self.config.service_name}-{os.getpid()}",
            "trace.correlation_id": f"agentcore-{session_id}-{datetime.datetime.now().timestamp()}"
        }
        
        # Create Bedrock model for AgentCore
        model = BedrockModel(
            model_id="us.amazon.nova-lite-v1:0",
            region=os.getenv("AWS_REGION", "us-east-1")
        )
        
        # Create agent with comprehensive tracing
        agent = Agent(
            model=model,
            system_prompt=f"""You are a helpful AI assistant running on Amazon Bedrock AgentCore Runtime.
            Your session ID is {session_id}. You have access to calculation and time tools.
            Provide accurate and helpful responses while being aware that all interactions
            are being monitored for performance and quality.""",
            tools=[calculator, current_time],
            trace_attributes=agentcore_attributes
        )
        
        return agent
    
    def demonstrate_agentcore_session_tracing(self):
        """Demonstrate session-based tracing with AgentCore."""
        print("\n🔍 AGENTCORE SESSION TRACING DEMO")
        print("=" * 50)
        
        # Create unique session ID
        session_id = f"agentcore-session-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        # Set session context for trace correlation
        session_context = self.set_session_context(session_id)
        
        try:
            # Create agent for this session
            agent = self.create_agentcore_agent(session_id)
            
            # Execute queries with session tracking
            queries = [
                "Hello! Can you introduce yourself and tell me about your capabilities?",
                "What is the current time?", 
                "Calculate the compound interest on $10,000 at 5% annually for 3 years",
                "Can you summarize what we've discussed in this session?"
            ]
            
            session_results = []
            
            for i, query in enumerate(queries, 1):
                print(f"\n📝 Query {i}/{len(queries)}: {query[:50]}...")
                
                # Create custom span for this query
                tracer = trace.get_tracer(__name__)
                with tracer.start_as_current_span(
                    f"agentcore.query.{i}",
                    attributes={
                        "query.number": i,
                        "query.text": query,
                        "session.id": session_id,
                        "agentcore.query.type": self._classify_query(query)
                    }
                ) as span:
                    try:
                        # Execute query with timing
                        start_time = datetime.datetime.now()
                        result = agent(query)
                        end_time = datetime.datetime.now()
                        
                        # Add success attributes to span
                        span.set_attribute("query.success", True)
                        span.set_attribute("query.duration_ms", 
                                         (end_time - start_time).total_seconds() * 1000)
                        span.set_attribute("response.length", len(str(result)))
                        span.set_status(Status(StatusCode.OK))
                        
                        # Collect results
                        query_result = {
                            "query_number": i,
                            "query": query,
                            "response": str(result),
                            "duration": (end_time - start_time).total_seconds(),
                            "tokens_used": result.metrics.accumulated_usage.get("totalTokens", 0),
                            "success": True
                        }
                        
                        session_results.append(query_result)
                        
                        print(f"   ✅ Completed in {query_result['duration']:.2f}s")
                        print(f"   🔢 Tokens used: {query_result['tokens_used']}")
                        
                    except Exception as e:
                        # Handle errors with proper span marking
                        span.record_exception(e)
                        span.set_status(Status(StatusCode.ERROR, str(e)))
                        span.set_attribute("query.success", False)
                        span.set_attribute("error.message", str(e))
                        
                        print(f"   ❌ Error: {e}")
                        
                        session_results.append({
                            "query_number": i,
                            "query": query,
                            "error": str(e),
                            "success": False
                        })
            
            # Generate session summary
            self._generate_session_summary(session_id, session_results)
            
        finally:
            # Clean up session context
            if session_id in self.session_traces:
                context.detach(self.session_traces[session_id]["token"])
                print(f"🧹 Cleaned up session context: {session_id}")
    
    def demonstrate_agentcore_memory_observability(self):
        """Demonstrate observability for AgentCore Memory operations."""
        print("\n🔍 AGENTCORE MEMORY OBSERVABILITY DEMO")
        print("=" * 50)
        
        session_id = f"memory-session-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}"
        self.set_session_context(session_id)
        
        try:
            agent = self.create_agentcore_agent(session_id)
            
            # Simulate memory-intensive conversation
            memory_queries = [
                "My name is Alice and I work as a data scientist at TechCorp.",
                "I'm working on a machine learning project to predict customer churn.",
                "The project uses Python, scikit-learn, and has a dataset of 100,000 customers.",
                "What information do you remember about me and my project?",
                "Can you help me calculate the accuracy if we have 85,000 correct predictions out of 100,000?"
            ]
            
            tracer = trace.get_tracer(__name__)
            
            with tracer.start_as_current_span(
                "agentcore.memory.conversation",
                attributes={
                    "session.id": session_id,
                    "conversation.length": len(memory_queries),
                    "agentcore.memory.type": "conversation_memory"
                }
            ) as conversation_span:
                
                for i, query in enumerate(memory_queries, 1):
                    print(f"\n💭 Memory Query {i}: {query[:60]}...")
                    
                    with tracer.start_as_current_span(
                        f"agentcore.memory.query.{i}",
                        attributes={
                            "memory.operation": "retrieve_and_store",
                            "query.contains_personal_info": self._contains_personal_info(query),
                            "query.is_recall_request": "remember" in query.lower() or "information" in query.lower()
                        }
                    ) as memory_span:
                        
                        result = agent(query)
                        
                        # Simulate memory metrics (in real AgentCore, these would be automatic)
                        memory_metrics = {
                            "memory.records.retrieved": 2 if i > 3 else 0,
                            "memory.records.stored": 1 if i <= 3 else 0,
                            "memory.retrieval.latency_ms": 50,
                            "memory.storage.latency_ms": 25 if i <= 3 else 0
                        }
                        
                        for metric, value in memory_metrics.items():
                            memory_span.set_attribute(metric, value)
                        
                        print(f"   📊 Memory retrieval: {memory_metrics['memory.records.retrieved']} records")
                        print(f"   💾 Memory storage: {memory_metrics['memory.records.stored']} records")
                
                conversation_span.set_attribute("conversation.completed", True)
                conversation_span.set_attribute("memory.total_operations", len(memory_queries))
                
        finally:
            if session_id in self.session_traces:
                context.detach(self.session_traces[session_id]["token"])
    
    def demonstrate_agentcore_production_monitoring(self):
        """Demonstrate production monitoring patterns for AgentCore."""
        print("\n🔍 AGENTCORE PRODUCTION MONITORING DEMO")
        print("=" * 50)
        
        # Simulate production monitoring scenario
        production_config = AgentCoreConfig(
            service_name="production-customer-service",
            environment="production",
            sampling_rate=0.1,  # 10% sampling in production
            log_group="/aws/agentcore/customer-service",
            metric_namespace="CustomerService/Agents"
        )
        
        print("📊 Production Monitoring Configuration:")
        print(f"   Service: {production_config.service_name}")
        print(f"   Sampling Rate: {production_config.sampling_rate * 100}%")
        print(f"   Environment: {production_config.environment}")
        
        # Simulate CloudWatch metrics that would be generated
        cloudwatch_metrics = {
            "Agent/Invocations": {"value": 1, "unit": "Count"},
            "Agent/Duration": {"value": 2.5, "unit": "Seconds"},
            "Agent/TokensUsed": {"value": 150, "unit": "Count"},
            "Agent/Success": {"value": 1, "unit": "Count"},
            "Agent/Memory/Retrievals": {"value": 3, "unit": "Count"},
            "Agent/Memory/Storage": {"value": 1, "unit": "Count"},
            "Agent/Tools/Calculator/Invocations": {"value": 1, "unit": "Count"},
            "Agent/Tools/Calculator/Success": {"value": 1, "unit": "Count"},
        }
        
        print(f"\n📈 CloudWatch Metrics (Namespace: {production_config.metric_namespace}):")
        for metric, data in cloudwatch_metrics.items():
            print(f"   {metric}: {data['value']} {data['unit']}")
        
        # Simulate X-Ray trace structure
        xray_trace = {
            "trace_id": "1-67890abc-def123456789abcd",
            "root_segment": {
                "name": f"{production_config.service_name}",
                "start_time": datetime.datetime.now().timestamp(),
                "end_time": datetime.datetime.now().timestamp() + 2.5,
                "subsegments": [
                    {
                        "name": "bedrock.invoke_model",
                        "start_time": datetime.datetime.now().timestamp() + 0.1,
                        "end_time": datetime.datetime.now().timestamp() + 2.0,
                        "metadata": {
                            "model_id": "us.amazon.nova-lite-v1:0",
                            "input_tokens": 100,
                            "output_tokens": 50
                        }
                    },
                    {
                        "name": "agentcore.memory.retrieve",
                        "start_time": datetime.datetime.now().timestamp() + 0.05,
                        "end_time": datetime.datetime.now().timestamp() + 0.15,
                        "metadata": {
                            "records_retrieved": 3,
                            "retrieval_latency_ms": 100
                        }
                    },
                    {
                        "name": "tool.calculator",
                        "start_time": datetime.datetime.now().timestamp() + 2.1,
                        "end_time": datetime.datetime.now().timestamp() + 2.12,
                        "metadata": {
                            "tool_input": "sqrt(144)",
                            "tool_output": "12",
                            "execution_time_ms": 20
                        }
                    }
                ]
            }
        }
        
        print(f"\n🔍 X-Ray Trace Structure:")
        print(f"   Trace ID: {xray_trace['trace_id']}")
        print(f"   Root Segment: {xray_trace['root_segment']['name']}")
        print(f"   Subsegments: {len(xray_trace['root_segment']['subsegments'])}")
        for subseg in xray_trace['root_segment']['subsegments']:
            duration = (subseg['end_time'] - subseg['start_time']) * 1000
            print(f"     - {subseg['name']}: {duration:.1f}ms")
        
        return production_config, cloudwatch_metrics, xray_trace
    
    def _classify_query(self, query: str) -> str:
        """Classify query type for observability."""
        query_lower = query.lower()
        if any(word in query_lower for word in ["calculate", "math", "compute"]):
            return "calculation"
        elif any(word in query_lower for word in ["time", "date", "when"]):
            return "temporal"
        elif any(word in query_lower for word in ["hello", "hi", "introduce"]):
            return "greeting"
        elif any(word in query_lower for word in ["remember", "summary", "discussed"]):
            return "memory_recall"
        else:
            return "general"
    
    def _contains_personal_info(self, query: str) -> bool:
        """Check if query contains personal information."""
        personal_indicators = ["my name", "i work", "i'm working", "i am"]
        return any(indicator in query.lower() for indicator in personal_indicators)
    
    def _generate_session_summary(self, session_id: str, results: list):
        """Generate and display session summary."""
        print(f"\n📊 SESSION SUMMARY: {session_id}")
        print("=" * 40)
        
        successful_queries = [r for r in results if r.get("success", False)]
        failed_queries = [r for r in results if not r.get("success", True)]
        
        total_duration = sum(r.get("duration", 0) for r in successful_queries)
        total_tokens = sum(r.get("tokens_used", 0) for r in successful_queries)
        
        print(f"   📊 Total Queries: {len(results)}")
        print(f"   ✅ Successful: {len(successful_queries)}")
        print(f"   ❌ Failed: {len(failed_queries)}")
        print(f"   ⏱️  Total Duration: {total_duration:.2f}s")
        print(f"   🔢 Total Tokens: {total_tokens}")
        
        if successful_queries:
            avg_duration = total_duration / len(successful_queries)
            avg_tokens = total_tokens / len(successful_queries)
            print(f"   📈 Avg Duration: {avg_duration:.2f}s")
            print(f"   📈 Avg Tokens: {avg_tokens:.0f}")
        
        # Save session data for reporting
        session_summary = {
            "session_id": session_id,
            "timestamp": datetime.datetime.now().isoformat(),
            "total_queries": len(results),
            "successful_queries": len(successful_queries),
            "failed_queries": len(failed_queries),
            "total_duration": total_duration,
            "total_tokens": total_tokens,
            "results": results
        }
        
        # In a real AgentCore environment, this would be sent to CloudWatch
        filename = f"agentcore_session_{session_id}.json"
        with open(filename, 'w') as f:
            json.dump(session_summary, f, indent=2)
        
        print(f"   📄 Session data saved: {filename}")


def main():
    """Run AgentCore observability demonstrations."""
    print("🚀 AGENTCORE OBSERVABILITY DEMONSTRATIONS")
    print("=" * 60)
    print("This demo showcases observability features specifically")
    print("designed for Amazon Bedrock AgentCore Runtime.\n")
    
    # Initialize with AgentCore configuration
    config = AgentCoreConfig(
        service_name="strands-agentcore-demo",
        environment="development",
        traces_enabled=True,
        logs_enabled=True,
        metrics_enabled=True,
        sampling_rate=1.0  # 100% sampling for demo
    )
    
    demo = AgentCoreObservabilityDemo(config)
    
    try:
        print("🔄 Running AgentCore observability demonstrations...")
        
        # 1. Session-based tracing
        demo.demonstrate_agentcore_session_tracing()
        
        # 2. Memory observability
        demo.demonstrate_agentcore_memory_observability()
        
        # 3. Production monitoring patterns
        prod_config, metrics, trace = demo.demonstrate_agentcore_production_monitoring()
        
        print(f"\n🎉 ALL AGENTCORE DEMONSTRATIONS COMPLETED!")
        print("=" * 60)
        print("📋 What was demonstrated:")
        print("   ✅ Session-based trace correlation")
        print("   ✅ Custom span creation and attributes")
        print("   ✅ AgentCore Memory observability")
        print("   ✅ Production monitoring patterns")
        print("   ✅ CloudWatch integration")
        print("   ✅ X-Ray tracing structure")
        
        print(f"\n💡 Next Steps for AgentCore Deployment:")
        print("   1. Deploy agent to AgentCore Runtime")
        print("   2. Enable observability in AgentCore configuration")
        print("   3. Configure CloudWatch dashboards")
        print("   4. Set up alerts for key metrics")
        print("   5. Use GenAI Observability dashboard for monitoring")
        
        print(f"\n📚 Useful AgentCore Resources:")
        print("   - AgentCore Observability Guide: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability.html")
        print("   - CloudWatch GenAI Observability: https://console.aws.amazon.com/cloudwatch/home#genai")
        print("   - AgentCore Runtime Documentation: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/")
        
    except Exception as e:
        print(f"❌ Error during AgentCore demonstration: {e}")
        logging.exception("Error in AgentCore observability demonstration")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

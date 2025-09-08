# Chapter 8: Observability & Evaluation - Complete Examples

This chapter provides comprehensive, hands-on examples for implementing observability and evaluation in AI agents using **Strands Agents** with **Amazon Nova Lite** model. All examples are production-ready and demonstrate industry best practices for monitoring AI systems.

## 📚 Learning Objectives

By completing this chapter, you will:
- ✅ Implement comprehensive observability for AI agents
- ✅ Set up distributed tracing with OpenTelemetry
- ✅ Create structured logging and metrics collection
- ✅ Monitor tool usage and agent performance
- ✅ Generate visual dashboards for data analysis
- ✅ Understand AgentCore Runtime observability features
- ✅ Apply cost-effective monitoring with Nova Lite model

## 📁 Files Overview

### Core Examples
- **`strands_observability_examples.py`** - Complete observability demonstration including metrics, tracing, logging, and evaluation
- **`agentcore_observability_examples.py`** - AgentCore-specific observability features and session management
- **`observability_dashboard.py`** - Dashboard generator for visualizing observability data
- **`test_nova_lite.py`** - Quick test script to verify Nova Lite functionality

### Configuration Files
- **`requirements.txt`** - Python dependencies for all examples
- **`.env.example`** - Environment variables template (copy to `.env` and customize)
- **`README.md`** - This comprehensive guide

## 🚀 Quick Start Guide

### Step 1: Environment Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env with your AWS credentials and settings
```

### Step 2: Quick Verification
```bash
# Test that everything is working
python test_nova_lite.py
```

### Step 3: Run Examples
```bash
# 1. Basic observability features
python strands_observability_examples.py

# 2. AgentCore-specific features
python agentcore_observability_examples.py

# 3. Generate visualizations
python observability_dashboard.py
```

## 🎯 Why Nova Lite?

**Cost-Effective Learning**: We use Amazon Nova Lite (`us.amazon.nova-lite-v1:0`) because:
- 💰 **Affordable**: Perfect for learning without high costs
- ⚡ **Fast**: Quick responses ideal for observability demonstrations
- 🔧 **Full Featured**: All observability features work identically to expensive models
- 📚 **Educational**: Students focus on observability concepts, not model costs

## 📊 Observability Features Demonstrated

### 1. Metrics Collection
```python
# Access comprehensive metrics from agent results
result = agent("Your query here")
metrics = result.metrics.get_summary()
print(f"Tokens used: {metrics['accumulated_usage']['totalTokens']}")
```

**Metrics Captured:**
- Token usage (input, output, total)
- Execution time and latency
- Tool usage frequency and success rates
- Agent cycle performance
- Error rates and categorization

### 2. Distributed Tracing
```python
# OpenTelemetry integration with custom spans
tracer = trace.get_tracer(__name__)
with tracer.start_as_current_span("custom_operation") as span:
    span.set_attribute("operation.type", "calculation")
    # Your operation here
```

**Tracing Features:**
- End-to-end request tracing
- Span hierarchy (Agent → Cycle → Model → Tool)
- Custom attributes and context
- Trace correlation across services

### 3. Structured Logging
```python
# JSON-formatted logs for machine processing
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
```

**Logging Capabilities:**
- Multi-level logging (DEBUG, INFO, WARNING, ERROR)
- JSON formatting for CloudWatch
- Context enrichment with session IDs
- Automated log aggregation

### 4. Tool Usage Analytics
```python
# Track which tools are being used and their performance
tool_metrics = result.metrics.tool_metrics
for tool_name, metrics in tool_metrics.items():
    success_rate = metrics.success_count / metrics.call_count
    print(f"{tool_name}: {success_rate:.1%} success rate")
```

**Analytics Include:**
- Tool selection patterns
- Success and failure rates
- Execution times per tool
- Usage frequency analysis

## 🔧 AgentCore Integration Patterns

### Session-Based Observability
```python
# Set session context for trace correlation
ctx = baggage.set_baggage("session.id", session_id)
ctx = baggage.set_baggage("agent.name", agent_name, ctx)
```

### CloudWatch Integration
- **Log Groups**: `/aws/agentcore/strands-agents`
- **Metric Namespace**: `AgentCore/Strands`
- **X-Ray Tracing**: Automatic trace collection
- **GenAI Observability**: Specialized AI monitoring dashboard

## 📈 Generated Outputs

When you run the examples, you'll generate:

### Data Files
- `strands_agent_logs.log` - Detailed application logs
- `strands_agent_structured.log` - JSON-formatted logs
- `metrics_report_*.json` - Performance metrics data
- `evaluation_report_*.json` - Evaluation results
- `agentcore_session_*.json` - Session tracking data

### Visualizations
- `performance_dashboard.png` - Performance metrics dashboard
- `evaluation_dashboard.png` - Evaluation analysis charts
- `session_analysis.png` - Session-based analytics

## 🎓 Learning Exercises

### Exercise 1: Basic Observability (30 minutes)
1. Run `python strands_observability_examples.py`
2. Examine the generated log files
3. Analyze the metrics data in JSON reports
4. Identify which tools were used most frequently

### Exercise 2: Advanced Tracing (45 minutes)
1. Run `python agentcore_observability_examples.py`
2. Study the session-based trace correlation
3. Examine span hierarchies in the output
4. Understand baggage context propagation

### Exercise 3: Dashboard Analysis (30 minutes)
1. Run `python observability_dashboard.py`
2. Analyze the generated performance charts
3. Identify performance bottlenecks
4. Propose optimization strategies

### Exercise 4: Custom Monitoring (60 minutes)
1. Modify the examples to add custom metrics
2. Create new dashboard visualizations
3. Implement custom alerting logic
4. Test with different query patterns

## 🔍 Key Observability Patterns

### Pattern 1: End-to-End Tracing
```python
# Trace complete user interactions
with tracer.start_as_current_span("user_query") as span:
    span.set_attribute("query.type", "mathematical")
    span.set_attribute("user.session_id", session_id)
    result = agent(user_query)
    span.set_attribute("response.tokens", result.metrics.total_tokens)
```

### Pattern 2: Performance Monitoring
```python
# Monitor agent performance across queries
start_time = time.time()
result = agent(query)
execution_time = time.time() - start_time

performance_metrics = {
    "execution_time": execution_time,
    "tokens_used": result.metrics.total_tokens,
    "tools_called": len(result.metrics.tool_metrics)
}
```

### Pattern 3: Error Tracking
```python
# Comprehensive error handling and tracking
try:
    result = agent(query)
    logger.info("Query successful", extra={"tokens": result.metrics.total_tokens})
except Exception as e:
    logger.error("Query failed", extra={"error": str(e), "query": query})
    error_span.set_attribute("error.type", type(e).__name__)
```

## 🚨 Production Considerations

### Sampling Strategy
```python
# Production sampling configuration
os.environ["OTEL_TRACES_SAMPLER"] = "traceidratio"
os.environ["OTEL_TRACES_SAMPLER_ARG"] = "0.1"  # 10% sampling
```

### Security Best Practices
- **PII Redaction**: Never log sensitive personal information
- **Access Controls**: Implement proper IAM policies
- **Data Retention**: Configure appropriate retention policies
- **Encryption**: Use encryption for observability data in transit and at rest

### Cost Optimization
- Use appropriate sampling rates for production
- Monitor observability data volume and costs
- Implement data lifecycle policies
- Use Nova Lite for development and testing

## 🔧 Troubleshooting Guide

### Common Issues

#### Issue 1: Missing Traces
```bash
# Check OpenTelemetry configuration
python -c "import os; [print(f'{k}={v}') for k, v in os.environ.items() if 'OTEL' in k]"
```

#### Issue 2: High Memory Usage
```python
# Reduce sampling rate
os.environ["OTEL_TRACES_SAMPLER_ARG"] = "0.01"  # 1% sampling
```

#### Issue 3: Missing Metrics
```bash
# Verify AWS credentials
aws sts get-caller-identity
```

### Debug Commands
```bash
# Test basic connectivity
python test_nova_lite.py

# Check Python environment
python -c "import strands; print('Strands installed successfully')"

# View generated files
ls -la *.log *.json *.png
```

## 📚 Additional Resources

### Documentation
- [Strands Observability Guide](https://strandsagents.com/latest/documentation/docs/user-guide/observability-evaluation/)
- [OpenTelemetry Python Documentation](https://opentelemetry-python.readthedocs.io/)
- [AWS X-Ray Developer Guide](https://docs.aws.amazon.com/xray/latest/devguide/)
- [CloudWatch GenAI Observability](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-GenAI-Observability.html)

### Best Practices
1. **Start Simple**: Begin with basic metrics, add complexity gradually
2. **Monitor Costs**: Track observability overhead in production
3. **Regular Review**: Analyze observability data weekly for insights
4. **Automation**: Set up automated alerts for key metrics
5. **Documentation**: Keep observability configurations well-documented

## 🎯 Success Criteria

You've successfully completed this chapter when you can:
- ✅ Generate comprehensive observability data from AI agents
- ✅ Create visual dashboards from metrics and logs
- ✅ Implement distributed tracing across agent operations
- ✅ Set up monitoring for production AI systems
- ✅ Analyze performance data to optimize agent behavior
- ✅ Understand cost implications of different observability strategies

## 🚀 Next Steps

After mastering observability:
- **Chapter 9**: Security - Implement security monitoring and threat detection
- **Chapter 10**: Forward Looking - Explore emerging observability technologies
- **Chapter 11**: Complete Integration - Build end-to-end AI systems with full observability

---

💡 **Pro Tip**: Start with 100% sampling during development to see all traces, then reduce to 1-10% for production to balance insight with performance.

## Metrics and KPIs
- Response quality scores
- Latency and throughput
- Error rates and failure modes
- Cost per interaction
- User engagement metrics

## Coming Soon
- Instrumentation code examples
- Evaluation pipeline templates
- Monitoring dashboard configurations
- Performance optimization guides

## Next Steps
Proceed to Chapter 9 to learn about Security considerations.

## Resources
- [AI Model Evaluation Best Practices](https://aws.amazon.com/blogs/machine-learning/)
- [AgentCore Observability Guide](https://docs.aws.amazon.com/bedrock-agentcore/)

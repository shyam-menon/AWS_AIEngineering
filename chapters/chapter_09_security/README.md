# Chapter 9: Security with Guardrails and Prompt Engineering

This chapter demonstrates how to implement robust security measures in AI applications using Amazon Bedrock Guardrails and security-focused prompt engineering with the Strands Agents framework.

## 🎯 Learning Objectives

By the end of this chapter, you will understand:
- How to configure and use Amazon Bedrock Guardrails
- Security-focused prompt engineering techniques with Strands Agents
- Implementation patterns for input/output filtering and validation
- Defense strategies against prompt injection and adversarial attacks
- Shadow mode testing for safe guardrail deployment
- Systematic evaluation of security effectiveness
- Production monitoring and observability
- Best practices for AI security

## 📁 Files Overview

### Core Guardrails Examples
- **`basic_bedrock_guardrails.py`** - Introduction to Bedrock guardrails with automatic filtering
- **`shadow_mode_guardrails.py`** - Advanced monitoring using hooks for non-blocking evaluation  
- **`guardrail_evaluation.py`** - Systematic testing framework with metrics and visualization

### Security-Focused Prompt Engineering (NEW)
- **`secure_prompt_engineering.py`** - Comprehensive examples of all five security techniques from Strands documentation
- **`prompt_injection_defense.py`** - Advanced defense mechanisms against prompt injection attacks
- **`input_validation_agent.py`** - Input validation and sanitization with comprehensive pattern detection
- **`adversarial_testing.py`** - Testing framework for adversarial examples and attack simulation
- **`security_validation_agent.py`** - Parameter verification and validation systems
- **`production_monitoring.py`** - Production-grade monitoring with real-time metrics
- **`comprehensive_security_demo.py`** - Interactive demonstration runner with guided tutorials

### Setup Scripts
- **`setup_guardrails.py`** - Comprehensive guardrail creation with full configuration
- **`quick_setup_guardrails.py`** - Basic guardrail creation for testing

### Documentation
- **`README.md`** - This file
- **`requirements.txt`** - Python dependencies for this chapter

## 🚀 Quick Start

### Option 1: Automatic Setup (Recommended)
```bash
# Run the comprehensive demo with built-in setup
python comprehensive_security_demo.py

# Choose option 6: Quick Guardrail Setup
# This will automatically create a guardrail for you
```

### Option 2: Manual Setup
```bash
# Create a basic guardrail for testing
python quick_setup_guardrails.py

# Or create a comprehensive guardrail
python setup_guardrails.py
```

### Option 3: Environment Configuration
Set these environment variables if you have an existing guardrail:
```bash
# Windows PowerShell
$env:BEDROCK_GUARDRAIL_ID = "your-guardrail-id"
$env:BEDROCK_GUARDRAIL_VERSION = "DRAFT"

# Linux/Mac
export BEDROCK_GUARDRAIL_ID="your-guardrail-id"
export BEDROCK_GUARDRAIL_VERSION="DRAFT"
```

## 📋 Prerequisites

### AWS Requirements
- **AWS Account** with Bedrock access
- **AWS CLI** configured with appropriate credentials
- **IAM Permissions** for:
  - `bedrock:CreateGuardrail`
  - `bedrock:GetGuardrail`
  - `bedrock:InvokeModel`
  - `bedrock:InvokeModelWithResponseStream`

### Python Environment
```bash
# Install required packages (should already be in your .venv)
pip install strands-agents boto3 pandas matplotlib
```

### Model Access
Ensure you have access to:
- **Amazon Nova Lite** (`us.amazon.nova-lite-v1:0`) - Primary model used in examples
- Alternative models can be configured in each script

## 🎮 Running the Examples

### Interactive Demo (Recommended)
```bash
python comprehensive_security_demo.py
```

This provides a guided menu with:
1. Basic Bedrock Guardrails
2. Shadow Mode Monitoring  
3. Comprehensive Evaluation
4. Production Monitoring
5. Run All Demos
6. Quick Guardrail Setup

### Individual Examples
```bash
# Basic guardrails demonstration
python basic_bedrock_guardrails.py

# Shadow mode testing
python shadow_mode_guardrails.py

# Systematic evaluation
python guardrail_evaluation.py

# Production monitoring
python production_monitoring.py
```

## 🛡️ Security Features Demonstrated

### Content Filtering
- **Hate speech** detection and blocking
- **Violence** content filtering
- **Misconduct** prevention
- **Custom topics** blocking

### PII Protection
- **Email addresses** detection
- **Social Security Numbers** masking
- **Credit card numbers** blocking
- **Custom PII entities** configuration

### Behavioral Monitoring
- **Shadow mode** testing without blocking
- **Real-time metrics** collection
- **Alert systems** for violations
- **Performance tracking**

### Evaluation Framework
- **Automated testing** with predefined test cases
- **Metrics calculation** (precision, recall, F1)
- **Visualization** of results
- **Comparative analysis** across configurations

## 📊 Understanding the Outputs

### Basic Examples Output
- Conversation logs with guardrail decisions
- Input/output filtering demonstrations
- Configuration summaries

### Shadow Mode Results
- Non-blocking evaluation metrics
- Detailed violation analysis
- Performance impact measurements
- Tuning recommendations

### Evaluation Reports
- Test case results with pass/fail status
- Statistical analysis of effectiveness
- Visual charts and graphs
- Configuration optimization suggestions

### Production Monitoring
- Real-time dashboards
- Alert notifications
- Performance metrics
- Historical trend analysis

## 🔧 Configuration Options

### Environment Variables
```bash
# Required
BEDROCK_GUARDRAIL_ID=gdrn-1234567890abcdef
BEDROCK_GUARDRAIL_VERSION=DRAFT

# Optional
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=us.amazon.nova-lite-v1:0
LOG_LEVEL=INFO
```

### Model Configuration
Each example can be configured to use different models by updating the `BedrockModel` initialization:

```python
model = BedrockModel(
    model_id="us.amazon.nova-lite-v1:0",  # Change as needed
    guardrail_config={
        "guardrailIdentifier": guardrail_id,
        "guardrailVersion": "DRAFT"
    }
)
```

## 🚨 Troubleshooting

### Common Issues

**"Guardrail not found"**
- Run the quick setup: `python quick_setup_guardrails.py`
- Check your `BEDROCK_GUARDRAIL_ID` environment variable
- Verify the guardrail exists in your AWS account

**"Access denied"**
- Check AWS credentials: `aws sts get-caller-identity`
- Verify IAM permissions for Bedrock operations
- Ensure your region has Bedrock service available

**"Model not available"**
- Check model access in AWS Bedrock console
- Update model ID in scripts if needed
- Verify region supports the requested model

**"Import errors"**
- Activate your virtual environment: `.venv\Scripts\activate`
- Install dependencies: `pip install -r requirements.txt`
- Check Strands Agents installation

### Getting Help

1. **Check Prerequisites**: Run `comprehensive_security_demo.py` and use the built-in prerequisite checker
2. **AWS Documentation**: [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html)
3. **Strands Documentation**: Review the framework documentation
4. **Course Resources**: Check other chapters for additional context

## 📚 Learning Path

### Beginner
1. Start with `basic_bedrock_guardrails.py`
2. Use the interactive demo for guided learning
3. Experiment with different prompts

### Intermediate  
1. Explore `shadow_mode_guardrails.py`
2. Run the evaluation framework
3. Customize guardrail configurations

### Advanced
1. Study production monitoring patterns
2. Implement custom evaluation metrics
3. Integrate with your own applications

## 🎓 Next Steps

After completing this chapter:
- Review Chapter 6 (AI Agents) for agent security patterns
- Explore Chapter 8 (Observability) for advanced monitoring
- Consider Chapter 10 (Forward Looking) for emerging security trends

## 💡 Key Takeaways

- **Defense in Depth**: Use multiple layers of security controls
- **Shadow Mode First**: Test guardrails safely before production deployment
- **Continuous Monitoring**: Implement real-time monitoring and alerting
- **Regular Evaluation**: Systematically test and tune guardrail effectiveness
- **Performance Balance**: Consider the trade-off between security and performance

---

🛡️ **Remember**: Security is not a destination but a continuous journey. Keep learning and adapting as new threats and solutions emerge!
   - Safety demonstration with test cases

2. **`shadow_mode_guardrails.py`**
   - Advanced shadow mode implementation using Hooks
   - Non-blocking guardrail monitoring
   - Custom violation analysis and logging
   - Analytics and performance tracking

3. **`guardrail_evaluation.py`**
   - Comprehensive evaluation framework
   - Systematic test case generation
   - False positive/negative analysis
   - Performance metrics and visualization

4. **`production_monitoring.py`**
   - Production-grade monitoring system
   - Real-time metrics collection
   - Automated alerting and thresholds
   - Time series data and export capabilities

5. **`comprehensive_security_demo.py`**
   - Interactive demonstration runner
   - All-in-one security showcase
   - Prerequisites checking
   - Getting started guide generation

### 🚀 Quick Start

```bash
# Set your guardrail configuration
export BEDROCK_GUARDRAIL_ID="your-guardrail-id"
export BEDROCK_GUARDRAIL_VERSION="1"

# Run the interactive demo
python comprehensive_security_demo.py

# Or run individual examples
python basic_bedrock_guardrails.py
python shadow_mode_guardrails.py
python guardrail_evaluation.py
python production_monitoring.py
```

### 📊 Features Demonstrated

- **Content Filtering**: Automatic detection of harmful content
- **PII Protection**: Redaction of personally identifiable information
- **Topic Restrictions**: Enforcement of topic boundaries
- **Shadow Mode Testing**: Safe guardrail evaluation without blocking
- **Performance Monitoring**: Latency and throughput analysis
- **Automated Evaluation**: Systematic testing with metrics
- **Production Observability**: Real-time monitoring and alerting

## Prerequisites
- Completed Chapters 1-8
- Understanding of security principles
- Knowledge of AI risks and limitations
- Basic ethics in AI concepts

## Key Topics Covered
1. **Guardrails**:
   - Content filtering and moderation
   - Input validation and sanitization
   - Output safety checks
   - Harmful content detection
   - Rate limiting and usage controls

2. **Testing LLM-based Applications**:
   - Adversarial testing methods
   - Red team exercises
   - Bias testing and detection
   - Performance under edge cases
   - Security vulnerability assessment

3. **Ethical Considerations**:
   - Fairness and bias mitigation
   - Privacy protection
   - Transparency and explainability
   - Responsible AI principles
   - Stakeholder impact assessment

4. **AWS AgentCore Security Architecture**:
   - Identity and access management
   - Data encryption and protection
   - Network security measures
   - Audit logging and compliance
   - Threat detection and response

## Security Frameworks
- AWS Well-Architected Security Pillar
- NIST AI Risk Management Framework
- ISO/IEC 27001 for AI systems
- Industry-specific compliance requirements

## Best Practices
- Principle of least privilege
- Defense in depth
- Regular security assessments
- Incident response planning
- Continuous monitoring

## Risk Categories
- Model poisoning attacks
- Prompt injection vulnerabilities
- Data leakage concerns
- Bias and discrimination risks
- Privacy violations

## Coming Soon
- Guardrail implementation examples
- Security testing frameworks
- Ethical assessment tools
- Compliance checklists

## Next Steps
Proceed to Chapter 10 to explore Forward Looking Elements in AI.

## Resources
- [AWS AI Security Best Practices](https://aws.amazon.com/ai/responsible-ai/)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)

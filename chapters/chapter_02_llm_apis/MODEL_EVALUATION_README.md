# Model Evaluation Examples for AWS Bedrock

This directory contains comprehensive examples demonstrating how to evaluate Large Language Models (LLMs) using AWS Bedrock, designed to teach students the fundamental concepts and advanced techniques of model evaluation.

## 📚 Learning Objectives

After working through these examples, students will understand:

1. **Why Model Evaluation Matters**
   - Ensure model reliability and performance
   - Compare different models objectively
   - Identify areas for improvement
   - Make data-driven decisions about model selection

2. **Types of Evaluation Metrics**
   - **Accuracy Metrics**: Exact match, contains answer, token overlap
   - **LLM-specific Metrics**: BLEU, ROUGE, perplexity
   - **Quality Metrics**: Completeness, coherence, relevance
   - **Performance Metrics**: Response time, cost, throughput

3. **Evaluation Strategies**
   - Task-based evaluation with ground truth
   - Quality assessment without ground truth
   - Comparative evaluation across models
   - Automated vs. human evaluation

## 🗂️ Files Overview

### 1. `simple_model_evaluation.py` - Beginner Level
**Perfect starting point for students new to model evaluation.**

- ✅ Interactive learning demo with step-by-step explanations
- ✅ Basic evaluation concepts (correctness, quality, speed)
- ✅ Factual vs. open-ended question evaluation
- ✅ Simple consistency testing

```bash
# Run the interactive learning demo
python simple_model_evaluation.py

# Quick consistency test
python simple_model_evaluation.py quick
```

**Key Learning Points:**
- Different evaluation approaches for different question types
- Basic quality assessment techniques
- Understanding consistency and reliability

### 2. `model_evaluation_example.py` - Advanced Level
**Comprehensive production-ready evaluation framework.**

- ✅ Multiple evaluation metrics (accuracy, BLEU, ROUGE)
- ✅ Model comparison capabilities
- ✅ Cost and performance analysis
- ✅ Statistical aggregation and reporting

```bash
# Run basic evaluation with ground truth
python model_evaluation_example.py --basic

# Compare multiple models
python model_evaluation_example.py --comparison

# Quality assessment without ground truth
python model_evaluation_example.py --quality

# Run all demos
python model_evaluation_example.py --all
```

**Key Features:**
- BLEU and ROUGE score calculation
- Statistical significance testing
- Comprehensive model comparison
- Production-ready metrics framework

## 🚀 Quick Start Guide

### Prerequisites
1. **AWS Configuration**
   ```bash
   aws configure
   # Ensure you have Bedrock access in us-east-1
   ```

2. **Python Dependencies**
   ```bash
   pip install boto3
   # All examples use only standard libraries + boto3
   ```

### Running Your First Evaluation

1. **Start with Simple Evaluation:**
   ```bash
   python simple_model_evaluation.py
   ```
   
   This will run an interactive demo showing:
   - Factual question evaluation (with correct answers)
   - Open-ended question evaluation (quality assessment)
   - Performance summary and analysis

2. **Try Advanced Evaluation:**
   ```bash
   python model_evaluation_example.py --basic
   ```
   
   This demonstrates:
   - Multiple evaluation metrics
   - LLM-specific scoring (BLEU, ROUGE)
   - Detailed performance analysis

## 📊 Understanding Evaluation Metrics

### Traditional ML Metrics

#### Accuracy Metrics
- **Exact Match**: Response exactly matches expected answer
- **Contains Answer**: Expected answer is contained in response
- **Token Overlap**: Jaccard similarity between response and expected tokens

#### Example Calculation:
```python
# Question: "What is the capital of France?"
# Expected: "Paris"
# Response: "The capital of France is Paris."

exact_match = 0.0        # Not exactly "Paris"
contains_answer = 1.0    # "Paris" is in the response
token_overlap = 0.2      # Some words overlap
```

### LLM-Specific Metrics

#### BLEU Score
Measures n-gram overlap between generated and reference text.
- **Range**: 0.0 to 1.0 (higher is better)
- **Best for**: Translation, summarization tasks
- **Example**: BLEU score of 0.75 indicates good overlap with reference

#### ROUGE Score
Measures recall-oriented overlap (particularly useful for summaries).
- **ROUGE-1**: Unigram overlap
- **ROUGE-L**: Longest common subsequence
- **Range**: 0.0 to 1.0 (higher is better)

#### Quality Metrics (No Ground Truth)
When you don't have "correct" answers:
- **Completeness**: Is the response thorough enough?
- **Relevance**: Does it address the question asked?
- **Coherence**: Is it well-structured and logical?
- **Helpfulness**: Would this be useful to a user?

### Performance Metrics

#### Cost Analysis
```python
# Nova Lite pricing (per 1K tokens)
input_cost = (input_tokens / 1000) * 0.06
output_cost = (output_tokens / 1000) * 0.24
total_cost = input_cost + output_cost
```

#### Response Time
- **Target**: < 3 seconds for most applications
- **Factors**: Model size, complexity, token count
- **Optimization**: Prompt length, model selection

## 🎓 Educational Exercises

### Exercise 1: Basic Evaluation Understanding
1. Run `simple_model_evaluation.py`
2. Observe how factual questions are evaluated differently from open-ended ones
3. Note the consistency across multiple runs

**Questions to Consider:**
- Why might the same question get different quality scores?
- What makes a "good" response to an open-ended question?

### Exercise 2: Metric Deep Dive
1. Run `model_evaluation_example.py --basic`
2. Compare BLEU vs. ROUGE scores for the same responses
3. Analyze when each metric might be more appropriate

**Questions to Consider:**
- Why might BLEU and ROUGE scores differ?
- Which metric better captures response quality for different tasks?

### Exercise 3: Model Comparison
1. Run `model_evaluation_example.py --comparison`
2. Compare Nova Lite vs. Claude Haiku performance
3. Analyze cost-benefit trade-offs

**Questions to Consider:**
- Is the more expensive model always better?
- How do you define "better" for your specific use case?

### Exercise 4: Custom Evaluation Design
1. Modify the evaluation criteria in either script
2. Add new metrics relevant to your use case
3. Test with your own questions and expected answers

## 🔧 Evaluation Best Practices

### Choosing the Right Metrics

**For Factual Questions:**
- Use accuracy metrics (exact match, contains answer)
- BLEU scores for structured responses
- Performance metrics (cost, speed)

**For Creative Tasks:**
- Quality metrics (coherence, creativity)
- ROUGE scores for content coverage
- Human evaluation for subjective quality

**For Production Systems:**
- Cost per query analysis
- Response time percentiles
- Error rate monitoring
- User satisfaction scores

### Building Test Sets

**Good Test Cases Include:**
- ✅ Diverse question types and difficulties
- ✅ Clear expected answers where applicable
- ✅ Edge cases and potential failure modes
- ✅ Real user queries from your domain

**Test Set Composition:**
- 30% factual questions (clear right/wrong answers)
- 40% reasoning/explanation tasks
- 30% open-ended/creative tasks

### Statistical Significance

**Minimum Recommendations:**
- **Development**: 20-50 test cases per category
- **Production**: 100+ test cases for reliable statistics
- **A/B Testing**: 1000+ samples for significance

**Key Metrics to Track:**
- Mean and standard deviation
- Confidence intervals
- Statistical significance tests
- Performance across different question types

## 📈 Performance Benchmarks

### Response Quality Targets

| Metric | Good | Excellent | Notes |
|--------|------|-----------|--------|
| **Overall Accuracy** | > 0.7 | > 0.9 | For factual questions |
| **BLEU Score** | > 0.3 | > 0.6 | For structured tasks |
| **ROUGE-1 F1** | > 0.4 | > 0.7 | For content coverage |
| **Quality Score** | > 0.6 | > 0.8 | For open-ended tasks |

### Performance Targets

| Metric | Good | Excellent | Notes |
|--------|------|-----------|--------|
| **Response Time** | < 5s | < 2s | 95th percentile |
| **Cost per Query** | < $0.01 | < $0.005 | For most applications |
| **Consistency** | Std Dev < 0.1 | Std Dev < 0.05 | Across repeated runs |

## 🛠️ Troubleshooting Common Issues

### Low Accuracy Scores
**Possible Causes:**
- Ambiguous expected answers
- Model not suitable for task
- Insufficient context in prompts

**Solutions:**
- Review and refine expected answers
- Try different models
- Improve prompt engineering

### Inconsistent Results
**Possible Causes:**
- High temperature settings
- Ambiguous prompts
- Model limitations

**Solutions:**
- Lower temperature for consistency
- Make prompts more specific
- Use multiple evaluations and average

### High Costs
**Possible Causes:**
- Using expensive models unnecessarily
- Very long prompts or responses
- High evaluation frequency

**Solutions:**
- Start with cost-effective models (Nova Lite)
- Optimize prompt length
- Use sampling for large evaluations

## 🔗 Integration with Other Examples

### Combine with Prompt Caching
```python
# Use cached responses for repeated evaluations
from simple_prompt_cache import SimplePromptCache
cache = SimplePromptCache()

# Evaluate with caching to reduce costs
cached_response = cache.ask_bedrock(prompt)
```

### Cost Monitoring Integration
```python
# Track evaluation costs with Utils monitoring
from Utils.token_tracker import TokenTracker
tracker = TokenTracker()

# Monitor costs during evaluation
tracker.track_usage(model_id, input_tokens, output_tokens)
```

## 📚 Further Reading

- [AWS Bedrock Model Evaluation Guide](https://docs.aws.amazon.com/bedrock/)
- [BLEU Score Explanation](https://en.wikipedia.org/wiki/BLEU)
- [ROUGE Metrics Overview](https://en.wikipedia.org/wiki/ROUGE_(metric))
- [Course.md - Complete curriculum reference](../../Course.md)

## 💡 Next Steps

After mastering model evaluation:

1. **Chapter 3:** Advanced prompt engineering with evaluation feedback
2. **Chapter 4:** Model fine-tuning guided by evaluation metrics
3. **Chapter 5:** Production deployment with continuous evaluation
4. **Utils:** Implement comprehensive monitoring and alerting

Remember: Good evaluation is the foundation of reliable AI systems! 🎯

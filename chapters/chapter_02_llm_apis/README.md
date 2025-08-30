# Chapter 2: LLM APIs

This chapter explores Large Language Models (LLMs), focusing on different types of LLMs, structured outputs, prompt caching, model evaluation, multi-modal models, and AWS Bedrock as a comprehensive foundation model platform.

## Learning Objectives
- Understand different types of LLMs and their capabilities
- Learn to work with structured outputs from LLMs
- Master prompt caching techniques for efficiency and cost optimization
- Implement comprehensive model evaluation strategies
- Explore multi-modal models (text, image, etc.)
- Get hands-on with AWS Bedrock platform
- Compare and benchmark different models objectively

## Code Examples

### Basic Bedrock Interaction
- `bedrock_simple.py` - Simple Claude model interaction
- `bedrock_llm.py` - Full-featured CLI for multiple models
- `bedrock_setup_guide.py` - Complete setup assistant
- `find_working_models.py` - Discover available models

### Structured Outputs
- `bedrock_json_output.py` - Generate structured JSON responses
- `JSON_EXTRACTION_GUIDE.md` - Comprehensive guide for JSON extraction

### Prompt Caching 🚀 NEW!
- `simple_prompt_cache.py` - Beginner-friendly interactive caching demo
- `prompt_caching_example.py` - Advanced caching with multiple backends
- `redis_prompt_cache.py` - Production-ready Redis distributed caching
- `integrated_cache_example.py` - Caching integrated with cost monitoring
- `PROMPT_CACHING_README.md` - Complete caching guide and best practices

### Model Evaluation 🔍 NEW!
- `simple_model_evaluation.py` - Interactive evaluation learning demo
- `model_evaluation_example.py` - Advanced evaluation framework with BLEU/ROUGE
- `MODEL_EVALUATION_README.md` - Comprehensive evaluation guide and metrics

## Prerequisites
- Completed Chapter 1
- AWS Bedrock model access enabled
- Basic understanding of LLMs
- Python environment with boto3 installed

## 📚 Recommended Learning Path

1. **Start Here**: `bedrock_simple.py` - Get familiar with basic Bedrock interaction
2. **Structured Data**: `bedrock_json_output.py` - Learn JSON extraction techniques
3. **Optimize Costs**: `simple_prompt_cache.py` - Understand caching fundamentals
4. **Evaluate Models**: `simple_model_evaluation.py` - Learn evaluation basics
5. **Advanced Caching**: `prompt_caching_example.py` - Production caching patterns
6. **Advanced Evaluation**: `model_evaluation_example.py` - Comprehensive metrics
7. **Integration**: `integrated_cache_example.py` - Combine concepts

## 🎯 Success Metrics

By the end of this chapter, you should be able to:
- ✅ Implement basic to advanced prompt caching (80%+ cost savings)
- ✅ Evaluate model performance using multiple metrics
- ✅ Compare different models objectively
- ✅ Optimize for both cost and quality
- ✅ Build production-ready LLM applications

## Key Topics Covered
1. **Types of LLMs**: Text, code, multimodal models
2. **Structured Outputs**: JSON extraction and validation
3. **Prompt Caching**: Efficient prompt reuse strategies for cost optimization
4. **Model Evaluation**: Comprehensive evaluation metrics and frameworks
5. **Multi-modal Models**: Working with text and images
6. **AWS Bedrock**: Foundation model platform overview

## 🚀 Quick Start Examples

### Try Prompt Caching (5 minutes)
```bash
# Interactive learning demo - see caching in action!
python simple_prompt_cache.py

# Quick cost comparison test
python simple_prompt_cache.py quick
```

### Try Model Evaluation (10 minutes)
```bash
# Interactive evaluation learning demo
python simple_model_evaluation.py

# Quick consistency test
python simple_model_evaluation.py quick

# Advanced evaluation with multiple metrics
python model_evaluation_example.py --basic
```

### Try Advanced Features
```bash
# File-based persistent caching
python prompt_caching_example.py --demo

# Compare multiple models
python model_evaluation_example.py --comparison

# Integrated caching + cost monitoring
python integrated_cache_example.py --demo
```

## 💡 Key Learning Highlights

### Prompt Caching Benefits
- **80% cost reduction** through effective caching
- **200-500x faster** response times for cache hits
- Multiple implementation patterns (memory, file, Redis)
- Production-ready monitoring and analytics

### Model Evaluation Insights
- Traditional ML metrics (accuracy, precision, recall, F1)
- LLM-specific metrics (BLEU, ROUGE scores)
- Quality assessment without ground truth
- Cost-performance trade-off analysis
- Statistical significance testing

## Next Steps
Proceed to Chapter 3 to learn about Model Adaptation techniques.

## Resources
- [AWS Bedrock User Guide](https://docs.aws.amazon.com/bedrock/)
- [Claude API Documentation](https://docs.anthropic.com/)
- [PROMPT_CACHING_README.md](./PROMPT_CACHING_README.md) - Complete caching guide
- [MODEL_EVALUATION_README.md](./MODEL_EVALUATION_README.md) - Comprehensive evaluation guide
- [JSON_EXTRACTION_GUIDE.md](./JSON_EXTRACTION_GUIDE.md) - Structured output guide

## 🔗 Integration with Course
- **Utils Directory**: Cost monitoring and tracking utilities
- **Chapter 1**: Python fundamentals and ML basics
- **Chapter 3**: **Comprehensive prompt engineering principles and interactive demonstrations**

---

**💡 Pro Tip**: Start with the simple examples to understand concepts, then progress to advanced implementations. The caching and evaluation techniques learned here will be essential for building production AI applications!

# Prompt Engineering - Key Principles Implementation

This directory contains comprehensive examples demonstrating the key principles of prompt engineering as part of Chapter 3: Model Adaptation.

## 📚 Learning Objectives

After working through these examples, you will understand:

1. **Clarity and Specificity**: How to write clear, specific prompts that yield better results
2. **Persona Assignment**: How to assign roles/personas to influence tone and style
3. **Few-Shot Learning**: How to provide examples to improve task performance
4. **Chain of Thought**: How to encourage step-by-step reasoning for complex tasks
5. **Combined Techniques**: How to use multiple principles together for optimal results

## 🗂️ Files Overview

- `prompt_engineering_example.py` - Comprehensive interactive demonstration of all principles
- `PROMPT_ENGINEERING_README.md` - This documentation file

## 🚀 Quick Start

### Prerequisites

1. **AWS Account Setup**:
   ```bash
   # Configure AWS credentials
   aws configure
   ```

2. **Python Environment**:
   ```bash
   # Activate your virtual environment
   .venv\Scripts\activate  # Windows
   # or
   source .venv/bin/activate  # macOS/Linux
   
   # Install dependencies
   pip install boto3
   ```

3. **AWS Bedrock Access**:
   - Ensure you have access to Amazon Nova Lite model
   - Check model availability in your AWS region

### Running the Demo

```bash
# Navigate to the chapter directory
cd chapters/chapter_03_model_adaptation

# Run the comprehensive demonstration
python prompt_engineering_example.py
```

## 🎯 Key Principles Explained

### 1. Clarity and Specificity

**Principle**: Be clear, concise, and specific about the desired output.

**Bad Example**:
```
"Write about running shoes."
```

**Good Example**:
```
"Write a compelling product description for a new pair of running shoes called 'The Velocity.'

Requirements:
- Target audience: Serious runners looking for racing shoes
- Tone: Exciting and persuasive  
- Length: Exactly 150 words
- Include key features: ultra-lightweight (7 ounces), responsive cushioning, breathable mesh, durable rubber outsole
- Focus on performance benefits for competitive runners"
```

**Why it works**: The improved prompt provides context, requirements, constraints, and specific details that guide the model toward the desired output.

### 2. Persona Assignment

**Principle**: Assign a specific role or persona to influence tone and style.

**Examples**:
- Medical Professional: "You are a medical doctor speaking to patients..."
- Fitness Enthusiast: "You are an energetic fitness coach talking to beginners..."
- Scientific Researcher: "You are a research scientist writing for an academic audience..."

**Why it works**: Different personas naturally produce different tones, vocabularies, and approaches to the same topic.

### 3. Few-Shot Learning (Examples)

**Principle**: Provide examples of desired input-output pairs to improve performance.

**Zero-Shot** (no examples):
```
"Convert this customer review into structured sentiment analysis: [review]"
```

**Few-Shot** (with examples):
```
"Convert customer reviews into structured sentiment analysis. Here are examples:

Example 1:
Review: 'Great product, fast delivery, but expensive.'
Analysis: {
    'overall_sentiment': 'positive',
    'sentiment_score': 0.6,
    'aspects': {
        'product_quality': {'sentiment': 'positive', 'score': 0.9},
        'delivery': {'sentiment': 'positive', 'score': 0.8},
        'price': {'sentiment': 'negative', 'score': -0.7}
    }
}

Now analyze: [new review]"
```

**Why it works**: Examples teach the model the exact format, structure, and level of detail you want.

### 4. Chain of Thought Reasoning

**Principle**: Ask the model to think step-by-step for complex reasoning tasks.

**Direct** (no reasoning):
```
"How many weeks will this project take? [project details]"
```

**Chain of Thought**:
```
"How many weeks will this project take? [project details]

Think through this step-by-step:
1. First, calculate the daily coding capacity
2. Then, determine how many days of coding are needed  
3. Convert to weeks
4. Add the buffer time
5. Provide the final answer

Please show your work for each step:"
```

**Why it works**: Breaking down complex problems into steps leads to more accurate and verifiable reasoning.

### 5. Combined Techniques

The most powerful prompts combine multiple principles:

```
"You are an expert technical product manager with 10+ years of experience. [PERSONA]

Your task: Create a comprehensive project risk assessment. [CLARITY]

Here are examples of good risk assessments: [FEW-SHOT]
[Examples...]

Please think through this systematically: [CHAIN OF THOUGHT]
1. Identify technical risks
2. Assess timeline and resource risks
3. Consider external dependencies
4. Evaluate business/market risks  
5. Prioritize by probability and impact"
```

## 📊 Expected Results

When you run the demonstration, you'll see:

1. **Clarity Comparison**: Vague vs. specific prompts showing dramatically different output quality
2. **Persona Variations**: Same task performed by different personas with distinct styles
3. **Few-Shot Improvement**: Zero-shot vs. few-shot examples showing better structure and consistency
4. **Reasoning Enhancement**: Direct answers vs. step-by-step reasoning showing better problem-solving
5. **Combined Power**: All techniques together producing professional-quality outputs

## 🔧 Customization

### Modify the Examples

Edit `prompt_engineering_example.py` to try your own prompts:

```python
# Example: Change the persona
persona_prompt = "You are a [YOUR_PERSONA] speaking to [YOUR_AUDIENCE]. [YOUR_TASK]"

# Example: Add your own few-shot examples
few_shot_examples = """
Example 1: [YOUR_EXAMPLE]
Example 2: [YOUR_EXAMPLE]
"""

# Example: Customize chain of thought steps
cot_steps = """
1. [YOUR_STEP_1]
2. [YOUR_STEP_2]
3. [YOUR_STEP_3]
"""
```

### Adjust Model Parameters

```python
# More creative outputs
response = demo.invoke_model(prompt, temperature=0.8)

# More deterministic outputs  
response = demo.invoke_model(prompt, temperature=0.1)

# Longer responses
response = demo.invoke_model(prompt, max_tokens=1000)
```

## 🎯 Real-World Applications

These principles apply to various AI use cases:

1. **Customer Support**: Use personas (helpful assistant) + few-shot examples of good responses
2. **Content Generation**: Use clarity + chain of thought for structured content creation
3. **Data Analysis**: Use examples + step-by-step reasoning for consistent analysis formats
4. **Code Generation**: Use specific requirements + examples of good code patterns
5. **Creative Writing**: Use personas + specific constraints for targeted creative outputs

## 📈 Best Practices

1. **Start Simple**: Begin with clarity and specificity, then add other techniques
2. **Iterate**: Test different prompts and measure quality improvements
3. **Context Matters**: Choose techniques based on your specific use case
4. **Measure Results**: Track response quality, consistency, and relevance
5. **Document Patterns**: Save successful prompt patterns for reuse

## 🔗 Related Examples

- `bedrock_conversation.py` - Basic AWS Bedrock model interaction
- `nova_lite_chat.py` - Interactive chat with Nova Lite model  
- `nova_lite_cli.py` - Command-line interface for model testing

## 📚 Further Reading

From Course.md:
- Chapter 3: Model Adaptation concepts
- AWS Bedrock documentation
- Prompt engineering best practices
- Few-shot learning techniques
- Chain of thought reasoning research

## 🚨 Troubleshooting

### Common Issues

1. **AWS Credentials Error**:
   ```bash
   aws configure
   # Enter your AWS Access Key ID, Secret Access Key, and region
   ```

2. **Model Access Error**:
   - Check AWS Bedrock console for model availability
   - Ensure your region supports Amazon Nova Lite
   - Verify IAM permissions for Bedrock access

3. **Import Errors**:
   ```bash
   pip install boto3
   ```

4. **Poor Response Quality**:
   - Check your prompt for clarity and specificity
   - Try adjusting temperature (lower = more focused)
   - Add more examples for few-shot learning

### Getting Help

- Check AWS Bedrock documentation
- Review Course.md for additional context
- Experiment with different prompt variations
- Use the interactive demo to understand each principle

## 🎉 Success Metrics

You'll know you've mastered prompt engineering when:

- [ ] You can write clear, specific prompts consistently
- [ ] You understand how persona affects response style
- [ ] You can create effective few-shot examples
- [ ] You can design step-by-step reasoning prompts
- [ ] You can combine techniques for complex tasks
- [ ] Your AI applications produce more consistent, higher-quality outputs

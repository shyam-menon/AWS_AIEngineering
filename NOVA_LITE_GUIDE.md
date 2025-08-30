# Amazon Nova Lite Applications - Complete Guide

## Overview

Amazon Nova Lite is Amazon's fast and cost-effective foundation model available in AWS Bedrock. This guide covers all the applications I've created specifically for Nova Lite, since that's the model you have access to.

## 📁 Nova Lite Applications

### 1. **`nova_lite_chat.py`** - Interactive Chat Application
**Best for**: Quick conversations, testing, and interactive exploration

**Features**:
- Interactive chat mode with command system
- System prompt customization
- Temperature and token controls
- Streaming and non-streaming modes
- Demo examples for different use cases

**Usage**:
```powershell
# Interactive chat
python nova_lite_chat.py

# Choose: 1 (Interactive) or 2 (Demo Examples)
```

**Interactive Commands**:
- `help` - Show available commands
- `settings` - View current configuration
- `system` - Set system prompt
- `temp 0.8` - Set temperature (creativity level)
- `tokens 1500` - Set maximum tokens
- `stream` - Toggle streaming mode
- `clear` - Clear system prompt
- `quit` - Exit

### 2. **`nova_lite_cli.py`** - Command Line Interface
**Best for**: One-off tasks, scripting, automation

**Features**:
- Rich command-line interface
- Built-in presets for different use cases
- Flexible parameter control
- Interactive and single-shot modes
- Verbose output options

**Usage Examples**:
```powershell
# Basic usage
python nova_lite_cli.py "Write a poem about coding"

# Use a preset (creative, technical, code, analysis, casual, business)
python nova_lite_cli.py "Explain quantum computing" --preset technical

# Custom parameters
python nova_lite_cli.py "Write a story" --system "You are Shakespeare" --temperature 0.9 --tokens 1500

# Streaming with verbose info
python nova_lite_cli.py "Explain AI" --stream --verbose

# Interactive mode
python nova_lite_cli.py --interactive

# List available presets
python nova_lite_cli.py --list-presets
```

**Available Presets**:
- **creative**: Creative writing and storytelling (temp: 0.8)
- **technical**: Technical explanations and documentation (temp: 0.3)
- **code**: Programming and code generation (temp: 0.2)
- **analysis**: Research and analytical tasks (temp: 0.4)
- **casual**: Friendly conversation and general help (temp: 0.6)
- **business**: Professional business content (temp: 0.5)

### 3. **`nova_lite_apps.py`** - Specialized Applications
**Best for**: Specific professional tasks and workflows

**Features**:
- Multiple specialized applications in one tool
- Task-specific optimizations
- Professional-grade outputs
- Structured workflows

**Applications Available**:

#### 📝 Content Creator
```powershell
# Blog post
python nova_lite_apps.py content blog "Machine Learning in Healthcare" --style professional --length long

# Social media content
python nova_lite_apps.py content social "New product launch" --style casual --length short

# Creative story
python nova_lite_apps.py content story "Time travel adventure" --style creative --length medium
```

**Content Types**: blog, article, email, social, story, poem, script
**Styles**: professional, casual, creative, technical, humorous
**Lengths**: short (300 tokens), medium (800 tokens), long (1500 tokens)

#### 💻 Code Assistant
```powershell
# Python function with tests
python nova_lite_apps.py code "Create a binary search algorithm" --language python --tests

# JavaScript help
python nova_lite_apps.py code "Build a REST API endpoint" --language javascript

# Any programming language
python nova_lite_apps.py code "Implement merge sort" --language java
```

#### 🔍 Research Analyst
```powershell
# Comprehensive analysis
python nova_lite_apps.py research "Climate change impact on agriculture" --type comprehensive

# Quick summary
python nova_lite_apps.py research "Blockchain technology" --type summary

# Pros and cons analysis
python nova_lite_apps.py research "Remote work policies" --type pros_cons --focus "productivity" "employee satisfaction"
```

**Analysis Types**: comprehensive, summary, comparison, pros_cons

#### 💼 Business Consultant
```powershell
# Business advice
python nova_lite_apps.py business "Expanding to international markets" --type advice --industry "e-commerce"

# Strategic planning
python nova_lite_apps.py business "Digital transformation initiative" --type strategy --industry "manufacturing"

# Business plan
python nova_lite_apps.py business "Launching a mobile app" --type plan --industry "fintech"
```

**Consultation Types**: advice, strategy, plan, analysis

#### ✍️ Creative Writer
```powershell
# Science fiction story
python nova_lite_apps.py creative story "AI becomes sentient" --genre scifi --length long

# Mystery poem
python nova_lite_apps.py creative poem "The missing key" --genre mystery --length medium

# Romantic dialogue
python nova_lite_apps.py creative dialogue "First date conversation" --genre romance --length short
```

**Writing Types**: story, poem, script, dialogue, description
**Genres**: fiction, mystery, romance, scifi, fantasy, horror, drama

### 4. **`test_nova_lite.py`** - Original Test Script
**Best for**: Understanding the basic Nova Lite API structure

This is the original Amazon example code that demonstrates:
- Streaming responses
- Performance metrics (time to first token)
- Basic request structure
- Creative writing example

## 🚀 Getting Started

### 1. Quick Test
```powershell
# Test the original example
python test_nova_lite.py

# Simple chat test
python nova_lite_cli.py "Hello, introduce yourself" --verbose
```

### 2. Interactive Exploration
```powershell
# Start interactive chat
python nova_lite_chat.py
# Choose option 1 for chat, 2 for demos
```

### 3. Professional Use
```powershell
# Content creation
python nova_lite_apps.py content blog "Your Topic Here" --style professional

# Code assistance
python nova_lite_apps.py code "Your programming question" --language python --tests

# Business consultation
python nova_lite_apps.py business "Your business challenge" --type advice
```

## ⚙️ Configuration Options

### Common Parameters

| Parameter | Description | Values | Default |
|-----------|-------------|--------|---------|
| `--temperature` | Creativity level | 0.0-1.0 | 0.7 |
| `--tokens` | Max response length | 1-4000 | 1000 |
| `--stream` | Stream response | true/false | true |
| `--verbose` | Show details | true/false | false |
| `--region` | AWS region | us-east-1, etc. | us-east-1 |

### Temperature Guide
- **0.0-0.3**: Factual, deterministic (good for code, technical content)
- **0.4-0.6**: Balanced creativity and accuracy (good for business, analysis)
- **0.7-0.9**: Creative and varied (good for writing, brainstorming)
- **0.9-1.0**: Highly creative, unpredictable (good for artistic content)

## 🎯 Use Case Examples

### Daily Tasks

**Email Writing**:
```powershell
python nova_lite_apps.py content email "Project status update" --style professional --length medium
```

**Code Review**:
```powershell
python nova_lite_apps.py code "Review this Python function for efficiency and best practices: [paste code]"
```

**Meeting Summary**:
```powershell
python nova_lite_apps.py business "Create action items from meeting notes" --type analysis
```

### Creative Projects

**Story Writing**:
```powershell
python nova_lite_apps.py creative story "A detective in a cyberpunk city" --genre mystery --length long
```

**Marketing Content**:
```powershell
python nova_lite_apps.py content social "Launch announcement for new AI tool" --style creative --length short
```

### Learning and Research

**Technical Learning**:
```powershell
python nova_lite_cli.py "Explain machine learning algorithms" --preset technical --tokens 1500
```

**Comparative Analysis**:
```powershell
python nova_lite_apps.py research "Python vs JavaScript for web development" --type comparison
```

## 🔧 Advanced Features

### System Prompts
Control Nova Lite's behavior with system prompts:

```powershell
# Act as a specific expert
python nova_lite_cli.py "Explain database optimization" --system "You are a senior database administrator with 15 years of experience"

# Set writing style
python nova_lite_cli.py "Write about AI ethics" --system "Write in the style of a philosophy professor, using clear examples"

# Control output format
python nova_lite_cli.py "List project risks" --system "Respond only with numbered bullet points, be concise"
```

### Streaming vs Non-Streaming

**Streaming** (default):
- See responses as they're generated
- Better for interactive use
- Shows "thinking" process

**Non-streaming**:
- Get complete response at once
- Better for automation/scripting
- Cleaner for file output

```powershell
# Force non-streaming
python nova_lite_cli.py "Write a summary" --no-stream
```

### Chaining Commands

You can chain multiple Nova Lite calls for complex workflows:

```powershell
# 1. Generate ideas
python nova_lite_apps.py research "Blog post topics about AI" --type summary > ideas.txt

# 2. Write the blog post
python nova_lite_apps.py content blog "Choose one topic from ideas.txt" --style professional --length long
```

## 📊 Performance and Costs

### Nova Lite Characteristics
- **Speed**: Very fast response times (1-3 seconds typically)
- **Cost**: Most cost-effective option in Bedrock
- **Quality**: Good for most general tasks
- **Context**: Handles reasonable context lengths

### Optimization Tips
1. **Use appropriate token limits**: Don't request more than you need
2. **Optimize prompts**: Clear, specific prompts get better results faster
3. **Use presets**: Pre-configured settings are optimized for specific tasks
4. **Streaming for UX**: Use streaming for better user experience

## 🛠️ Troubleshooting

### Common Issues

**1. "Access Denied" Errors**
```powershell
# Check if Nova Lite is enabled
python nova_lite_cli.py "test" --verbose
```
- Go to AWS Bedrock Console → Model Access
- Ensure Nova Lite is enabled

**2. "Invalid Parameters" Errors**
- Check temperature is between 0.0-1.0
- Check max tokens is reasonable (1-4000)
- Verify region supports Nova Lite

**3. Slow Responses**
- Try reducing max_tokens
- Check your internet connection
- Verify AWS region is geographically close

**4. Poor Quality Responses**
- Improve your prompts (be more specific)
- Use appropriate presets
- Adjust temperature for your use case
- Add system prompts for better context

### Getting Help

1. **Test basic functionality**:
```powershell
python nova_lite_cli.py "Hello" --verbose
```

2. **Check available options**:
```powershell
python nova_lite_cli.py --help
python nova_lite_apps.py --help
```

3. **Try different approaches**:
- Start with simple prompts
- Use presets before custom configurations
- Test with different temperature settings

## 🚀 Next Steps

1. **Start Simple**: Begin with `nova_lite_cli.py` for basic tasks
2. **Explore Presets**: Try different presets to understand capabilities
3. **Use Specialized Apps**: Move to `nova_lite_apps.py` for professional workflows
4. **Customize**: Create your own scripts using the examples as templates
5. **Integrate**: Use in your existing workflows and automation

## 💡 Pro Tips

1. **Be Specific**: "Write a 500-word technical blog post about Docker containers for beginners" is better than "Tell me about Docker"

2. **Use Examples**: Include examples in your prompts when possible

3. **Iterate**: Start with a basic prompt, then refine based on the output

4. **Save Good Prompts**: Keep a collection of prompts that work well for your use cases

5. **Combine Tools**: Use research app to gather info, then content app to write about it

6. **Test Different Settings**: Same prompt with different temperatures can yield very different results

---

**Nova Lite is now ready for your projects! 🎉**

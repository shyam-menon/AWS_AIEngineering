# Chapter 3: Model Adaptation

This chapter focuses on adapting and customizing LLMs for specific needs through prompt engineering, tool use, fine-tuning techniques, and leveraging graph databases.

## Learning Objectives
- Master prompt engineering techniques
- Implement tool use patterns with LLMs
- Understand fine-tuning approaches
- Learn graph database integration for enhanced context

## Code Examples

### Prompt Engineering
- `prompt_engineering_example.py` - **Comprehensive demonstration of key prompt engineering principles**
- `PROMPT_ENGINEERING_README.md` - Detailed guide and documentation

### Tool Use with Strands Agents
- `strands_tool_use_example.py` - **Complete tool use demonstration with multiple tool types**
- `STRANDS_TOOL_USE_README.md` - Comprehensive tool development guide

### Advanced Conversation Patterns
- `bedrock_conversation.py` - Advanced conversation patterns and context management
- `nova_lite_chat.py` - Interactive chat with Amazon Nova Lite
- `nova_lite_cli.py` - Command-line interface with conversation presets

## Prerequisites
- Completed Chapters 1-2
- Understanding of LLM basics
- AWS Bedrock access

## Key Topics Covered
1. **Prompt Engineering**: 
   - **Clarity and Specificity**: Clear, specific prompts for better results
   - **Persona Assignment**: Role-based responses with appropriate tone
   - **Few-shot Learning**: Using examples to improve task performance
   - **Chain-of-Thought Reasoning**: Step-by-step thinking for complex tasks
   - **Combined Techniques**: Integrating multiple principles for optimal results

2. **Tool Use with Strands Agents**:
   - **Tool Definition**: Creating custom tools with @tool decorator
   - **Agent Integration**: Registering tools with Strands agents
   - **Automatic Tool Selection**: How agents decide which tools to use
   - **Multi-Tool Workflows**: Chaining tools for complex tasks
   - **AWS Integration**: Tools for S3, CloudWatch, and Bedrock services
   - **Error Handling**: Robust tool design and failure recovery
   - **Real-World Applications**: Practical tool patterns for production use

3. **Fine-tuning**:
   - When to fine-tune vs. prompt engineering
   - Data preparation for fine-tuning
   - Evaluation metrics

4. **Graph Databases**:
   - Knowledge graph integration
   - Contextual information retrieval
   - Relationship modeling

## Quick Start - Prompt Engineering

Run the comprehensive prompt engineering demonstration:

```bash
cd chapters/chapter_03_model_adaptation
python prompt_engineering_example.py
```

This will show you:
- ✅ Before/after comparisons for each principle
- 🎭 Different persona responses to the same task
- 📚 Zero-shot vs. few-shot learning examples
- 🔗 Direct vs. chain-of-thought reasoning
- 🚀 All techniques combined for professional results

## Quick Start - Tool Use with Strands Agents

Run the comprehensive tool use demonstration:

```bash
cd chapters/chapter_03_model_adaptation
python strands_tool_use_example.py
```

This will demonstrate:
- 🔧 Multiple tool types (utility, AWS, external API, data processing)
- 🤖 How agents automatically select and use tools
- 🔗 Multi-tool workflows for complex tasks
- ⚠️ Error handling and graceful failure recovery
- 📊 Tool inspection and capabilities overview

**Note**: Works with or without Strands installed - shows educational content regardless

## Practical Exercises
- Build conversational agents with memory
- **Create custom tools for your specific use cases**
- **Build multi-tool workflows for complex automation**
- Create custom prompt templates
- Design conversation flow patterns
- **Practice prompt engineering principles with your own use cases**

## Next Steps
Proceed to Chapter 4 to learn about Storage for Retrieval systems.

## Resources
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [AWS Bedrock Model Customization](https://docs.aws.amazon.com/bedrock/latest/userguide/custom-models.html)

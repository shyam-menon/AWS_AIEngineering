# Simple Tool-Augmented Agent with Strands

This example demonstrates how to create a simple yet powerful tool-augmented agent using the Strands framework. The agent combines the conversational abilities of Large Language Models (LLMs) with practical tools to perform real-world tasks.

## 🎯 Learning Objectives

- Understand how to integrate built-in Strands tools with agents
- Learn to create custom tools using the `@tool` decorator
- See how agents intelligently select and use tools based on user queries
- Experience the power of multi-tool workflows
- Learn best practices for encouraging tool usage

## 📁 Files in This Example

- **`simple_tool_agent.py`** - Basic tool-augmented agent example
- **`simple_tool_agent_improved.py`** - Enhanced version with better tool usage patterns
- **`test_strands.py`** - Installation and configuration test script
- **`requirements.txt`** - Dependencies for this chapter

## 🔧 Available Tools

### Built-in Strands Tools
- **`calculator`**: Perform mathematical calculations and operations
- **`current_time`**: Get current date and time information
- **`file_read`**: Read and analyze file contents
- ~~**`shell`**: Execute shell commands~~ (Not compatible with Windows)

### Custom Tools
- **`character_counter`**: Analyze character types in text (letters, digits, spaces, punctuation)
- **`text_processor`**: Process text in various ways (uppercase, lowercase, reverse, title case)

## 🚀 Features

### 1. Model Configuration
The examples are configured to use **Amazon Nova Lite** (`us.amazon.nova-lite-v1:0`), which is available in your AWS account:
```python
agent = Agent(
    model="us.amazon.nova-lite-v1:0",  # Nova Lite model
    tools=[calculator, current_time, ...]
)
```

### 2. Intelligent Tool Selection
The agent automatically determines which tool(s) to use based on the user's query:
```python
# Mathematical query → Uses calculator tool
"What is the square root of 144 plus 25% of 200?"

# Time query → Uses current_time tool
"What time is it right now?"

# Text analysis → Uses character_counter tool
"Analyze the characters in 'Hello, World! 123'"
```

### 3. Multi-Tool Workflows
The agent can use multiple tools in sequence to complete complex tasks:
```python
query = """I need you to:
1. Calculate 15 * 8 + 32
2. Get the current time
3. Analyze the character count in 'AI Engineering 2025!'
4. Convert 'strands agents' to title case
Please do all of these tasks."""
```

### 4. Custom Tool Development
Learn how to create custom tools using the `@tool` decorator:
```python
@tool
def character_counter(text: str) -> str:
    """Count various types of characters in a given text."""
    # Implementation here
    return result
```

### 5. Enhanced Tool Usage
The improved version (`simple_tool_agent_improved.py`) demonstrates better practices for encouraging tool usage:
```python
system_prompt = """You are a helpful assistant with access to powerful tools. 
IMPORTANT: Always use the appropriate tools when available instead of doing tasks manually.

Available tools:
- calculator: Use for ALL mathematical calculations
- current_time: Use to get the current date and time
- character_counter: Use to analyze character counts in text
- text_processor: Use to transform text (uppercase, lowercase, reverse, title case)

When a user asks for text analysis, character counting, or text processing, 
ALWAYS use the appropriate tool rather than doing it manually."""
```

## 📋 Prerequisites

1. **Strands Installation**: Ensure Strands is installed in your environment
   ```bash
   pip install strands-agents strands-agents-tools
   ```

2. **AWS Configuration**: Configure AWS credentials for Bedrock access
   ```bash
   aws configure
   ```

3. **Model Access**: Ensure you have access to Amazon Nova Lite model in AWS Bedrock
   ```bash
   # Check model access in AWS console or via CLI
   aws bedrock list-foundation-models
   ```

4. **Python Environment**: Python 3.8+ with required dependencies

## 🏃‍♂️ Running the Examples

### Test Installation First
```bash
python test_strands.py
```

### Option 1: Basic Example
Run the basic tool-augmented agent:
```bash
python simple_tool_agent.py
```

### Option 2: Improved Example (Recommended)
Run the enhanced version with better tool usage:
```bash
python simple_tool_agent_improved.py
```

Both scripts will show:
- Mathematical calculations using the calculator tool
- Time queries using the current_time tool
- Text analysis using the character_counter tool
- Text processing using the text_processor tool
- Complex multi-tool workflows

### Option 3: Interactive Mode
After the demonstrations, choose interactive mode to chat with the agent:
```
🎮 Would you like to try interactive mode? (y/n): y
```

Try queries like:
- `"Use calculator for 25 * 16 / 4"`
- `"Get current time"`
- `"Use character_counter to analyze 'Hello World'"`
- `"Use text_processor to convert my name to uppercase"`

## 🔍 Code Structure

### Key Differences Between Basic and Improved Versions

**Basic Version (`simple_tool_agent.py`)**:
- Simple system prompt
- Tools may not be used consistently
- Good for understanding basic concepts

**Improved Version (`simple_tool_agent_improved.py`)**:
- Enhanced system prompt that explicitly encourages tool usage
- More focused demonstrations
- Better tool selection patterns
- Recommended for learning best practices

### Main Components

1. **Custom Tools**: `character_counter()` and `text_processor()`
   - Demonstrate how to create tools with the `@tool` decorator
   - Handle different input types and validation
   - Return structured, user-friendly responses

2. **SimpleToolAgent Class**: Main agent wrapper
   - Initializes agent with multiple tools
   - Provides demonstration and interactive modes
   - Handles errors gracefully

3. **Agent Configuration**:
   ```python
   self.agent = Agent(
       tools=[
           calculator,           # Built-in: Math
           current_time,         # Built-in: Time
           file_read,           # Built-in: File operations
           shell,               # Built-in: Shell commands
           character_counter,   # Custom: Text analysis
           text_processor       # Custom: Text processing
       ],
       system_prompt="""You are a helpful assistant with access to various tools..."""
   )
   ```

## 💡 Key Concepts Demonstrated

### 1. Tool Registration
```python
# Built-in tools from strands_tools
from strands_tools import calculator, current_time, file_read, shell

# Custom tools with @tool decorator
@tool
def my_custom_tool(param: str) -> str:
    """Tool description for the LLM."""
    return result
```

### 2. Automatic Tool Selection
The agent uses natural language understanding to select appropriate tools:
- Mathematical expressions → `calculator`
- Time-related queries → `current_time`
- Text analysis requests → `character_counter`
- Text transformation requests → `text_processor`

### 3. Error Handling
```python
try:
    response = self.agent(user_query)
    print(response)
except Exception as e:
    logger.error(f"Error: {e}")
    print(f"❌ Error: {e}")
```

### 4. Tool Information Access
```python
# Get available tools
print(f"Available tools: {agent.tool_names}")

# Get tool configuration
print(f"Tool config: {agent.tool_config}")
```

## 🎓 Educational Value

This example teaches:

1. **Tool Integration**: How to combine built-in and custom tools
2. **Agent Design**: Best practices for tool-augmented agents
3. **Custom Tool Development**: Creating tools with proper documentation
4. **Error Handling**: Robust error management in agent workflows
5. **User Experience**: Creating interactive and demonstration modes

## 🔧 Extending the Example

### Add More Tools
```python
@tool
def weather_tool(city: str) -> str:
    """Get weather information for a city."""
    # Implementation here
    return weather_data

# Add to agent
agent = Agent(tools=[calculator, current_time, weather_tool])
```

### Enhanced Error Handling
```python
@tool
def robust_tool(input_data: str) -> str:
    """A tool with comprehensive error handling."""
    try:
        # Validate input
        if not input_data:
            return "Error: Input cannot be empty"
        
        # Process
        result = process_data(input_data)
        return f"Success: {result}"
        
    except ValueError as e:
        return f"Validation Error: {e}"
    except Exception as e:
        return f"Unexpected Error: {e}"
```

### Tool Composition
```python
@tool
def composite_tool(text: str) -> str:
    """A tool that uses other tools internally."""
    # Analyze text
    char_analysis = character_counter(text)
    
    # Process text
    processed = text_processor(text, "uppercase")
    
    return f"Analysis: {char_analysis}\nProcessed: {processed}"
```

## 🚨 Important Notes

1. **Shell Tool Security**: The `shell` tool can execute system commands. Use with caution in production.

2. **Tool Documentation**: Always provide clear docstrings for custom tools. The LLM uses these to understand when and how to use tools.

3. **Error Handling**: Implement proper error handling in custom tools to provide meaningful feedback.

4. **Type Hints**: Use type hints in tool functions for better code clarity and validation.

## 🔗 Next Steps

After understanding this example, explore:

1. **Advanced Tool Patterns**: Multi-step workflows, tool chaining
2. **MCP Integration**: Using Model Context Protocol for external tools
3. **Agent Memory**: Persistent memory across conversations
4. **Multi-Agent Systems**: Coordinating multiple specialized agents
5. **Production Deployment**: Scaling tool-augmented agents in production

## 📚 Additional Resources

- [Strands Tools Documentation](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/tools/)
- [Custom Tool Development Guide](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/tools/python-tools/)
- [Agent Design Patterns](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/agents/)

# Tool Use with Strands Agents - Comprehensive Example

This directory contains a comprehensive demonstration of tool use with Strands Agents, showcasing how to extend AI capabilities with external tools and services.

## 📚 Learning Objectives

After working through this example, you will understand:

1. **Tool Definition**: How to create custom tools using the `@tool` decorator
2. **Agent Integration**: How to register tools with Strands agents
3. **Automatic Tool Selection**: How agents decide when and which tools to use
4. **Multi-Tool Workflows**: How agents chain multiple tools to solve complex tasks
5. **Error Handling**: How to build robust tools that handle failures gracefully
6. **AWS Integration**: How to create tools that interact with AWS services
7. **Real-World Applications**: Practical examples of tool use in AI applications

## 🗂️ Files Overview

- `strands_tool_use_example.py` - Comprehensive tool use demonstration
- `STRANDS_TOOL_USE_README.md` - This documentation file

## 🚀 Quick Start

### Prerequisites

1. **Strands Agents Installation**:
   ```bash
   pip install strands-agents strands-agents-tools
   ```

2. **AWS Account Setup**:
   ```bash
   # Configure AWS credentials
   aws configure
   ```

3. **Python Environment**:
   ```bash
   # Activate your virtual environment
   .venv\Scripts\activate  # Windows
   # or
   source .venv/bin/activate  # macOS/Linux
   ```

4. **AWS Bedrock Access**:
   - Ensure you have access to Amazon Nova Lite model
   - Check model availability in your AWS region

### Running the Demo

```bash
# Navigate to the chapter directory
cd chapters/chapter_03_model_adaptation

# Run the comprehensive demonstration
python strands_tool_use_example.py
```

## 🔧 Tool Categories Demonstrated

### 1. Utility Tools

**Purpose**: Common utility functions that agents often need

**Examples**:
- `get_current_time()` - Get current timestamp with timezone support
- `calculate_business_days()` - Calculate working days between dates

**Usage Pattern**:
```python
@tool
def get_current_time(timezone: str = "UTC") -> str:
    """Get the current time in a specified timezone."""
    # Implementation here
    return formatted_time
```

### 2. AWS Integration Tools

**Purpose**: Connect agents to AWS services for cloud operations

**Examples**:
- `check_s3_bucket_size()` - Get S3 bucket metrics via CloudWatch
- `estimate_bedrock_cost()` - Calculate model usage costs

**Key Features**:
- Real AWS service integration
- Error handling for service failures
- Structured response formats

### 3. External API Tools

**Purpose**: Connect to third-party services and APIs

**Examples**:
- `get_weather_info()` - Weather data retrieval
- `search_web_content()` - Web search capabilities

**Best Practices**:
- API key management
- Rate limiting considerations
- Fallback mechanisms

### 4. Data Processing Tools

**Purpose**: Analyze and process various types of data

**Examples**:
- `analyze_text_metrics()` - Text analysis and statistics

**Capabilities**:
- Text analysis and metrics
- Data transformation
- Statistical calculations

## 💡 How Tool Use Works

### Agent Decision Process

1. **Query Analysis**: Agent receives user request
2. **Tool Assessment**: Agent evaluates available tools
3. **Tool Selection**: Agent chooses appropriate tool(s)
4. **Execution**: Agent calls selected tools with parameters
5. **Response Integration**: Agent incorporates tool results into response

### Example Flow

```
User: "How many business days between Aug 1 and Aug 15, 2024?"

Agent Thinking:
1. Analyze query: Need to calculate business days between dates
2. Available tools: calculate_business_days() matches this need
3. Extract parameters: start_date="2024-08-01", end_date="2024-08-15"
4. Execute tool: calculate_business_days("2024-08-01", "2024-08-15")
5. Return result: Integrated into natural language response
```

## 🎯 Demonstration Scenarios

### 1. Single Tool Use

**Scenario**: Agent uses one tool to answer a specific question

**Examples**:
- Time queries → `get_current_time()`
- Date calculations → `calculate_business_days()`
- Weather requests → `get_weather_info()`
- Cost estimates → `estimate_bedrock_cost()`

### 2. Multi-Tool Workflows

**Scenario**: Agent chains multiple tools to solve complex tasks

**Example Query**:
```
"I need to plan a project. What time is it now, how many business days 
are between Sep 1 and Oct 15, and what would it cost to process this 
analysis using Nova Lite?"
```

**Agent Response**:
1. Calls `get_current_time()` for current timestamp
2. Calls `calculate_business_days()` for date calculation
3. Calls `estimate_bedrock_cost()` for pricing estimate
4. Synthesizes all results into comprehensive response

### 3. Error Handling

**Scenario**: Tools encounter errors and handle them gracefully

**Examples**:
- Invalid date formats
- Non-existent S3 buckets
- Unsupported model IDs
- Network connectivity issues

## 🔧 Creating Custom Tools

### Basic Tool Structure

```python
from strands.tools import tool

@tool
def your_tool_name(parameter: str, optional_param: int = 10) -> dict:
    """
    Clear description of what this tool does.
    
    Args:
        parameter: Description of required parameter
        optional_param: Description of optional parameter
        
    Returns:
        Description of return value
    """
    try:
        # Your tool implementation
        result = perform_task(parameter, optional_param)
        
        return {
            "success": True,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
```

### Best Practices for Tool Development

1. **Clear Documentation**:
   - Write descriptive docstrings
   - Document all parameters and return values
   - Include usage examples

2. **Type Hints**:
   - Use proper type annotations
   - Help the agent understand parameter types
   - Enable better error messages

3. **Error Handling**:
   - Wrap operations in try-catch blocks
   - Return structured error messages
   - Don't let tools crash the agent

4. **Structured Returns**:
   - Return dictionaries with consistent structure
   - Include status indicators
   - Provide timestamps and metadata

5. **Parameter Validation**:
   - Validate input parameters
   - Provide helpful error messages
   - Handle edge cases gracefully

## 🌟 Real-World Applications

### Business Automation

```python
@tool
def generate_report(start_date: str, end_date: str) -> dict:
    """Generate automated business reports."""
    # Combine multiple data sources
    # Calculate metrics
    # Format results
    pass

@tool 
def send_notification(recipient: str, message: str) -> dict:
    """Send notifications via various channels."""
    # Email, Slack, SMS integration
    pass
```

### DevOps Integration

```python
@tool
def check_service_health(service_name: str) -> dict:
    """Check the health of deployed services."""
    # CloudWatch metrics
    # Container status
    # Performance indicators
    pass

@tool
def deploy_application(version: str, environment: str) -> dict:
    """Deploy applications to specified environments."""
    # Infrastructure as code
    # Deployment automation
    pass
```

### Data Analysis

```python
@tool
def analyze_user_behavior(user_id: str, period: str) -> dict:
    """Analyze user behavior patterns."""
    # Database queries
    # Statistical analysis
    # Pattern recognition
    pass

@tool
def generate_insights(dataset: str) -> dict:
    """Generate insights from datasets."""
    # Machine learning analysis
    # Trend identification
    # Predictive modeling
    pass
```

## 📊 Expected Results

When you run the demonstration, you'll see:

### 1. Tool Inspection
- Complete list of available tools
- Parameter descriptions and types
- Tool capabilities overview

### 2. Single Tool Demonstrations
- Individual tool usage examples
- Clear input/output examples
- Success and error scenarios

### 3. Multi-Tool Workflows
- Complex query handling
- Tool chaining examples
- Integrated responses

### 4. Error Handling
- Graceful failure recovery
- Informative error messages
- Agent resilience demonstration

## 🔧 Customization Guide

### Adding New Tools

1. **Define Your Tool**:
   ```python
   @tool
   def my_custom_tool(param: str) -> dict:
       """My custom tool description."""
       # Implementation
       return result
   ```

2. **Add to Tools List**:
   ```python
   self.tools.append(my_custom_tool)
   ```

3. **Test Independently**:
   ```python
   # Test tool before agent integration
   result = my_custom_tool("test_input")
   print(result)
   ```

### Modifying Existing Tools

1. **Update Function Logic**:
   - Modify the tool implementation
   - Maintain the same interface
   - Update documentation

2. **Test Changes**:
   - Run individual tool tests
   - Verify agent integration
   - Check error handling

### Integration Examples

```python
# Database integration
@tool
def query_database(sql: str) -> dict:
    """Execute database queries safely."""
    # SQL execution with safety checks
    pass

# API integration  
@tool
def call_external_api(endpoint: str, params: dict) -> dict:
    """Call external APIs with authentication."""
    # HTTP requests with error handling
    pass

# File processing
@tool
def process_document(file_path: str) -> dict:
    """Process and analyze documents."""
    # Document parsing and analysis
    pass
```

## 🚨 Troubleshooting

### Common Issues

1. **Import Errors**:
   ```bash
   pip install strands-agents strands-agents-tools
   ```

2. **AWS Permissions**:
   ```bash
   aws configure
   # Ensure proper IAM permissions for services used
   ```

3. **Tool Not Found**:
   - Check tool registration with agent
   - Verify @tool decorator is applied
   - Ensure tool is in the tools list

4. **Parameter Errors**:
   - Check parameter types and names
   - Verify required vs optional parameters
   - Review tool documentation

### Debugging Tips

1. **Test Tools Individually**:
   ```python
   # Test before agent integration
   result = your_tool("test_input")
   print(f"Tool result: {result}")
   ```

2. **Enable Verbose Logging**:
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

3. **Check Agent Response**:
   ```python
   try:
       response = agent("Your query")
       print(f"Agent response: {response}")
   except Exception as e:
       print(f"Error: {e}")
   ```

## 📈 Performance Considerations

### Tool Efficiency

1. **Minimize External Calls**:
   - Cache results when appropriate
   - Batch operations when possible
   - Use connection pooling

2. **Error Recovery**:
   - Implement retry logic
   - Provide fallback mechanisms
   - Timeout handling

3. **Resource Management**:
   - Close connections properly
   - Manage memory usage
   - Handle large datasets efficiently

## 🔗 Integration with Other Chapters

- **Chapter 1**: Basic Strands setup and simple tools
- **Chapter 2**: LLM APIs and model integration
- **Chapter 4**: Vector database tools for RAG
- **Chapter 5**: Retrieval and generation tools
- **Chapter 6**: Multi-agent tool sharing

## 📚 Further Reading

- Strands Agents Documentation
- AWS SDK for Python (Boto3)
- Tool Design Patterns
- Agent Architecture Best Practices
- Production Deployment Considerations

## 🎉 Success Metrics

You'll know you've mastered tool use when:

- [ ] You can create custom tools for your specific needs
- [ ] You understand how agents decide which tools to use
- [ ] You can build multi-tool workflows for complex tasks
- [ ] You can handle errors gracefully in your tools
- [ ] You can integrate with external APIs and services
- [ ] Your AI applications can interact with the real world effectively

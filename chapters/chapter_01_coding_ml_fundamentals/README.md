# Chapter 1: Coding & ML Fundamentals

This chapter covers the foundational skills needed for AI engineering, including Python programming, Bash scripting, statistics, and an overview of machine learning model types.

## Learning Objectives
- Master essential Python concepts for AI development
- Understand Bash for infrastructure management
- Review key statistical concepts for ML
- Learn about different types of ML models

## Code Examples

### Python Fundamentals
- `python_data_types.py` - Data types and structures (int, float, str, bool, list, dict, tuple, set)
- `python_control_flow.py` - Conditional statements (if/elif/else) and loops (for/while)
- `python_functions.py` - Function definition, parameters, return values, scope
- `python_oop.py` - Classes, objects, inheritance, polymorphism, encapsulation
- `python_file_io.py` - Reading/writing files, JSON, CSV, error handling
- `python_strands_agents.py` - Strands Agents framework for building AI agents
- `run_chapter_demo.py` - Interactive demonstration of all concepts

### AWS & Infrastructure Basics
- `requirements.txt` - Essential Python packages for AI development
- `aws_config_examples.txt` - AWS credential configuration examples
- `ec2_list.py` - List and manage EC2 instances using Boto3

## Python Core Concepts Covered

### 1. Data Types and Structures
- **Basic Types**: integers, floats, strings, booleans, None
- **Collections**: lists (ordered, mutable), tuples (ordered, immutable)
- **Mappings**: dictionaries (key-value pairs, mutable)
- **Sets**: unordered collections of unique elements
- **Type conversion** between different data types

### 2. Control Flow
- **Conditional statements**: if, elif, else with comparison operators
- **Loops**: for loops with range, lists, dictionaries; while loops
- **Loop control**: break, continue, else clauses
- **List comprehensions**: concise iteration patterns

### 3. Functions
- **Basic functions**: definition, parameters, return values
- **Advanced parameters**: default values, *args, **kwargs
- **Variable scope**: local, global, nonlocal
- **Lambda functions**: anonymous functions for simple operations

### 4. Object-Oriented Programming
- **Classes and objects**: blueprint and instance concepts
- **Encapsulation**: private/protected attributes and methods
- **Inheritance**: code reuse and specialization
- **Polymorphism**: same interface, different implementations
- **Class methods and static methods**

### 5. File I/O
- **Basic operations**: reading, writing, appending files
- **File modes**: text vs binary, different access modes
- **Structured data**: JSON and CSV handling
- **Error handling**: FileNotFoundError, PermissionError
- **Modern path handling**: pathlib for better file management

### 6. Strands Agents Framework
- **Agent creation**: Using the Strands open-source framework
- **Agent interactions**: Basic communication patterns
- **Tool integration**: Connecting agents with AWS services
- **Multi-agent systems**: Collaborative agent workflows
- **AI engineering applications**: Automation and workflow management

## Running the Examples

### Individual Examples
```bash
# Run specific Python fundamentals examples
python python_data_types.py
python python_control_flow.py
python python_functions.py
python python_oop.py
python python_file_io.py
python python_strands_agents.py
```

### Strands Agents Examples
```bash
# Run Strands Agents framework examples
python python_strands_agents.py

# Run simple working Strands example (requires AWS Bedrock access)
python simple_strands_example.py
```

### AWS Infrastructure
```bash
# List EC2 instances (requires AWS credentials)
python ec2_list.py
```

## Prerequisites
- Basic programming knowledge
- AWS account setup
- Python 3.10+ installed
- Strands Agents library: `pip install strands-agents strands-agents-tools`

### AWS Bedrock Setup (for Strands Agents)
To use Strands Agents with AWS Bedrock (default model provider):

1. **Configure AWS Credentials**:
   ```bash
   # Option 1: Environment variables
   export AWS_ACCESS_KEY_ID=your_access_key
   export AWS_SECRET_ACCESS_KEY=your_secret_key
   
   # Option 2: AWS CLI
   aws configure
   ```

2. **Enable Bedrock Model Access**:
   - Go to AWS Bedrock Console
   - Navigate to "Model access" 
   - Request access to Claude 4 Sonnet model
   - Wait for approval (can take a few minutes)

3. **Verify Setup**:
   ```bash
   python simple_strands_example.py
   ```
- Python 3.8+ installed

## AI Development Context

Each example includes practical applications for AI development:
- **Data structures** for model configurations and datasets
- **Control flow** for training loops and data processing
- **Functions** for modular AI pipeline components
- **OOP** for building model hierarchies and frameworks
- **File I/O** for dataset loading, model checkpoints, and logging

## Next Steps
After completing this chapter, proceed to Chapter 2 to learn about LLM APIs and AWS Bedrock.

## Resources
- [Python for AI Development (Course.md)](#python-for-ai-development)
- [AWS Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [Python Official Tutorial](https://docs.python.org/3/tutorial/)
- [Python Data Structures Guide](https://docs.python.org/3/tutorial/datastructures.html)

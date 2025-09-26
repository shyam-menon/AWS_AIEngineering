# Markdown Requirements Analyzer

A comprehensive Python solution that converts business requirement files from markdown format to JSON and analyzes them using AWS Bedrock LLM for completeness and quality assessment.

## Features

### Core Functionality
- **Markdown to JSON Conversion**: Convert markdown business requirements to structured JSON format
- **AWS Bedrock Integration**: Analyze requirements using powerful LLM models
- **Batch Processing**: Process multiple files simultaneously
- **Comprehensive Analysis**: Get detailed feedback on requirements completeness and quality
- **Command-Line Interface**: Easy-to-use CLI for all operations
- **Configuration Management**: Flexible configuration via files and environment variables

### Analysis Capabilities
- **Completeness Assessment**: Identify missing or incomplete requirements
- **Quality Evaluation**: Assess the clarity and specificity of requirements
- **Structure Review**: Analyze organization and hierarchy
- **Improvement Suggestions**: Get actionable recommendations
- **Gap Analysis**: Identify critical missing elements

## Installation

### Prerequisites
- Python 3.8 or higher
- AWS account with Bedrock access
- AWS credentials configured

### Setup
1. Clone or download the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure AWS credentials:
   ```bash
   aws configure
   # OR set environment variables:
   export AWS_ACCESS_KEY_ID=your_key
   export AWS_SECRET_ACCESS_KEY=your_secret
   export AWS_DEFAULT_REGION=us-east-1
   ```

## Quick Start

### Basic Conversion
Convert a markdown file to JSON:
```bash
python main.py convert requirements.md
```

### Convert and Analyze
Convert markdown and analyze with Bedrock:
```bash
python main.py convert requirements.md --analyze
```

### Batch Processing
Process multiple files in a directory:
```bash
python main.py batch ./requirements_dir --output ./json_output --analyze
```

### Analyze Existing JSON
Analyze previously converted JSON files:
```bash
python main.py analyze requirements.json --type comprehensive
```

## Configuration

### Configuration File
Create a configuration file for customized settings:
```bash
python main.py config --create-sample --output config.json
```

Example configuration:
```json
{
  "aws": {
    "region": "us-east-1",
    "bedrock": {
      "model_id": "amazon.nova-lite-v1:0",
      "max_tokens": 1000,
      "temperature": 0.1
    }
  },
  "converter": {
    "validate_structure": true,
    "output_format": "json",
    "pretty_print": true
  },
  "logging": {
    "level": "INFO",
    "console": true
  }
}
```

### Environment Variables
Override configuration with environment variables:
- `AWS_REGION`: AWS region for Bedrock
- `BEDROCK_MODEL_ID`: Bedrock model to use
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `OUTPUT_DIR`: Default output directory

## Usage Examples

### 1. Single File Conversion
```bash
# Basic conversion
python main.py convert sample_requirements.md

# Convert with custom output
python main.py convert sample_requirements.md --output ./output/requirements.json

# Convert and analyze
python main.py convert sample_requirements.md --analyze --analysis-type completeness
```

### 2. Batch Processing
```bash
# Process all markdown files in a directory
python main.py batch ./requirements_docs --output ./json_results

# Process with analysis and reporting
python main.py batch ./requirements_docs --analyze --report --output ./results
```

### 3. Analysis Only
```bash
# Comprehensive analysis
python main.py analyze requirements.json --type comprehensive

# Focus on completeness
python main.py analyze requirements.json --type completeness

# Structure analysis
python main.py analyze requirements.json --type structure
```

### 4. Configuration Management
```bash
# Create sample configuration
python main.py config --create-sample --output my_config.json

# Validate configuration
python main.py config --validate

# Show current configuration
python main.py config --show
```

## Analysis Types

### Comprehensive Analysis
Provides a complete assessment including:
- Completeness score (0-100)
- Quality evaluation
- Structure review
- Missing elements identification
- Improvement recommendations

### Completeness Analysis
Focuses on:
- Present vs. missing requirement elements
- Incomplete sections identification
- Questions that need addressing
- Specific recommendations for gaps

### Improvements Analysis
Suggests:
- Clarity enhancements
- Additional details needed
- Structural improvements
- Industry best practices
- Quick wins for immediate improvement

### Structure Analysis
Reviews:
- Logical flow and organization
- Hierarchy and categorization
- Consistency in format
- Readability assessment

## Output Formats

### JSON Conversion Output
```json
{
  "success": true,
  "file_path": "requirements.md",
  "data": {
    "Project Overview": {
      "Business Objectives": [
        "Increase online sales by 40%",
        "Reduce customer acquisition cost by 25%"
      ]
    }
  },
  "metadata": {
    "sections_count": 8,
    "file_size": 7031
  }
}
```

### Analysis Output
```json
{
  "success": true,
  "analysis_type": "comprehensive",
  "analysis": {
    "completeness_score": 85,
    "quality_score": 78,
    "missing_elements": [
      "Detailed user acceptance criteria",
      "Integration testing requirements"
    ],
    "recommendations": [
      "Add specific success metrics for each feature",
      "Include detailed error handling requirements"
    ]
  }
}
```

## Architecture

### Module Structure
```
markdown_requirements_analyzer/
├── main.py                 # Main entry point
├── cli_interface.py        # Command-line interface
├── markdown_converter.py   # Markdown to JSON conversion
├── bedrock_analyzer.py     # AWS Bedrock integration
├── config_manager.py       # Configuration management
├── utils.py               # Utility functions
├── requirements.txt       # Dependencies
├── examples/              # Sample files
│   └── sample_requirements.md
└── README.md             # This file
```

### Key Classes
- **MarkdownConverter**: Handles markdown to JSON conversion
- **BedrockRequirementsAnalyzer**: Manages Bedrock LLM interactions
- **ConfigManager**: Handles configuration loading and validation
- **CLIInterface**: Provides command-line interface

## AWS Bedrock Models

### Supported Models
- **Amazon Nova Lite** (default): Fast, cost-effective analysis
- **Claude Models**: Advanced reasoning capabilities
- **Titan Models**: AWS native models

### Model Configuration
```json
{
  "aws": {
    "bedrock": {
      "model_id": "amazon.nova-lite-v1:0",
      "max_tokens": 1000,
      "temperature": 0.1,
      "top_p": 0.9
    }
  }
}
```

## Error Handling

The tool includes comprehensive error handling for:
- File not found errors
- Invalid markdown format
- AWS credential issues
- Bedrock API errors
- Network connectivity problems
- Configuration validation errors

## Logging

### Log Levels
- **DEBUG**: Detailed debugging information
- **INFO**: General information about operations
- **WARNING**: Warning messages for potential issues
- **ERROR**: Error messages for failed operations

### Log Configuration
```bash
# Set log level via environment
export LOG_LEVEL=DEBUG

# Or via command line
python main.py convert requirements.md --verbose
```

## Performance Considerations

### Optimization Tips
- Use batch processing for multiple files
- Configure appropriate token limits for large documents
- Consider using faster models for initial analysis
- Enable caching for repeated analyses

### Limitations
- Large markdown files may need chunking for analysis
- API rate limits apply for Bedrock requests
- Network latency affects processing time

## Troubleshooting

### Common Issues

#### AWS Credentials Not Found
```bash
# Configure AWS credentials
aws configure

# Or set environment variables
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
```

#### Bedrock Access Denied
- Ensure your AWS account has Bedrock access enabled
- Check IAM permissions for Bedrock services
- Verify the model is available in your region

#### Import Errors
```bash
# Install missing dependencies
pip install -r requirements.txt

# Verify Python path
python -c "import markdown_to_json; print('OK')"
```

### Validation Commands
```bash
# Test configuration
python main.py config --validate

# Test Bedrock connectivity
python -c "import boto3; boto3.client('bedrock-runtime', region_name='us-east-1').list_foundation_models()"
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is part of the AWS AI Engineering course and is provided for educational purposes.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the configuration guide
3. Validate your AWS setup
4. Check the example files for reference

## Examples and Tutorials

See the `examples/` directory for:
- Sample markdown requirements
- Configuration examples
- Expected output formats
- Common use cases

Run the examples:
```bash
# Convert sample requirements
python main.py convert examples/sample_requirements.md --analyze

# Test with different analysis types
python main.py convert examples/sample_requirements.md --analyze --analysis-type completeness
```
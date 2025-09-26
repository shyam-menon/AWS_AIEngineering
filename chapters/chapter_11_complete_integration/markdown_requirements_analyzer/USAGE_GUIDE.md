# Markdown Requirements Analyzer - Usage Guide

## Quick Start Commands

### 1. Basic Conversion
Convert a single markdown file to JSON:
```bash
python main.py convert requirements.md
```

### 2. Convert with Custom Output
Specify the output file location:
```bash
python main.py convert requirements.md --output ./output/requirements.json
```

### 3. Convert and Analyze (Requires AWS Setup)
Convert markdown and analyze with AWS Bedrock:
```bash
python main.py convert requirements.md --analyze
```

### 4. Batch Processing
Process all markdown files in a directory:
```bash
python main.py batch ./requirements_dir --output ./json_output
```

### 5. Batch with Analysis and Reporting
```bash
python main.py batch ./requirements_dir --output ./results --analyze --report
```

### 6. Analyze Existing JSON
Analyze previously converted JSON files:
```bash
python main.py analyze requirements.json --type comprehensive
```

## Analysis Types

### Comprehensive Analysis (Default)
Provides complete assessment:
```bash
python main.py analyze requirements.json --type comprehensive
```

### Completeness Focus
Focus on missing elements:
```bash
python main.py analyze requirements.json --type completeness
```

### Improvement Suggestions
Get actionable recommendations:
```bash
python main.py analyze requirements.json --type improvements
```

### Structure Review
Analyze organization and hierarchy:
```bash
python main.py analyze requirements.json --type structure
```

## Configuration Management

### Create Sample Configuration
```bash
python main.py config --create-sample --output my_config.json
```

### Validate Configuration
```bash
python main.py config --validate
```

### Show Current Configuration
```bash
python main.py config --show
```

### Use Custom Configuration File
```bash
python main.py --config my_config.json convert requirements.md
```

## AWS Bedrock Setup

### 1. Configure AWS Credentials
```bash
# Method 1: AWS CLI
aws configure

# Method 2: Environment Variables
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=us-east-1
```

### 2. Enable Bedrock Models
- Log into AWS Console
- Navigate to Amazon Bedrock
- Enable model access for required models
- Default model: amazon.nova-lite-v1:0

### 3. Test Bedrock Connection
```bash
python main.py convert examples/simple_requirements.md --analyze
```

## Environment Variables

Override configuration with environment variables:

```bash
# AWS Configuration
export AWS_REGION=us-west-2
export BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
export BEDROCK_MAX_TOKENS=2000
export BEDROCK_TEMPERATURE=0.2

# Application Configuration
export LOG_LEVEL=DEBUG
export OUTPUT_DIR=./my_outputs

# Run with environment variables
python main.py convert requirements.md --analyze
```

## Output Examples

### JSON Conversion Output
```json
{
  "success": true,
  "file_path": "requirements.md",
  "data": {
    "Project Overview": {
      "Business Objectives": [
        "Increase sales by 40%",
        "Reduce costs by 25%"
      ]
    },
    "Functional Requirements": {
      "User Management": {
        "Registration": ["Email signup", "Social login"]
      }
    }
  },
  "metadata": {
    "sections_count": 8,
    "file_size": 5432
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
      "Security requirements",
      "Performance metrics"
    ],
    "recommendations": [
      "Add specific success criteria",
      "Include error handling requirements"
    ],
    "overall_assessment": "Good foundation with improvement areas"
  }
}
```

## File Organization

### Recommended Project Structure
```
project/
├── requirements/
│   ├── user_stories.md
│   ├── technical_specs.md
│   └── business_rules.md
├── output/
│   ├── json/
│   ├── analysis/
│   └── reports/
└── config/
    └── analyzer_config.json
```

### Processing Command
```bash
python main.py batch requirements --output output/json --analyze
```

## Troubleshooting

### Common Issues

#### 1. AWS Credentials Not Found
```
Error: AWS credentials not configured
```
**Solution:**
```bash
aws configure
# OR
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
```

#### 2. Bedrock Access Denied
```
Error: User is not authorized to perform: bedrock:InvokeModel
```
**Solution:**
- Check IAM permissions for Bedrock
- Enable model access in Bedrock console
- Verify model is available in your region

#### 3. Model Not Available
```
Error: The requested model is not available
```
**Solution:**
```bash
# Check available models
python main.py list --models

# Use different model
export BEDROCK_MODEL_ID=amazon.nova-lite-v1:0
```

#### 4. Import Errors
```
ModuleNotFoundError: No module named 'markdown_to_json'
```
**Solution:**
```bash
pip install -r requirements.txt
```

### Validation Commands

#### Test Configuration
```bash
python main.py config --validate
```

#### Test Basic Functionality
```bash
python test_functionality.py
```

#### Test AWS Connection
```bash
python -c "
import boto3
client = boto3.client('bedrock-runtime', region_name='us-east-1')
print('✅ AWS connection successful')
"
```

## Performance Tips

### For Large Files
- Use batch processing for multiple files
- Set appropriate token limits
- Consider chunking very large documents

### For Better Analysis
- Provide structured markdown with clear headers
- Include specific requirements language
- Use consistent formatting

### For Speed
- Use faster models for initial analysis
- Process files in parallel with batch mode
- Cache results when possible

## Best Practices

### Markdown Structure
```markdown
# Project Requirements

## Overview
Brief description of the project

## Functional Requirements
### Feature 1
- Specific requirement 1
- Specific requirement 2

### Feature 2
- Requirement with acceptance criteria
- Performance requirements

## Non-Functional Requirements
### Performance
- Response time requirements
- Scalability requirements

### Security
- Authentication requirements
- Data protection requirements
```

### Analysis Workflow
1. Convert markdown to JSON
2. Review conversion results
3. Run comprehensive analysis
4. Focus on specific areas (completeness, structure)
5. Implement recommendations
6. Re-analyze to track improvements

## Integration Examples

### CI/CD Pipeline
```bash
#!/bin/bash
# requirements_check.sh

# Convert and analyze all requirements
python main.py batch requirements/ --output artifacts/json --analyze --report

# Check if analysis meets quality threshold
python -c "
import json
with open('artifacts/json/batch_analysis.json') as f:
    results = json.load(f)
    
scores = [r['analysis']['completeness_score'] for r in results if r['success']]
avg_score = sum(scores) / len(scores) if scores else 0

if avg_score < 80:
    print(f'❌ Quality gate failed: {avg_score:.1f}% < 80%')
    exit(1)
else:
    print(f'✅ Quality gate passed: {avg_score:.1f}%')
"
```

### Automation Script
```python
#!/usr/bin/env python3
import subprocess
import json
from pathlib import Path

def analyze_requirements(input_dir, output_dir):
    """Automated requirements analysis."""
    cmd = [
        'python', 'main.py', 'batch', 
        str(input_dir), 
        '--output', str(output_dir),
        '--analyze', '--report'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Analysis completed successfully")
        
        # Load and display summary
        report_file = Path(output_dir) / 'batch_report.json'
        if report_file.exists():
            with open(report_file) as f:
                report = json.load(f)
            
            print(f"📊 Processed {report['summary']['total_files']} files")
            print(f"✅ Successful: {report['summary']['successful']}")
            print(f"❌ Failed: {report['summary']['failed']}")
        
    else:
        print(f"❌ Analysis failed: {result.stderr}")
        return False
    
    return True

if __name__ == "__main__":
    analyze_requirements('./requirements', './output')
```

## Support and Resources

### Getting Help
1. Check this usage guide
2. Review the main README.md
3. Run the test suite: `python test_functionality.py`
4. Try the demo: `python examples/demo_script.py`

### Example Files
- `examples/sample_requirements.md` - Comprehensive example
- `examples/simple_requirements.md` - Basic example
- `examples/incomplete_requirements.md` - Shows validation warnings

### Configuration Templates
```bash
# Create sample configurations
python main.py config --create-sample --output config.json
python main.py config --create-sample --output config.yml
```
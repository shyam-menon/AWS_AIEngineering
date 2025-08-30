# AWS Boto3 and Strands Library Examples

A collection of practical examples demonstrating how to use AWS Boto3 SDK and Strands library for various AWS services and AI/ML workflows.

## 📁 Repository Structure

```
AWS_Boto/
├── examples/
│   ├── ec2/                 # EC2 service examples
│   ├── bedrock/             # AWS Bedrock (AI/ML) examples
│   └── strands/             # Strands library examples
├── docs/                    # Documentation and guides
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🚀 Quick Start

### 1. Setup Environment
```powershell
# Create virtual environment (if not exists)
python -m venv .venv

# Activate virtual environment
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure AWS Credentials
```powershell
# Option 1: AWS CLI
aws configure

# Option 2: Environment Variables
$env:AWS_ACCESS_KEY_ID="your_key"
$env:AWS_SECRET_ACCESS_KEY="your_secret"
$env:AWS_DEFAULT_REGION="us-east-1"
```

### 3. Run Examples
```powershell
# List EC2 instances
python examples\ec2\ec2_list.py

# Interactive AI chat with Nova Lite
python examples\bedrock\nova_lite_chat.py

# Extract JSON data from text
python examples\bedrock\bedrock_json_output.py --mode examples

# Specialized AI applications
python examples\bedrock\nova_lite_apps.py --help
```

## 📚 Examples Overview

### 🖥️ EC2 Examples
- **`ec2_list.py`** - List and display EC2 instances across regions

### 🤖 Bedrock (AI/ML) Examples
- **`test_nova_lite.py`** - Basic Nova Lite model invocation
- **`nova_lite_chat.py`** - Interactive chat interface
- **`nova_lite_cli.py`** - Command-line interface with presets
- **`nova_lite_apps.py`** - Professional applications (content, code, research, business)
- **`bedrock_json_output.py`** - Structured JSON data extraction from text

### 🔗 Strands Library Examples
*Coming soon - examples demonstrating Strands library integration*

## 🎯 Use Cases

### Infrastructure Management
- Monitor EC2 instances across multiple regions
- Automate AWS resource discovery and reporting

### AI-Powered Applications
- Content generation and editing
- Code assistance and review
- Business analysis and strategy
- Creative writing and storytelling

### Hybrid Workflows
- Combine AWS services with AI capabilities
- Automated reporting with natural language summaries
- Intelligent infrastructure monitoring

## 📖 Documentation

- **[Nova Lite Guide](docs/NOVA_LITE_GUIDE.md)** - Complete guide for Amazon Nova Lite
- **[AWS Configuration](docs/aws_config_examples.txt)** - AWS credentials setup examples

## 🛠️ Requirements

### AWS Services Access
- **EC2**: `ec2:DescribeInstances`
- **Bedrock**: `bedrock:InvokeModel`, `bedrock:ListFoundationModels`

### Python Dependencies
- `boto3` - AWS SDK for Python
- `botocore` - Core functionality for Boto3
- Additional dependencies as needed for Strands integration

## 🔧 Development

### Adding New Examples

1. **EC2 Examples**: Add to `examples/ec2/`
2. **Bedrock Examples**: Add to `examples/bedrock/`
3. **Strands Examples**: Add to `examples/strands/`

### Best Practices
- Include error handling and logging
- Use environment variables for configuration
- Add documentation and examples
- Follow AWS security best practices

## 🚨 Security Notes

- Never commit AWS credentials to version control
- Use IAM roles when possible
- Follow principle of least privilege
- Regularly rotate access keys

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve these examples.

# AWS Boto3 Applications Index

Welcome to your AWS Boto3 applications collection! This repository contains Python applications for interacting with AWS services, specifically EC2 and Bedrock.

## 📁 Repository Structure

### 🖥️ EC2 Applications
| File | Description | Usage |
|------|-------------|-------|
| `ec2_list.py` | Main EC2 instance lister | `python ec2_list.py [region]` |
| `test_setup.py` | Test AWS credentials and setup | `python test_setup.py` |

### 🤖 Bedrock LLM Applications
| File | Description | Usage |
|------|-------------|-------|
| `bedrock_simple.py` | Simple Claude interaction | `python bedrock_simple.py` |
| `bedrock_llm.py` | Full-featured CLI for multiple models | `python bedrock_llm.py --help` |
| `bedrock_conversation.py` | Advanced conversation patterns | `python bedrock_conversation.py` |
| `bedrock_manager.py` | Model status and management | `python bedrock_manager.py` |

### 🌟 Amazon Nova Lite Applications (Recommended)
| File | Description | Usage |
|------|-------------|-------|
| `nova_lite_chat.py` | Interactive chat with Nova Lite | `python nova_lite_chat.py` |
| `nova_lite_cli.py` | Command-line interface with presets | `python nova_lite_cli.py --help` |
| `nova_lite_apps.py` | Specialized professional applications | `python nova_lite_apps.py --help` |
| `test_nova_lite.py` | Original Amazon example code | `python test_nova_lite.py` |

### 🔧 Setup and Configuration
| File | Description | Usage |
|------|-------------|-------|
| `bedrock_setup_guide.py` | Complete setup assistant | `python bedrock_setup_guide.py` |
| `bedrock_inference_profiles.py` | Inference profiles demo | `python bedrock_inference_profiles.py` |
| `find_working_models.py` | Find directly invokable models | `python find_working_models.py` |
| `bedrock_test_after_setup.py` | Test after enabling models | `python bedrock_test_after_setup.py` |

### 📚 Documentation
| File | Description |
|------|-------------|
| `README.md` | Main EC2 application guide |
| `BEDROCK_README.md` | Comprehensive Bedrock guide |
| `NOVA_LITE_GUIDE.md` | Complete Nova Lite applications guide |
| `aws_config_examples.txt` | AWS credentials examples |
| `requirements.txt` | Python dependencies |

## 🚀 Quick Start

### For EC2 Listing:
```powershell
# Test your setup
python test_setup.py

# List EC2 instances
python ec2_list.py

# List in specific region
python ec2_list.py us-west-2
```

### For Bedrock LLMs (Nova Lite - Recommended):
```powershell
# Quick test with your accessible model
python test_nova_lite.py

# Interactive chat
python nova_lite_chat.py

# Professional content creation
python nova_lite_apps.py content blog "Your Topic" --style professional

# Code assistance
python nova_lite_apps.py code "Your programming question" --tests

# Command line with presets
python nova_lite_cli.py "Your prompt" --preset creative --stream
```

### For Bedrock LLMs (Other Models - Requires Setup):
```powershell
# 1. Check what models are available
python bedrock_manager.py

# 2. Follow the setup guide
python bedrock_setup_guide.py

# 3. Enable models in AWS console (see guide output)

# 4. Test your setup
python bedrock_test_after_setup.py

# 5. Use the applications
python bedrock_simple.py
python bedrock_llm.py --interactive
```

## 🎯 Use Cases by Application

### EC2 Management
- **Inventory**: See all EC2 instances across regions
- **Monitoring**: Check instance states and types
- **Cost Optimization**: Identify unused instances

### AI/LLM Applications
- **Content Creation**: Generate articles, blog posts, marketing copy
- **Code Assistance**: Get help with programming problems
- **Research & Analysis**: Analyze documents, summarize content
- **Customer Support**: Create chatbots and automated responses
- **Creative Writing**: Stories, poems, creative content

## ⚙️ Configuration Requirements

### AWS Credentials
Choose one method:
```bash
# Option 1: AWS CLI
aws configure

# Option 2: Environment Variables (PowerShell)
$env:AWS_ACCESS_KEY_ID="your_key"
$env:AWS_SECRET_ACCESS_KEY="your_secret"
$env:AWS_DEFAULT_REGION="us-east-1"

# Option 3: IAM Roles (if running on EC2)
```

### Required Permissions

#### For EC2:
```json
{
    "Effect": "Allow",
    "Action": ["ec2:DescribeInstances"],
    "Resource": "*"
}
```

#### For Bedrock:
```json
{
    "Effect": "Allow",
    "Action": [
        "bedrock:InvokeModel",
        "bedrock:ListFoundationModels",
        "bedrock:ListInferenceProfiles"
    ],
    "Resource": "*"
}
```

## 🛠️ Troubleshooting

### Common Issues

#### EC2 Applications:
- **No instances found**: Check the correct region
- **Permission denied**: Verify IAM permissions
- **No credentials**: Run `aws configure`

#### Bedrock Applications:
- **Model not enabled**: Enable models in [Bedrock Console](https://console.aws.amazon.com/bedrock/)
- **Access denied**: Check model access permissions
- **Inference profile needed**: Use newer applications with profile support
- **Region not supported**: Try `us-east-1`, `us-west-2`, or `eu-west-1`

### Getting Help
1. Run the setup guides first
2. Check the detailed READMEs
3. Verify AWS credentials and permissions
4. Start with simple examples before advanced features

## 📊 Model Recommendations

### For Cost-Effective Use:
- **Claude Instant** or **Claude 3 Haiku** - Fastest and cheapest
- **Amazon Titan Text** - Good balance of cost and performance

### For Complex Tasks:
- **Claude 3 Sonnet** - Balanced performance
- **Claude 3.5 Sonnet** - Advanced reasoning
- **Claude Opus** - Highest capability

### For Getting Started:
1. Enable **Claude Instant v1** first (easiest to set up)
2. Try **Claude 3 Haiku** for modern features
3. Upgrade to **Claude 3 Sonnet** for complex tasks

## 🔄 Workflow Examples

### Daily EC2 Monitoring:
```powershell
# Morning check
python ec2_list.py

# Check multiple regions
python ec2_list.py us-east-1
python ec2_list.py us-west-2
python ec2_list.py eu-west-1
```

### Content Creation Workflow:
```powershell
# Interactive brainstorming
python bedrock_llm.py --interactive

# Specific content generation
python bedrock_llm.py --model claude-sonnet --prompt "Write a technical blog post about..."

# Multiple model comparison
python bedrock_conversation.py
```

### Development Workflow:
```powershell
# Quick code help
python bedrock_llm.py --prompt "How to handle errors in Python?"

# Code review assistance
python bedrock_llm.py --model claude-sonnet --prompt "Review this code: [paste code]"
```

## 🚀 Next Steps

1. **Start with setup**: Run `python bedrock_setup_guide.py`
2. **Enable models**: Follow the console instructions
3. **Test basic functionality**: Use the simple scripts
4. **Explore advanced features**: Try conversation patterns
5. **Build custom integrations**: Use the code as a foundation

## 📞 Support

- Check the detailed READMEs for specific applications
- Review AWS Bedrock documentation for model-specific guidance
- Ensure proper IAM permissions are configured
- Start with simpler models before trying advanced ones

---

**Happy coding with AWS Boto3! 🎉**

#!/usr/bin/env python3
"""
AWS Bedrock Model Management Utility

This script helps you manage and check the status of foundation models
in your AWS Bedrock account, including enabling models and checking access.
"""

import boto3
import json
from typing import List, Dict
from botocore.exceptions import ClientError, NoCredentialsError


class BedrockModelManager:
    """Class to manage Bedrock foundation models."""
    
    def __init__(self, region='us-east-1'):
        """Initialize Bedrock clients."""
        try:
            self.bedrock = boto3.client('bedrock', region_name=region)
            self.bedrock_runtime = boto3.client('bedrock-runtime', region_name=region)
            self.region = region
        except NoCredentialsError:
            print("Error: AWS credentials not found.")
            raise
        except Exception as e:
            print(f"Error initializing Bedrock clients: {e}")
            raise
    
    def list_foundation_models(self) -> List[Dict]:
        """List all available foundation models."""
        try:
            response = self.bedrock.list_foundation_models()
            return response['modelSummaries']
        except ClientError as e:
            print(f"Error listing foundation models: {e}")
            return []
    
    def get_model_access_status(self) -> Dict:
        """Get the access status for all models."""
        try:
            # This endpoint might not be available in all regions
            # We'll use a different approach to check model access
            models = self.list_foundation_models()
            access_status = {}
            
            for model in models:
                model_id = model['modelId']
                # Try to invoke the model with a simple test to check access
                access_status[model_id] = self._test_model_access(model_id)
            
            return access_status
        except Exception as e:
            print(f"Error checking model access: {e}")
            return {}
    
    def _test_model_access(self, model_id: str) -> Dict:
        """Test if we can access a specific model."""
        try:
            # Create a minimal test request based on model type
            if "anthropic.claude" in model_id:
                body = {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 10,
                    "messages": [{"role": "user", "content": "Hi"}]
                }
            elif "amazon.titan-text" in model_id:
                body = {
                    "inputText": "Hi",
                    "textGenerationConfig": {"maxTokenCount": 10}
                }
            elif "meta.llama2" in model_id:
                body = {
                    "prompt": "Hi",
                    "max_gen_len": 10
                }
            elif "mistral" in model_id:
                body = {
                    "prompt": "Hi",
                    "max_tokens": 10
                }
            else:
                return {"accessible": False, "error": "Unknown model type"}
            
            # Try to invoke the model
            self.bedrock_runtime.invoke_model(
                modelId=model_id,
                body=json.dumps(body),
                contentType='application/json'
            )
            
            return {"accessible": True, "error": None}
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'AccessDeniedException':
                return {"accessible": False, "error": "Access denied - Model not enabled"}
            elif error_code == 'ValidationException':
                return {"accessible": True, "error": "Model accessible but validation error (expected)"}
            else:
                return {"accessible": False, "error": f"AWS Error: {error_code}"}
        except Exception as e:
            return {"accessible": False, "error": f"Error: {str(e)}"}
    
    def get_popular_models(self) -> List[Dict]:
        """Get a list of popular/recommended models."""
        popular_models = [
            {
                "modelId": "anthropic.claude-3-haiku-20240307-v1:0",
                "name": "Claude 3 Haiku",
                "description": "Fast and cost-effective for everyday tasks",
                "use_cases": ["Q&A", "Content creation", "Code assistance"]
            },
            {
                "modelId": "anthropic.claude-3-sonnet-20240229-v1:0",
                "name": "Claude 3 Sonnet",
                "description": "Balanced performance for complex tasks",
                "use_cases": ["Analysis", "Research", "Creative writing"]
            },
            {
                "modelId": "amazon.titan-text-express-v1",
                "name": "Amazon Titan Text Express",
                "description": "Amazon's foundation model for text generation",
                "use_cases": ["Summarization", "Q&A", "Text completion"]
            },
            {
                "modelId": "meta.llama2-13b-chat-v1",
                "name": "Llama 2 13B Chat",
                "description": "Meta's conversational AI model",
                "use_cases": ["Chat", "Dialogue", "Conversational AI"]
            }
        ]
        
        # Check which ones are available
        available_models = self.list_foundation_models()
        available_ids = [model['modelId'] for model in available_models]
        
        return [model for model in popular_models if model['modelId'] in available_ids]
    
    def display_model_status(self):
        """Display a comprehensive status of all models."""
        print(f"Bedrock Foundation Models Status - Region: {self.region}")
        print("=" * 80)
        
        models = self.list_foundation_models()
        if not models:
            print("No foundation models found or accessible.")
            return
        
        print(f"Total models available: {len(models)}")
        print()
        
        # Group by provider
        providers = {}
        for model in models:
            provider = model['providerName']
            if provider not in providers:
                providers[provider] = []
            providers[provider].append(model)
        
        for provider, provider_models in providers.items():
            print(f"\n{provider} Models ({len(provider_models)}):")
            print("-" * 50)
            
            for model in provider_models:
                print(f"  Model ID: {model['modelId']}")
                print(f"  Name: {model['modelName']}")
                print(f"  Input: {', '.join(model['inputModalities'])}")
                print(f"  Output: {', '.join(model['outputModalities'])}")
                
                # Test access
                access_info = self._test_model_access(model['modelId'])
                if access_info['accessible']:
                    print(f"  Status: ✅ ACCESSIBLE")
                else:
                    print(f"  Status: ❌ NOT ACCESSIBLE - {access_info['error']}")
                
                print()
    
    def display_quick_start_guide(self):
        """Display a quick start guide for enabling models."""
        print("\nQuick Start Guide for AWS Bedrock")
        print("=" * 40)
        print("""
To use Bedrock models, you need to:

1. Enable Models in AWS Console:
   - Go to AWS Bedrock console
   - Navigate to 'Model access' in the left sidebar
   - Request access to the models you want to use
   - Wait for approval (usually instant for most models)

2. Required IAM Permissions:
   Your AWS user/role needs these permissions:
   - bedrock:InvokeModel
   - bedrock:ListFoundationModels
   - bedrock:GetFoundationModel

3. Popular Models to Enable:
   - Claude 3 Haiku (anthropic.claude-3-haiku-20240307-v1:0)
   - Claude 3 Sonnet (anthropic.claude-3-sonnet-20240229-v1:0)
   - Amazon Titan Text (amazon.titan-text-express-v1)

4. Test Your Setup:
   Run: python bedrock_simple.py

For detailed setup instructions, visit:
https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html
        """)


def main():
    """Main function."""
    print("AWS Bedrock Model Management Utility")
    
    try:
        manager = BedrockModelManager()
        
        # Display model status
        manager.display_model_status()
        
        # Show popular models
        print("\nRecommended Models for Getting Started:")
        print("=" * 45)
        popular = manager.get_popular_models()
        
        for model in popular:
            print(f"\n🔹 {model['name']}")
            print(f"   ID: {model['modelId']}")
            print(f"   Description: {model['description']}")
            print(f"   Use Cases: {', '.join(model['use_cases'])}")
            
            # Check access
            access_info = manager._test_model_access(model['modelId'])
            if access_info['accessible']:
                print(f"   Status: ✅ Ready to use")
            else:
                print(f"   Status: ❌ {access_info['error']}")
        
        # Show quick start guide
        manager.display_quick_start_guide()
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure your AWS credentials are configured and you have Bedrock access.")


if __name__ == "__main__":
    main()

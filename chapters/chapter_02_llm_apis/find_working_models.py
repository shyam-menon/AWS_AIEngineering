#!/usr/bin/env python3
"""
AWS Bedrock Working Models Finder

This script finds models that can be directly invoked without inference profiles.
It tests various Claude models to find which ones work with direct invocation.
"""

import boto3
import json
from botocore.exceptions import ClientError


def test_claude_models():
    """Test different Claude models to find working ones."""
    bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')
    
    # List of Claude models to test (older models that might work directly)
    test_models = [
        "anthropic.claude-instant-v1",
        "anthropic.claude-v2",
        "anthropic.claude-v2:1", 
        "anthropic.claude-3-haiku-20240307-v1:0",
        "anthropic.claude-3-sonnet-20240229-v1:0",
        "anthropic.claude-3-opus-20240229-v1:0",
        "anthropic.claude-3-5-sonnet-20240620-v1:0",
        "anthropic.claude-3-5-sonnet-20241022-v2:0",
        "anthropic.claude-3-5-haiku-20241022-v1:0",
        "anthropic.claude-opus-4-1-20250805-v1:0"
    ]
    
    working_models = []
    
    for model_id in test_models:
        print(f"Testing {model_id}...")
        
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 10,
            "messages": [
                {
                    "role": "user",
                    "content": "Hi"
                }
            ]
        }
        
        try:
            response = bedrock_runtime.invoke_model(
                modelId=model_id,
                body=json.dumps(body),
                contentType='application/json'
            )
            
            # If we get here, the model works
            response_body = json.loads(response['body'].read())
            content = response_body['content'][0]['text']
            print(f"✅ {model_id} - WORKS: {content[:50]}")
            working_models.append(model_id)
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if 'ValidationException' in str(e) and 'inference profile' in str(e):
                print(f"❌ {model_id} - Needs inference profile")
            elif error_code == 'AccessDeniedException':
                print(f"❌ {model_id} - Access denied (not enabled)")
            elif error_code == 'ResourceNotFoundException':
                print(f"❌ {model_id} - Not found in this region")
            else:
                print(f"❌ {model_id} - Error: {error_code}")
        except Exception as e:
            print(f"❌ {model_id} - Error: {e}")
    
    return working_models


def main():
    """Main function."""
    print("Finding Working Claude Models in Bedrock")
    print("=" * 45)
    
    try:
        working_models = test_claude_models()
        
        print(f"\n🎉 Found {len(working_models)} working models:")
        for model in working_models:
            print(f"  - {model}")
        
        if working_models:
            print(f"\nRecommended model to use: {working_models[0]}")
        else:
            print("\n⚠️  No directly invokable models found.")
            print("You may need to:")
            print("1. Enable models in the Bedrock console")
            print("2. Use inference profiles for newer models")
            print("3. Check if models are available in your region")
    
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
AWS Bedrock with Inference Profiles

This script demonstrates how to use AWS Bedrock with inference profiles
for newer models that require them.
"""

import boto3
import json
from botocore.exceptions import ClientError


def list_inference_profiles():
    """List available inference profiles."""
    try:
        bedrock = boto3.client('bedrock', region_name='us-east-1')
        response = bedrock.list_inference_profiles()
        return response.get('inferenceProfileSummaries', [])
    except Exception as e:
        print(f"Error listing inference profiles: {e}")
        return []


def invoke_with_inference_profile(profile_name, prompt):
    """
    Invoke a model using an inference profile.
    
    Args:
        profile_name (str): Name or ARN of the inference profile
        prompt (str): The prompt to send
        
    Returns:
        str: Model response
    """
    try:
        bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')
        
        # Prepare request body (Claude format)
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        # Invoke using inference profile
        response = bedrock_runtime.invoke_model(
            modelId=profile_name,  # Use profile name as model ID
            body=json.dumps(body),
            contentType='application/json'
        )
        
        # Parse response
        response_body = json.loads(response['body'].read())
        return response_body['content'][0]['text']
        
    except ClientError as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"


def demonstrate_inference_profiles():
    """Demonstrate using inference profiles."""
    print("AWS Bedrock Inference Profiles Demo")
    print("=" * 37)
    
    # List available profiles
    profiles = list_inference_profiles()
    
    if not profiles:
        print("❌ No inference profiles found or accessible.")
        print("💡 Make sure you have the right permissions and models are enabled.")
        return
    
    print(f"📋 Found {len(profiles)} inference profiles:")
    
    # Show Claude profiles
    claude_profiles = [p for p in profiles if 'claude' in p.get('inferenceProfileName', '').lower()]
    
    if not claude_profiles:
        print("❌ No Claude inference profiles found.")
        return
    
    print("\n🤖 Claude Inference Profiles:")
    for i, profile in enumerate(claude_profiles[:3], 1):  # Show first 3
        name = profile.get('inferenceProfileName', 'Unknown')
        profile_id = profile.get('inferenceProfileId', 'Unknown')
        print(f"  {i}. {name} (ID: {profile_id})")
    
    # Try to use the first Claude profile
    if claude_profiles:
        profile_to_test = claude_profiles[0]['inferenceProfileId']
        print(f"\n🧪 Testing with profile: {profile_to_test}")
        
        test_prompts = [
            "What is the capital of France?",
            "Explain quantum computing in one sentence.",
            "Write a haiku about programming."
        ]
        
        for prompt in test_prompts:
            print(f"\n📝 Prompt: {prompt}")
            print("🤔 Thinking...")
            
            response = invoke_with_inference_profile(profile_to_test, prompt)
            
            if response.startswith("Error:"):
                print(f"❌ {response}")
            else:
                print(f"✅ Response: {response}")


def create_inference_profile_example():
    """Create a standalone example for inference profiles."""
    example_code = '''#!/usr/bin/env python3
"""
Example: Using Bedrock Inference Profiles
"""
import boto3
import json

def chat_with_claude_profile():
    """Chat with Claude using inference profile."""
    bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')
    
    # Use a Claude inference profile (replace with actual profile ID)
    # You can get profile IDs from the bedrock_setup_guide.py output
    claude_profiles = [
        "us.anthropic.claude-3-sonnet-20240229-v1:0",  # Example profile ID
        "us.anthropic.claude-3-haiku-20240307-v1:0",   # Example profile ID
    ]
    
    for profile_id in claude_profiles:
        try:
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 500,
                "messages": [
                    {
                        "role": "user", 
                        "content": "Hello! Please introduce yourself."
                    }
                ]
            }
            
            response = bedrock_runtime.invoke_model(
                modelId=profile_id,
                body=json.dumps(body),
                contentType='application/json'
            )
            
            result = json.loads(response['body'].read())
            print(f"✅ SUCCESS with {profile_id}")
            print(f"Claude: {result['content'][0]['text']}")
            return
            
        except Exception as e:
            print(f"❌ Failed with {profile_id}: {str(e)[:100]}...")
    
    print("❌ No inference profiles worked.")
    print("💡 Check the setup guide output for correct profile IDs.")

if __name__ == "__main__":
    chat_with_claude_profile()
'''
    
    with open('bedrock_inference_profile_example.py', 'w', encoding='utf-8') as f:
        f.write(example_code)
    
    print("\n📄 Created 'bedrock_inference_profile_example.py'")
    print("🔧 Edit the profile IDs in the file based on your available profiles")


def main():
    """Main function."""
    print("This script helps you work with Bedrock Inference Profiles")
    print("=" * 55)
    
    try:
        demonstrate_inference_profiles()
        create_inference_profile_example()
        
        print("\n" + "=" * 55)
        print("💡 KEY POINTS:")
        print("1. Newer models often require inference profiles")
        print("2. Use profile ID as the modelId parameter")
        print("3. Enable models in Bedrock console first")
        print("4. Check permissions for inference profile access")
        print("=" * 55)
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

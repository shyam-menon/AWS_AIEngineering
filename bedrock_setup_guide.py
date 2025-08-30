#!/usr/bin/env python3
"""
AWS Bedrock Setup Guide and Model Enabler

This script provides guidance on setting up Bedrock models and also demonstrates
how to work with inference profiles for newer models.
"""

import boto3
import json
from botocore.exceptions import ClientError


def check_bedrock_setup():
    """Check the current Bedrock setup status."""
    print("🔍 Checking AWS Bedrock Setup")
    print("=" * 35)
    
    try:
        # Check if we can access Bedrock
        bedrock = boto3.client('bedrock', region_name='us-east-1')
        bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')
        
        print("✅ Bedrock clients initialized successfully")
        
        # List foundation models
        models = bedrock.list_foundation_models()
        total_models = len(models['modelSummaries'])
        print(f"✅ Found {total_models} foundation models available")
        
        # Count Claude models specifically
        claude_models = [m for m in models['modelSummaries'] if 'claude' in m['modelId'].lower()]
        print(f"✅ Found {len(claude_models)} Claude models available")
        
        return True
        
    except ClientError as e:
        print(f"❌ Error accessing Bedrock: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def get_inference_profiles():
    """Get available inference profiles."""
    try:
        bedrock = boto3.client('bedrock', region_name='us-east-1')
        
        # Try to list inference profiles (this might not work in all regions/accounts)
        try:
            response = bedrock.list_inference_profiles()
            profiles = response.get('inferenceProfileSummaries', [])
            
            if profiles:
                print(f"\n📋 Found {len(profiles)} inference profiles:")
                for profile in profiles[:5]:  # Show first 5
                    print(f"  - {profile.get('inferenceProfileName', profile.get('inferenceProfileId', 'Unknown'))}")
                if len(profiles) > 5:
                    print(f"  ... and {len(profiles) - 5} more")
            else:
                print("\n📋 No inference profiles found")
                
            return profiles
            
        except ClientError as e:
            if 'AccessDenied' in str(e):
                print("\n📋 Cannot list inference profiles (permission denied)")
            else:
                print(f"\n📋 Error listing inference profiles: {e}")
            return []
            
    except Exception as e:
        print(f"\n📋 Error checking inference profiles: {e}")
        return []


def demonstrate_model_enabling():
    """Show how to enable models."""
    print("\n🚀 How to Enable Bedrock Models")
    print("=" * 32)
    
    print("""
STEP 1: Go to AWS Bedrock Console
   🌐 https://console.aws.amazon.com/bedrock/

STEP 2: Navigate to Model Access
   📍 In the left sidebar, click "Model access"

STEP 3: Enable Models
   ✅ Click "Enable specific models" or "Manage model access"
   ✅ Find these recommended models and enable them:
   
   BEGINNER-FRIENDLY (Direct Invocation):
   📌 Claude Instant v1
   📌 Claude v2
   📌 Claude 3 Haiku
   📌 Claude 3 Sonnet
   
   ADVANCED (May need inference profiles):
   📌 Claude 3.5 Sonnet
   📌 Claude 3.5 Haiku
   📌 Claude Opus 4

STEP 4: Submit Request
   📝 Fill out the use case form (usually auto-approved)
   ⏱️  Wait for approval (typically instant for most models)

STEP 5: Test Your Setup
   🧪 Run: python bedrock_simple.py
   
IMPORTANT NOTES:
💡 Some models require "Provisioned Throughput" or "Inference Profiles"
💡 Start with Claude Instant or Claude v2 for easiest setup
💡 Different regions have different model availability
    """)


def create_simple_working_example():
    """Create a simple example that will work once models are enabled."""
    print("\n📝 Creating Simple Working Example")
    print("=" * 35)
    
    example_code = '''#!/usr/bin/env python3
"""
Simple Bedrock Example - Works after enabling models
"""
import boto3
import json

def test_bedrock_simple():
    """Test basic Bedrock functionality."""
    client = boto3.client('bedrock-runtime', region_name='us-east-1')
    
    # Try Claude Instant first (usually easiest to enable)
    models_to_try = [
        "anthropic.claude-instant-v1",
        "anthropic.claude-v2", 
        "anthropic.claude-3-haiku-20240307-v1:0"
    ]
    
    for model_id in models_to_try:
        try:
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 100,
                "messages": [{"role": "user", "content": "Hello! Can you respond?"}]
            }
            
            response = client.invoke_model(
                modelId=model_id,
                body=json.dumps(body),
                contentType='application/json'
            )
            
            result = json.loads(response['body'].read())
            print(f"✅ SUCCESS with {model_id}")
            print(f"Response: {result['content'][0]['text']}")
            return True
            
        except Exception as e:
            print(f"❌ {model_id}: {str(e)[:100]}...")
    
    print("❌ No models worked. Please enable models in Bedrock console.")
    return False

if __name__ == "__main__":
    test_bedrock_simple()
'''
    
    with open('bedrock_test_after_setup.py', 'w', encoding='utf-8') as f:
        f.write(example_code)
    
    print("✅ Created 'bedrock_test_after_setup.py'")
    print("🎯 Run this script after enabling models in the console!")


def main():
    """Main function."""
    print("AWS Bedrock Setup Assistant")
    print("=" * 27)
    
    # Check basic setup
    if not check_bedrock_setup():
        print("\n❌ Basic Bedrock setup failed. Check your AWS credentials.")
        return
    
    # Check inference profiles
    get_inference_profiles()
    
    # Show how to enable models
    demonstrate_model_enabling()
    
    # Create working example
    create_simple_working_example()
    
    print("\n" + "=" * 50)
    print("🎉 NEXT STEPS:")
    print("1. Enable models in AWS Bedrock Console")
    print("2. Run: python bedrock_test_after_setup.py") 
    print("3. Once working, use the full applications!")
    print("=" * 50)


if __name__ == "__main__":
    main()

"""
Simple test script to verify the basic setup works without complex dependencies
"""

import boto3
import json


def test_basic_boto3():
    """Test basic boto3 functionality"""
    print("🧪 Testing Basic Setup...")
    
    try:
        # Test AWS session
        session = boto3.Session()
        region = session.region_name
        print(f"✅ AWS Region: {region}")
        
        # Test Bedrock client creation
        bedrock = boto3.client('bedrock-runtime', region_name=region)
        print("✅ Bedrock client created")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic setup error: {e}")
        return False


def test_nova_lite_simple():
    """Test Nova Lite with simple API call"""
    print("\n🤖 Testing Nova Lite Model...")
    
    try:
        bedrock = boto3.client('bedrock-runtime')
        
        # Simple payload for Nova Lite - correct format
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "text": "What is 2 + 2?"
                        }
                    ]
                }
            ],
            "inferenceConfig": {
                "max_new_tokens": 100,
                "temperature": 0.1
            }
        }
        
        response = bedrock.invoke_model(
            modelId="us.amazon.nova-lite-v1:0",
            body=json.dumps(payload)
        )
        
        response_body = json.loads(response['body'].read())
        output_text = response_body.get('output', {}).get('message', {}).get('content', [{}])[0].get('text', 'No output')
        
        print("✅ Nova Lite responded successfully!")
        print(f"📝 Response: {output_text}")
        
        return True
        
    except Exception as e:
        print(f"❌ Nova Lite test failed: {e}")
        print("💡 This might be normal if Strands packages aren't installed yet")
        return False


def main():
    """Main test function"""
    print("🔧 Simple Setup Test")
    print("=" * 40)
    
    basic_ok = test_basic_boto3()
    
    if basic_ok:
        test_nova_lite_simple()
    
    print("\n" + "=" * 40)
    print("✅ Simple test complete!")
    print("\n📋 Next steps:")
    print("1. If Nova Lite test worked, you're ready to go!")
    print("2. If not, install the AgentCore packages:")
    print("   pip install strands-agents strands-tools")


if __name__ == "__main__":
    main()

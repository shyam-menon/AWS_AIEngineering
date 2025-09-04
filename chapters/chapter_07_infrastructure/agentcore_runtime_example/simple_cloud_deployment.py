"""
Simple AWS Lambda Deployment for Strands Agent
==============================================

This script creates a simple Lambda function to test your agent in the cloud
without complex packaging requirements.
"""

import boto3
import json
import time
import base64


def create_simple_lambda():
    """Create a simple Lambda function for testing"""
    
    # Initialize AWS clients
    lambda_client = boto3.client('lambda')
    iam_client = boto3.client('iam')
    account_id = boto3.client('sts').get_caller_identity()['Account']
    region = boto3.client('lambda')._client_config.region_name or 'us-east-1'
    
    function_name = 'strands-agent-simple'
    role_name = 'StrandsAgentSimpleRole'
    
    print(f"🌍 Deploying to region: {region}")
    print(f"📍 Account ID: {account_id}")
    
    # Create IAM role
    print("🔑 Creating IAM role...")
    
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": "lambda.amazonaws.com"},
                "Action": "sts:AssumeRole"
            }
        ]
    }
    
    try:
        role_response = iam_client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description='Simple role for Strands Agent Lambda'
        )
        role_arn = role_response['Role']['Arn']
        print(f"✅ Created new role: {role_arn}")
        
        # Attach policies
        iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
        )
        iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn='arn:aws:iam::aws:policy/AmazonBedrockFullAccess'
        )
        
        # Wait for role propagation
        print("⏳ Waiting for role to propagate...")
        time.sleep(10)
        
    except iam_client.exceptions.EntityAlreadyExistsException:
        print("ℹ️ Role already exists, using existing role")
        role = iam_client.get_role(RoleName=role_name)
        role_arn = role['Role']['Arn']
    
    # Create simple Lambda function code
    lambda_code = '''
import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Simple Lambda handler that uses Bedrock directly
    """
    try:
        logger.info(f"Received event: {json.dumps(event)}")
        
        # Extract user input
        if 'body' in event:
            if event.get('isBase64Encoded', False):
                import base64
                body = base64.b64decode(event['body']).decode('utf-8')
            else:
                body = event['body']
            
            if isinstance(body, str):
                body = json.loads(body)
        else:
            body = event
        
        user_input = body.get('prompt', 'Hello!')
        logger.info(f"User input: {user_input}")
        
        # Initialize Bedrock client
        bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')
        
        # Prepare message for Nova Lite
        messages = [
            {
                "role": "user",
                "content": [{"text": user_input}]
            }
        ]
        
        # Call Nova Lite model
        response = bedrock_client.converse(
            modelId="us.amazon.nova-lite-v1:0",
            messages=messages,
            inferenceConfig={
                "maxTokens": 1000,
                "temperature": 0.7
            },
            system=[
                {
                    "text": "You are a helpful assistant. You can answer questions and help with various tasks."
                }
            ]
        )
        
        # Extract response
        agent_response = response['output']['message']['content'][0]['text']
        logger.info(f"Agent response: {agent_response}")
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'response': agent_response,
                'user_input': user_input,
                'status': 'success',
                'model': 'nova-lite-v1:0'
            })
        }
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': str(e),
                'status': 'error'
            })
        }
'''
    
    print("🚀 Creating Lambda function...")
    
    # Create a proper zip file
    import zipfile
    import tempfile
    import os
    
    # Create temp directory and zip file
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_path = os.path.join(temp_dir, 'lambda_function.zip')
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.writestr('index.py', lambda_code)
        
        # Read the zip file content
        with open(zip_path, 'rb') as f:
            zip_content = f.read()
    
    print(f"📦 Package size: {len(zip_content)} bytes")
    
    try:
        # Create Lambda function
        response = lambda_client.create_function(
            FunctionName=function_name,
            Runtime='python3.12',
            Role=role_arn,
            Handler='index.lambda_handler',
            Code={'ZipFile': zip_content},
            Description='Simple Strands Agent with Nova Lite',
            Timeout=30,
            MemorySize=512
        )
        
        function_arn = response['FunctionArn']
        print(f"✅ Lambda function created: {function_arn}")
        
    except lambda_client.exceptions.ResourceConflictException:
        print("ℹ️ Function already exists, updating code...")
        lambda_client.update_function_code(
            FunctionName=function_name,
            ZipFile=zip_content
        )
        
        response = lambda_client.get_function(FunctionName=function_name)
        function_arn = response['Configuration']['FunctionArn']
        print(f"✅ Function updated: {function_arn}")
    
    # Create Function URL for easy access
    print("🌐 Creating Function URL...")
    
    try:
        url_response = lambda_client.create_function_url_config(
            FunctionName=function_name,
            AuthType='NONE',
            Cors={
                'AllowCredentials': False,
                'AllowHeaders': ['*'],
                'AllowMethods': ['*'],
                'AllowOrigins': ['*']
            }
        )
        function_url = url_response['FunctionUrl']
        print(f"✅ Function URL created: {function_url}")
        
    except lambda_client.exceptions.ResourceConflictException:
        print("ℹ️ Function URL already exists")
        url_response = lambda_client.get_function_url_config(FunctionName=function_name)
        function_url = url_response['FunctionUrl']
        print(f"✅ Using existing URL: {function_url}")
    
    return function_arn, function_url


def test_lambda_function(function_url):
    """Test the deployed Lambda function"""
    print("🧪 Testing deployed function...")
    
    import requests
    
    test_cases = [
        {"prompt": "Hello! What is 15 + 27?"},
        {"prompt": "Can you explain what AWS Lambda is?"},
        {"prompt": "What is the weather like today?"}
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: {test_case['prompt']}")
        
        try:
            response = requests.post(
                function_url,
                json=test_case,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success!")
                print(f"Response: {result.get('response', 'N/A')[:100]}...")
            else:
                print(f"❌ Failed with status {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Test failed: {e}")


def main():
    """Main deployment function"""
    print("🌟 Simple AWS Lambda Deployment for Nova Lite Agent")
    print("=" * 60)
    
    confirm = input("Deploy a simple Nova Lite agent to AWS Lambda? (y/n): ")
    if confirm.lower() != 'y':
        print("Deployment cancelled.")
        return
    
    try:
        function_arn, function_url = create_simple_lambda()
        
        print("\n⏳ Waiting for function to be ready...")
        time.sleep(5)
        
        test_lambda_function(function_url)
        
        print("\n" + "=" * 60)
        print("🎉 DEPLOYMENT SUCCESSFUL!")
        print("=" * 60)
        print(f"Function URL: {function_url}")
        
        print("\n🎯 How to test your cloud agent:")
        print(f'curl -X POST {function_url} \\')
        print('     -H "Content-Type: application/json" \\')
        print('     -d \'{"prompt": "Hello! How are you?"}\'')
        
        print(f"\n📊 View logs: https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups/log-group/%252Faws%252Flambda%252Fstrands-agent-simple")
        
        print("\n🧹 To clean up:")
        print("aws lambda delete-function --function-name strands-agent-simple")
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")


if __name__ == "__main__":
    main()

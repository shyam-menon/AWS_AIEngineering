"""
AWS Lambda Cloud Deployment for Strands Agent
============================================

This script deploys the Strands agent to AWS Lambda with API Gateway,
providing a cloud-hosted solution similar to AgentCore Runtime.
"""

import boto3
import json
import zipfile
import os
import time
import base64
from pathlib import Path
import tempfile
import shutil


class StrandsLambdaDeployer:
    def __init__(self, region='us-east-1'):
        self.region = region
        self.lambda_client = boto3.client('lambda', region_name=region)
        self.iam_client = boto3.client('iam', region_name=region)
        self.apigateway_client = boto3.client('apigateway', region_name=region)
        self.account_id = boto3.client('sts').get_caller_identity()['Account']
        
        # Configuration
        self.function_name = 'strands-agent-nova-lite'
        self.role_name = 'StrandsAgentLambdaRole'
        self.api_name = 'strands-agent-api'
        
    def create_iam_role(self):
        """Create IAM role for Lambda function"""
        print("🔑 Creating IAM role for Lambda...")
        
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
            # Create role
            role_response = self.iam_client.create_role(
                RoleName=self.role_name,
                AssumeRolePolicyDocument=json.dumps(trust_policy),
                Description='Role for Strands Agent Lambda function'
            )
            
            # Attach policies
            policies = [
                'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole',
                'arn:aws:iam::aws:policy/AmazonBedrockFullAccess'
            ]
            
            for policy in policies:
                self.iam_client.attach_role_policy(
                    RoleName=self.role_name,
                    PolicyArn=policy
                )
            
            role_arn = role_response['Role']['Arn']
            print(f"✅ IAM role created: {role_arn}")
            
            # Wait for role to be ready
            print("⏳ Waiting for IAM role to propagate...")
            time.sleep(10)
            
            return role_arn
            
        except self.iam_client.exceptions.EntityAlreadyExistsException:
            print("ℹ️ IAM role already exists, using existing role")
            role = self.iam_client.get_role(RoleName=self.role_name)
            return role['Role']['Arn']
    
    def create_lambda_package(self):
        """Create deployment package for Lambda"""
        print("📦 Creating Lambda deployment package...")
        
        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            package_dir = Path(temp_dir) / 'package'
            package_dir.mkdir()
            
            # Copy our agent code
            lambda_handler_code = '''
import json
import os
import sys
import logging
from strands import Agent, tool
from strands_tools import calculator
from strands.models import BedrockModel

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create a custom weather tool
@tool
def weather():
    """Get current weather information"""
    # Mock weather data for demonstration
    return "sunny with a temperature of 72°F"

# Initialize the Strands agent with Nova Lite
model = BedrockModel(
    model_id="us.amazon.nova-lite-v1:0",
    region="us-east-1"
)

agent = Agent(
    model=model,
    tools=[calculator, weather],
    system_prompt="You're a helpful assistant. You can do simple math calculations and tell the weather."
)

def lambda_handler(event, context):
    """
    AWS Lambda handler function
    """
    try:
        logger.info(f"Received event: {json.dumps(event)}")
        
        # Extract user input from API Gateway event
        if 'body' in event:
            if event.get('isBase64Encoded', False):
                body = base64.b64decode(event['body']).decode('utf-8')
            else:
                body = event['body']
            
            if isinstance(body, str):
                body = json.loads(body)
        else:
            body = event
        
        user_input = body.get('prompt', 'Hello!')
        logger.info(f"User input: {user_input}")
        
        # Run the agent
        response = agent(user_input)
        agent_response = response.message['content'][0]['text']
        
        logger.info(f"Agent response: {agent_response}")
        
        # Return response in API Gateway format
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'response': agent_response,
                'user_input': user_input,
                'status': 'success'
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
            
            # Write lambda handler
            with open(package_dir / 'lambda_function.py', 'w') as f:
                f.write(lambda_handler_code)
            
            # Copy requirements and install dependencies
            print("📚 Installing dependencies...")
            
            # Create requirements.txt for Lambda
            lambda_requirements = '''
strands-agents[all]
strands-tools
boto3>=1.34.0
'''
            with open(package_dir / 'requirements.txt', 'w') as f:
                f.write(lambda_requirements)
            
            # Install dependencies
            os.system(f'pip install -r {package_dir}/requirements.txt -t {package_dir}')
            
            # Create zip file
            zip_path = Path(temp_dir) / 'deployment_package.zip'
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in package_dir.rglob('*'):
                    if file_path.is_file():
                        arcname = file_path.relative_to(package_dir)
                        zipf.write(file_path, arcname)
            
            # Read zip content
            with open(zip_path, 'rb') as f:
                zip_content = f.read()
            
            print(f"✅ Package created, size: {len(zip_content) / 1024 / 1024:.2f} MB")
            return zip_content
    
    def deploy_lambda_function(self, role_arn, zip_content):
        """Deploy Lambda function"""
        print("🚀 Deploying Lambda function...")
        
        try:
            # Create Lambda function
            response = self.lambda_client.create_function(
                FunctionName=self.function_name,
                Runtime='python3.12',
                Role=role_arn,
                Handler='lambda_function.lambda_handler',
                Code={'ZipFile': zip_content},
                Description='Strands Agent with Nova Lite model',
                Timeout=30,
                MemorySize=512,
                Environment={
                    'Variables': {
                        'AWS_DEFAULT_REGION': self.region
                    }
                }
            )
            
            function_arn = response['FunctionArn']
            print(f"✅ Lambda function created: {function_arn}")
            return function_arn
            
        except self.lambda_client.exceptions.ResourceConflictException:
            print("ℹ️ Lambda function already exists, updating code...")
            
            # Update existing function
            self.lambda_client.update_function_code(
                FunctionName=self.function_name,
                ZipFile=zip_content
            )
            
            # Get function ARN
            response = self.lambda_client.get_function(FunctionName=self.function_name)
            function_arn = response['Configuration']['FunctionArn']
            print(f"✅ Lambda function updated: {function_arn}")
            return function_arn
    
    def create_api_gateway(self, function_arn):
        """Create API Gateway for the Lambda function"""
        print("🌐 Creating API Gateway...")
        
        try:
            # Create REST API
            api_response = self.apigateway_client.create_rest_api(
                name=self.api_name,
                description='API for Strands Agent',
                endpointConfiguration={'types': ['REGIONAL']}
            )
            api_id = api_response['id']
            
            # Get root resource
            resources = self.apigateway_client.get_resources(restApiId=api_id)
            root_resource_id = None
            for resource in resources['items']:
                if resource['path'] == '/':
                    root_resource_id = resource['id']
                    break
            
            # Create resource for agent
            resource_response = self.apigateway_client.create_resource(
                restApiId=api_id,
                parentId=root_resource_id,
                pathPart='agent'
            )
            resource_id = resource_response['id']
            
            # Create POST method
            self.apigateway_client.put_method(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod='POST',
                authorizationType='NONE'
            )
            
            # Set up integration
            lambda_uri = f"arn:aws:apigateway:{self.region}:lambda:path/2015-03-31/functions/{function_arn}/invocations"
            
            self.apigateway_client.put_integration(
                restApiId=api_id,
                resourceId=resource_id,
                httpMethod='POST',
                type='AWS_PROXY',
                integrationHttpMethod='POST',
                uri=lambda_uri
            )
            
            # Deploy API
            deployment = self.apigateway_client.create_deployment(
                restApiId=api_id,
                stageName='prod'
            )
            
            # Add Lambda permission for API Gateway
            self.lambda_client.add_permission(
                FunctionName=self.function_name,
                StatementId='api-gateway-invoke',
                Action='lambda:InvokeFunction',
                Principal='apigateway.amazonaws.com',
                SourceArn=f"arn:aws:execute-api:{self.region}:{self.account_id}:{api_id}/*/*"
            )
            
            api_url = f"https://{api_id}.execute-api.{self.region}.amazonaws.com/prod/agent"
            print(f"✅ API Gateway created: {api_url}")
            
            return api_url, api_id
            
        except Exception as e:
            print(f"⚠️ API Gateway creation failed: {e}")
            # Return Lambda function URL as fallback
            try:
                url_response = self.lambda_client.create_function_url_config(
                    FunctionName=self.function_name,
                    AuthType='NONE',
                    Cors={
                        'AllowCredentials': False,
                        'AllowHeaders': ['*'],
                        'AllowMethods': ['*'],
                        'AllowOrigins': ['*']
                    }
                )
                function_url = url_response['FunctionUrl']
                print(f"✅ Lambda Function URL created: {function_url}")
                return function_url, None
            except Exception as url_error:
                print(f"❌ Failed to create function URL: {url_error}")
                return None, None
    
    def test_deployment(self, api_url):
        """Test the deployed agent"""
        print("🧪 Testing deployed agent...")
        
        import requests
        
        test_payload = {
            'prompt': 'Hello! What is 15 + 27? Also, what is the weather like?'
        }
        
        try:
            response = requests.post(
                api_url,
                json=test_payload,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Test successful!")
                print(f"User Input: {result.get('user_input', 'N/A')}")
                print(f"Agent Response: {result.get('response', 'N/A')}")
                return True
            else:
                print(f"❌ Test failed with status {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Test failed: {e}")
            return False
    
    def deploy(self):
        """Main deployment method"""
        print("🚀 Starting AWS Lambda deployment for Strands Agent")
        print("=" * 60)
        
        try:
            # Step 1: Create IAM role
            role_arn = self.create_iam_role()
            
            # Step 2: Create deployment package
            zip_content = self.create_lambda_package()
            
            # Step 3: Deploy Lambda function
            function_arn = self.deploy_lambda_function(role_arn, zip_content)
            
            # Step 4: Create API Gateway
            api_url, api_id = self.create_api_gateway(function_arn)
            
            if api_url:
                # Step 5: Test deployment
                print("\n⏳ Waiting for deployment to be ready...")
                time.sleep(5)
                
                success = self.test_deployment(api_url)
                
                print("\n" + "=" * 60)
                print("🎉 DEPLOYMENT COMPLETE!")
                print("=" * 60)
                print(f"Function Name: {self.function_name}")
                print(f"API Endpoint: {api_url}")
                print(f"Region: {self.region}")
                
                if success:
                    print("\n✅ Agent is working correctly in the cloud!")
                else:
                    print("\n⚠️ Deployment completed but test failed. Check CloudWatch logs.")
                
                print(f"\n📊 Monitor logs: https://console.aws.amazon.com/cloudwatch/home?region={self.region}#logsV2:log-groups/log-group/%252Faws%252Flambda%252F{self.function_name}")
                
                return {
                    'status': 'success',
                    'function_arn': function_arn,
                    'api_url': api_url,
                    'api_id': api_id
                }
            else:
                print("❌ Failed to create API endpoint")
                return {'status': 'failed', 'error': 'API creation failed'}
                
        except Exception as e:
            print(f"❌ Deployment failed: {e}")
            return {'status': 'failed', 'error': str(e)}


def main():
    """Main function"""
    print("🌟 Strands Agent AWS Lambda Deployment")
    print("This will deploy your Strands agent to AWS Lambda with API Gateway")
    print()
    
    # Confirm deployment
    confirm = input("Do you want to deploy to AWS Lambda? (y/n): ")
    if confirm.lower() != 'y':
        print("Deployment cancelled.")
        return
    
    # Deploy
    deployer = StrandsLambdaDeployer()
    result = deployer.deploy()
    
    if result['status'] == 'success':
        print("\n🎯 How to use your cloud agent:")
        print(f"curl -X POST {result['api_url']} \\")
        print('     -H "Content-Type: application/json" \\')
        print('     -d \'{"prompt": "What is 10 + 15? Also what is the weather?"}\'')
        
        print("\n🧹 To clean up later:")
        print(f"aws lambda delete-function --function-name {deployer.function_name}")
        if result.get('api_id'):
            print(f"aws apigateway delete-rest-api --rest-api-id {result['api_id']}")


if __name__ == "__main__":
    main()

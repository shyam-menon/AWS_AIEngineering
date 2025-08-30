#!/usr/bin/env python3
"""
Simple AWS Bedrock LLM Example

A simple script demonstrating how to invoke Amazon Nova Lite model in AWS Bedrock.
This is a minimal example for quick testing with Nova Lite.
"""

import boto3
import json
from botocore.exceptions import ClientError, NoCredentialsError


def invoke_nova_lite(prompt, region='us-east-1'):
    """
    Simple function to invoke Amazon Nova Lite model.
    
    Args:
        prompt (str): The question or prompt to send to Nova Lite
        region (str): AWS region (default: us-east-1)
        
    Returns:
        str: Nova Lite's response
    """
    try:
        # Create Bedrock Runtime client
        bedrock_runtime = boto3.client('bedrock-runtime', region_name=region)
        
        # Model ID for Amazon Nova Lite (accessible model)
        model_id = "amazon.nova-lite-v1:0"
        
        # Prepare the request body for Nova Lite
        body = {
            "schemaVersion": "messages-v1",
            "messages": [
                {
                    "role": "user",
                    "content": [{"text": prompt}]
                }
            ],
            "inferenceConfig": {
                "maxTokens": 1000,
                "temperature": 0.7,
                "topP": 0.9
            }
        }
        
        # Invoke the model
        response = bedrock_runtime.invoke_model(
            modelId=model_id,
            body=json.dumps(body),
            contentType='application/json'
        )
        
        # Parse the response for Nova Lite
        response_body = json.loads(response['body'].read())
        return response_body['output']['message']['content'][0]['text']
        
    except NoCredentialsError:
        return "Error: AWS credentials not found. Please configure your credentials."
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'AccessDeniedException':
            return "Error: Access denied. Make sure Amazon Nova Lite is enabled in your Bedrock console."
        else:
            return f"AWS Error: {e}"
    except Exception as e:
        return f"Error: {e}"


def main():
    """Main function with example usage."""
    print("Simple AWS Bedrock Amazon Nova Lite Example")
    print("=" * 45)
    
    # Example prompts
    examples = [
        "What is the capital of France?",
        "Explain quantum computing in simple terms.",
        "Write a short poem about coding.",
        "What are the benefits of cloud computing?"
    ]
    
    print("\nTesting with example prompts...")
    
    for i, prompt in enumerate(examples, 1):
        print(f"\n{i}. Prompt: {prompt}")
        print("-" * 30)
        
        response = invoke_nova_lite(prompt)
        print(f"Response: {response}")
        
        if i < len(examples):
            input("\nPress Enter to continue to next example...")
    
    print("=" * 45)
    print("Interactive mode - Ask Nova Lite anything!")
    print("Type 'quit' to exit")
    
    while True:
        try:
            user_prompt = input("\nYour question: ").strip()
            
            if user_prompt.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if not user_prompt:
                continue
                
            print("\nNova Lite is thinking...")
            response = invoke_nova_lite(user_prompt)
            print(f"\nNova Lite: {response}")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break


if __name__ == "__main__":
    main()

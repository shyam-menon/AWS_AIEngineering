#!/usr/bin/env python3
"""
Simple AWS Bedrock LLM Example

A simple script demonstrating how to invoke Claude 3 Haiku model in AWS Bedrock.
This is a minimal example for quick testing.
"""

import boto3
import json
from botocore.exceptions import ClientError, NoCredentialsError


def invoke_claude_simple(prompt, region='us-east-1'):
    """
    Simple function to invoke Claude 3 Haiku model.
    
    Args:
        prompt (str): The question or prompt to send to Claude
        region (str): AWS region (default: us-east-1)
        
    Returns:
        str: Claude's response
    """
    try:
        # Create Bedrock Runtime client
        bedrock_runtime = boto3.client('bedrock-runtime', region_name=region)
        
        # Model ID for Claude Opus 4.1 (accessible model)
        model_id = "anthropic.claude-opus-4-1-20250805-v1:0"
        
        # Prepare the request body
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
        
        # Invoke the model
        response = bedrock_runtime.invoke_model(
            modelId=model_id,
            body=json.dumps(body),
            contentType='application/json'
        )
        
        # Parse the response
        response_body = json.loads(response['body'].read())
        return response_body['content'][0]['text']
        
    except NoCredentialsError:
        return "Error: AWS credentials not found. Please configure your credentials."
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'AccessDeniedException':
            return "Error: Access denied. Make sure Claude 3 Haiku is enabled in your Bedrock console."
        else:
            return f"AWS Error: {e}"
    except Exception as e:
        return f"Error: {e}"


def main():
    """Main function with example usage."""
    print("Simple AWS Bedrock Claude 3 Haiku Example")
    print("=" * 40)
    
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
        
        response = invoke_claude_simple(prompt)
        print(f"Response: {response}")
        
        if i < len(examples):
            input("\nPress Enter to continue to next example...")
    
    print("\n" + "=" * 40)
    print("Interactive mode - Ask Claude anything!")
    print("Type 'quit' to exit")
    
    while True:
        try:
            user_prompt = input("\nYour question: ").strip()
            
            if user_prompt.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if not user_prompt:
                continue
                
            print("\nClaude is thinking...")
            response = invoke_claude_simple(user_prompt)
            print(f"\nClaude: {response}")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break


if __name__ == "__main__":
    main()

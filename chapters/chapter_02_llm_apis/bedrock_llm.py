#!/usr/bin/env python3
"""
AWS Bedrock LLM Invoker

This script uses Boto3 to invoke Large Language Models (LLMs) available in AWS Bedrock.
It supports multiple models including Claude, Titan, Llama, and others.

Prerequisites:
- AWS credentials configured with Bedrock access
- boto3 library installed
- Bedrock models enabled in your AWS account
"""

import boto3
import json
import sys
import argparse
from typing import Dict, Any, Optional
from botocore.exceptions import ClientError, NoCredentialsError


class BedrockLLMClient:
    """Client for invoking AWS Bedrock LLM models."""
    
    def __init__(self, region='us-east-1'):
        """
        Initialize the Bedrock client.
        
        Args:
            region (str): AWS region where Bedrock is available
        """
        self.region = region
        try:
            self.bedrock_runtime = boto3.client('bedrock-runtime', region_name=region)
            self.bedrock = boto3.client('bedrock', region_name=region)
        except NoCredentialsError:
            print("Error: AWS credentials not found. Please configure your credentials.")
            sys.exit(1)
        except Exception as e:
            print(f"Error initializing Bedrock client: {e}")
            sys.exit(1)
    
    def list_available_models(self):
        """List all available foundation models in Bedrock."""
        try:
            response = self.bedrock.list_foundation_models()
            return response['modelSummaries']
        except ClientError as e:
            print(f"Error listing models: {e}")
            return []
    
    def invoke_claude_3_sonnet(self, prompt: str, max_tokens: int = 1000) -> str:
        """
        Invoke Claude 3.5 Sonnet v2 model.
        
        Args:
            prompt (str): The input prompt
            max_tokens (int): Maximum tokens to generate
            
        Returns:
            str: Generated response
        """
        model_id = "anthropic.claude-3-5-sonnet-20241022-v2:0"
        
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        return self._invoke_model(model_id, body)
    
    def invoke_claude_3_haiku(self, prompt: str, max_tokens: int = 1000) -> str:
        """
        Invoke Claude 3.5 Haiku model (faster and cheaper).
        
        Args:
            prompt (str): The input prompt
            max_tokens (int): Maximum tokens to generate
            
        Returns:
            str: Generated response
        """
        model_id = "anthropic.claude-3-5-haiku-20241022-v1:0"
        
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        return self._invoke_model(model_id, body)
    
    def invoke_nova_lite(self, prompt: str, max_tokens: int = 1000) -> str:
        """
        Invoke Amazon Nova Lite model (fast and cost-effective).
        
        Args:
            prompt (str): The input prompt
            max_tokens (int): Maximum tokens to generate
            
        Returns:
            str: Generated response
        """
        model_id = "amazon.nova-lite-v1:0"
        
        body = {
            "schemaVersion": "messages-v1",
            "messages": [
                {
                    "role": "user",
                    "content": [{"text": prompt}]
                }
            ],
            "inferenceConfig": {
                "maxTokens": max_tokens,
                "temperature": 0.7,
                "topP": 0.9
            }
        }
        
        return self._invoke_model(model_id, body)
    
    def invoke_titan_text(self, prompt: str, max_tokens: int = 1000) -> str:
        """
        Invoke Amazon Titan Text model.
        
        Args:
            prompt (str): The input prompt
            max_tokens (int): Maximum tokens to generate
            
        Returns:
            str: Generated response
        """
        model_id = "amazon.titan-text-express-v1"
        
        body = {
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": max_tokens,
                "temperature": 0.7,
                "topP": 0.9
            }
        }
        
        return self._invoke_model(model_id, body)
    
    def invoke_llama2_chat(self, prompt: str, max_tokens: int = 1000) -> str:
        """
        Invoke Meta Llama 2 Chat model.
        
        Args:
            prompt (str): The input prompt
            max_tokens (int): Maximum tokens to generate
            
        Returns:
            str: Generated response
        """
        model_id = "meta.llama2-13b-chat-v1"
        
        body = {
            "prompt": f"[INST] {prompt} [/INST]",
            "max_gen_len": max_tokens,
            "temperature": 0.7,
            "top_p": 0.9
        }
        
        return self._invoke_model(model_id, body)
    
    def invoke_mistral_7b(self, prompt: str, max_tokens: int = 1000) -> str:
        """
        Invoke Mistral 7B Instruct model.
        
        Args:
            prompt (str): The input prompt
            max_tokens (int): Maximum tokens to generate
            
        Returns:
            str: Generated response
        """
        model_id = "mistral.mistral-7b-instruct-v0:2"
        
        body = {
            "prompt": f"<s>[INST] {prompt} [/INST]",
            "max_tokens": max_tokens,
            "temperature": 0.7,
            "top_p": 0.9
        }
        
        return self._invoke_model(model_id, body)
    
    def _invoke_model(self, model_id: str, body: Dict[str, Any]) -> str:
        """
        Internal method to invoke a Bedrock model.
        
        Args:
            model_id (str): The model ID to invoke
            body (Dict): The request body
            
        Returns:
            str: Model response
        """
        try:
            response = self.bedrock_runtime.invoke_model(
                modelId=model_id,
                body=json.dumps(body),
                contentType='application/json'
            )
            
            response_body = json.loads(response['body'].read())
            
            # Parse response based on model type
            if "anthropic.claude" in model_id:
                return response_body['content'][0]['text']
            elif "amazon.nova-lite" in model_id:
                return response_body['output']['message']['content'][0]['text']
            elif "amazon.titan" in model_id:
                return response_body['results'][0]['outputText']
            elif "meta.llama2" in model_id:
                return response_body['generation']
            elif "mistral" in model_id:
                return response_body['outputs'][0]['text']
            else:
                return str(response_body)
                
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'AccessDeniedException':
                return f"Error: Access denied. Make sure the model '{model_id}' is enabled in your Bedrock console."
            elif error_code == 'ResourceNotFoundException':
                return f"Error: Model '{model_id}' not found or not available in region '{self.region}'."
            else:
                return f"Error invoking model: {e}"
        except Exception as e:
            return f"Unexpected error: {e}"


def main():
    """Main function to run the Bedrock LLM application."""
    parser = argparse.ArgumentParser(description='AWS Bedrock LLM Invoker')
    parser.add_argument('--model', '-m', 
                       choices=['nova-lite', 'claude-sonnet', 'claude-haiku', 'titan', 'llama2', 'mistral'],
                       default='nova-lite',
                       help='LLM model to use (default: nova-lite)')
    parser.add_argument('--prompt', '-p', 
                       type=str,
                       help='Prompt to send to the model')
    parser.add_argument('--max-tokens', '-t',
                       type=int,
                       default=1000,
                       help='Maximum tokens to generate (default: 1000)')
    parser.add_argument('--region', '-r',
                       type=str,
                       default='us-east-1',
                       help='AWS region (default: us-east-1)')
    parser.add_argument('--list-models', '-l',
                       action='store_true',
                       help='List available foundation models')
    parser.add_argument('--interactive', '-i',
                       action='store_true',
                       help='Interactive mode')
    
    args = parser.parse_args()
    
    print("AWS Bedrock LLM Invoker")
    print("=" * 30)
    
    # Initialize Bedrock client
    client = BedrockLLMClient(region=args.region)
    
    # List models if requested
    if args.list_models:
        print(f"\nAvailable Foundation Models in {args.region}:")
        print("-" * 50)
        models = client.list_available_models()
        for model in models:
            print(f"Model ID: {model['modelId']}")
            print(f"Model Name: {model['modelName']}")
            print(f"Provider: {model['providerName']}")
            print(f"Input Modalities: {', '.join(model['inputModalities'])}")
            print(f"Output Modalities: {', '.join(model['outputModalities'])}")
            print("-" * 50)
        return
    
    # Interactive mode
    if args.interactive:
        print(f"\nInteractive mode with model: {args.model}")
        print("Type 'quit' or 'exit' to stop, 'help' for commands")
        print("-" * 50)
        
        while True:
            try:
                prompt = input("\nYour prompt: ").strip()
                
                if prompt.lower() in ['quit', 'exit']:
                    print("Goodbye!")
                    break
                elif prompt.lower() == 'help':
                    print("\nAvailable commands:")
                    print("- Type your prompt to get a response")
                    print("- 'quit' or 'exit' to stop")
                    print("- 'help' to show this message")
                    continue
                elif not prompt:
                    continue
                
                print(f"\nInvoking {args.model}...")
                response = invoke_model(client, args.model, prompt, args.max_tokens)
                print(f"\nResponse:\n{response}")
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    # Single prompt mode
    elif args.prompt:
        print(f"\nUsing model: {args.model}")
        print(f"Region: {args.region}")
        print(f"Max tokens: {args.max_tokens}")
        print(f"Prompt: {args.prompt}")
        print("-" * 50)
        
        response = invoke_model(client, args.model, args.prompt, args.max_tokens)
        print(f"\nResponse:\n{response}")
    
    else:
        print("\nNo prompt provided. Use --prompt or --interactive mode.")
        print("For help: python bedrock_llm.py --help")


def invoke_model(client: BedrockLLMClient, model: str, prompt: str, max_tokens: int) -> str:
    """
    Invoke the specified model with the given prompt.
    
    Args:
        client: BedrockLLMClient instance
        model: Model name
        prompt: Input prompt
        max_tokens: Maximum tokens to generate
        
    Returns:
        str: Model response
    """
    model_functions = {
        'nova-lite': client.invoke_nova_lite,
        'claude-sonnet': client.invoke_claude_3_sonnet,
        'claude-haiku': client.invoke_claude_3_haiku,
        'titan': client.invoke_titan_text,
        'llama2': client.invoke_llama2_chat,
        'mistral': client.invoke_mistral_7b
    }
    
    if model in model_functions:
        return model_functions[model](prompt, max_tokens)
    else:
        return f"Error: Unknown model '{model}'"


if __name__ == "__main__":
    main()

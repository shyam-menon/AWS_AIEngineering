#!/usr/bin/env python3
"""
Bedrock with Token Tracking Example

This example shows how to integrate the token tracker with your Bedrock AI calls
to monitor usage and costs in real-time.

Author: AWS AI Engineering Course
Date: August 2025
"""

import json
import boto3
from typing import Dict, Any
from token_tracker import TokenTracker


class BedrockWithTracking:
    """Bedrock client with built-in token tracking."""
    
    def __init__(self, region_name: str = 'us-east-1', session_file: str = None):
        """Initialize Bedrock client with token tracking."""
        self.bedrock_runtime = boto3.client('bedrock-runtime', region_name=region_name)
        self.tracker = TokenTracker(session_file)
        
    def invoke_with_tracking(self, model_id: str, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        Invoke Bedrock model and track token usage.
        
        Args:
            model_id (str): The model to invoke
            prompt (str): The input prompt
            **kwargs: Additional parameters for the model
            
        Returns:
            Dict containing response and tracking info
        """
        # Prepare request body based on model
        if 'nova' in model_id.lower():
            request_body = {
                "schemaVersion": "messages-v1",
                "messages": [
                    {
                        "role": "user", 
                        "content": [{"text": prompt}]
                    }
                ],
                "inferenceConfig": {
                    "maxTokens": kwargs.get('max_tokens', 1000),
                    "temperature": kwargs.get('temperature', 0.7),
                    "topP": kwargs.get('top_p', 0.9)
                }
            }
        else:
            # For Claude models
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": kwargs.get('max_tokens', 1000),
                "temperature": kwargs.get('temperature', 0.7)
            }
        
        try:
            # Make the API call
            response = self.bedrock_runtime.invoke_model(
                modelId=model_id,
                body=json.dumps(request_body),
                contentType='application/json'
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            
            # Extract content and usage info
            if 'nova' in model_id.lower():
                content = response_body['output']['message']['content'][0]['text']
                usage = response_body.get('usage', {})
                input_tokens = usage.get('inputTokens', 0)
                output_tokens = usage.get('outputTokens', 0)
            else:
                # For Claude models
                content = response_body['content'][0]['text']
                usage = response_body.get('usage', {})
                input_tokens = usage.get('input_tokens', 0)
                output_tokens = usage.get('output_tokens', 0)
            
            # Track the request
            tracking_info = self.tracker.track_request(
                model_id=model_id,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                prompt=prompt,
                response=content
            )
            
            return {
                'content': content,
                'usage': {
                    'input_tokens': input_tokens,
                    'output_tokens': output_tokens,
                    'total_tokens': input_tokens + output_tokens
                },
                'tracking': tracking_info,
                'raw_response': response_body
            }
            
        except Exception as e:
            print(f"❌ Error invoking model: {e}")
            return {
                'error': str(e),
                'content': None,
                'usage': None,
                'tracking': None
            }
    
    def get_session_summary(self) -> Dict:
        """Get current session tracking summary."""
        return self.tracker.get_session_summary()
    
    def print_summary(self) -> None:
        """Print current session summary."""
        self.tracker.print_session_summary()
    
    def print_recent(self, count: int = 3) -> None:
        """Print recent requests."""
        self.tracker.print_recent_requests(count)


def main():
    """Demonstrate Bedrock with token tracking."""
    print("🚀 Bedrock with Token Tracking Demo")
    print("=" * 50)
    
    # Initialize client with tracking
    client = BedrockWithTracking(session_file="bedrock_session.json")
    
    # Test prompts
    test_prompts = [
        "What is AWS Bedrock?",
        "Explain the benefits of serverless computing.",
        "Write a short Python function to calculate fibonacci numbers."
    ]
    
    model_id = "amazon.nova-lite-v1:0"
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n🔄 Request {i}: {prompt}")
        
        result = client.invoke_with_tracking(
            model_id=model_id,
            prompt=prompt,
            max_tokens=500,
            temperature=0.7
        )
        
        if result.get('error'):
            print(f"❌ Error: {result['error']}")
            continue
        
        # Display results
        print(f"✅ Response: {result['content'][:100]}...")
        print(f"📊 Tokens: {result['usage']['input_tokens']}→{result['usage']['output_tokens']}")
        print(f"💰 Cost: ${result['tracking']['total_cost']:.4f}")
    
    # Show session summary
    print("\n" + "=" * 50)
    client.print_summary()
    client.print_recent()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
AWS Bedrock JSON Output Examples

This module demonstrates how to get structured JSON output from AWS Bedrock models.
Includes examples for Nova Lite (available) and other models (for reference).
"""

import boto3
import json
import argparse
from typing import Dict, Any, Optional


class BedrockJSONExtractor:
    """
    A class for extracting structured JSON data using AWS Bedrock models.
    
    Supports multiple models and provides robust JSON parsing.
    """
    
    def __init__(self, region: str = 'us-east-1'):
        """Initialize the Bedrock client."""
        self.region = region
        self.bedrock_runtime = boto3.client('bedrock-runtime', region_name=region)
    
    def extract_with_nova_lite(self, prompt: str, max_tokens: int = 500) -> Dict[str, Any]:
        """
        Extract JSON data using Amazon Nova Lite model.
        
        Args:
            prompt: The extraction prompt
            max_tokens: Maximum tokens to generate
            
        Returns:
            Dictionary containing the extracted data
        """
        try:
            # Format prompt for JSON extraction
            json_prompt = f"""
{prompt}

Please respond with valid JSON only. Do not include any explanatory text before or after the JSON.
"""
            
            request_body = {
                "schemaVersion": "messages-v1",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "text": json_prompt
                            }
                        ]
                    }
                ],
                "inferenceConfig": {
                    "maxTokens": max_tokens,
                    "temperature": 0.1,  # Low temperature for consistent JSON output
                    "topP": 0.9
                }
            }
            
            response = self.bedrock_runtime.invoke_model(
                modelId="us.amazon.nova-lite-v1:0",
                body=json.dumps(request_body),
                contentType='application/json',
                accept='application/json'
            )
            
            response_body = json.loads(response['body'].read())
            response_text = response_body['output']['message']['content'][0]['text']
            
            # Clean and parse JSON response
            json_data = self._parse_json_response(response_text)
            
            return {
                "success": True,
                "model": "nova-lite",
                "data": json_data,
                "raw_response": response_text
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model": "nova-lite"
            }
    
    def extract_with_claude(self, prompt: str, max_tokens: int = 300) -> Dict[str, Any]:
        """
        Extract JSON data using Claude model (for reference - requires access).
        
        This is the updated version of the code pattern you provided.
        """
        try:
            # Updated Claude API format
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "temperature": 0.1,
                "messages": [
                    {
                        "role": "user",
                        "content": f"{prompt}\n\nPlease respond with valid JSON only."
                    }
                ]
            }
            
            response = self.bedrock_runtime.invoke_model(
                modelId="anthropic.claude-3-sonnet-20240229-v1:0",  # Updated model ID
                body=json.dumps(request_body),
                contentType='application/json',
                accept='application/json'
            )
            
            response_body = json.loads(response['body'].read())
            response_text = response_body['content'][0]['text']
            
            json_data = self._parse_json_response(response_text)
            
            return {
                "success": True,
                "model": "claude-3-sonnet",
                "data": json_data,
                "raw_response": response_text
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model": "claude-3-sonnet"
            }
    
    def extract_with_legacy_claude(self, prompt: str, max_tokens: int = 300) -> Dict[str, Any]:
        """
        Extract JSON data using legacy Claude format (your original code pattern).
        
        Note: This format is deprecated but shown for reference.
        """
        try:
            # Legacy format (deprecated)
            body = json.dumps({
                "prompt": f"\n\nHuman: {prompt}\n\nPlease respond with valid JSON only.\n\nAssistant:",
                "max_tokens_to_sample": max_tokens,
                "temperature": 0.1,
                "top_p": 0.9,
            })
            
            response = self.bedrock_runtime.invoke_model(
                body=body,
                modelId="anthropic.claude-v2",  # Legacy model
                accept="application/json",
                contentType="application/json",
            )
            
            response_body = json.loads(response.get("body").read())
            response_text = response_body["completion"]
            
            json_data = self._parse_json_response(response_text)
            
            return {
                "success": True,
                "model": "claude-v2-legacy",
                "data": json_data,
                "raw_response": response_text
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model": "claude-v2-legacy"
            }
    
    def _parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse JSON from model response with robust error handling.
        
        Args:
            response_text: Raw text response from the model
            
        Returns:
            Parsed JSON data
        """
        try:
            # Clean the response text
            cleaned_text = response_text.strip()
            
            # Remove markdown code blocks if present
            if cleaned_text.startswith('```json'):
                cleaned_text = cleaned_text[7:]
            if cleaned_text.startswith('```'):
                cleaned_text = cleaned_text[3:]
            if cleaned_text.endswith('```'):
                cleaned_text = cleaned_text[:-3]
            
            cleaned_text = cleaned_text.strip()
            
            # Find JSON content between braces
            start_idx = cleaned_text.find('{')
            end_idx = cleaned_text.rfind('}')
            
            if start_idx != -1 and end_idx != -1:
                json_str = cleaned_text[start_idx:end_idx + 1]
                return json.loads(json_str)
            else:
                # Try parsing the entire cleaned text
                return json.loads(cleaned_text)
                
        except json.JSONDecodeError as e:
            return {
                "error": "Failed to parse JSON",
                "raw_text": response_text,
                "json_error": str(e)
            }


def example_user_data_extraction():
    """Example: Extract user information from text."""
    extractor = BedrockJSONExtractor()
    
    prompt = """Please extract the user's name and email address from the following text and return it in a JSON format with the keys 'name' and 'email'.

Text: "My name is John Doe and my email is john.doe@example.com."
"""
    
    print("🔍 Extracting User Data")
    print("=" * 25)
    
    # Try with Nova Lite (available model)
    result = extractor.extract_with_nova_lite(prompt)
    
    if result["success"]:
        print(f"✅ Success with {result['model']}")
        print(f"📄 Raw Response: {result['raw_response']}")
        print(f"📊 Parsed Data: {json.dumps(result['data'], indent=2)}")
    else:
        print(f"❌ Error with {result['model']}: {result['error']}")
    
    return result


def example_product_extraction():
    """Example: Extract product information from a description."""
    extractor = BedrockJSONExtractor()
    
    prompt = """Extract product information from this description and return JSON with keys: 'name', 'price', 'category', 'features' (array).

Description: "The UltraBook Pro 15 is a premium laptop priced at $1,299. It's in the electronics category and features a 15-inch 4K display, 32GB RAM, 1TB SSD storage, and Intel i7 processor."
"""
    
    print("\n🛍️ Extracting Product Information")
    print("=" * 35)
    
    result = extractor.extract_with_nova_lite(prompt)
    
    if result["success"]:
        print(f"✅ Success with {result['model']}")
        print(f"📊 Product Data:")
        print(json.dumps(result['data'], indent=2))
    else:
        print(f"❌ Error: {result['error']}")
    
    return result


def example_event_extraction():
    """Example: Extract event details from text."""
    extractor = BedrockJSONExtractor()
    
    prompt = """Extract event information and return JSON with keys: 'title', 'date', 'time', 'location', 'description'.

Text: "Join us for the Annual Tech Conference on March 15, 2024, at 9:00 AM. The event will be held at the Grand Convention Center in downtown Seattle. This conference brings together technology leaders to discuss the future of AI and machine learning."
"""
    
    print("\n📅 Extracting Event Information")
    print("=" * 32)
    
    result = extractor.extract_with_nova_lite(prompt, max_tokens=600)
    
    if result["success"]:
        print(f"✅ Success with {result['model']}")
        print(f"📊 Event Data:")
        print(json.dumps(result['data'], indent=2))
    else:
        print(f"❌ Error: {result['error']}")
    
    return result


def interactive_json_extraction():
    """Interactive mode for custom JSON extraction."""
    extractor = BedrockJSONExtractor()
    
    print("\n🎯 Interactive JSON Extraction")
    print("=" * 32)
    print("Enter your text and specify what JSON structure you want to extract.")
    print("Type 'quit' to exit.\n")
    
    while True:
        try:
            text = input("📝 Enter text to analyze: ").strip()
            if text.lower() == 'quit':
                break
            
            if not text:
                continue
            
            structure = input("🗂️ Describe desired JSON structure: ").strip()
            if not structure:
                structure = "relevant information in appropriate JSON format"
            
            prompt = f"""Extract information from this text and return it as JSON. Structure: {structure}

Text: "{text}"
"""
            
            print("\n🔄 Processing...")
            result = extractor.extract_with_nova_lite(prompt)
            
            if result["success"]:
                print(f"✅ Extracted JSON:")
                print(json.dumps(result['data'], indent=2))
            else:
                print(f"❌ Error: {result['error']}")
            
            print("\n" + "-" * 50)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def main():
    """Main function with command-line interface."""
    parser = argparse.ArgumentParser(description="AWS Bedrock JSON Output Examples")
    parser.add_argument(
        '--mode',
        choices=['examples', 'interactive', 'user', 'product', 'event'],
        default='examples',
        help='Mode to run: examples (all), interactive, or specific example'
    )
    parser.add_argument(
        '--region',
        default='us-east-1',
        help='AWS region for Bedrock service'
    )
    
    args = parser.parse_args()
    
    print("🤖 AWS Bedrock JSON Output Examples")
    print("=" * 38)
    print(f"🌍 Region: {args.region}")
    print(f"🎯 Mode: {args.mode}")
    print()
    
    if args.mode == 'examples':
        # Run all examples
        example_user_data_extraction()
        example_product_extraction()
        example_event_extraction()
    elif args.mode == 'interactive':
        interactive_json_extraction()
    elif args.mode == 'user':
        example_user_data_extraction()
    elif args.mode == 'product':
        example_product_extraction()
    elif args.mode == 'event':
        example_event_extraction()


if __name__ == "__main__":
    main()

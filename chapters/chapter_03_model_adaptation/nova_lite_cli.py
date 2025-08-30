#!/usr/bin/env python3
"""
Amazon Nova Lite CLI - Command Line Interface

A comprehensive command-line tool for interacting with Amazon Nova Lite model.
Supports various use cases including content generation, code assistance, and analysis.
"""

import boto3
import json
import argparse
import sys
from datetime import datetime
from botocore.exceptions import ClientError, NoCredentialsError


class NovaLiteCLI:
    """Command-line interface for Amazon Nova Lite."""
    
    def __init__(self, region='us-east-1'):
        """Initialize the Nova Lite CLI."""
        try:
            self.client = boto3.client("bedrock-runtime", region_name=region)
            self.model_id = "us.amazon.nova-lite-v1:0"
            self.region = region
        except NoCredentialsError:
            print("❌ Error: AWS credentials not found.")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)
    
    def generate_text(self, prompt, system_prompt=None, max_tokens=1000, 
                     temperature=0.7, top_p=0.9, top_k=20, stream=False, verbose=False):
        """
        Generate text using Nova Lite.
        
        Args:
            prompt (str): The input prompt
            system_prompt (str): Optional system prompt
            max_tokens (int): Maximum tokens to generate
            temperature (float): Creativity level (0.0-1.0)
            top_p (float): Nucleus sampling parameter
            top_k (int): Top-k sampling parameter
            stream (bool): Whether to stream the response
            verbose (bool): Show detailed information
            
        Returns:
            str: Generated text
        """
        try:
            start_time = datetime.now()
            
            # Prepare request
            system_list = []
            if system_prompt:
                system_list.append({"text": system_prompt})
            
            message_list = [{"role": "user", "content": [{"text": prompt}]}]
            
            inf_params = {
                "maxTokens": max_tokens,
                "temperature": temperature,
                "topP": top_p,
                "topK": top_k
            }
            
            request_body = {
                "schemaVersion": "messages-v1",
                "messages": message_list,
                "inferenceConfig": inf_params,
            }
            
            if system_list:
                request_body["system"] = system_list
            
            if verbose:
                print(f"🔧 Model: {self.model_id}")
                print(f"🔧 Region: {self.region}")
                print(f"🔧 Temperature: {temperature}")
                print(f"🔧 Max tokens: {max_tokens}")
                print(f"🔧 System prompt: {system_prompt or 'None'}")
                print(f"🔧 Streaming: {stream}")
                print("-" * 50)
            
            if stream:
                return self._stream_response(request_body, verbose, start_time)
            else:
                return self._get_response(request_body, verbose, start_time)
                
        except ClientError as e:
            return f"❌ AWS Error: {e}"
        except Exception as e:
            return f"❌ Error: {e}"
    
    def _get_response(self, request_body, verbose, start_time):
        """Get non-streaming response."""
        if verbose:
            print("🤔 Generating response...")
        
        response = self.client.invoke_model(
            modelId=self.model_id,
            body=json.dumps(request_body)
        )
        
        end_time = datetime.now()
        response_body = json.loads(response['body'].read())
        text = response_body['output']['message']['content'][0]['text']
        
        if verbose:
            duration = end_time - start_time
            print(f"⏱️  Generation time: {duration.total_seconds():.2f} seconds")
            print(f"📊 Response length: {len(text)} characters")
            print("-" * 50)
        
        return text
    
    def _stream_response(self, request_body, verbose, start_time):
        """Get streaming response."""
        if verbose:
            print("🤔 Streaming response...")
            print("-" * 50)
        
        response = self.client.invoke_model_with_response_stream(
            modelId=self.model_id,
            body=json.dumps(request_body)
        )
        
        full_response = ""
        chunk_count = 0
        time_to_first_token = None
        
        stream = response.get("body")
        if stream:
            for event in stream:
                chunk = event.get("chunk")
                if chunk:
                    chunk_json = json.loads(chunk.get("bytes").decode())
                    content_block_delta = chunk_json.get("contentBlockDelta")
                    if content_block_delta:
                        if time_to_first_token is None:
                            time_to_first_token = datetime.now() - start_time
                            if verbose:
                                print(f"⚡ Time to first token: {time_to_first_token.total_seconds():.2f}s")
                        
                        chunk_count += 1
                        text = content_block_delta.get("delta").get("text")
                        if text:
                            print(text, end="", flush=True)
                            full_response += text
        
        end_time = datetime.now()
        print()  # New line
        
        if verbose:
            duration = end_time - start_time
            print(f"\n⏱️  Total time: {duration.total_seconds():.2f} seconds")
            print(f"📊 Chunks received: {chunk_count}")
            print(f"📊 Response length: {len(full_response)} characters")
        
        return full_response


def create_presets():
    """Create common use case presets."""
    return {
        "creative": {
            "system": "You are a creative writing assistant. Write engaging, imaginative, and vivid content with rich descriptions and compelling narratives.",
            "temperature": 0.8,
            "description": "Creative writing and storytelling"
        },
        "technical": {
            "system": "You are a technical expert. Provide accurate, detailed, and well-structured explanations. Use clear language and provide examples when helpful.",
            "temperature": 0.3,
            "description": "Technical explanations and documentation"
        },
        "code": {
            "system": "You are a programming expert. Provide clean, well-commented code with explanations. Follow best practices and include error handling when appropriate.",
            "temperature": 0.2,
            "description": "Code generation and programming help"
        },
        "analysis": {
            "system": "You are an analytical expert. Provide thorough, objective analysis with clear reasoning. Break down complex topics into understandable components.",
            "temperature": 0.4,
            "description": "Analysis and research tasks"
        },
        "casual": {
            "system": "You are a helpful, friendly assistant. Respond in a conversational, approachable tone while being informative and accurate.",
            "temperature": 0.6,
            "description": "Casual conversation and general assistance"
        },
        "business": {
            "system": "You are a professional business consultant. Provide clear, actionable advice with a focus on practical implementation and business value.",
            "temperature": 0.5,
            "description": "Business and professional content"
        }
    }


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description='Amazon Nova Lite CLI - Interact with Amazon Nova Lite model',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  python nova_lite_cli.py "Write a poem about coding"
  
  # Use a preset
  python nova_lite_cli.py "Explain quantum computing" --preset technical
  
  # Custom system prompt
  python nova_lite_cli.py "Write a story" --system "You are Shakespeare"
  
  # Streaming with verbose output
  python nova_lite_cli.py "Explain AI" --stream --verbose
  
  # Creative writing with high temperature
  python nova_lite_cli.py "Write a fantasy story" --temperature 0.9 --tokens 1500
  
  # Interactive mode
  python nova_lite_cli.py --interactive
        """
    )
    
    parser.add_argument('prompt', nargs='?', help='The prompt to send to Nova Lite')
    parser.add_argument('--system', '-s', help='System prompt to guide behavior')
    parser.add_argument('--preset', '-p', choices=create_presets().keys(),
                       help='Use a predefined preset')
    parser.add_argument('--tokens', '-t', type=int, default=1000,
                       help='Maximum tokens to generate (default: 1000)')
    parser.add_argument('--temperature', '--temp', type=float, default=0.7,
                       help='Temperature for creativity (0.0-1.0, default: 0.7)')
    parser.add_argument('--top-p', type=float, default=0.9,
                       help='Top-p sampling parameter (default: 0.9)')
    parser.add_argument('--top-k', type=int, default=20,
                       help='Top-k sampling parameter (default: 20)')
    parser.add_argument('--region', '-r', default='us-east-1',
                       help='AWS region (default: us-east-1)')
    parser.add_argument('--stream', action='store_true',
                       help='Stream the response (default: False)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show detailed information')
    parser.add_argument('--interactive', '-i', action='store_true',
                       help='Interactive mode')
    parser.add_argument('--list-presets', action='store_true',
                       help='List available presets')
    
    args = parser.parse_args()
    
    # List presets if requested
    if args.list_presets:
        presets = create_presets()
        print("📋 Available Presets:")
        print("=" * 20)
        for name, config in presets.items():
            print(f"🔸 {name}: {config['description']}")
            print(f"   Temperature: {config['temperature']}")
            print(f"   System: {config['system'][:80]}...")
            print()
        return
    
    # Initialize CLI
    try:
        cli = NovaLiteCLI(region=args.region)
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        return
    
    # Interactive mode
    if args.interactive:
        print("🚀 Nova Lite Interactive Mode")
        print("Type 'help' for commands, 'quit' to exit")
        print("=" * 40)
        
        while True:
            try:
                user_input = input("\n💬 Prompt: ").strip()
                
                if user_input.lower() in ['quit', 'exit']:
                    print("👋 Goodbye!")
                    break
                elif user_input.lower() == 'help':
                    print("\n📋 Commands:")
                    print("  help - Show this help")
                    print("  quit - Exit interactive mode")
                    print("  Just type your prompt and press Enter")
                    continue
                elif not user_input:
                    continue
                
                print(f"\n🤖 Nova Lite:")
                response = cli.generate_text(
                    prompt=user_input,
                    max_tokens=args.tokens,
                    temperature=args.temperature,
                    stream=True,
                    verbose=args.verbose
                )
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
        return
    
    # Check if prompt is provided
    if not args.prompt:
        print("❌ Error: No prompt provided. Use --interactive or provide a prompt.")
        print("Use --help for usage information.")
        return
    
    # Apply preset if specified
    system_prompt = args.system
    temperature = args.temperature
    
    if args.preset:
        presets = create_presets()
        preset = presets[args.preset]
        if not system_prompt:
            system_prompt = preset['system']
        temperature = preset['temperature']
        
        if args.verbose:
            print(f"📋 Using preset: {args.preset}")
    
    # Generate response
    print("🤖 Nova Lite Response:")
    print("=" * 22)
    
    response = cli.generate_text(
        prompt=args.prompt,
        system_prompt=system_prompt,
        max_tokens=args.tokens,
        temperature=temperature,
        top_p=args.top_p,
        top_k=args.top_k,
        stream=args.stream,
        verbose=args.verbose
    )
    
    if not args.stream:
        print(response)


if __name__ == "__main__":
    main()

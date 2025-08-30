#!/usr/bin/env python3
"""
Amazon Nova Lite - Simple Chat Application

This script uses Amazon Nova Lite model in AWS Bedrock for text generation.
Nova Lite is Amazon's fast and cost-effective language model.
"""

import boto3
import json
from datetime import datetime
from botocore.exceptions import ClientError, NoCredentialsError


class NovaLiteClient:
    """Client for Amazon Nova Lite model."""
    
    def __init__(self, region='us-east-1'):
        """Initialize the Nova Lite client."""
        try:
            self.client = boto3.client("bedrock-runtime", region_name=region)
            self.model_id = "us.amazon.nova-lite-v1:0"
            self.region = region
        except NoCredentialsError:
            print("❌ Error: AWS credentials not found. Please configure your credentials.")
            raise
        except Exception as e:
            print(f"❌ Error initializing Nova Lite client: {e}")
            raise
    
    def chat(self, user_message, system_prompt=None, max_tokens=1000, temperature=0.7, stream=False):
        """
        Send a message to Nova Lite and get a response.
        
        Args:
            user_message (str): The user's message
            system_prompt (str): Optional system prompt to guide behavior
            max_tokens (int): Maximum tokens to generate
            temperature (float): Creativity level (0.0-1.0)
            stream (bool): Whether to stream the response
            
        Returns:
            str: The model's response
        """
        try:
            # Prepare system prompt
            system_list = []
            if system_prompt:
                system_list.append({"text": system_prompt})
            
            # Prepare messages
            message_list = [
                {
                    "role": "user", 
                    "content": [{"text": user_message}]
                }
            ]
            
            # Configure inference parameters
            inf_params = {
                "maxTokens": max_tokens,
                "temperature": temperature,
                "topP": 0.9,
                "topK": 20
            }
            
            # Prepare request body
            request_body = {
                "schemaVersion": "messages-v1",
                "messages": message_list,
                "inferenceConfig": inf_params,
            }
            
            if system_list:
                request_body["system"] = system_list
            
            if stream:
                return self._stream_response(request_body)
            else:
                return self._get_response(request_body)
                
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'AccessDeniedException':
                return "❌ Error: Access denied. Make sure Nova Lite is enabled in your Bedrock console."
            else:
                return f"❌ AWS Error: {e}"
        except Exception as e:
            return f"❌ Error: {e}"
    
    def _get_response(self, request_body):
        """Get a non-streaming response."""
        response = self.client.invoke_model(
            modelId=self.model_id,
            body=json.dumps(request_body)
        )
        
        response_body = json.loads(response['body'].read())
        return response_body['output']['message']['content'][0]['text']
    
    def _stream_response(self, request_body):
        """Get a streaming response."""
        print("🤔 Nova Lite is thinking...\n")
        
        response = self.client.invoke_model_with_response_stream(
            modelId=self.model_id,
            body=json.dumps(request_body)
        )
        
        full_response = ""
        stream = response.get("body")
        
        if stream:
            for event in stream:
                chunk = event.get("chunk")
                if chunk:
                    chunk_json = json.loads(chunk.get("bytes").decode())
                    content_block_delta = chunk_json.get("contentBlockDelta")
                    if content_block_delta:
                        text = content_block_delta.get("delta").get("text")
                        if text:
                            print(text, end="", flush=True)
                            full_response += text
        
        print()  # New line after streaming
        return full_response


def interactive_chat():
    """Interactive chat session with Nova Lite."""
    print("🚀 Amazon Nova Lite - Interactive Chat")
    print("=" * 40)
    print("Type 'quit' to exit, 'help' for commands")
    print("=" * 40)
    
    client = NovaLiteClient()
    
    # Chat settings
    system_prompt = None
    temperature = 0.7
    max_tokens = 1000
    stream_mode = True
    
    while True:
        try:
            user_input = input("\n💬 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            elif user_input.lower() == 'help':
                print("\n📋 Available commands:")
                print("  help        - Show this help")
                print("  settings    - Show current settings")
                print("  system      - Set system prompt")
                print("  temp [0-1]  - Set temperature (creativity)")
                print("  tokens [n]  - Set max tokens")
                print("  stream      - Toggle streaming mode")
                print("  clear       - Clear system prompt")
                print("  quit        - Exit chat")
                continue
            
            elif user_input.lower() == 'settings':
                print(f"\n⚙️  Current settings:")
                print(f"   System prompt: {system_prompt or 'None'}")
                print(f"   Temperature: {temperature}")
                print(f"   Max tokens: {max_tokens}")
                print(f"   Streaming: {stream_mode}")
                continue
            
            elif user_input.lower().startswith('system'):
                new_prompt = input("🎭 Enter system prompt: ").strip()
                if new_prompt:
                    system_prompt = new_prompt
                    print(f"✅ System prompt set: {system_prompt}")
                continue
            
            elif user_input.lower().startswith('temp'):
                try:
                    parts = user_input.split()
                    if len(parts) > 1:
                        temperature = float(parts[1])
                        temperature = max(0.0, min(1.0, temperature))
                        print(f"✅ Temperature set to: {temperature}")
                    else:
                        print("❌ Usage: temp 0.7")
                except ValueError:
                    print("❌ Invalid temperature. Use a number between 0 and 1.")
                continue
            
            elif user_input.lower().startswith('tokens'):
                try:
                    parts = user_input.split()
                    if len(parts) > 1:
                        max_tokens = int(parts[1])
                        max_tokens = max(1, min(4000, max_tokens))
                        print(f"✅ Max tokens set to: {max_tokens}")
                    else:
                        print("❌ Usage: tokens 1000")
                except ValueError:
                    print("❌ Invalid token count. Use a positive integer.")
                continue
            
            elif user_input.lower() == 'stream':
                stream_mode = not stream_mode
                print(f"✅ Streaming mode: {'ON' if stream_mode else 'OFF'}")
                continue
            
            elif user_input.lower() == 'clear':
                system_prompt = None
                print("✅ System prompt cleared")
                continue
            
            elif not user_input:
                continue
            
            # Send message to Nova Lite
            print(f"\n🤖 Nova Lite:", end=" " if not stream_mode else "\n")
            
            response = client.chat(
                user_message=user_input,
                system_prompt=system_prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                stream=stream_mode
            )
            
            if not stream_mode:
                print(response)
            
        except KeyboardInterrupt:
            print("\n\n👋 Chat interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


def demo_examples():
    """Run some demonstration examples."""
    print("🎯 Amazon Nova Lite - Demo Examples")
    print("=" * 37)
    
    client = NovaLiteClient()
    
    examples = [
        {
            "title": "Creative Writing",
            "system": "You are a creative writing assistant. Write engaging, vivid content.",
            "prompt": "Write a short story about a robot discovering emotions for the first time.",
            "tokens": 500
        },
        {
            "title": "Technical Explanation", 
            "system": "You are a helpful technical assistant. Explain concepts clearly and concisely.",
            "prompt": "Explain how machine learning works in simple terms that a beginner can understand.",
            "tokens": 300
        },
        {
            "title": "Code Assistant",
            "system": "You are a programming expert. Provide clear, working code examples.",
            "prompt": "Write a Python function that finds the most frequent word in a text file.",
            "tokens": 400
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n📝 Example {i}: {example['title']}")
        print("-" * 30)
        print(f"System: {example['system']}")
        print(f"Prompt: {example['prompt']}")
        print("\n🤖 Nova Lite Response:")
        print("-" * 30)
        
        response = client.chat(
            user_message=example['prompt'],
            system_prompt=example['system'],
            max_tokens=example['tokens'],
            stream=True
        )
        
        if i < len(examples):
            input("\n⏸️  Press Enter to continue to next example...")


def main():
    """Main function."""
    print("Welcome to Amazon Nova Lite Chat Application!")
    print("=" * 45)
    
    try:
        choice = input("\nChoose mode:\n1. Interactive Chat\n2. Demo Examples\n\nEnter choice (1 or 2): ").strip()
        
        if choice == "1":
            interactive_chat()
        elif choice == "2":
            demo_examples()
        else:
            print("Invalid choice. Starting interactive chat...")
            interactive_chat()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure AWS credentials are configured and Nova Lite is enabled.")


if __name__ == "__main__":
    main()

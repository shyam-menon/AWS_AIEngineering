#!/usr/bin/env python3
"""
AWS Bedrock Conversation Examples

This script demonstrates different conversation patterns with AWS Bedrock models,
including multi-turn conversations, system prompts, and different model comparisons.
"""

import boto3
import json
import time
from typing import List, Dict
from botocore.exceptions import ClientError


class BedrockConversation:
    """Class to manage conversations with Bedrock models."""
    
    def __init__(self, region='us-east-1'):
        """Initialize the Bedrock client."""
        self.bedrock_runtime = boto3.client('bedrock-runtime', region_name=region)
        self.conversation_history = []
    
    def add_to_history(self, role: str, content: str):
        """Add a message to conversation history."""
        self.conversation_history.append({"role": role, "content": content})
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
    
    def chat_with_claude(self, user_message: str, system_prompt: str = None) -> str:
        """
        Have a conversation with Claude, maintaining context.
        
        Args:
            user_message (str): User's message
            system_prompt (str): Optional system prompt to set behavior
            
        Returns:
            str: Claude's response
        """
        try:
            # Add user message to history
            self.add_to_history("user", user_message)
            
            # Prepare messages
            messages = self.conversation_history.copy()
            
            # Prepare request body
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": messages
            }
            
            # Add system prompt if provided
            if system_prompt:
                body["system"] = system_prompt
            
            # Invoke Claude
            response = self.bedrock_runtime.invoke_model(
                modelId="anthropic.claude-3-5-haiku-20241022-v1:0",
                body=json.dumps(body),
                contentType='application/json'
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            claude_response = response_body['content'][0]['text']
            
            # Add Claude's response to history
            self.add_to_history("assistant", claude_response)
            
            return claude_response
            
        except Exception as e:
            return f"Error: {e}"
    
    def compare_models(self, prompt: str) -> Dict[str, str]:
        """
        Compare responses from different models for the same prompt.
        
        Args:
            prompt (str): The prompt to send to all models
            
        Returns:
            Dict[str, str]: Dictionary with model names as keys and responses as values
        """
        models = {
            "Claude 3 Haiku": {
                "id": "anthropic.claude-3-haiku-20240307-v1:0",
                "body": {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 500,
                    "messages": [{"role": "user", "content": prompt}]
                }
            },
            "Amazon Titan": {
                "id": "amazon.titan-text-express-v1",
                "body": {
                    "inputText": prompt,
                    "textGenerationConfig": {
                        "maxTokenCount": 500,
                        "temperature": 0.7,
                        "topP": 0.9
                    }
                }
            }
        }
        
        results = {}
        
        for model_name, config in models.items():
            try:
                response = self.bedrock_runtime.invoke_model(
                    modelId=config["id"],
                    body=json.dumps(config["body"]),
                    contentType='application/json'
                )
                
                response_body = json.loads(response['body'].read())
                
                if "anthropic.claude" in config["id"]:
                    results[model_name] = response_body['content'][0]['text']
                elif "amazon.titan" in config["id"]:
                    results[model_name] = response_body['results'][0]['outputText']
                    
            except Exception as e:
                results[model_name] = f"Error: {e}"
        
        return results


def demo_simple_question():
    """Demo: Simple question and answer."""
    print("\n" + "="*50)
    print("DEMO 1: Simple Question & Answer")
    print("="*50)
    
    conv = BedrockConversation()
    
    question = "What are the main benefits of using cloud computing?"
    print(f"Question: {question}")
    print("\nClaude's response:")
    print("-" * 30)
    
    response = conv.chat_with_claude(question)
    print(response)


def demo_system_prompt():
    """Demo: Using system prompts to control behavior."""
    print("\n" + "="*50)
    print("DEMO 2: System Prompt - Acting as a Python Expert")
    print("="*50)
    
    conv = BedrockConversation()
    
    system_prompt = "You are a senior Python developer with 10+ years of experience. Provide practical, production-ready advice with code examples when relevant."
    question = "How should I handle errors in a Python web API?"
    
    print(f"System Prompt: {system_prompt}")
    print(f"\nQuestion: {question}")
    print("\nClaude's response:")
    print("-" * 30)
    
    response = conv.chat_with_claude(question, system_prompt)
    print(response)


def demo_multi_turn_conversation():
    """Demo: Multi-turn conversation with context."""
    print("\n" + "="*50)
    print("DEMO 3: Multi-turn Conversation")
    print("="*50)
    
    conv = BedrockConversation()
    
    # First turn
    print("Turn 1:")
    response1 = conv.chat_with_claude("I'm planning to build a web application. What technologies would you recommend?")
    print(f"Claude: {response1}")
    
    time.sleep(1)  # Brief pause for readability
    
    # Second turn - Claude should remember the context
    print("\nTurn 2:")
    response2 = conv.chat_with_claude("What about for the database? I expect to have about 100,000 users.")
    print(f"Claude: {response2}")
    
    time.sleep(1)
    
    # Third turn
    print("\nTurn 3:")
    response3 = conv.chat_with_claude("And how should I handle user authentication?")
    print(f"Claude: {response3}")


def demo_model_comparison():
    """Demo: Compare responses from different models."""
    print("\n" + "="*50)
    print("DEMO 4: Model Comparison")
    print("="*50)
    
    conv = BedrockConversation()
    
    prompt = "Explain machine learning in exactly 3 sentences."
    print(f"Prompt: {prompt}")
    print("\nResponses from different models:")
    print("-" * 40)
    
    results = conv.compare_models(prompt)
    
    for model_name, response in results.items():
        print(f"\n{model_name}:")
        print(f"{response}")
        print("-" * 40)


def demo_creative_writing():
    """Demo: Creative writing with specific instructions."""
    print("\n" + "="*50)
    print("DEMO 5: Creative Writing")
    print("="*50)
    
    conv = BedrockConversation()
    
    system_prompt = "You are a creative writer who writes engaging, vivid short stories. Use descriptive language and create compelling characters."
    prompt = "Write a short story (150 words) about a programmer who discovers their code can predict the future."
    
    print(f"Creative Writing Prompt: {prompt}")
    print("\nClaude's story:")
    print("-" * 30)
    
    response = conv.chat_with_claude(prompt, system_prompt)
    print(response)


def main():
    """Run all demos."""
    print("AWS Bedrock Conversation Examples")
    print("This will demonstrate various conversation patterns with Bedrock models")
    
    try:
        demo_simple_question()
        input("\nPress Enter to continue to next demo...")
        
        demo_system_prompt()
        input("\nPress Enter to continue to next demo...")
        
        demo_multi_turn_conversation()
        input("\nPress Enter to continue to next demo...")
        
        demo_model_comparison()
        input("\nPress Enter to continue to next demo...")
        
        demo_creative_writing()
        
        print("\n" + "="*50)
        print("All demos completed!")
        print("="*50)
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\nError running demos: {e}")


if __name__ == "__main__":
    main()

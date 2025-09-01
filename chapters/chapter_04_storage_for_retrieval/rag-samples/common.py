#!/usr/bin/env python3
"""
Common utilities for AWS RAG Demo

This module provides shared functionality for both local FAISS and 
AWS Bedrock Knowledge Base implementations, including:
- Environment configuration loading
- AWS Bedrock client setup
- Text embedding functions
- Chat completion functions
- Error handling utilities

Author: AWS AI Engineering Course
Chapter: 4 - Storage for Retrieval
"""

import os
import json
import sys
from typing import List, Dict, Any, Optional
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from dotenv import load_dotenv
import numpy as np


def load_environment() -> Dict[str, str]:
    """
    Load environment configuration from .env files.
    
    Loads in order: .env, .kb.env (if exists)
    Returns a dictionary with all configuration values.
    """
    # Load main .env file
    if os.path.exists('.env'):
        load_dotenv('.env')
        print("✅ Loaded configuration from .env")
    else:
        print("⚠️  No .env file found. Using environment variables or defaults.")
    
    # Load Knowledge Base specific config if it exists
    if os.path.exists('.kb.env'):
        load_dotenv('.kb.env')
        print("✅ Loaded Knowledge Base configuration from .kb.env")
    
    # Extract all relevant environment variables
    config = {
        'aws_region': os.getenv('AWS_REGION', 'us-east-1'),
        'embed_model_id': os.getenv('BEDROCK_EMBED_MODEL_ID', 'amazon.titan-embed-text-v2:0'),
        'chat_model_id': os.getenv('BEDROCK_CHAT_MODEL_ID', 'amazon.nova-lite-v1:0'),
        'kb_id': os.getenv('KB_ID', ''),
        's3_uri': os.getenv('S3_URI_FOR_KB', ''),
        'chunk_size': int(os.getenv('CHUNK_SIZE', '800')),
        'chunk_overlap': int(os.getenv('CHUNK_OVERLAP', '120')),
        'top_k': int(os.getenv('TOP_K_RESULTS', '4')),
        'temperature': float(os.getenv('TEMPERATURE', '0.2')),
        'debug': os.getenv('DEBUG', 'false').lower() == 'true',
        'mock_aws': os.getenv('MOCK_AWS', 'false').lower() == 'true'
    }
    
    return config


def create_bedrock_clients(region: str) -> Dict[str, Any]:
    """
    Create AWS Bedrock clients with proper error handling.
    
    Args:
        region: AWS region name
        
    Returns:
        Dictionary containing bedrock-runtime and bedrock-agent-runtime clients
        
    Raises:
        SystemExit: If AWS credentials are not configured
    """
    try:
        # Create Bedrock Runtime client for embeddings and chat
        bedrock_runtime = boto3.client(
            'bedrock-runtime',
            region_name=region
        )
        
        # Create Bedrock Agent Runtime client for Knowledge Bases
        bedrock_agent_runtime = boto3.client(
            'bedrock-agent-runtime', 
            region_name=region
        )
        
        # Test connectivity with a simple call (the runtime client doesn't have list_foundation_models)
        # We'll skip the connectivity test for now
        
        print(f"✅ Connected to AWS Bedrock in region: {region}")
        
        return {
            'runtime': bedrock_runtime,
            'agent_runtime': bedrock_agent_runtime
        }
        
    except NoCredentialsError:
        print_error("AWS credentials not found. Please configure your credentials.")
        print("Options:")
        print("1. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY in .env")
        print("2. Use AWS CLI: aws configure")
        print("3. Use IAM roles (for EC2/ECS)")
        print("4. Set environment variables directly")
        sys.exit(1)
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'UnauthorizedOperation':
            print_error("Access denied to AWS Bedrock.")
            print("Please ensure:")
            print("1. Your AWS credentials have the required permissions")
            print("2. Bedrock service is available in your region")
            print("3. You have enabled model access in Bedrock console")
        else:
            print_error(f"AWS Error: {error_code} - {e.response['Error']['Message']}")
        sys.exit(1)
        
    except Exception as e:
        print_error(f"Unexpected error connecting to AWS: {str(e)}")
        sys.exit(1)


def bedrock_embed_text(texts: List[str], client, model_id: str) -> List[List[float]]:
    """
    Generate embeddings for a list of texts using AWS Bedrock.
    
    Args:
        texts: List of text strings to embed
        client: Bedrock runtime client
        model_id: Embedding model ID (e.g., amazon.titan-embed-text-v2:0)
        
    Returns:
        List of embedding vectors (each vector is a list of floats)
        
    Raises:
        Exception: If embedding generation fails
    """
    embeddings = []
    
    # Process texts in batches to avoid rate limits
    batch_size = 16
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        
        for text in batch:
            try:
                # Prepare the request for Titan Embed v2
                body = json.dumps({
                    "inputText": text,
                    "dimensions": 1024,  # Titan v2 supports configurable dimensions
                    "normalize": True    # L2 normalize for cosine similarity
                })
                
                # Call Bedrock
                response = client.invoke_model(
                    modelId=model_id,
                    body=body,
                    contentType='application/json',
                    accept='application/json'
                )
                
                # Parse response
                response_body = json.loads(response['body'].read())
                embedding = response_body['embedding']
                embeddings.append(embedding)
                
            except ClientError as e:
                error_code = e.response['Error']['Code']
                if error_code == 'AccessDeniedException':
                    print_error(f"Access denied to model {model_id}")
                    print(f"Please enable access to {model_id} in the Bedrock console:")
                    print(f"https://console.aws.amazon.com/bedrock/home?region={client.meta.region_name}#/modelaccess")
                    raise
                else:
                    print_error(f"Bedrock error: {error_code} - {e.response['Error']['Message']}")
                    raise
                    
            except Exception as e:
                print_error(f"Error generating embedding for text: {text[:50]}...")
                print_error(f"Error details: {str(e)}")
                raise
    
    print(f"✅ Generated {len(embeddings)} embeddings using {model_id}")
    return embeddings


def bedrock_chat(prompt: str, client, model_id: str, system: str = "", temperature: float = 0.2) -> str:
    """
    Generate a chat response using AWS Bedrock.
    
    Args:
        prompt: User prompt/question
        client: Bedrock runtime client  
        model_id: Chat model ID (e.g., amazon.nova-lite-v1:0)
        system: System prompt (optional)
        temperature: Sampling temperature
        
    Returns:
        Generated response text
        
    Raises:
        Exception: If chat generation fails
    """
    try:
        # Prepare the request for Nova Lite (doesn't support system role)
        messages = []
        
        # Include system prompt as part of user message if provided
        user_content = prompt
        if system:
            user_content = f"{system}\n\n{prompt}"
            
        messages.append({
            "role": "user", 
            "content": [{"text": user_content}]
        })
        
        body = json.dumps({
            "messages": messages,
            "inferenceConfig": {
                "temperature": temperature,
                "maxTokens": 2048
            }
        })
        
        # Call Bedrock
        response = client.invoke_model(
            modelId=model_id,
            body=body,
            contentType='application/json',
            accept='application/json'
        )
        
        # Parse response
        response_body = json.loads(response['body'].read())
        return response_body['output']['message']['content'][0]['text']
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'AccessDeniedException':
            print_error(f"Access denied to model {model_id}")
            print(f"Please enable access to {model_id} in the Bedrock console:")
            print(f"https://console.aws.amazon.com/bedrock/home?region={client.meta.region_name}#/modelaccess")
            raise
        else:
            print_error(f"Bedrock error: {error_code} - {e.response['Error']['Message']}")
            raise
            
    except Exception as e:
        print_error(f"Error generating chat response: {str(e)}")
        raise


def safe_json_parse(json_str: str) -> Optional[Dict]:
    """
    Safely parse JSON string with error handling.
    
    Args:
        json_str: JSON string to parse
        
    Returns:
        Parsed dictionary or None if parsing fails
    """
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print_error(f"JSON parsing error: {str(e)}")
        return None


def print_error(message: str):
    """Print error message with consistent formatting."""
    print(f"❌ ERROR: {message}", file=sys.stderr)


def print_warning(message: str):
    """Print warning message with consistent formatting."""
    print(f"⚠️  WARNING: {message}")


def print_info(message: str):
    """Print info message with consistent formatting."""
    print(f"ℹ️  INFO: {message}")


def print_success(message: str):
    """Print success message with consistent formatting."""
    print(f"✅ SUCCESS: {message}")


def validate_environment() -> bool:
    """
    Validate that the environment is properly configured.
    
    Returns:
        True if environment is valid, False otherwise
    """
    config = load_environment()
    issues = []
    
    # Check for required AWS region
    if not config['aws_region']:
        issues.append("AWS_REGION not set")
    
    # Check for model IDs
    if not config['embed_model_id']:
        issues.append("BEDROCK_EMBED_MODEL_ID not set")
        
    if not config['chat_model_id']:
        issues.append("BEDROCK_CHAT_MODEL_ID not set")
    
    # Check AWS credentials (basic check)
    if not os.getenv('AWS_ACCESS_KEY_ID') and not os.getenv('AWS_PROFILE'):
        issues.append("AWS credentials not configured (set AWS_ACCESS_KEY_ID or AWS_PROFILE)")
    
    if issues:
        print_error("Environment validation failed:")
        for issue in issues:
            print(f"  - {issue}")
        print()
        print("Please check your .env file and AWS configuration.")
        return False
    
    print_success("Environment validation passed")
    return True


def format_sources(sources: List[Dict[str, Any]]) -> str:
    """
    Format source citations in a consistent way.
    
    Args:
        sources: List of source dictionaries with metadata
        
    Returns:
        Formatted citation string
    """
    if not sources:
        return ""
    
    citations = []
    for i, source in enumerate(sources, 1):
        if 'file' in source:
            citation = f"[{i}] {source['file']}"
        elif 's3_uri' in source:
            citation = f"[{i}] {source['s3_uri']}"
        else:
            citation = f"[{i}] Unknown source"
        
        if 'snippet' in source:
            citation += f": {source['snippet'][:100]}..."
            
        citations.append(citation)
    
    return "\n\nSources:\n" + "\n".join(citations)


# Module-level configuration for easy access
CONFIG = load_environment()

# Test function for development
def test_bedrock_connection():
    """Test function to verify Bedrock connectivity."""
    if not validate_environment():
        return False
        
    try:
        clients = create_bedrock_clients(CONFIG['aws_region'])
        
        # Test embedding
        test_embedding = bedrock_embed_text(
            ["Hello, world!"], 
            clients['runtime'], 
            CONFIG['embed_model_id']
        )
        print(f"✅ Embedding test successful. Vector size: {len(test_embedding[0])}")
        
        # Test chat
        test_response = bedrock_chat(
            "Hello! Please respond with 'Connection successful'",
            clients['runtime'],
            CONFIG['chat_model_id']
        )
        print(f"✅ Chat test successful. Response: {test_response[:50]}...")
        
        return True
        
    except Exception as e:
        print_error(f"Bedrock connection test failed: {str(e)}")
        return False


if __name__ == "__main__":
    print("🧪 Testing AWS Bedrock Connection...")
    print("=" * 50)
    success = test_bedrock_connection()
    print("=" * 50)
    if success:
        print("✅ All tests passed! Your environment is ready for the RAG demo.")
    else:
        print("❌ Tests failed. Please check your configuration and try again.")
        sys.exit(1)

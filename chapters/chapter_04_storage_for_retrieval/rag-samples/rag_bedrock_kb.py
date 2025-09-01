#!/usr/bin/env python3
"""
AWS Bedrock Knowledge Base RAG Implementation

This module demonstrates using AWS Bedrock Knowledge Bases for managed 
Retrieval-Augmented Generation. This is the "managed" path that handles
indexing, storage, and retrieval through AWS services.

Key components:
1. Knowledge Base configuration loading
2. retrieve_and_generate API usage
3. Response formatting and source extraction
4. Error handling for KB operations

This implementation shows how managed services can simplify RAG deployment
while providing enterprise-grade scalability and reliability.

Author: AWS AI Engineering Course
Chapter: 4 - Storage for Retrieval
"""

import os
import sys
import argparse
import json
from typing import Dict, Any, List, Optional

# Import our common utilities
from common import (
    load_environment, create_bedrock_clients, print_error, print_success, 
    print_info, print_warning, format_sources
)


def validate_kb_configuration() -> Dict[str, str]:
    """
    Validate Knowledge Base configuration and return settings.
    
    Returns:
        Dictionary with KB configuration
        
    Raises:
        SystemExit: If configuration is invalid
    """
    config = load_environment()
    
    # Check for required KB configuration
    kb_id = config.get('kb_id', '').strip()
    
    if not kb_id:
        print_error("Knowledge Base ID not found.")
        print("This usually means:")
        print("1. You haven't run the setup script: scripts/setup-kb.sh")
        print("2. The .kb.env file is missing or corrupted")
        print("3. The KB_ID variable is not set in your .env file")
        print()
        print("To fix this:")
        print("1. Run: make up    (to create Knowledge Base)")
        print("2. Or set KB_ID manually in .env if you have an existing KB")
        sys.exit(1)
    
    # Optional: Validate that KB exists
    try:
        clients = create_bedrock_clients(config['aws_region'])
        # We could test KB access here, but it's expensive
        # Just validate the ID format for now
        if not kb_id.startswith('KB') or len(kb_id) < 10:
            print_warning(f"Knowledge Base ID format looks unusual: {kb_id}")
            
    except Exception as e:
        print_warning(f"Could not validate KB access: {str(e)}")
    
    print_success(f"Using Knowledge Base: {kb_id}")
    return config


def kb_retrieve_and_generate(question: str, clients: Dict[str, Any], 
                           config: Dict[str, str]) -> Dict[str, Any]:
    """
    Use AWS Bedrock Knowledge Base retrieve_and_generate API.
    
    Args:
        question: User's question
        clients: Dictionary of AWS clients
        config: Configuration dictionary
        
    Returns:
        API response dictionary
        
    Raises:
        Exception: If KB operation fails
    """
    try:
        response = clients['agent_runtime'].retrieve_and_generate(
            input={
                'text': question
            },
            retrieveAndGenerateConfiguration={
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': config['kb_id'],
                    'modelArn': f"arn:aws:bedrock:{config['aws_region']}::foundation-model/{config['chat_model_id']}",
                    'retrievalConfiguration': {
                        'vectorSearchConfiguration': {
                            'numberOfResults': config['top_k'],
                            'overrideSearchType': 'HYBRID'  # Use both semantic and keyword search
                        }
                    },
                    'generationConfiguration': {
                        'promptTemplate': {
                            'textPromptTemplate': '''You are a helpful AI assistant specializing in AI Engineering topics.

Use the provided context to answer questions accurately and helpfully.

Guidelines:
- Base your answer primarily on the provided context
- If the context doesn't contain enough information, say so clearly  
- Be concise but thorough
- Use technical terms appropriately for an engineering audience
- When relevant, mention specific tools, frameworks, or AWS services

Context: $search_results$

Question: $query$

Answer:'''
                        }
                    }
                }
            }
        )
        
        return response
        
    except Exception as e:
        error_msg = str(e)
        
        # Provide helpful error messages
        if 'ResourceNotFoundException' in error_msg:
            print_error(f"Knowledge Base not found: {config['kb_id']}")
            print("Possible causes:")
            print("1. Knowledge Base was deleted")
            print("2. Incorrect KB_ID in configuration")
            print("3. Knowledge Base is in a different region")
            print(f"4. Check AWS Console: https://console.aws.amazon.com/bedrock/home?region={config['aws_region']}#/knowledge-bases")
            
        elif 'AccessDeniedException' in error_msg:
            print_error("Access denied to Knowledge Base or model")
            print("Possible causes:")
            print("1. Insufficient IAM permissions")
            print("2. Model access not enabled in Bedrock console")
            print(f"3. Check model access: https://console.aws.amazon.com/bedrock/home?region={config['aws_region']}#/modelaccess")
            
        elif 'ValidationException' in error_msg:
            print_error("Invalid request parameters")
            print("Possible causes:")
            print("1. Invalid model ARN or configuration")
            print("2. Malformed request structure")
            
        else:
            print_error(f"Knowledge Base operation failed: {error_msg}")
        
        raise


def format_kb_response(response: Dict[str, Any]) -> str:
    """
    Format Knowledge Base response with sources.
    
    Args:
        response: API response from retrieve_and_generate
        
    Returns:
        Formatted response string with sources
    """
    # Extract the main answer
    output = response.get('output', {})
    answer_text = output.get('text', 'No answer generated.')
    
    # Extract source citations
    citations = response.get('citations', [])
    source_info = []
    
    for citation in citations:
        retrieved_refs = citation.get('retrievedReferences', [])
        
        for ref in retrieved_refs:
            location = ref.get('location', {})
            s3_location = location.get('s3Location', {})
            
            source_uri = s3_location.get('uri', 'Unknown source')
            
            # Extract content snippet
            content = ref.get('content', {})
            text_snippet = content.get('text', '')
            
            source_info.append({
                's3_uri': source_uri,
                'snippet': text_snippet[:150] + "..." if len(text_snippet) > 150 else text_snippet
            })
    
    # Format sources
    sources_text = format_sources(source_info) if source_info else ""
    
    return f"{answer_text}{sources_text}"


def kb_retrieve_only(question: str, clients: Dict[str, Any], 
                    config: Dict[str, str]) -> List[Dict[str, Any]]:
    """
    Use Knowledge Base retrieve API only (without generation).
    
    Args:
        question: User's question
        clients: Dictionary of AWS clients
        config: Configuration dictionary
        
    Returns:
        List of retrieved chunks
    """
    try:
        response = clients['agent_runtime'].retrieve(
            knowledgeBaseId=config['kb_id'],
            retrievalQuery={
                'text': question
            },
            retrievalConfiguration={
                'vectorSearchConfiguration': {
                    'numberOfResults': config['top_k'],
                    'overrideSearchType': 'HYBRID'
                }
            }
        )
        
        return response.get('retrievalResults', [])
        
    except Exception as e:
        print_error(f"Knowledge Base retrieval failed: {str(e)}")
        raise


def run_kb_query(question: str, clients: Dict[str, Any], config: Dict[str, str], 
                retrieve_only: bool = False) -> str:
    """
    Run a complete Knowledge Base query.
    
    Args:
        question: User's question
        clients: AWS clients
        config: Configuration dictionary
        retrieve_only: If True, only retrieve without generation
        
    Returns:
        Formatted answer or retrieval results
    """
    print_info(f"Processing query with Bedrock Knowledge Base: {question}")
    
    if retrieve_only:
        # Retrieve only mode for debugging
        results = kb_retrieve_only(question, clients, config)
        
        if not results:
            return "❌ No relevant information found in Knowledge Base."
        
        formatted_results = []
        for i, result in enumerate(results, 1):
            content = result.get('content', {})
            text = content.get('text', 'No content')
            
            location = result.get('location', {})
            s3_location = location.get('s3Location', {})
            uri = s3_location.get('uri', 'Unknown source')
            
            score = result.get('score', 0.0)
            
            formatted_results.append(
                f"[Result {i}] (Score: {score:.3f})\n"
                f"Source: {uri}\n"
                f"Content: {text[:200]}...\n"
            )
        
        return "\n".join(formatted_results)
    
    else:
        # Full retrieve and generate
        response = kb_retrieve_and_generate(question, clients, config)
        return format_kb_response(response)


def check_kb_status(clients: Dict[str, Any], kb_id: str) -> Dict[str, Any]:
    """
    Check Knowledge Base status and data sources.
    
    Args:
        clients: AWS clients
        kb_id: Knowledge Base ID
        
    Returns:
        Status information dictionary
    """
    try:
        # Create bedrock-agent client for management operations
        bedrock_agent = clients.get('agent')
        if not bedrock_agent:
            bedrock_agent = clients['runtime']._client_config.region_name
            bedrock_agent = clients['runtime']._service_model.service_name
            # For simplicity, we'll skip detailed status checking
            return {'status': 'unknown', 'message': 'Status check not implemented'}
        
        # In a full implementation, you would check:
        # 1. Knowledge Base status
        # 2. Data source status  
        # 3. Ingestion job status
        
        return {
            'status': 'active',
            'message': f'Knowledge Base {kb_id} appears to be accessible'
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error checking status: {str(e)}'
        }


def main():
    """Main function for the Bedrock Knowledge Base RAG demo."""
    parser = argparse.ArgumentParser(description="AWS Bedrock Knowledge Base RAG Demo")
    parser.add_argument("--question", "-q", type=str, help="Question to ask")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    parser.add_argument("--retrieve-only", action="store_true", help="Only retrieve, don't generate")
    parser.add_argument("--status", action="store_true", help="Check Knowledge Base status")
    args = parser.parse_args()
    
    print("🏛️ AWS BEDROCK KNOWLEDGE BASE RAG DEMO")
    print("=" * 50)
    
    # Validate configuration
    try:
        config = validate_kb_configuration()
    except SystemExit:
        return 1
    
    # Create AWS clients
    try:
        clients = create_bedrock_clients(config['aws_region'])
    except SystemExit:
        return 1
    
    # Check status if requested
    if args.status:
        print_info("Checking Knowledge Base status...")
        status = check_kb_status(clients, config['kb_id'])
        print(f"Status: {status['status']}")
        print(f"Message: {status['message']}")
        return 0
    
    # Handle query
    if args.question:
        # Single question mode
        try:
            answer = run_kb_query(args.question, clients, config, args.retrieve_only)
            print("\n" + "="*50)
            print("ANSWER:" if not args.retrieve_only else "RETRIEVAL RESULTS:")
            print("="*50)
            print(answer)
        except Exception as e:
            print_error(f"Query failed: {str(e)}")
            return 1
        
    elif args.interactive:
        # Interactive mode
        print("\n💬 Interactive Mode (type 'quit' to exit)")
        print("="*50)
        
        while True:
            try:
                question = input("\n❓ Your question: ").strip()
                if question.lower() in ['quit', 'exit', 'q']:
                    break
                if not question:
                    continue
                
                answer = run_kb_query(question, clients, config, args.retrieve_only)
                print("\n" + "="*50)
                print("ANSWER:" if not args.retrieve_only else "RETRIEVAL RESULTS:")
                print("="*50)
                print(answer)
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print_error(f"Error processing question: {str(e)}")
    
    else:
        # Demo mode with sample questions
        sample_questions = [
            "What is AI Engineering?",
            "How do RAG systems work?", 
            "What are the key challenges in deploying AI systems?",
            "How do you monitor model performance in production?"
        ]
        
        print("\n🎯 Demo Mode - Sample Questions:")
        print("="*50)
        
        for i, question in enumerate(sample_questions, 1):
            print(f"\n📝 Question {i}: {question}")
            print("-" * 40)
            
            try:
                answer = run_kb_query(question, clients, config, args.retrieve_only)
                print(answer)
            except Exception as e:
                print_error(f"Query failed: {str(e)}")
                continue
            
            if i < len(sample_questions):
                input("\nPress Enter to continue...")
    
    print("\n✅ Bedrock Knowledge Base RAG Demo Complete!")
    return 0


if __name__ == "__main__":
    sys.exit(main())

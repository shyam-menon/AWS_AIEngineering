#!/usr/bin/env python3
"""
Strands Agent RAG Wrapper

This module demonstrates how to use the Strands Agent framework to create
an intelligent RAG system that can:
1. Try AWS Bedrock Knowledge Base first
2. Fall back to local FAISS if KB fails
3. Compare results from both approaches
4. Provide clear feedback about which approach was used

This showcases how agents can orchestrate multiple AI services and provide
intelligent fallback mechanisms for robust production systems.

Author: AWS AI Engineering Course  
Chapter: 4 - Storage for Retrieval
"""

import os
import sys
import argparse
from typing import Optional, Dict, Any, List
import traceback

# Import our RAG implementations
from rag_bedrock_kb import run_kb_query, validate_kb_configuration
from rag_vector_local import run_query, load_index, load_documents
from common import (
    load_environment, create_bedrock_clients, print_error, print_success, 
    print_info, print_warning
)

# Import Strands with fallback
try:
    from strands import Agent
    from strands.tools import tool
    STRANDS_AVAILABLE = True
    print_success("Strands framework loaded successfully")
except ImportError:
    STRANDS_AVAILABLE = False
    print_warning("Strands framework not available. Running in demonstration mode.")
    print("To install: pip install strands")
    
    # Mock implementation for demonstration
    def tool(func):
        """Mock tool decorator for when Strands is not available."""
        func._is_tool = True
        return func
    
    class Agent:
        """Mock Agent class for demonstration."""
        def __init__(self, tools=None, model=None):
            self.tools = tools or []
            self.model = model
            
        def __call__(self, message):
            # Simple dispatcher for demo mode
            if "knowledge base" in message.lower() or "managed" in message.lower():
                return attempt_kb_retrieval(message)
            elif "local" in message.lower() or "faiss" in message.lower():
                return attempt_local_retrieval(message)
            elif "compare" in message.lower():
                return compare_approaches(message)
            else:
                return agent_answer(message)


# Global variables for loaded indexes and configuration
FAISS_INDEX = None
FAISS_METADATA = None  
FAISS_SOURCES = None
BEDROCK_CLIENTS = None
CONFIG = None


def initialize_rag_systems():
    """Initialize both RAG systems (KB and local FAISS)."""
    global FAISS_INDEX, FAISS_METADATA, FAISS_SOURCES, BEDROCK_CLIENTS, CONFIG
    
    print_info("Initializing RAG systems...")
    
    # Load configuration
    CONFIG = load_environment()
    
    # Create Bedrock clients
    try:
        BEDROCK_CLIENTS = create_bedrock_clients(CONFIG['aws_region'])
        print_success("AWS Bedrock clients initialized")
    except Exception as e:
        print_error(f"Failed to initialize Bedrock clients: {str(e)}")
        BEDROCK_CLIENTS = None
    
    # Try to load local FAISS index
    try:
        if os.path.exists("faiss_index.faiss"):
            FAISS_INDEX, _, FAISS_METADATA = load_index("faiss_index")
            FAISS_SOURCES = load_documents("data/sample_docs")
            print_success("Local FAISS index loaded")
        else:
            print_warning("Local FAISS index not found. Run rag_vector_local.py first.")
    except Exception as e:
        print_warning(f"Could not load local FAISS index: {str(e)}")


@tool
def attempt_kb_retrieval(question: str) -> Optional[str]:
    """
    Attempt to answer question using AWS Bedrock Knowledge Base.
    
    Args:
        question (str): The question to answer
        
    Returns:
        Optional[str]: Answer from Knowledge Base or None if failed
    """
    if not BEDROCK_CLIENTS:
        return None
        
    try:
        # Validate KB configuration
        kb_config = validate_kb_configuration()
        
        # Run KB query
        answer = run_kb_query(question, BEDROCK_CLIENTS, kb_config)
        
        return f"[Bedrock Knowledge Base] {answer}"
        
    except Exception as e:
        print_warning(f"Knowledge Base retrieval failed: {str(e)}")
        return None


@tool  
def attempt_local_retrieval(question: str) -> str:
    """
    Answer question using local FAISS vector search.
    
    Args:
        question (str): The question to answer
        
    Returns:
        str: Answer from local FAISS system
    """
    if not FAISS_INDEX or not BEDROCK_CLIENTS:
        return "❌ Local FAISS system not available. Please run setup first."
        
    try:
        answer = run_query(
            question, FAISS_INDEX, FAISS_METADATA, 
            FAISS_SOURCES, BEDROCK_CLIENTS, CONFIG
        )
        
        return f"[Local Vector RAG] {answer}"
        
    except Exception as e:
        return f"❌ Local retrieval failed: {str(e)}"


@tool
def compare_approaches(question: str) -> str:
    """
    Compare answers from both Knowledge Base and local FAISS.
    
    Args:
        question (str): The question to answer with both approaches
        
    Returns:
        str: Comparison of both approaches
    """
    print_info(f"Comparing both approaches for: {question}")
    
    # Try Knowledge Base
    kb_answer = attempt_kb_retrieval(question)
    
    # Try local FAISS
    local_answer = attempt_local_retrieval(question)
    
    # Format comparison
    comparison = "🔍 APPROACH COMPARISON\n"
    comparison += "=" * 50 + "\n\n"
    
    if kb_answer:
        comparison += f"📊 MANAGED APPROACH (Bedrock KB):\n{kb_answer}\n\n"
    else:
        comparison += "📊 MANAGED APPROACH: ❌ Failed\n\n"
    
    comparison += f"🔧 DIY APPROACH (Local FAISS):\n{local_answer}\n\n"
    
    # Add analysis
    comparison += "🧠 ANALYSIS:\n"
    comparison += "-" * 20 + "\n"
    
    if kb_answer and not kb_answer.startswith("❌"):
        comparison += "✅ Knowledge Base: Available and responsive\n"
    else:
        comparison += "❌ Knowledge Base: Not available or failed\n"
    
    if not local_answer.startswith("❌"):
        comparison += "✅ Local FAISS: Available and responsive\n"
    else:
        comparison += "❌ Local FAISS: Not available or failed\n"
    
    return comparison


def agent_answer(question: str) -> str:
    """
    Main agent function that tries KB first, then falls back to local.
    
    Args:
        question: User's question
        
    Returns:
        Answer with indication of which backend was used
    """
    print_info(f"Agent processing question: {question}")
    
    # Strategy: Try KB first, fallback to local
    kb_answer = attempt_kb_retrieval(question)
    
    if kb_answer and not kb_answer.startswith("❌"):
        print_success("Used Bedrock Knowledge Base")
        return kb_answer
    
    print_info("Knowledge Base unavailable, falling back to local FAISS")
    local_answer = attempt_local_retrieval(question)
    
    if not local_answer.startswith("❌"):
        print_success("Used local FAISS as fallback")
        return local_answer
    
    # Both failed
    print_error("Both retrieval methods failed")
    return "❌ Unable to answer question - both Knowledge Base and local retrieval failed."


def create_rag_agent() -> Agent:
    """Create and configure the RAG agent."""
    if not STRANDS_AVAILABLE:
        print_warning("Creating mock agent (Strands not available)")
        return Agent(
            tools=[attempt_kb_retrieval, attempt_local_retrieval, compare_approaches],
            model="amazon.nova-lite-v1:0"  # This would be ignored in mock mode
        )
    
    try:
        agent = Agent(
            tools=[attempt_kb_retrieval, attempt_local_retrieval, compare_approaches],
            model="amazon.nova-lite-v1:0"
        )
        print_success("Created Strands RAG agent with KB and local tools")
        return agent
        
    except Exception as e:
        print_error(f"Failed to create Strands agent: {str(e)}")
        print_info("Creating fallback agent...")
        return Agent(tools=[])


def run_agent_demo():
    """Run demonstration of the agent capabilities."""
    print("🤖 RAG AGENT DEMONSTRATION")
    print("=" * 50)
    
    # Initialize systems
    initialize_rag_systems()
    
    # Create agent
    agent = create_rag_agent()
    
    # Demo queries
    demo_queries = [
        {
            'query': 'What is AI Engineering?',
            'mode': 'auto'
        },
        {
            'query': 'How do RAG systems work?', 
            'mode': 'kb_only'
        },
        {
            'query': 'What are vector databases?',
            'mode': 'local_only' 
        },
        {
            'query': 'How do you monitor AI systems?',
            'mode': 'compare'
        }
    ]
    
    for i, demo in enumerate(demo_queries, 1):
        print(f"\n📝 Demo {i}: {demo['query']}")
        print(f"Mode: {demo['mode']}")
        print("-" * 40)
        
        try:
            if demo['mode'] == 'auto':
                # Let agent decide
                if STRANDS_AVAILABLE:
                    response = agent(demo['query'])
                else:
                    response = agent_answer(demo['query'])
                    
            elif demo['mode'] == 'kb_only':
                response = attempt_kb_retrieval(demo['query'])
                if not response:
                    response = "❌ Knowledge Base not available"
                    
            elif demo['mode'] == 'local_only':
                response = attempt_local_retrieval(demo['query'])
                
            elif demo['mode'] == 'compare':
                response = compare_approaches(demo['query'])
            
            print(response)
            
        except Exception as e:
            print_error(f"Demo failed: {str(e)}")
            if CONFIG and CONFIG.get('debug'):
                traceback.print_exc()
        
        if i < len(demo_queries):
            input("\nPress Enter to continue...")


def interactive_mode():
    """Run interactive agent mode."""
    print("\n💬 Interactive Agent Mode")
    print("Commands:")
    print("  - Ask any question for automatic routing")
    print("  - 'kb: <question>' to force Knowledge Base")
    print("  - 'local: <question>' to force local FAISS")
    print("  - 'compare: <question>' to compare both")
    print("  - 'quit' to exit")
    print("="*50)
    
    # Initialize systems
    initialize_rag_systems()
    agent = create_rag_agent()
    
    while True:
        try:
            user_input = input("\n❓ Your question: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            if not user_input:
                continue
            
            # Parse command
            if user_input.startswith('kb:'):
                question = user_input[3:].strip()
                response = attempt_kb_retrieval(question)
                if not response:
                    response = "❌ Knowledge Base not available"
                    
            elif user_input.startswith('local:'):
                question = user_input[6:].strip()
                response = attempt_local_retrieval(question)
                
            elif user_input.startswith('compare:'):
                question = user_input[8:].strip()
                response = compare_approaches(question)
                
            else:
                # Automatic routing
                if STRANDS_AVAILABLE:
                    response = agent(user_input)
                else:
                    response = agent_answer(user_input)
            
            print("\n" + "="*50)
            print("RESPONSE:")
            print("="*50)
            print(response)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print_error(f"Error: {str(e)}")
            if CONFIG and CONFIG.get('debug'):
                traceback.print_exc()


def main():
    """Main function for the Strands agent RAG demo."""
    parser = argparse.ArgumentParser(description="Strands Agent RAG Demo")
    parser.add_argument("--question", "-q", type=str, help="Single question to ask")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    parser.add_argument("--demo", "-d", action="store_true", help="Run demonstration")
    parser.add_argument("--force-kb", action="store_true", help="Force Knowledge Base only")
    parser.add_argument("--force-local", action="store_true", help="Force local FAISS only")
    parser.add_argument("--compare", action="store_true", help="Compare both approaches")
    args = parser.parse_args()
    
    print("🤖 STRANDS AGENT RAG WRAPPER")
    print("=" * 50)
    
    if not any([args.question, args.interactive, args.demo]):
        args.demo = True  # Default to demo mode
    
    if args.question:
        # Single question mode
        initialize_rag_systems()
        
        try:
            if args.force_kb:
                response = attempt_kb_retrieval(args.question)
                if not response:
                    response = "❌ Knowledge Base not available"
            elif args.force_local:
                response = attempt_local_retrieval(args.question)
            elif args.compare:
                response = compare_approaches(args.question)
            else:
                # Automatic routing
                agent = create_rag_agent()
                if STRANDS_AVAILABLE:
                    response = agent(args.question)
                else:
                    response = agent_answer(args.question)
            
            print("\n" + "="*50)
            print("RESPONSE:")
            print("="*50)
            print(response)
            
        except Exception as e:
            print_error(f"Query failed: {str(e)}")
            return 1
    
    elif args.interactive:
        interactive_mode()
    
    elif args.demo:
        run_agent_demo()
    
    print("\n✅ Strands Agent RAG Demo Complete!")
    return 0


if __name__ == "__main__":
    sys.exit(main())

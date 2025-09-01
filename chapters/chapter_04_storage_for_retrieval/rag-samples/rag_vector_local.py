#!/usr/bin/env python3
"""
Local FAISS Vector RAG Implementation

This module demonstrates a DIY approach to Retrieval-Augmented Generation (RAG)
using FAISS for local vector storage and AWS Bedrock for embeddings and chat.

Key components:
1. Document loading and chunking
2. Local FAISS index creation and management
3. Vector similarity search
4. Context formatting and answer generation

This implementation is designed for educational purposes and small-scale
applications where you want full control over the retrieval pipeline.

Author: AWS AI Engineering Course
Chapter: 4 - Storage for Retrieval
"""

import os
import sys
import argparse
from typing import List, Tuple, Dict, Any
import numpy as np
import faiss
import tiktoken
from pathlib import Path

# Import our common utilities
from common import (
    load_environment, create_bedrock_clients, bedrock_embed_text, 
    bedrock_chat, print_error, print_success, print_info, format_sources
)


def load_documents(docs_dir: str = "data/sample_docs") -> List[Tuple[str, str]]:
    """
    Load documents from a directory.
    
    Args:
        docs_dir: Path to directory containing documents
        
    Returns:
        List of tuples (filename, content)
        
    Raises:
        FileNotFoundError: If docs directory doesn't exist or is empty
    """
    docs_path = Path(docs_dir)
    
    if not docs_path.exists():
        print_error(f"Documents directory not found: {docs_dir}")
        print("Please ensure you have documents in the data/sample_docs directory.")
        print("You can copy the sample documents from the course materials.")
        raise FileNotFoundError(f"Directory not found: {docs_dir}")
    
    documents = []
    supported_extensions = ['.md', '.txt', '.rst']
    
    for file_path in docs_path.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:  # Only include non-empty files
                        documents.append((file_path.name, content))
                        print_info(f"Loaded document: {file_path.name} ({len(content)} characters)")
            except Exception as e:
                print_error(f"Error reading {file_path.name}: {str(e)}")
                continue
    
    if not documents:
        print_error(f"No valid documents found in {docs_dir}")
        print("Supported file types: .md, .txt, .rst")
        raise FileNotFoundError("No documents found")
    
    print_success(f"Loaded {len(documents)} documents")
    return documents


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 120) -> List[str]:
    """
    Split text into overlapping chunks for better retrieval.
    
    Args:
        text: Input text to chunk
        chunk_size: Maximum chunk size in tokens
        overlap: Number of tokens to overlap between chunks
        
    Returns:
        List of text chunks
    """
    # Use tiktoken to count tokens accurately
    encoding = tiktoken.get_encoding("cl100k_base")  # GPT-4 encoding
    tokens = encoding.encode(text)
    
    chunks = []
    start = 0
    
    while start < len(tokens):
        # Define chunk end
        end = start + chunk_size
        
        # Extract chunk tokens
        chunk_tokens = tokens[start:end]
        
        # Decode back to text
        chunk_text = encoding.decode(chunk_tokens)
        chunks.append(chunk_text.strip())
        
        # Move start position (with overlap)
        start = end - overlap
        
        # Break if we've processed all tokens
        if end >= len(tokens):
            break
    
    return chunks


def build_faiss_index(chunks: List[str], clients: Dict[str, Any], embed_model_id: str) -> Tuple[faiss.Index, np.ndarray, List[Dict[str, Any]]]:
    """
    Build a FAISS index from text chunks.
    
    Args:
        chunks: List of text chunks
        clients: Dictionary of AWS clients
        embed_model_id: Embedding model ID
        
    Returns:
        Tuple of (FAISS index, embeddings array, chunk metadata)
    """
    print_info(f"Generating embeddings for {len(chunks)} chunks...")
    
    # Generate embeddings in batches
    embeddings = bedrock_embed_text(chunks, clients['runtime'], embed_model_id)
    embeddings_array = np.array(embeddings, dtype=np.float32)
    
    # L2 normalize embeddings for cosine similarity with dot product
    faiss.normalize_L2(embeddings_array)
    
    # Create FAISS index (using Inner Product for normalized vectors = cosine similarity)
    dimension = embeddings_array.shape[1]
    index = faiss.IndexFlatIP(dimension)
    
    # Add embeddings to index
    index.add(embeddings_array)
    
    # Create metadata for chunks
    metadata = []
    for i, chunk in enumerate(chunks):
        metadata.append({
            'chunk_id': i,
            'text': chunk,
            'preview': chunk[:100] + "..." if len(chunk) > 100 else chunk
        })
    
    print_success(f"Built FAISS index with {index.ntotal} vectors (dimension: {dimension})")
    return index, embeddings_array, metadata


def search_index(index: faiss.Index, query: str, clients: Dict[str, Any], 
                embed_model_id: str, metadata: List[Dict[str, Any]], 
                top_k: int = 4) -> List[Tuple[int, float, Dict[str, Any]]]:
    """
    Search the FAISS index for relevant chunks.
    
    Args:
        index: FAISS index
        query: Search query
        clients: Dictionary of AWS clients
        embed_model_id: Embedding model ID
        metadata: Chunk metadata
        top_k: Number of results to return
        
    Returns:
        List of tuples (chunk_index, similarity_score, metadata)
    """
    # Generate query embedding
    query_embedding = bedrock_embed_text([query], clients['runtime'], embed_model_id)[0]
    query_vector = np.array([query_embedding], dtype=np.float32)
    
    # Normalize query vector
    faiss.normalize_L2(query_vector)
    
    # Search index
    scores, indices = index.search(query_vector, top_k)
    
    # Prepare results
    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx != -1:  # Valid result
            results.append((idx, float(score), metadata[idx]))
    
    return results


def format_context(results: List[Tuple[int, float, Dict[str, Any]]], 
                  sources: List[Tuple[str, str]]) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Format search results into context for the LLM.
    
    Args:
        results: Search results from FAISS
        sources: Original documents (filename, content) tuples
        
    Returns:
        Tuple of (formatted_context, source_info)
    """
    if not results:
        return "No relevant information found.", []
    
    context_parts = []
    source_info = []
    
    # Create a mapping of chunk text to source document
    chunk_to_source = {}
    for filename, content in sources:
        for chunk_idx, (_, _, metadata) in enumerate(results):
            chunk_text = metadata['text']
            if chunk_text in content:
                chunk_to_source[chunk_idx] = filename
                break
    
    for idx, (chunk_idx, score, metadata) in enumerate(results, 1):
        source_file = chunk_to_source.get(chunk_idx, "Unknown")
        
        context_parts.append(
            f"[Source {idx}] {metadata['text']}"
        )
        
        source_info.append({
            'file': source_file,
            'snippet': metadata['preview'],
            'similarity_score': score
        })
    
    context = "\n\n".join(context_parts)
    return context, source_info


def answer_with_context(question: str, context: str, clients: Dict[str, Any], 
                       chat_model_id: str, temperature: float = 0.2) -> str:
    """
    Generate an answer using the retrieved context.
    
    Args:
        question: User's question
        context: Retrieved context
        clients: Dictionary of AWS clients
        chat_model_id: Chat model ID
        temperature: Sampling temperature
        
    Returns:
        Generated answer
    """
    system_prompt = """You are a helpful AI assistant specializing in AI Engineering topics. 
Use the provided context to answer questions accurately and helpfully.

Guidelines:
- Base your answer primarily on the provided context
- If the context doesn't contain enough information, say so clearly
- Be concise but thorough
- Use technical terms appropriately for an engineering audience
- When relevant, mention specific tools, frameworks, or AWS services discussed in the context"""

    user_prompt = f"""Context:
{context}

Question: {question}

Please provide a helpful answer based on the context above."""

    response = bedrock_chat(
        user_prompt, 
        clients['runtime'], 
        chat_model_id, 
        system=system_prompt,
        temperature=temperature
    )
    
    return response


def save_index(index: faiss.Index, embeddings: np.ndarray, metadata: List[Dict[str, Any]], 
               filepath: str = "faiss_index"):
    """
    Save FAISS index and metadata to disk.
    
    Args:
        index: FAISS index
        embeddings: Embeddings array
        metadata: Chunk metadata
        filepath: Base filepath for saving (without extension)
    """
    try:
        # Save FAISS index
        faiss.write_index(index, f"{filepath}.faiss")
        
        # Save embeddings and metadata
        np.savez(f"{filepath}_data.npz", 
                embeddings=embeddings, 
                metadata=np.array(metadata, dtype=object))
        
        print_success(f"Saved index to {filepath}.faiss and {filepath}_data.npz")
        
    except Exception as e:
        print_error(f"Error saving index: {str(e)}")


def load_index(filepath: str = "faiss_index") -> Tuple[faiss.Index, np.ndarray, List[Dict[str, Any]]]:
    """
    Load FAISS index and metadata from disk.
    
    Args:
        filepath: Base filepath for loading (without extension)
        
    Returns:
        Tuple of (FAISS index, embeddings array, chunk metadata)
    """
    try:
        # Load FAISS index
        index = faiss.read_index(f"{filepath}.faiss")
        
        # Load embeddings and metadata
        data = np.load(f"{filepath}_data.npz", allow_pickle=True)
        embeddings = data['embeddings']
        metadata = data['metadata'].tolist()
        
        print_success(f"Loaded index from {filepath}.faiss")
        return index, embeddings, metadata
        
    except FileNotFoundError:
        print_error(f"Index files not found: {filepath}.faiss or {filepath}_data.npz")
        raise
    except Exception as e:
        print_error(f"Error loading index: {str(e)}")
        raise


def run_query(question: str, index: faiss.Index, metadata: List[Dict[str, Any]], 
              sources: List[Tuple[str, str]], clients: Dict[str, Any], 
              config: Dict[str, Any]) -> str:
    """
    Run a complete RAG query.
    
    Args:
        question: User's question
        index: FAISS index
        metadata: Chunk metadata
        sources: Original documents
        clients: AWS clients
        config: Configuration dictionary
        
    Returns:
        Complete answer with sources
    """
    print_info(f"Processing query: {question}")
    
    # Search for relevant chunks
    results = search_index(
        index, question, clients, config['embed_model_id'], 
        metadata, config['top_k']
    )
    
    if not results:
        return "❌ No relevant information found for your question."
    
    # Format context
    context, source_info = format_context(results, sources)
    
    # Generate answer
    answer = answer_with_context(
        question, context, clients, config['chat_model_id'], config['temperature']
    )
    
    # Format sources
    sources_text = format_sources(source_info)
    
    return f"{answer}{sources_text}"


def main():
    """Main function for the local FAISS RAG demo."""
    parser = argparse.ArgumentParser(description="Local FAISS Vector RAG Demo")
    parser.add_argument("--question", "-q", type=str, help="Question to ask")
    parser.add_argument("--rebuild", action="store_true", help="Force rebuild of index")
    parser.add_argument("--docs-dir", default="data/sample_docs", help="Documents directory")
    parser.add_argument("--top-k", type=int, help="Number of results to retrieve")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    args = parser.parse_args()
    
    print("🔍 LOCAL FAISS VECTOR RAG DEMO")
    print("=" * 50)
    
    # Load configuration
    config = load_environment()
    if args.top_k:
        config['top_k'] = args.top_k
    
    # Create AWS clients
    try:
        clients = create_bedrock_clients(config['aws_region'])
    except SystemExit:
        return 1
    
    # Try to load existing index
    index_path = "faiss_index"
    index, embeddings, metadata, sources = None, None, None, None
    
    if not args.rebuild and os.path.exists(f"{index_path}.faiss"):
        try:
            print_info("Loading existing FAISS index...")
            index, embeddings, metadata = load_index(index_path)
            # Reload documents for source mapping
            sources = load_documents(args.docs_dir)
        except Exception as e:
            print_error(f"Failed to load existing index: {str(e)}")
            print_info("Building new index...")
            index = None
    
    # Build new index if needed
    if index is None:
        try:
            # Load documents
            sources = load_documents(args.docs_dir)
            
            # Chunk all documents
            all_chunks = []
            for filename, content in sources:
                chunks = chunk_text(content, config['chunk_size'], config['chunk_overlap'])
                print_info(f"{filename}: {len(chunks)} chunks")
                all_chunks.extend(chunks)
            
            print_info(f"Total chunks: {len(all_chunks)}")
            
            # Build index
            index, embeddings, metadata = build_faiss_index(
                all_chunks, clients, config['embed_model_id']
            )
            
            # Save index for future use
            save_index(index, embeddings, metadata, index_path)
            
        except Exception as e:
            print_error(f"Failed to build index: {str(e)}")
            return 1
    
    # Handle query
    if args.question:
        # Single question mode
        answer = run_query(args.question, index, metadata, sources, clients, config)
        print("\n" + "="*50)
        print("ANSWER:")
        print("="*50)
        print(answer)
        
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
                    
                answer = run_query(question, index, metadata, sources, clients, config)
                print("\n" + "="*50)
                print("ANSWER:")
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
            "How do vector databases work?",
            "What are the key components of RAG systems?",
            "How do you monitor AI systems in production?"
        ]
        
        print("\n🎯 Demo Mode - Sample Questions:")
        print("="*50)
        
        for i, question in enumerate(sample_questions, 1):
            print(f"\n📝 Question {i}: {question}")
            print("-" * 40)
            
            answer = run_query(question, index, metadata, sources, clients, config)
            print(answer)
            
            if i < len(sample_questions):
                input("\nPress Enter to continue...")
    
    print("\n✅ Local FAISS RAG Demo Complete!")
    return 0


if __name__ == "__main__":
    sys.exit(main())

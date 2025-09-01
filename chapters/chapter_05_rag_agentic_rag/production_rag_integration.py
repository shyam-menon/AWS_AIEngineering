#!/usr/bin/env python3
"""
Intelligent Query Router - Integration Example

This example demonstrates how to integrate the Intelligent Query Routing Agent
into a production RAG application, showing how it can orchestrate multiple
data sources and retrieval strategies.

Author: AWS AI Engineering Course
Chapter: 5 - RAG & Agentic RAG
"""

import json
from typing import Dict, List, Any
from intelligent_query_router import IntelligentQueryRouter, QueryType

class ProductionRAGSystem:
    """
    Production RAG system that uses intelligent query routing to optimize
    information retrieval across multiple data sources.
    """
    
    def __init__(self):
        """Initialize the production RAG system."""
        print("🚀 Initializing Production RAG System with Intelligent Routing...")
        
        # Initialize the intelligent router
        self.router = IntelligentQueryRouter()
        
        # Initialize data sources (in production, these would be real connections)
        self.data_sources = {
            "bedrock_kb": self._mock_bedrock_kb,
            "code_repo": self._mock_code_repository,
            "docs_site": self._mock_documentation,
            "support_kb": self._mock_support_knowledge,
            "general_kb": self._mock_general_knowledge
        }
        
        print("✅ Production RAG System initialized successfully")
    
    def _mock_bedrock_kb(self, query: str) -> Dict[str, Any]:
        """Mock AWS Bedrock Knowledge Base retrieval."""
        return {
            "source": "AWS Bedrock Knowledge Base",
            "results": [
                {
                    "content": f"Bedrock KB result for: {query}",
                    "confidence": 0.85,
                    "metadata": {"source": "official_docs", "updated": "2024-08-15"}
                }
            ]
        }
    
    def _mock_code_repository(self, query: str) -> Dict[str, Any]:
        """Mock code repository search."""
        return {
            "source": "Code Repository",
            "results": [
                {
                    "content": f"# Code example for: {query}\ndef example_function():\n    pass",
                    "confidence": 0.90,
                    "metadata": {"language": "python", "repo": "aws-samples"}
                }
            ]
        }
    
    def _mock_documentation(self, query: str) -> Dict[str, Any]:
        """Mock documentation site search."""
        return {
            "source": "Documentation Site",
            "results": [
                {
                    "content": f"Documentation for: {query}",
                    "confidence": 0.80,
                    "metadata": {"section": "user_guide", "version": "latest"}
                }
            ]
        }
    
    def _mock_support_knowledge(self, query: str) -> Dict[str, Any]:
        """Mock support knowledge base."""
        return {
            "source": "Support Knowledge Base",
            "results": [
                {
                    "content": f"Support solution for: {query}",
                    "confidence": 0.88,
                    "metadata": {"category": "troubleshooting", "difficulty": "medium"}
                }
            ]
        }
    
    def _mock_general_knowledge(self, query: str) -> Dict[str, Any]:
        """Mock general knowledge base."""
        return {
            "source": "General Knowledge Base",
            "results": [
                {
                    "content": f"General information about: {query}",
                    "confidence": 0.75,
                    "metadata": {"category": "general", "authority": "high"}
                }
            ]
        }
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Process a user query using intelligent routing.
        
        Args:
            query: The user query
            
        Returns:
            Complete response with routing information and results
        """
        print(f"\n🔍 Processing query: {query}")
        
        # Step 1: Analyze the query using the intelligent router
        analysis = self.router.analyze_query_intent(query)
        query_type = analysis.get('query_type', 'unknown')
        confidence = analysis.get('confidence', 0.0)
        preferred_sources = analysis.get('preferred_sources', [])
        
        print(f"📊 Query Analysis:")
        print(f"   Type: {query_type}")
        print(f"   Confidence: {confidence:.2f}")
        print(f"   Preferred Sources: {', '.join(preferred_sources)}")
        
        # Step 2: Route to appropriate sources based on analysis
        results = []
        
        # Try preferred sources first
        for source in preferred_sources[:2]:  # Limit to top 2 sources
            if source in self._get_source_mapping():
                source_name = self._get_source_mapping()[source]
                if source_name in self.data_sources:
                    print(f"🎯 Querying {source_name}...")
                    try:
                        result = self.data_sources[source_name](query)
                        results.append(result)
                    except Exception as e:
                        print(f"⚠️  Error querying {source_name}: {e}")
        
        # Step 3: If no results, use fallback
        if not results:
            print("🔄 Using fallback strategy...")
            fallback_result = self.router.execute_fallback_strategy(query)
            if fallback_result.get('success'):
                results.append({
                    "source": "Fallback Strategy",
                    "results": fallback_result.get('results', [])
                })
        
        # Step 4: Synthesize final response
        response = self._synthesize_response(query, analysis, results)
        
        return response
    
    def _get_source_mapping(self) -> Dict[str, str]:
        """Map routing sources to actual data source methods."""
        return {
            "bedrock_knowledge_base": "bedrock_kb",
            "code_repo": "code_repo", 
            "documentation": "docs_site",
            "local_vector_db": "support_kb",
            "external_api": "general_kb"
        }
    
    def _synthesize_response(self, query: str, analysis: Dict, results: List[Dict]) -> Dict[str, Any]:
        """Synthesize the final response from multiple sources."""
        
        # Rank results by confidence
        all_results = []
        for source_result in results:
            source_name = source_result.get('source', 'Unknown')
            for result in source_result.get('results', []):
                result['source_name'] = source_name
                all_results.append(result)
        
        # Sort by confidence
        all_results.sort(key=lambda x: x.get('confidence', 0), reverse=True)
        
        # Create final response
        response = {
            "query": query,
            "routing_analysis": analysis,
            "sources_consulted": len(results),
            "total_results": len(all_results),
            "best_result": all_results[0] if all_results else None,
            "all_results": all_results[:5],  # Top 5 results
            "response_confidence": all_results[0].get('confidence', 0) if all_results else 0,
            "routing_successful": len(results) > 0
        }
        
        return response
    
    def demonstrate_routing_scenarios(self):
        """Demonstrate different routing scenarios."""
        print("=" * 80)
        print("🎯 PRODUCTION RAG SYSTEM - ROUTING DEMONSTRATION")
        print("=" * 80)
        
        scenarios = [
            {
                "query": "How do I setup AWS Bedrock Knowledge Base with my documents?",
                "description": "Technical configuration query"
            },
            {
                "query": "Show me Python code for implementing semantic search with embeddings",
                "description": "Code implementation query"
            },
            {
                "query": "My RAG system is returning irrelevant results, how can I improve it?",
                "description": "Troubleshooting query"
            },
            {
                "query": "What's the difference between FAISS and Pinecone for vector storage?",
                "description": "Product comparison query"
            },
            {
                "query": "Explain the concept of retrieval-augmented generation",
                "description": "Educational/conceptual query"
            }
        ]
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n🎯 Scenario {i}: {scenario['description']}")
            print("-" * 60)
            
            response = self.process_query(scenario['query'])
            
            print(f"\n📋 Final Response Summary:")
            print(f"   Sources Consulted: {response['sources_consulted']}")
            print(f"   Total Results: {response['total_results']}")
            print(f"   Response Confidence: {response['response_confidence']:.2f}")
            print(f"   Routing Successful: {response['routing_successful']}")
            
            if response['best_result']:
                best = response['best_result']
                print(f"   Best Result Source: {best['source_name']}")
                print(f"   Best Result Confidence: {best['confidence']:.2f}")
            
            print("\n" + "=" * 80)


def main():
    """Main function to demonstrate the production RAG system."""
    print("🚀 Production RAG System with Intelligent Query Routing")
    print()
    
    # Initialize the system
    rag_system = ProductionRAGSystem()
    
    # Run demonstration
    rag_system.demonstrate_routing_scenarios()
    
    print("\n🎉 Demonstration completed!")
    print("\nThis example shows how intelligent query routing can:")
    print("  ✅ Analyze query intent and characteristics")
    print("  ✅ Route queries to optimal data sources")
    print("  ✅ Handle multiple sources and fallback strategies")
    print("  ✅ Synthesize results for optimal user experience")
    print("  ✅ Track performance for continuous improvement")


if __name__ == "__main__":
    main()

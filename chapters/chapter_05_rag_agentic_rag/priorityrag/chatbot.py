"""
Priority-Aware Chatbot Implementation

This module implements a chatbot that uses priority-based routing to 
provide intelligent responses from multiple knowledge base sources.
"""

import boto3
import json
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

try:
    from .priority_router import PriorityBasedRouter, SourceResult
except ImportError:
    from priority_router import PriorityBasedRouter, SourceResult

logger = logging.getLogger(__name__)


class PriorityAwareChatBot:
    """
    Chatbot that uses priority-based routing for intelligent responses
    from multiple knowledge base sources.
    """
    
    def __init__(self, 
                 knowledge_base_id: str, 
                 model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0",
                 region: str = "us-east-1",
                 use_mock: bool = True):
        """
        Initialize the priority-aware chatbot.
        
        Args:
            knowledge_base_id: AWS Knowledge Base ID
            model_id: AWS Bedrock model ID for response generation
            region: AWS region
            use_mock: Whether to use mock data for demonstration
        """
        self.knowledge_base_id = knowledge_base_id
        self.model_id = model_id
        self.region = region
        self.use_mock = use_mock
        
        # Initialize the priority router
        self.router = PriorityBasedRouter(knowledge_base_id, region, use_mock)
        
        # Initialize AWS Bedrock runtime client (only if not using mock)
        if not use_mock:
            self.bedrock_runtime = boto3.client('bedrock-runtime', region_name=region)
        
        # Conversation history
        self.conversation_history = []
        
        # Response templates
        self.response_templates = {
            "no_results": "I couldn't find relevant information in the knowledge base for your query.",
            "single_source": "Based on information from {source}:",
            "multiple_sources": "Based on information from multiple sources (prioritized by relevance):",
            "high_confidence": "I'm confident this information is accurate:",
            "medium_confidence": "Here's what I found (moderate confidence):",
            "low_confidence": "I found some potentially relevant information:"
        }
    
    def generate_response(self, query: str, max_context_results: int = 5) -> Dict[str, Any]:
        """
        Generate a response using priority-based retrieval and Claude.
        
        Args:
            query: User query
            max_context_results: Maximum number of results to use for context
            
        Returns:
            Dictionary containing response, sources, and metadata
        """
        start_time = datetime.now()
        
        # Get prioritized results
        results = self.router.retrieve_with_priority(query, max_results=10)
        
        if not results:
            return {
                "response": self.response_templates["no_results"],
                "sources": [],
                "metadata": {
                    "query": query,
                    "processing_time": (datetime.now() - start_time).total_seconds(),
                    "confidence": 0.0,
                    "source_count": 0
                }
            }
        
        # Prepare context from prioritized results
        context_results = results[:max_context_results]
        context = self._prepare_context(context_results)
        
        # Determine response confidence level
        avg_confidence = sum(r.confidence for r in context_results) / len(context_results)
        confidence_level = self._get_confidence_level(avg_confidence)
        
        # Generate response
        if self.use_mock:
            response_text = self._generate_mock_response(query, context_results, context)
        else:
            response_text = self._generate_claude_response(query, context, confidence_level)
        
        # Prepare source information
        sources_info = self._prepare_sources_info(context_results)
        
        # Add to conversation history
        self.conversation_history.append({
            "query": query,
            "response": response_text,
            "sources": sources_info,
            "timestamp": datetime.now().isoformat()
        })
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return {
            "response": response_text,
            "sources": sources_info,
            "metadata": {
                "query": query,
                "processing_time": processing_time,
                "confidence": avg_confidence,
                "source_count": len(context_results),
                "routing_metrics": self.router.get_routing_metrics()
            }
        }
    
    def _prepare_context(self, results: List[SourceResult]) -> str:
        """Prepare context string from prioritized results"""
        context_parts = []
        
        for i, result in enumerate(results, 1):
            context_parts.append(
                f"Source {i} ({result.source}, Priority: {result.priority:.2f}, "
                f"Confidence: {result.confidence:.2f}):\n{result.content}"
            )
        
        return "\n\n".join(context_parts)
    
    def _get_confidence_level(self, avg_confidence: float) -> str:
        """Determine confidence level based on average confidence score"""
        if avg_confidence >= 0.8:
            return "high_confidence"
        elif avg_confidence >= 0.6:
            return "medium_confidence"
        else:
            return "low_confidence"
    
    def _generate_claude_response(self, query: str, context: str, confidence_level: str) -> str:
        """Generate response using Claude via AWS Bedrock"""
        prompt = f"""Based on the following prioritized information from our knowledge base, please provide a comprehensive answer to the user's question. Pay special attention to information from higher-priority sources.

Context:
{context}

User Question: {query}

Instructions:
- Provide a clear, accurate answer based on the information provided
- If there are conflicting information from different sources, prioritize the higher-priority sources
- Mention the source types when relevant (e.g., "According to the SDM Playbook...")
- Be concise but comprehensive
- If the information is incomplete, acknowledge this

Answer:"""
        
        try:
            response = self.bedrock_runtime.invoke_model(
                modelId=self.model_id,
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 1000,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                })
            )
            
            response_body = json.loads(response['body'].read())
            return response_body['content'][0]['text']
            
        except Exception as e:
            logger.error(f"Error generating Claude response: {e}")
            return self._generate_fallback_response(query, context)
    
    def _generate_mock_response(self, query: str, results: List[SourceResult], context: str) -> str:
        """Generate a mock response for demonstration purposes"""
        if not results:
            return self.response_templates["no_results"]
        
        # Get the highest priority source
        top_source = results[0]
        source_names = list(set(r.source for r in results))
        
        response_parts = []
        
        # Add introduction based on sources
        if len(source_names) == 1:
            response_parts.append(f"Based on information from the {top_source.source}:")
        else:
            response_parts.append(f"Based on information from multiple sources (prioritized by relevance):")
        
        # Add synthesized content
        if "template" in query.lower():
            response_parts.append(
                f"Here are the key template guidelines found:\n\n"
                f"• Use the standardized format from our Templates repository\n"
                f"• Follow the structure outlined in the {top_source.source}\n"
                f"• Ensure all required fields are completed\n"
                f"• Review with your manager before finalizing"
            )
        elif "process" in query.lower():
            response_parts.append(
                f"The process workflow includes:\n\n"
                f"1. Initial assessment and planning\n"
                f"2. Stakeholder consultation\n"
                f"3. Implementation steps as defined in {top_source.source}\n"
                f"4. Review and validation\n"
                f"5. Documentation and handover"
            )
        elif "training" in query.lower():
            response_parts.append(
                f"Available training resources:\n\n"
                f"• Online modules in the Training portal\n"
                f"• Instructor-led sessions (schedule via HR)\n"
                f"• Self-paced learning materials\n"
                f"• Mentorship program enrollment"
            )
        else:
            # Generic response based on top result
            content = top_source.content
            response_parts.append(f"{content[:200]}...")
        
        # Add source reference
        response_parts.append(f"\n📚 Primary source: {top_source.source} (Priority: {top_source.priority:.2f})")
        
        if len(source_names) > 1:
            other_sources = [s for s in source_names if s != top_source.source]
            response_parts.append(f"📋 Additional sources consulted: {', '.join(other_sources)}")
        
        return "\n".join(response_parts)
    
    def _generate_fallback_response(self, query: str, context: str) -> str:
        """Generate a fallback response when Claude fails"""
        return f"""Based on the available information in our knowledge base:

{context[:500]}...

This information is provided from our prioritized knowledge sources. For more detailed information, please consult the original documents or contact your team lead."""
    
    def _prepare_sources_info(self, results: List[SourceResult]) -> List[Dict[str, Any]]:
        """Prepare structured source information"""
        sources_info = []
        
        for result in results:
            sources_info.append({
                "source": result.source,
                "priority": result.priority,
                "confidence": result.confidence,
                "query_match_score": result.query_match_score,
                "content_preview": result.content[:100] + "..." if len(result.content) > 100 else result.content,
                "metadata": result.metadata
            })
        
        return sources_info
    
    def get_conversation_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent conversation history"""
        return self.conversation_history[-limit:]
    
    def clear_conversation_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        logger.info("Conversation history cleared")
    
    def update_priority_settings(self, new_priorities: Dict[str, float]):
        """Update priority mapping in the router"""
        self.router.update_priority_map(new_priorities)
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get comprehensive performance metrics"""
        router_metrics = self.router.get_routing_metrics()
        
        return {
            "router_metrics": router_metrics,
            "conversation_count": len(self.conversation_history),
            "active_since": datetime.now().isoformat() if self.conversation_history else None,
            "priority_map": self.router.priority_map
        }


class InteractiveChatSession:
    """Interactive chat session manager for demonstrations"""
    
    def __init__(self, chatbot: PriorityAwareChatBot):
        self.chatbot = chatbot
        self.session_active = False
    
    def start_session(self):
        """Start an interactive chat session"""
        self.session_active = True
        print("🤖 Priority-Aware Chatbot Demo")
        print("=" * 50)
        print("Ask questions about templates, processes, training, tools, or reports.")
        print("Type 'quit', 'exit', or 'bye' to end the session.")
        print("Type 'metrics' to see routing performance.")
        print("Type 'history' to see conversation history.")
        print("-" * 50)
        
        while self.session_active:
            try:
                user_input = input("\n🙋 You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    self._end_session()
                    break
                elif user_input.lower() == 'metrics':
                    self._show_metrics()
                elif user_input.lower() == 'history':
                    self._show_history()
                else:
                    self._process_query(user_input)
                    
            except KeyboardInterrupt:
                self._end_session()
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def _process_query(self, query: str):
        """Process a user query and display results"""
        print(f"\n🔍 Processing: {query}")
        print("⏳ Analyzing query and routing to appropriate sources...")
        
        result = self.chatbot.generate_response(query)
        
        print(f"\n🤖 Response:")
        print("-" * 40)
        print(result["response"])
        
        # Show source information
        if result["sources"]:
            print(f"\n📊 Sources Used:")
            for i, source in enumerate(result["sources"][:3], 1):
                print(f"{i}. {source['source']} (Priority: {source['priority']:.2f}, "
                      f"Confidence: {source['confidence']:.2f})")
        
        # Show metadata
        metadata = result["metadata"]
        print(f"\n⚡ Processing time: {metadata['processing_time']:.2f}s")
        print(f"🎯 Average confidence: {metadata['confidence']:.2f}")
    
    def _show_metrics(self):
        """Display performance metrics"""
        metrics = self.chatbot.get_performance_metrics()
        
        print("\n📈 Performance Metrics:")
        print("-" * 30)
        
        router_metrics = metrics["router_metrics"]
        print(f"Total queries: {router_metrics['total_queries']}")
        print(f"Success rate: {router_metrics['success_rate']:.2%}")
        print(f"Average confidence: {router_metrics['average_confidence']:.2f}")
        
        if router_metrics["source_usage"]:
            print("\n📚 Source Usage:")
            for source, count in router_metrics["source_usage"].items():
                print(f"  • {source}: {count} queries")
        
        print(f"\n💬 Conversations: {metrics['conversation_count']}")
    
    def _show_history(self):
        """Display conversation history"""
        history = self.chatbot.get_conversation_history(5)
        
        if not history:
            print("\n📝 No conversation history yet.")
            return
        
        print("\n📝 Recent Conversations:")
        print("-" * 40)
        
        for i, conv in enumerate(history, 1):
            print(f"\n{i}. Q: {conv['query']}")
            print(f"   A: {conv['response'][:100]}...")
            if conv['sources']:
                source_names = [s['source'] for s in conv['sources'][:2]]
                print(f"   Sources: {', '.join(source_names)}")
    
    def _end_session(self):
        """End the chat session"""
        self.session_active = False
        print("\n👋 Thanks for using the Priority-Aware Chatbot!")
        
        # Show final metrics
        metrics = self.chatbot.get_performance_metrics()
        if metrics["conversation_count"] > 0:
            print(f"\n📊 Session Summary:")
            print(f"   Conversations: {metrics['conversation_count']}")
            print(f"   Success rate: {metrics['router_metrics']['success_rate']:.2%}")
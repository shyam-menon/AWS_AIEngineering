"""
Priority-Based Knowledge Base Router

This module implements intelligent routing for AWS Knowledge Base queries
with source prioritization based on document types and content categories.
"""

import boto3
import json
import re
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SourceResult:
    """Represents a result from a knowledge base source with priority information"""
    content: str
    source: str
    priority: float
    confidence: float
    metadata: Dict[str, Any]
    query_match_score: float = 0.0
    timestamp: str = ""
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)


class PriorityBasedRouter:
    """
    Intelligent router that prioritizes knowledge base sources based on
    content type and query analysis.
    """
    
    def __init__(self, knowledge_base_id: str, region: str = 'us-east-1', use_mock: bool = True):
        """
        Initialize the priority-based router.
        
        Args:
            knowledge_base_id: AWS Knowledge Base ID
            region: AWS region
            use_mock: Whether to use mock data (for demo purposes)
        """
        self.knowledge_base_id = knowledge_base_id
        self.region = region
        self.use_mock = use_mock
        
        if not use_mock:
            self.bedrock_agent = boto3.client('bedrock-agent-runtime', region_name=region)
        
        # Priority mapping for different document sources
        self.priority_map = {
            "SDM Playbook": 1.0,      # Highest priority (playbooks)
            "Templates": 0.8,         # High priority (one-pagers)
            "Process Master Document": 0.7,  # Medium-high priority
            "Trainings": 0.6,         # Medium priority
            "Reports": 0.5,           # Medium-low priority
            "Tools": 0.4              # Lowest priority
        }
        
        # Keywords that help identify source priority based on query
        self.query_source_hints = {
            "playbook": ["SDM Playbook"],
            "template": ["Templates"],
            "one-pager": ["Templates"],
            "process": ["Process Master Document"],
            "procedure": ["SDM Playbook", "Process Master Document"],
            "training": ["Trainings"],
            "course": ["Trainings"],
            "learn": ["Trainings"],
            "report": ["Reports"],
            "analysis": ["Reports"],
            "metrics": ["Reports"],
            "tool": ["Tools"],
            "software": ["Tools"],
            "application": ["Tools"]
        }
        
        # Regex patterns for more sophisticated matching
        self.query_patterns = {
            r'how\s+to|step\s+by\s+step|guide|instruction': ["SDM Playbook", "Templates"],
            r'template|format|example': ["Templates"],
            r'process|workflow|procedure': ["Process Master Document", "SDM Playbook"],
            r'training|tutorial|course|learn': ["Trainings"],
            r'report|analysis|data|metrics|statistics': ["Reports"],
            r'tool|software|app|system': ["Tools"]
        }
        
        # Configuration parameters
        self.priority_weight = 0.6  # Weight for source priority
        self.confidence_weight = 0.3  # Weight for retrieval confidence
        self.query_match_weight = 0.1  # Weight for query matching
        
        # Tracking metrics
        self.routing_metrics = {
            "total_queries": 0,
            "successful_routes": 0,
            "source_usage": {},
            "average_confidence": 0.0,
            "query_types": {}
        }
    
    def analyze_query_for_source_preference(self, query: str) -> Tuple[List[str], Dict[str, float]]:
        """
        Analyze query to determine preferred sources based on keywords and patterns.
        
        Args:
            query: User query string
            
        Returns:
            Tuple of (preferred_sources, match_scores)
        """
        query_lower = query.lower()
        preferred_sources = []
        match_scores = {}
        
        # Check keyword-based hints
        for keyword, sources in self.query_source_hints.items():
            if keyword in query_lower:
                preferred_sources.extend(sources)
                for source in sources:
                    match_scores[source] = match_scores.get(source, 0) + 0.3
        
        # Check regex patterns
        for pattern, sources in self.query_patterns.items():
            if re.search(pattern, query_lower):
                preferred_sources.extend(sources)
                for source in sources:
                    match_scores[source] = match_scores.get(source, 0) + 0.5
        
        # Remove duplicates while preserving order
        preferred_sources = list(dict.fromkeys(preferred_sources))
        
        # Normalize match scores
        if match_scores:
            max_score = max(match_scores.values())
            match_scores = {k: v / max_score for k, v in match_scores.items()}
        
        logger.info(f"Query analysis - Preferred sources: {preferred_sources}")
        logger.info(f"Match scores: {match_scores}")
        
        return preferred_sources, match_scores
    
    def get_source_priority(self, source_name: str) -> float:
        """
        Get priority score for a given source.
        
        Args:
            source_name: Name of the source
            
        Returns:
            Priority score (0.0 to 1.0)
        """
        # Try exact match first
        if source_name in self.priority_map:
            return self.priority_map[source_name]
        
        # Try partial matching for cases where source names might vary
        for priority_source, priority in self.priority_map.items():
            if priority_source.lower() in source_name.lower():
                return priority
        
        # Default priority for unknown sources
        return 0.3
    
    def retrieve_with_priority(self, query: str, max_results: int = 10) -> List[SourceResult]:
        """
        Retrieve results from Knowledge Base and apply priority-based ranking.
        
        Args:
            query: User query
            max_results: Maximum number of results to return
            
        Returns:
            List of prioritized SourceResult objects
        """
        try:
            self.routing_metrics["total_queries"] += 1
            
            # Get preferred sources based on query analysis
            preferred_sources, match_scores = self.analyze_query_for_source_preference(query)
            
            # Retrieve from AWS Knowledge Base or use mock data
            if self.use_mock:
                raw_results = self._get_mock_results(query)
            else:
                raw_results = self._retrieve_from_aws(query, max_results * 2)
            
            results = []
            total_confidence = 0
            
            for item in raw_results:
                # Extract source information from metadata
                metadata = item.get('metadata', {})
                source_name = self._extract_source_name(metadata)
                
                # Calculate priority score
                base_priority = self.get_source_priority(source_name)
                
                # Apply query match boost
                query_match_score = match_scores.get(source_name, 0.0)
                
                # Boost priority if source matches query preference
                priority_boost = 1.3 if source_name in preferred_sources else 1.0
                final_priority = (base_priority * priority_boost) + (query_match_score * 0.2)
                
                # Get confidence score from retrieval
                confidence = item.get('score', 0.8)  # Default confidence for mock data
                total_confidence += confidence
                
                result = SourceResult(
                    content=item.get('content', {}).get('text', '') if 'content' in item else item.get('text', ''),
                    source=source_name,
                    priority=min(final_priority, 1.0),  # Cap at 1.0
                    confidence=confidence,
                    metadata=metadata,
                    query_match_score=query_match_score
                )
                results.append(result)
                
                # Update metrics
                self.routing_metrics["source_usage"][source_name] = \
                    self.routing_metrics["source_usage"].get(source_name, 0) + 1
            
            # Calculate combined score and sort
            for result in results:
                combined_score = (
                    result.priority * self.priority_weight +
                    result.confidence * self.confidence_weight +
                    result.query_match_score * self.query_match_weight
                )
                result.metadata['combined_score'] = combined_score
            
            # Sort by combined score
            results.sort(key=lambda x: x.metadata.get('combined_score', 0), reverse=True)
            
            # Update metrics
            if results:
                self.routing_metrics["successful_routes"] += 1
                self.routing_metrics["average_confidence"] = total_confidence / len(results)
            
            return results[:max_results]
            
        except Exception as e:
            logger.error(f"Error retrieving from Knowledge Base: {e}")
            return []
    
    def _retrieve_from_aws(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Retrieve results from AWS Bedrock Knowledge Base"""
        response = self.bedrock_agent.retrieve(
            knowledgeBaseId=self.knowledge_base_id,
            retrievalQuery={
                'text': query
            },
            retrievalConfiguration={
                'vectorSearchConfiguration': {
                    'numberOfResults': max_results
                }
            }
        )
        return response.get('retrievalResults', [])
    
    def _get_mock_results(self, query: str) -> List[Dict[str, Any]]:
        """Generate mock results for demonstration purposes"""
        try:
            from .data.mock_knowledge_base import get_mock_results
        except ImportError:
            from data.mock_knowledge_base import get_mock_results
        return get_mock_results(query)
    
    def _extract_source_name(self, metadata: Dict[str, Any]) -> str:
        """
        Extract source name from metadata.
        
        Args:
            metadata: Metadata dictionary from knowledge base result
            
        Returns:
            Source name string
        """
        # Common metadata fields that might contain source information
        possible_fields = ['source', 'x-amz-bedrock-kb-source-uri', 'document_type', 'category', 'source_type']
        
        for field in possible_fields:
            if field in metadata:
                source_value = metadata[field]
                # Extract meaningful source name from path or URI
                if isinstance(source_value, str):
                    # Handle S3 URIs or file paths
                    if '/' in source_value:
                        source_value = source_value.split('/')[-1]
                    # Remove file extensions
                    source_value = re.sub(r'\.[^.]+$', '', source_value)
                    
                    # Map to known source categories
                    for source_key in self.priority_map.keys():
                        if source_key.lower() in source_value.lower():
                            return source_key
                    
                    return source_value.title()
        
        return "Unknown Source"
    
    def format_prioritized_response(self, results: List[SourceResult], query: str) -> str:
        """
        Format the results into a comprehensive response.
        
        Args:
            results: List of SourceResult objects
            query: Original query
            
        Returns:
            Formatted response string
        """
        if not results:
            return "I couldn't find relevant information in the knowledge base."
        
        response_parts = []
        
        # Group results by source for better organization
        source_groups = {}
        for result in results:
            if result.source not in source_groups:
                source_groups[result.source] = []
            source_groups[result.source].append(result)
        
        # Sort source groups by highest priority in each group
        sorted_sources = sorted(source_groups.items(), 
                              key=lambda x: max(r.priority for r in x[1]), 
                              reverse=True)
        
        response_parts.append(f"📋 Query: '{query}'\n")
        response_parts.append("🎯 Prioritized Results:\n")
        
        for source_name, source_results in sorted_sources:
            priority = source_results[0].priority
            confidence = source_results[0].confidence
            
            response_parts.append(f"\n**{source_name}** (Priority: {priority:.2f}, Confidence: {confidence:.2f}):")
            
            for i, result in enumerate(source_results[:2], 1):  # Limit to top 2 per source
                content_preview = result.content[:250] + "..." if len(result.content) > 250 else result.content
                response_parts.append(f"\n{i}. {content_preview}")
                response_parts.append(f"   📊 Combined Score: {result.metadata.get('combined_score', 0):.3f}")
        
        return "\n".join(response_parts)
    
    def get_routing_metrics(self) -> Dict[str, Any]:
        """Get current routing performance metrics"""
        success_rate = (
            self.routing_metrics["successful_routes"] / self.routing_metrics["total_queries"]
            if self.routing_metrics["total_queries"] > 0 else 0
        )
        
        return {
            **self.routing_metrics,
            "success_rate": success_rate,
            "priority_map": self.priority_map
        }
    
    def update_priority_map(self, new_priorities: Dict[str, float]):
        """Update the priority mapping"""
        self.priority_map.update(new_priorities)
        logger.info(f"Updated priority map: {self.priority_map}")
    
    def reset_metrics(self):
        """Reset routing metrics"""
        self.routing_metrics = {
            "total_queries": 0,
            "successful_routes": 0,
            "source_usage": {},
            "average_confidence": 0.0,
            "query_types": {}
        }
        logger.info("Routing metrics reset")
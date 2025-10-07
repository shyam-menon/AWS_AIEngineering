"""
Utility Functions for Priority-Based RAG System

This module provides utility functions for logging, metrics, visualization,
and other helper functionality.
"""

import time
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import asdict
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict, Counter


class PerformanceTracker:
    """Track and analyze performance metrics for the routing system"""
    
    def __init__(self):
        self.metrics = {
            "queries": [],
            "response_times": [],
            "source_usage": defaultdict(int),
            "confidence_scores": [],
            "priority_distribution": defaultdict(list),
            "query_types": defaultdict(int)
        }
        self.start_time = datetime.now()
    
    def record_query(self, 
                    query: str, 
                    response_time: float, 
                    sources_used: List[str], 
                    avg_confidence: float,
                    avg_priority: float,
                    query_type: str = "general"):
        """Record a query and its performance metrics"""
        timestamp = datetime.now()
        
        self.metrics["queries"].append({
            "timestamp": timestamp.isoformat(),
            "query": query,
            "response_time": response_time,
            "sources_used": sources_used,
            "avg_confidence": avg_confidence,
            "avg_priority": avg_priority,
            "query_type": query_type
        })
        
        self.metrics["response_times"].append(response_time)
        self.metrics["confidence_scores"].append(avg_confidence)
        self.metrics["query_types"][query_type] += 1
        
        for source in sources_used:
            self.metrics["source_usage"][source] += 1
            self.metrics["priority_distribution"][source].append(avg_priority)
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """Get summary statistics"""
        if not self.metrics["queries"]:
            return {"status": "No data available"}
        
        return {
            "total_queries": len(self.metrics["queries"]),
            "avg_response_time": sum(self.metrics["response_times"]) / len(self.metrics["response_times"]),
            "min_response_time": min(self.metrics["response_times"]),
            "max_response_time": max(self.metrics["response_times"]),
            "avg_confidence": sum(self.metrics["confidence_scores"]) / len(self.metrics["confidence_scores"]),
            "most_used_source": max(self.metrics["source_usage"], key=self.metrics["source_usage"].get) if self.metrics["source_usage"] else None,
            "query_type_distribution": dict(self.metrics["query_types"]),
            "uptime": str(datetime.now() - self.start_time)
        }
    
    def generate_report(self) -> str:
        """Generate a formatted performance report"""
        stats = self.get_summary_stats()
        
        if "status" in stats:
            return stats["status"]
        
        report_lines = [
            "🚀 PRIORITY RAG PERFORMANCE REPORT",
            "=" * 40,
            f"📊 Total Queries: {stats['total_queries']}",
            f"⏱️  Average Response Time: {stats['avg_response_time']:.2f}s",
            f"⚡ Fastest Response: {stats['min_response_time']:.2f}s",
            f"🐌 Slowest Response: {stats['max_response_time']:.2f}s",
            f"🎯 Average Confidence: {stats['avg_confidence']:.2f}",
            f"📈 System Uptime: {stats['uptime']}",
            "",
            "📚 SOURCE USAGE:",
            "-" * 20
        ]
        
        for source, count in sorted(self.metrics["source_usage"].items(), key=lambda x: x[1], reverse=True):
            percentage = (count / stats['total_queries']) * 100
            report_lines.append(f"  {source}: {count} queries ({percentage:.1f}%)")
        
        if self.metrics["query_types"]:
            report_lines.extend([
                "",
                "🔍 QUERY TYPES:",
                "-" * 15
            ])
            for query_type, count in sorted(self.metrics["query_types"].items(), key=lambda x: x[1], reverse=True):
                percentage = (count / stats['total_queries']) * 100
                report_lines.append(f"  {query_type}: {count} queries ({percentage:.1f}%)")
        
        return "\n".join(report_lines)
    
    def export_data(self, file_path: str):
        """Export metrics data to JSON file"""
        export_data = {
            "summary": self.get_summary_stats(),
            "detailed_metrics": self.metrics,
            "export_timestamp": datetime.now().isoformat()
        }
        
        # Convert defaultdict to regular dict for JSON serialization
        export_data["detailed_metrics"]["source_usage"] = dict(self.metrics["source_usage"])
        export_data["detailed_metrics"]["priority_distribution"] = dict(self.metrics["priority_distribution"])
        export_data["detailed_metrics"]["query_types"] = dict(self.metrics["query_types"])
        
        with open(file_path, 'w') as f:
            json.dump(export_data, f, indent=2)


class QueryAnalyzer:
    """Analyze queries to extract insights and patterns"""
    
    @staticmethod
    def classify_query_intent(query: str) -> Dict[str, Any]:
        """Classify the intent of a query"""
        query_lower = query.lower()
        
        intent_patterns = {
            "information_seeking": ["what", "how", "why", "when", "where", "explain", "tell me"],
            "action_oriented": ["create", "make", "build", "generate", "setup", "configure"],
            "comparison": ["compare", "difference", "versus", "vs", "better", "best"],
            "troubleshooting": ["error", "problem", "issue", "fix", "debug", "not working"],
            "template_request": ["template", "format", "example", "sample"],
            "process_inquiry": ["process", "procedure", "workflow", "steps"]
        }
        
        intent_scores = {}
        for intent, patterns in intent_patterns.items():
            score = sum(1 for pattern in patterns if pattern in query_lower)
            if score > 0:
                intent_scores[intent] = score / len(patterns)
        
        primary_intent = max(intent_scores, key=intent_scores.get) if intent_scores else "general"
        
        return {
            "primary_intent": primary_intent,
            "intent_scores": intent_scores,
            "query_length": len(query.split()),
            "contains_question_words": any(word in query_lower for word in ["what", "how", "why", "when", "where"])
        }
    
    @staticmethod
    def extract_key_entities(query: str) -> List[str]:
        """Extract key entities/concepts from a query"""
        # Simple keyword extraction (in practice, you might use NLP libraries)
        
        # Remove common stop words
        stop_words = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", 
            "of", "with", "by", "is", "are", "was", "were", "be", "been", "have", 
            "has", "had", "do", "does", "did", "will", "would", "could", "should",
            "can", "may", "might", "must", "i", "you", "he", "she", "it", "we", "they"
        }
        
        # Important domain-specific terms
        important_terms = {
            "template", "process", "training", "report", "tool", "playbook",
            "project", "management", "development", "security", "analytics",
            "documentation", "workflow", "procedure", "guideline"
        }
        
        words = query.lower().split()
        entities = []
        
        for word in words:
            # Remove punctuation
            clean_word = ''.join(char for char in word if char.isalnum())
            
            # Keep important terms or longer words not in stop words
            if clean_word in important_terms or (len(clean_word) > 3 and clean_word not in stop_words):
                entities.append(clean_word)
        
        return list(set(entities))  # Remove duplicates


class ResultsFormatter:
    """Format and present results in various ways"""
    
    @staticmethod
    def format_results_table(results: List[Dict[str, Any]]) -> str:
        """Format results as a text table"""
        if not results:
            return "No results to display."
        
        # Extract key information
        table_data = []
        for i, result in enumerate(results, 1):
            table_data.append([
                str(i),
                result.get("source", "Unknown")[:20],
                f"{result.get('priority', 0):.2f}",
                f"{result.get('confidence', 0):.2f}",
                result.get("content", "")[:50] + "..."
            ])
        
        # Create table
        headers = ["#", "Source", "Priority", "Confidence", "Content Preview"]
        col_widths = [3, 22, 10, 12, 52]
        
        # Header row
        header_row = "|".join(h.ljust(w) for h, w in zip(headers, col_widths))
        separator = "|".join("-" * w for w in col_widths)
        
        # Data rows
        data_rows = []
        for row in table_data:
            data_row = "|".join(str(cell).ljust(w) for cell, w in zip(row, col_widths))
            data_rows.append(data_row)
        
        return "\n".join([header_row, separator] + data_rows)
    
    @staticmethod
    def format_results_json(results: List[Dict[str, Any]], pretty: bool = True) -> str:
        """Format results as JSON"""
        indent = 2 if pretty else None
        return json.dumps(results, indent=indent, default=str)
    
    @staticmethod
    def format_source_summary(results: List[Dict[str, Any]]) -> str:
        """Format a summary by source"""
        if not results:
            return "No results to summarize."
        
        source_groups = defaultdict(list)
        for result in results:
            source = result.get("source", "Unknown")
            source_groups[source].append(result)
        
        summary_lines = ["📊 RESULTS BY SOURCE:", "=" * 25]
        
        for source, source_results in sorted(source_groups.items()):
            avg_priority = sum(r.get("priority", 0) for r in source_results) / len(source_results)
            avg_confidence = sum(r.get("confidence", 0) for r in source_results) / len(source_results)
            
            summary_lines.append(f"\n📚 {source} ({len(source_results)} results)")
            summary_lines.append(f"   Average Priority: {avg_priority:.2f}")
            summary_lines.append(f"   Average Confidence: {avg_confidence:.2f}")
            
            for i, result in enumerate(source_results[:2], 1):  # Show top 2 per source
                content_preview = result.get("content", "")[:100] + "..."
                summary_lines.append(f"   {i}. {content_preview}")
        
        return "\n".join(summary_lines)


class Logger:
    """Enhanced logging for the priority RAG system"""
    
    def __init__(self, name: str = "PriorityRAG", level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console handler
        if not self.logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
    
    def log_query(self, query: str, source_preferences: List[str]):
        """Log query processing"""
        self.logger.info(f"Processing query: '{query[:50]}...' | Preferred sources: {source_preferences}")
    
    def log_routing_decision(self, source: str, priority: float, confidence: float):
        """Log routing decisions"""
        self.logger.info(f"Routing to {source} | Priority: {priority:.2f} | Confidence: {confidence:.2f}")
    
    def log_performance(self, response_time: float, source_count: int):
        """Log performance metrics"""
        self.logger.info(f"Response generated in {response_time:.2f}s using {source_count} sources")
    
    def log_error(self, error: Exception, context: str = ""):
        """Log errors with context"""
        self.logger.error(f"Error in {context}: {str(error)}")


# Utility functions
def calculate_relevance_score(query: str, content: str) -> float:
    """Calculate relevance score between query and content"""
    query_terms = set(query.lower().split())
    content_terms = set(content.lower().split())
    
    if not query_terms:
        return 0.0
    
    # Simple Jaccard similarity
    intersection = len(query_terms.intersection(content_terms))
    union = len(query_terms.union(content_terms))
    
    return intersection / union if union > 0 else 0.0


def time_function(func):
    """Decorator to time function execution"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        execution_time = end_time - start_time
        print(f"⏱️ {func.__name__} executed in {execution_time:.4f} seconds")
        
        return result
    return wrapper


def validate_priority_map(priority_map: Dict[str, float]) -> List[str]:
    """Validate priority mapping values"""
    issues = []
    
    for source, priority in priority_map.items():
        if not isinstance(priority, (int, float)):
            issues.append(f"Priority for '{source}' must be numeric")
        elif not 0.0 <= priority <= 1.0:
            issues.append(f"Priority for '{source}' must be between 0.0 and 1.0")
    
    return issues


def normalize_source_name(source_name: str) -> str:
    """Normalize source names for consistent matching"""
    # Remove common prefixes/suffixes
    normalized = source_name.strip()
    
    # Remove file extensions
    if '.' in normalized:
        normalized = normalized.rsplit('.', 1)[0]
    
    # Remove path components
    if '/' in normalized:
        normalized = normalized.split('/')[-1]
    
    # Convert to title case
    normalized = normalized.replace('_', ' ').replace('-', ' ').title()
    
    return normalized


def create_demo_visualization(metrics_data: Dict[str, Any]) -> str:
    """Create a simple text-based visualization of metrics"""
    if not metrics_data or "source_usage" not in metrics_data:
        return "No data available for visualization."
    
    source_usage = metrics_data["source_usage"]
    total_queries = sum(source_usage.values())
    
    if total_queries == 0:
        return "No queries processed yet."
    
    viz_lines = ["📊 SOURCE USAGE VISUALIZATION", "=" * 35]
    
    # Create simple bar chart using text
    max_count = max(source_usage.values())
    for source, count in sorted(source_usage.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_queries) * 100
        bar_length = int((count / max_count) * 30) if max_count > 0 else 0
        bar = "█" * bar_length + "░" * (30 - bar_length)
        
        viz_lines.append(f"{source[:20]:20} |{bar}| {count:3d} ({percentage:5.1f}%)")
    
    viz_lines.append(f"\nTotal queries: {total_queries}")
    
    return "\n".join(viz_lines)
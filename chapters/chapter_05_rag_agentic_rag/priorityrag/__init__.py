"""
Priority-Based RAG System

This package implements an intelligent query routing system for AWS Knowledge Base
that prioritizes sources based on document types and query analysis.
"""

__version__ = "1.0.0"
__author__ = "AI Engineering Team"

# Main exports
from .priority_router import PriorityBasedRouter, SourceResult
from .chatbot import PriorityAwareChatBot, InteractiveChatSession
from .utils.config import RouterConfig, ConfigManager
from .utils.helpers import PerformanceTracker, QueryAnalyzer, ResultsFormatter

__all__ = [
    "PriorityBasedRouter",
    "SourceResult", 
    "PriorityAwareChatBot",
    "InteractiveChatSession",
    "RouterConfig",
    "ConfigManager",
    "PerformanceTracker",
    "QueryAnalyzer", 
    "ResultsFormatter"
]
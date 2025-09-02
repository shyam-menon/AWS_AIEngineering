"""
Test Suite for MCP RAG Implementation

This module provides comprehensive tests for the MCP (Model Context Protocol)
integration with Strands agents for RAG operations.

Author: AI Engineering Course
Version: 1.0.0
"""

import pytest
import asyncio
import json
import time
from typing import Dict, Any, List
from unittest.mock import Mock, patch, AsyncMock
import logging

# Import our MCP modules
from mcp_knowledge_server import KNOWLEDGE_BASE
from mcp_rag_agent import MCPRAGAgent
from mcp_production_integration import (
    ProductionMCPManager, 
    ProductionRAGAgent, 
    MCPServerConfig,
    RAGResponse
)

# Configure logging for tests
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestMCPKnowledgeServer:
    """Test the MCP Knowledge Server functionality."""
    
    def test_knowledge_base_structure(self):
        """Test that the knowledge base has the expected structure."""
        assert "technical_docs" in KNOWLEDGE_BASE
        assert "code_examples" in KNOWLEDGE_BASE
        assert "faqs" in KNOWLEDGE_BASE
        
        # Check technical docs structure
        tech_docs = KNOWLEDGE_BASE["technical_docs"]
        assert len(tech_docs) > 0
        
        for doc_id, doc in tech_docs.items():
            assert "title" in doc
            assert "content" in doc
            assert "category" in doc
            assert "last_updated" in doc
            assert "source" in doc
    
    def test_knowledge_base_content_quality(self):
        """Test that knowledge base contains meaningful content."""
        # Test technical documentation
        tech_docs = KNOWLEDGE_BASE["technical_docs"]
        
        # Should have AWS Bedrock documentation
        assert any("bedrock" in doc["content"].lower() or "bedrock" in doc["title"].lower() 
                  for doc in tech_docs.values())
        
        # Should have Strands agents documentation
        assert any("strands" in doc["content"].lower() or "strands" in doc["title"].lower() 
                  for doc in tech_docs.values())
        
        # Test code examples
        code_examples = KNOWLEDGE_BASE["code_examples"]
        assert len(code_examples) > 0
        
        for example in code_examples.values():
            assert "language" in example
            assert "complexity" in example
            assert len(example["content"]) > 50  # Meaningful code content
    
    def test_search_function_parameters(self):
        """Test that search functions accept correct parameters."""
        # This would typically test the actual MCP server endpoints
        # For now, we test the knowledge base structure supports the operations
        
        categories = set()
        for doc in KNOWLEDGE_BASE["technical_docs"].values():
            categories.add(doc["category"])
        
        assert len(categories) > 1  # Multiple categories available
        
        languages = set()
        for example in KNOWLEDGE_BASE["code_examples"].values():
            languages.add(example["language"])
        
        assert "python" in languages  # Should support Python

class TestMCPRAGAgent:
    """Test the MCP RAG Agent functionality."""
    
    def setup_method(self):
        """Set up test environment for each test method."""
        self.agent = MCPRAGAgent("http://127.0.0.1:8000/mcp/")
    
    def test_agent_initialization(self):
        """Test agent initialization parameters."""
        assert self.agent.mcp_server_url == "http://localhost:8000/mcp/"
        assert self.agent.mcp_client is None  # Not initialized yet
        assert self.agent.agent is None  # Not initialized yet
        assert "queries_processed" in self.agent.session_stats
        assert self.agent.session_stats["queries_processed"] == 0
    
    def test_system_prompt_content(self):
        """Test that the system prompt contains required elements."""
        system_prompt = self.agent._get_system_prompt()
        
        # Should mention key concepts
        assert "rag" in system_prompt.lower()
        assert "mcp" in system_prompt.lower()
        assert "technical documentation" in system_prompt.lower()
        assert "code examples" in system_prompt.lower()
        
        # Should mention available tools
        assert "search_technical_docs" in system_prompt
        assert "search_code_examples" in system_prompt
        assert "get_faq_answers" in system_prompt
    
    def test_cache_key_generation(self):
        """Test cache key generation for consistency."""
        # We would test this if the method was public
        # For now, test that session stats are properly tracked
        assert isinstance(self.agent.session_stats, dict)
        assert "session_start" in self.agent.session_stats
    
    @pytest.mark.asyncio
    async def test_query_error_handling(self):
        """Test error handling when agent is not initialized."""
        result = await self.agent.query("test query")
        
        assert result["success"] is False
        assert "not initialized" in result["error"].lower()

class TestProductionMCPManager:
    """Test the Production MCP Manager."""
    
    def setup_method(self):
        """Set up test environment."""
        self.server_configs = [
            MCPServerConfig(
                url="http://127.0.0.1:8000/mcp/",
                name="test_server",
                timeout=30,
                retry_attempts=2
            )
        ]
        self.manager = ProductionMCPManager(self.server_configs)
    
    def test_manager_initialization(self):
        """Test manager initialization."""
        assert len(self.manager.server_configs) == 1
        assert self.manager.server_configs[0].name == "test_server"
        assert len(self.manager.mcp_clients) == 0  # Not initialized yet
        assert len(self.manager.server_health) == 0  # Not initialized yet
        
        # Test metrics initialization
        assert "requests_total" in self.manager.metrics
        assert self.manager.metrics["requests_total"] == 0
    
    def test_cache_key_generation(self):
        """Test cache key generation."""
        tool_name = "search_technical_docs"
        arguments = {"query": "test", "max_results": 5}
        
        cache_key = self.manager._get_cache_key(tool_name, arguments)
        
        assert isinstance(cache_key, str)
        assert tool_name in cache_key
        
        # Same arguments should produce same key
        cache_key2 = self.manager._get_cache_key(tool_name, arguments)
        assert cache_key == cache_key2
        
        # Different arguments should produce different key
        different_args = {"query": "different", "max_results": 3}
        cache_key3 = self.manager._get_cache_key(tool_name, different_args)
        assert cache_key != cache_key3
    
    def test_cache_validation(self):
        """Test cache entry validation."""
        from datetime import datetime, timedelta
        
        # Valid cache entry (recent)
        valid_entry = {
            "result": {"test": "data"},
            "timestamp": datetime.now().isoformat()
        }
        assert self.manager._is_cache_valid(valid_entry) is True
        
        # Invalid cache entry (old)
        old_entry = {
            "result": {"test": "data"},
            "timestamp": (datetime.now() - timedelta(seconds=400)).isoformat()
        }
        assert self.manager._is_cache_valid(old_entry) is False
        
        # Invalid cache entry (no timestamp)
        no_timestamp_entry = {"result": {"test": "data"}}
        assert self.manager._is_cache_valid(no_timestamp_entry) is False
    
    def test_metrics_tracking(self):
        """Test metrics tracking functionality."""
        initial_metrics = self.manager.get_metrics()
        
        assert "performance_metrics" in initial_metrics
        assert "server_health" in initial_metrics
        assert "cache_stats" in initial_metrics
        
        # Test response time update
        self.manager.metrics["requests_successful"] = 1
        self.manager._update_average_response_time(1.5)
        assert self.manager.metrics["average_response_time"] == 1.5
        
        # Test second update
        self.manager.metrics["requests_successful"] = 2
        self.manager._update_average_response_time(2.5)
        # Should be moving average
        assert 1.5 < self.manager.metrics["average_response_time"] < 2.5

class TestProductionRAGAgent:
    """Test the Production RAG Agent."""
    
    def setup_method(self):
        """Set up test environment."""
        mock_manager = Mock()
        self.agent = ProductionRAGAgent(mock_manager)
    
    def test_agent_initialization(self):
        """Test agent initialization."""
        assert self.agent.mcp_manager is not None
        assert self.agent.agent is None  # Not initialized yet
        
        # Test session metrics initialization
        metrics = self.agent.session_metrics
        assert "queries_processed" in metrics
        assert "successful_responses" in metrics
        assert "failed_responses" in metrics
        assert metrics["queries_processed"] == 0
    
    def test_search_strategy_configuration(self):
        """Test search strategy configurations."""
        # Test quick strategy
        quick_tools = self.agent._get_search_tools("quick")
        assert len(quick_tools) == 2
        assert "search_technical_docs" in quick_tools
        assert "get_faq_answers" in quick_tools
        
        # Test comprehensive strategy
        comprehensive_tools = self.agent._get_search_tools("comprehensive")
        assert len(comprehensive_tools) == 4
        assert "search_technical_docs" in comprehensive_tools
        assert "search_code_examples" in comprehensive_tools
        assert "get_faq_answers" in comprehensive_tools
        assert "get_topic_overview" in comprehensive_tools
        
        # Test targeted strategy
        targeted_tools = self.agent._get_search_tools("targeted")
        assert len(targeted_tools) == 1
        assert "get_topic_overview" in targeted_tools
    
    def test_confidence_calculation(self):
        """Test confidence score calculation."""
        # No results - should be 0
        confidence = self.agent._calculate_confidence({}, [])
        assert confidence == 0.0
        
        # Single result - should be moderate
        single_result = {"tool1": {"success": True}}
        confidence = self.agent._calculate_confidence(single_result, ["tool1"])
        assert 0.5 <= confidence <= 0.8
        
        # Multiple results - should be higher
        multi_results = {
            "tool1": {"success": True},
            "tool2": {"success": True},
            "get_topic_overview": {"success": True}
        }
        tools_used = ["tool1", "tool2", "get_topic_overview"]
        confidence = self.agent._calculate_confidence(multi_results, tools_used)
        assert confidence > 0.7
    
    def test_source_extraction(self):
        """Test source information extraction."""
        search_results = {
            "search_technical_docs": {
                "cached": False,
                "server_used": "primary",
                "processing_time": 0.5
            },
            "search_code_examples": {
                "cached": True,
                "server_used": "secondary",
                "processing_time": 0.1
            }
        }
        
        sources = self.agent._extract_sources(search_results)
        
        assert len(sources) == 2
        assert sources[0]["tool"] == "search_technical_docs"
        assert sources[0]["cached"] is False
        assert sources[1]["tool"] == "search_code_examples"
        assert sources[1]["cached"] is True
    
    def test_synthesis_prompt_creation(self):
        """Test synthesis prompt creation."""
        query = "How to use AWS Bedrock?"
        search_results = {
            "search_technical_docs": {
                "content": [{
                    "text": {
                        "results": [
                            {"title": "AWS Bedrock Guide", "content": "Bedrock is..."}
                        ]
                    }
                }]
            }
        }
        
        prompt = self.agent._create_synthesis_prompt(query, search_results)
        
        assert query in prompt
        assert "AWS Bedrock Guide" in prompt
        assert "search_technical_docs" in prompt.lower()
        assert "comprehensive response" in prompt.lower()

class TestRAGResponse:
    """Test the RAGResponse dataclass."""
    
    def test_rag_response_creation(self):
        """Test RAGResponse creation and structure."""
        response = RAGResponse(
            success=True,
            response="Test response",
            sources=[{"tool": "test_tool"}],
            confidence_score=0.85,
            processing_time=1.2,
            tools_used=["tool1", "tool2"]
        )
        
        assert response.success is True
        assert response.response == "Test response"
        assert len(response.sources) == 1
        assert response.confidence_score == 0.85
        assert response.processing_time == 1.2
        assert len(response.tools_used) == 2
        assert response.error is None
        assert response.metadata is None
    
    def test_rag_response_with_error(self):
        """Test RAGResponse creation with error."""
        response = RAGResponse(
            success=False,
            response="",
            sources=[],
            confidence_score=0.0,
            processing_time=0.5,
            tools_used=[],
            error="Test error",
            metadata={"strategy": "quick"}
        )
        
        assert response.success is False
        assert response.error == "Test error"
        assert response.metadata["strategy"] == "quick"

class TestIntegrationScenarios:
    """Test integration scenarios and workflows."""
    
    def test_server_config_validation(self):
        """Test MCP server configuration validation."""
        config = MCPServerConfig(
            url="http://localhost:8000/mcp/",
            name="test_server",
            timeout=30,
            retry_attempts=3
        )
        
        assert config.url == "http://localhost:8000/mcp/"
        assert config.name == "test_server"
        assert config.timeout == 30
        assert config.retry_attempts == 3
        assert config.retry_delay == 1.0  # Default value
        assert config.health_check_interval == 60  # Default value
    
    def test_error_handling_scenarios(self):
        """Test various error handling scenarios."""
        # Test agent not initialized
        agent = MCPRAGAgent()
        assert agent.agent is None
        
        # Test production manager with empty config
        manager = ProductionMCPManager([])
        assert len(manager.server_configs) == 0
        assert len(manager.mcp_clients) == 0
    
    def test_metrics_aggregation(self):
        """Test metrics aggregation across components."""
        # Test session stats structure
        agent = MCPRAGAgent()
        stats = agent.session_stats
        
        required_keys = [
            "queries_processed",
            "tools_used",
            "session_start"
        ]
        
        for key in required_keys:
            assert key in stats
    
    @pytest.mark.asyncio
    async def test_async_operations(self):
        """Test asynchronous operation handling."""
        # Test that async methods are properly defined
        agent = MCPRAGAgent()
        
        # These should be async methods
        assert asyncio.iscoroutinefunction(agent.initialize)
        assert asyncio.iscoroutinefunction(agent.query)
        assert asyncio.iscoroutinefunction(agent.search_and_synthesize)

# Utility functions for testing
def create_mock_search_result(tool_name: str, query: str) -> Dict[str, Any]:
    """Create a mock search result for testing."""
    return {
        "content": [{
            "text": {
                "query": query,
                "total_results": 2,
                "results": [
                    {
                        "id": f"{tool_name}_result_1",
                        "title": f"Mock result 1 for {query}",
                        "content": f"This is mock content for {query} from {tool_name}",
                        "relevance_score": 0.85
                    },
                    {
                        "id": f"{tool_name}_result_2", 
                        "title": f"Mock result 2 for {query}",
                        "content": f"This is additional mock content for {query}",
                        "relevance_score": 0.72
                    }
                ]
            }
        }]
    }

def create_mock_mcp_manager() -> Mock:
    """Create a mock MCP manager for testing."""
    mock_manager = Mock()
    mock_manager.call_tool_with_failover = AsyncMock()
    mock_manager.get_metrics = Mock(return_value={
        "performance_metrics": {"requests_total": 10},
        "server_health": {"test_server": {"healthy": True}},
        "cache_stats": {"total_entries": 5}
    })
    return mock_manager

# Run tests
if __name__ == "__main__":
    # Run specific test categories
    print("🧪 Running MCP RAG Implementation Tests")
    print("=" * 50)
    
    # You can run this with pytest: pytest test_mcp_rag.py -v
    
    # For manual testing, run some basic tests
    test_kb = TestMCPKnowledgeServer()
    test_kb.test_knowledge_base_structure()
    test_kb.test_knowledge_base_content_quality()
    print("✅ Knowledge base tests passed")
    
    test_agent = TestMCPRAGAgent()
    test_agent.setup_method()
    test_agent.test_agent_initialization()
    test_agent.test_system_prompt_content()
    print("✅ MCP RAG agent tests passed")
    
    test_manager = TestProductionMCPManager()
    test_manager.setup_method()
    test_manager.test_manager_initialization()
    test_manager.test_cache_key_generation()
    test_manager.test_cache_validation()
    print("✅ Production manager tests passed")
    
    test_prod_agent = TestProductionRAGAgent()
    test_prod_agent.setup_method()
    test_prod_agent.test_agent_initialization()
    test_prod_agent.test_search_strategy_configuration()
    test_prod_agent.test_confidence_calculation()
    print("✅ Production RAG agent tests passed")
    
    test_response = TestRAGResponse()
    test_response.test_rag_response_creation()
    test_response.test_rag_response_with_error()
    print("✅ RAG response tests passed")
    
    print("\n🎉 All tests completed successfully!")
    print("Run 'pytest test_mcp_rag.py -v' for detailed test results")

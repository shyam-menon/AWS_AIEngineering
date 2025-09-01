"""
Test suite for RAG Demo - AWS AI Engineering Course

This module provides unit tests for the RAG implementation components
that can run without AWS credentials or expensive API calls.

Run with: python -m pytest tests/
"""

import pytest
import numpy as np
from unittest.mock import Mock, patch, MagicMock
import json
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import (
    load_environment, safe_json_parse, format_sources, 
    print_error, print_success, print_info
)

# Only import FAISS-dependent functions if available
try:
    from rag_vector_local import chunk_text, format_context
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False


class TestCommonUtilities:
    """Test common utility functions."""
    
    def test_safe_json_parse_valid(self):
        """Test JSON parsing with valid JSON."""
        valid_json = '{"key": "value", "number": 42}'
        result = safe_json_parse(valid_json)
        
        assert result is not None
        assert result["key"] == "value"
        assert result["number"] == 42
    
    def test_safe_json_parse_invalid(self):
        """Test JSON parsing with invalid JSON."""
        invalid_json = '{"key": "value", "incomplete":'
        result = safe_json_parse(invalid_json)
        
        assert result is None
    
    def test_format_sources_empty(self):
        """Test source formatting with empty list."""
        result = format_sources([])
        assert result == ""
    
    def test_format_sources_with_files(self):
        """Test source formatting with file sources."""
        sources = [
            {"file": "test1.md", "snippet": "This is a test snippet"},
            {"file": "test2.md", "snippet": "Another test snippet"}
        ]
        
        result = format_sources(sources)
        
        assert "Sources:" in result
        assert "[1] test1.md" in result
        assert "[2] test2.md" in result
        assert "This is a test snippet" in result
    
    def test_format_sources_with_s3_uris(self):
        """Test source formatting with S3 sources."""
        sources = [
            {"s3_uri": "s3://bucket/doc1.md", "snippet": "S3 content"}
        ]
        
        result = format_sources(sources)
        
        assert "Sources:" in result
        assert "[1] s3://bucket/doc1.md" in result
        assert "S3 content" in result


@pytest.mark.skipif(not FAISS_AVAILABLE, reason="FAISS not available")
class TestLocalRAGComponents:
    """Test local RAG implementation components."""
    
    def test_chunk_text_basic(self):
        """Test basic text chunking."""
        text = "This is a test. " * 100  # Create long text
        chunks = chunk_text(text, chunk_size=50, overlap=10)
        
        assert len(chunks) > 1
        assert all(isinstance(chunk, str) for chunk in chunks)
        assert all(len(chunk.strip()) > 0 for chunk in chunks)
    
    def test_chunk_text_short(self):
        """Test chunking with text shorter than chunk size."""
        text = "Short text"
        chunks = chunk_text(text, chunk_size=100, overlap=20)
        
        assert len(chunks) == 1
        assert chunks[0].strip() == text
    
    def test_format_context_empty(self):
        """Test context formatting with empty results."""
        results = []
        sources = []
        
        context, source_info = format_context(results, sources)
        
        assert context == "No relevant information found."
        assert source_info == []
    
    def test_format_context_with_results(self):
        """Test context formatting with search results."""
        # Mock search results
        results = [
            (0, 0.95, {"text": "First chunk content", "preview": "First chunk..."}),
            (1, 0.88, {"text": "Second chunk content", "preview": "Second chunk..."})
        ]
        
        # Mock sources
        sources = [
            ("doc1.md", "First chunk content is here"),
            ("doc2.md", "Second chunk content is here")
        ]
        
        context, source_info = format_context(results, sources)
        
        assert "First chunk content" in context
        assert "Second chunk content" in context
        assert len(source_info) == 2
        assert source_info[0]["similarity_score"] == 0.95


class TestConfigurationLoading:
    """Test configuration and environment loading."""
    
    @patch.dict(os.environ, {
        'AWS_REGION': 'us-west-2',
        'BEDROCK_EMBED_MODEL_ID': 'test-embed-model',
        'CHUNK_SIZE': '1000'
    })
    def test_load_environment_from_env_vars(self):
        """Test loading configuration from environment variables."""
        config = load_environment()
        
        assert config['aws_region'] == 'us-west-2'
        assert config['embed_model_id'] == 'test-embed-model'
        assert config['chunk_size'] == 1000
    
    def test_load_environment_defaults(self):
        """Test loading configuration with defaults."""
        # Clear any existing environment variables
        env_vars_to_clear = [
            'AWS_REGION', 'BEDROCK_EMBED_MODEL_ID', 'BEDROCK_CHAT_MODEL_ID',
            'CHUNK_SIZE', 'CHUNK_OVERLAP', 'TOP_K_RESULTS', 'TEMPERATURE'
        ]
        
        with patch.dict(os.environ, {}, clear=True):
            config = load_environment()
        
        # Check defaults
        assert config['aws_region'] == 'us-east-1'
        assert config['embed_model_id'] == 'amazon.titan-embed-text-v2:0'
        assert config['chat_model_id'] == 'amazon.nova-lite-v1:0'
        assert config['chunk_size'] == 800
        assert config['chunk_overlap'] == 120
        assert config['top_k'] == 4
        assert config['temperature'] == 0.2


class TestErrorHandling:
    """Test error handling and logging functions."""
    
    def test_print_functions_dont_crash(self, capsys):
        """Test that print functions don't crash and produce output."""
        print_error("Test error message")
        print_success("Test success message")
        print_info("Test info message")
        
        captured = capsys.readouterr()
        
        assert "Test error message" in captured.out or "Test error message" in captured.err
        assert "Test success message" in captured.out
        assert "Test info message" in captured.out


class TestMockedAWSInteractions:
    """Test AWS interactions with mocked responses."""
    
    @patch('common.boto3.client')
    def test_create_bedrock_clients_success(self, mock_boto_client):
        """Test successful Bedrock client creation."""
        # Mock the clients
        mock_runtime = Mock()
        mock_runtime.list_foundation_models.return_value = {"modelSummaries": []}
        mock_agent_runtime = Mock()
        
        mock_boto_client.side_effect = [mock_runtime, mock_agent_runtime]
        
        from common import create_bedrock_clients
        
        clients = create_bedrock_clients("us-east-1")
        
        assert 'runtime' in clients
        assert 'agent_runtime' in clients
        assert clients['runtime'] == mock_runtime
        assert clients['agent_runtime'] == mock_agent_runtime
    
    @patch('common.boto3.client')
    def test_bedrock_embed_text_success(self, mock_boto_client):
        """Test successful embedding generation."""
        # Mock the runtime client
        mock_client = Mock()
        mock_response = {
            'body': Mock()
        }
        
        # Mock the response body
        mock_response['body'].read.return_value = json.dumps({
            'embedding': [0.1, 0.2, 0.3, 0.4]
        }).encode()
        
        mock_client.invoke_model.return_value = mock_response
        
        from common import bedrock_embed_text
        
        embeddings = bedrock_embed_text(["test text"], mock_client, "test-model")
        
        assert len(embeddings) == 1
        assert embeddings[0] == [0.1, 0.2, 0.3, 0.4]
        mock_client.invoke_model.assert_called_once()
    
    @patch('common.boto3.client')
    def test_bedrock_chat_success(self, mock_boto_client):
        """Test successful chat completion."""
        # Mock the runtime client
        mock_client = Mock()
        mock_response = {
            'body': Mock()
        }
        
        # Mock the response body
        mock_response['body'].read.return_value = json.dumps({
            'output': {
                'message': {
                    'content': [{'text': 'This is a test response'}]
                }
            }
        }).encode()
        
        mock_client.invoke_model.return_value = mock_response
        
        from common import bedrock_chat
        
        response = bedrock_chat("Test prompt", mock_client, "test-model")
        
        assert response == "This is a test response"
        mock_client.invoke_model.assert_called_once()


class TestIntegrationScenarios:
    """Test integration scenarios without actual AWS calls."""
    
    def test_complete_rag_workflow_structure(self):
        """Test that the RAG workflow components exist and are callable."""
        # This test verifies the structure exists for integration
        
        # Check common utilities
        assert callable(load_environment)
        assert callable(safe_json_parse)
        assert callable(format_sources)
        
        # Check that modules can be imported
        import common
        assert hasattr(common, 'bedrock_embed_text')
        assert hasattr(common, 'bedrock_chat')
        
        # Verify configuration loading works
        config = load_environment()
        assert isinstance(config, dict)
        assert 'aws_region' in config
        assert 'embed_model_id' in config


# Performance tests (lightweight)
class TestPerformance:
    """Test performance characteristics of non-AWS components."""
    
    @pytest.mark.skipif(not FAISS_AVAILABLE, reason="FAISS not available")
    def test_chunking_performance(self):
        """Test that text chunking performs reasonably."""
        # Create a moderately large text
        text = "This is a test sentence. " * 1000  # ~25KB
        
        import time
        start_time = time.time()
        
        chunks = chunk_text(text, chunk_size=500, overlap=50)
        
        end_time = time.time()
        
        # Should complete in under 1 second for this size
        assert end_time - start_time < 1.0
        assert len(chunks) > 10  # Should produce multiple chunks
    
    def test_json_parsing_performance(self):
        """Test JSON parsing performance."""
        # Create a reasonably large JSON structure
        large_json = json.dumps({
            "data": [{"id": i, "text": f"Sample text {i}"} for i in range(1000)]
        })
        
        import time
        start_time = time.time()
        
        result = safe_json_parse(large_json)
        
        end_time = time.time()
        
        # Should complete quickly
        assert end_time - start_time < 0.1
        assert result is not None
        assert len(result["data"]) == 1000


# Pytest fixtures
@pytest.fixture
def sample_config():
    """Provide sample configuration for tests."""
    return {
        'aws_region': 'us-east-1',
        'embed_model_id': 'amazon.titan-embed-text-v2:0',
        'chat_model_id': 'amazon.nova-lite-v1:0',
        'chunk_size': 800,
        'chunk_overlap': 120,
        'top_k': 4,
        'temperature': 0.2,
        'debug': False
    }


@pytest.fixture
def sample_sources():
    """Provide sample source data for tests."""
    return [
        ("doc1.md", "This is the content of the first document. It contains information about AI engineering."),
        ("doc2.md", "This is the content of the second document. It discusses RAG systems in detail."),
        ("doc3.md", "This is the content of the third document. It covers deployment and operations.")
    ]


@pytest.fixture
def mock_embeddings():
    """Provide mock embedding vectors for tests."""
    # Generate consistent mock embeddings
    np.random.seed(42)
    return np.random.rand(3, 1024).astype(np.float32)


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__])

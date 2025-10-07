"""
Configuration Management for Priority-Based RAG System

This module provides configuration classes and utilities for customizing
the priority-based routing behavior.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
import json
import os


@dataclass
class RouterConfig:
    """Configuration class for the priority router"""
    
    # Priority mapping for different document sources
    priority_map: Dict[str, float] = field(default_factory=lambda: {
        "SDM Playbook": 1.0,      # Highest priority (playbooks)
        "Templates": 0.8,         # High priority (one-pagers)
        "Process Master Document": 0.7,  # Medium-high priority
        "Trainings": 0.6,         # Medium priority
        "Reports": 0.5,           # Medium-low priority
        "Tools": 0.4              # Lowest priority
    })
    
    # Query-to-source mapping for intelligent routing
    query_source_hints: Dict[str, List[str]] = field(default_factory=lambda: {
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
    })
    
    # Regex patterns for sophisticated matching
    query_patterns: Dict[str, List[str]] = field(default_factory=lambda: {
        r'how\s+to|step\s+by\s+step|guide|instruction': ["SDM Playbook", "Templates"],
        r'template|format|example': ["Templates"],
        r'process|workflow|procedure': ["Process Master Document", "SDM Playbook"],
        r'training|tutorial|course|learn': ["Trainings"],
        r'report|analysis|data|metrics|statistics': ["Reports"],
        r'tool|software|app|system': ["Tools"]
    })
    
    # Weighting factors for final scoring
    priority_weight: float = 0.6      # Weight for source priority
    confidence_weight: float = 0.3    # Weight for retrieval confidence
    query_match_weight: float = 0.1   # Weight for query matching
    
    # Retrieval configuration
    max_retrieval_results: int = 20   # Maximum results to retrieve from KB
    max_final_results: int = 10       # Maximum results to return to user
    
    # AWS configuration
    knowledge_base_id: str = ""
    aws_region: str = "us-east-1"
    bedrock_model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"
    
    # Demo configuration
    use_mock_data: bool = True
    verbose_logging: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            "priority_map": self.priority_map,
            "query_source_hints": self.query_source_hints,
            "query_patterns": self.query_patterns,
            "priority_weight": self.priority_weight,
            "confidence_weight": self.confidence_weight,
            "query_match_weight": self.query_match_weight,
            "max_retrieval_results": self.max_retrieval_results,
            "max_final_results": self.max_final_results,
            "knowledge_base_id": self.knowledge_base_id,
            "aws_region": self.aws_region,
            "bedrock_model_id": self.bedrock_model_id,
            "use_mock_data": self.use_mock_data,
            "verbose_logging": self.verbose_logging
        }
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'RouterConfig':
        """Create configuration from dictionary"""
        return cls(**config_dict)
    
    def save_to_file(self, file_path: str):
        """Save configuration to JSON file"""
        with open(file_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load_from_file(cls, file_path: str) -> 'RouterConfig':
        """Load configuration from JSON file"""
        with open(file_path, 'r') as f:
            config_dict = json.load(f)
        return cls.from_dict(config_dict)
    
    def update_priorities(self, new_priorities: Dict[str, float]):
        """Update priority mapping"""
        self.priority_map.update(new_priorities)
    
    def add_query_pattern(self, pattern: str, sources: List[str]):
        """Add new query pattern for source routing"""
        self.query_patterns[pattern] = sources
    
    def validate(self) -> List[str]:
        """Validate configuration and return any issues"""
        issues = []
        
        # Check priority values
        for source, priority in self.priority_map.items():
            if not 0.0 <= priority <= 1.0:
                issues.append(f"Priority for '{source}' must be between 0.0 and 1.0")
        
        # Check weights sum to reasonable value
        total_weight = self.priority_weight + self.confidence_weight + self.query_match_weight
        if abs(total_weight - 1.0) > 0.1:
            issues.append(f"Weights should sum to ~1.0, current sum: {total_weight}")
        
        # Check required fields for non-mock usage
        if not self.use_mock_data and not self.knowledge_base_id:
            issues.append("knowledge_base_id required when use_mock_data is False")
        
        return issues


@dataclass
class ChatbotConfig:
    """Configuration class for the chatbot"""
    
    # Response generation settings
    max_context_results: int = 5
    response_max_tokens: int = 1000
    
    # Response templates
    response_templates: Dict[str, str] = field(default_factory=lambda: {
        "no_results": "I couldn't find relevant information in the knowledge base for your query.",
        "single_source": "Based on information from {source}:",
        "multiple_sources": "Based on information from multiple sources (prioritized by relevance):",
        "high_confidence": "I'm confident this information is accurate:",
        "medium_confidence": "Here's what I found (moderate confidence):",
        "low_confidence": "I found some potentially relevant information:"
    })
    
    # Conversation settings
    max_conversation_history: int = 50
    enable_conversation_context: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            "max_context_results": self.max_context_results,
            "response_max_tokens": self.response_max_tokens,
            "response_templates": self.response_templates,
            "max_conversation_history": self.max_conversation_history,
            "enable_conversation_context": self.enable_conversation_context
        }


class ConfigManager:
    """Utility class for managing configurations"""
    
    def __init__(self, config_dir: str = None):
        self.config_dir = config_dir or os.path.join(os.path.dirname(__file__), "configs")
        os.makedirs(self.config_dir, exist_ok=True)
    
    def create_default_config(self) -> RouterConfig:
        """Create a default configuration"""
        return RouterConfig()
    
    def create_production_config(self, knowledge_base_id: str) -> RouterConfig:
        """Create a production-ready configuration"""
        config = RouterConfig()
        config.knowledge_base_id = knowledge_base_id
        config.use_mock_data = False
        config.verbose_logging = False
        return config
    
    def create_demo_config(self) -> RouterConfig:
        """Create a demonstration configuration with mock data"""
        config = RouterConfig()
        config.use_mock_data = True
        config.verbose_logging = True
        return config
    
    def save_config(self, config: RouterConfig, name: str):
        """Save configuration with a specific name"""
        file_path = os.path.join(self.config_dir, f"{name}.json")
        config.save_to_file(file_path)
    
    def load_config(self, name: str) -> RouterConfig:
        """Load configuration by name"""
        file_path = os.path.join(self.config_dir, f"{name}.json")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Configuration '{name}' not found at {file_path}")
        return RouterConfig.load_from_file(file_path)
    
    def list_configs(self) -> List[str]:
        """List available configuration names"""
        if not os.path.exists(self.config_dir):
            return []
        
        config_files = [f for f in os.listdir(self.config_dir) if f.endswith('.json')]
        return [f[:-5] for f in config_files]  # Remove .json extension
    
    def validate_config(self, config: RouterConfig) -> bool:
        """Validate a configuration and print any issues"""
        issues = config.validate()
        if issues:
            print("Configuration validation issues:")
            for issue in issues:
                print(f"  - {issue}")
            return False
        return True


# Predefined configurations for different use cases
PREDEFINED_CONFIGS = {
    "balanced": {
        "description": "Balanced weighting between priority, confidence, and query matching",
        "priority_weight": 0.5,
        "confidence_weight": 0.3,
        "query_match_weight": 0.2
    },
    
    "priority_focused": {
        "description": "Heavily weighted towards source priority",
        "priority_weight": 0.8,
        "confidence_weight": 0.15,
        "query_match_weight": 0.05
    },
    
    "confidence_focused": {
        "description": "Heavily weighted towards retrieval confidence",
        "priority_weight": 0.2,
        "confidence_weight": 0.7,
        "query_match_weight": 0.1
    },
    
    "query_focused": {
        "description": "Heavily weighted towards query-source matching",
        "priority_weight": 0.3,
        "confidence_weight": 0.2,
        "query_match_weight": 0.5
    }
}


def get_config_preset(preset_name: str) -> Dict[str, Any]:
    """Get predefined configuration preset"""
    if preset_name not in PREDEFINED_CONFIGS:
        available = list(PREDEFINED_CONFIGS.keys())
        raise ValueError(f"Unknown preset '{preset_name}'. Available: {available}")
    
    return PREDEFINED_CONFIGS[preset_name]


def apply_config_preset(config: RouterConfig, preset_name: str) -> RouterConfig:
    """Apply a predefined configuration preset to a RouterConfig"""
    preset = get_config_preset(preset_name)
    
    config.priority_weight = preset.get("priority_weight", config.priority_weight)
    config.confidence_weight = preset.get("confidence_weight", config.confidence_weight)
    config.query_match_weight = preset.get("query_match_weight", config.query_match_weight)
    
    return config


# Environment variable configuration
def load_config_from_env() -> RouterConfig:
    """Load configuration from environment variables"""
    config = RouterConfig()
    
    # AWS settings
    if os.getenv("KNOWLEDGE_BASE_ID"):
        config.knowledge_base_id = os.getenv("KNOWLEDGE_BASE_ID")
        config.use_mock_data = False
    
    if os.getenv("AWS_REGION"):
        config.aws_region = os.getenv("AWS_REGION")
    
    if os.getenv("BEDROCK_MODEL_ID"):
        config.bedrock_model_id = os.getenv("BEDROCK_MODEL_ID")
    
    # Weighting settings
    if os.getenv("PRIORITY_WEIGHT"):
        config.priority_weight = float(os.getenv("PRIORITY_WEIGHT"))
    
    if os.getenv("CONFIDENCE_WEIGHT"):
        config.confidence_weight = float(os.getenv("CONFIDENCE_WEIGHT"))
    
    if os.getenv("QUERY_MATCH_WEIGHT"):
        config.query_match_weight = float(os.getenv("QUERY_MATCH_WEIGHT"))
    
    # Other settings
    if os.getenv("VERBOSE_LOGGING"):
        config.verbose_logging = os.getenv("VERBOSE_LOGGING").lower() == "true"
    
    return config
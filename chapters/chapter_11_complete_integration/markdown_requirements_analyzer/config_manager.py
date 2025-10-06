#!/usr/bin/env python3
"""
Configuration Manager

This module handles configuration management for the markdown requirements analyzer,
including AWS Bedrock settings, logging configuration, and application preferences.
"""

import json
import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Union
import yaml

logger = logging.getLogger(__name__)


class ConfigManager:
    """
    Manages configuration for the markdown requirements analyzer.
    
    Supports configuration via files (JSON/YAML), environment variables,
    and programmatic settings with precedence handling.
    """
    
    DEFAULT_CONFIG = {
        'aws': {
            'region': 'us-east-1',
            'bedrock': {
                'model_id': 'amazon.nova-lite-v1:0',
                'max_tokens': 1000,
                'temperature': 0.1,
                'top_p': 0.9
            }
        },
        'converter': {
            'validate_structure': True,
            'batch_size': 10,
            'output_format': 'json',
            'pretty_print': True
        },
        'analyzer': {
            'default_analysis_type': 'comprehensive',
            'enable_caching': False,
            'cache_ttl': 3600
        },
        'logging': {
            'level': 'INFO',
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'file': None,
            'console': True
        },
        'output': {
            'base_directory': './output',
            'create_subdirectories': True,
            'filename_template': '{original_name}_{timestamp}',
            'include_metadata': True
        }
    }
    
    def __init__(self, config_file: Optional[Union[str, Path]] = None):
        """
        Initialize configuration manager.
        
        Args:
            config_file: Optional path to configuration file
        """
        self.config_file = Path(config_file) if config_file else None
        self.config = self._load_config()
        self._setup_logging()
    
    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from various sources with precedence.
        
        Precedence order:
        1. Environment variables (highest)
        2. Configuration file
        3. Default configuration (lowest)
        
        Returns:
            Merged configuration dictionary
        """
        # Start with default configuration
        config = self.DEFAULT_CONFIG.copy()
        
        # Load from configuration file if provided
        if self.config_file and self.config_file.exists():
            file_config = self._load_config_file(self.config_file)
            config = self._deep_merge(config, file_config)
        
        # Override with environment variables
        env_config = self._load_env_config()
        config = self._deep_merge(config, env_config)
        
        return config
    
    def _load_config_file(self, config_file: Path) -> Dict[str, Any]:
        """
        Load configuration from a file (JSON or YAML).
        
        Args:
            config_file: Path to configuration file
            
        Returns:
            Configuration dictionary
        """
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                if config_file.suffix.lower() in ['.yml', '.yaml']:
                    return yaml.safe_load(f) or {}
                else:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load config file {config_file}: {str(e)}")
            return {}
    
    def _load_env_config(self) -> Dict[str, Any]:
        """
        Load configuration from environment variables.
        
        Expected environment variables:
        - AWS_REGION
        - BEDROCK_MODEL_ID
        - BEDROCK_MAX_TOKENS
        - BEDROCK_TEMPERATURE
        - LOG_LEVEL
        - OUTPUT_DIR
        
        Returns:
            Configuration dictionary from environment variables
        """
        env_config = {}
        
        # AWS configuration
        if os.getenv('AWS_REGION'):
            env_config.setdefault('aws', {})['region'] = os.getenv('AWS_REGION')
        
        # Bedrock configuration
        bedrock_vars = {
            'BEDROCK_MODEL_ID': 'model_id',
            'BEDROCK_MAX_TOKENS': 'max_tokens',
            'BEDROCK_TEMPERATURE': 'temperature',
            'BEDROCK_TOP_P': 'top_p'
        }
        
        for env_var, config_key in bedrock_vars.items():
            if os.getenv(env_var):
                env_config.setdefault('aws', {}).setdefault('bedrock', {})[config_key] = os.getenv(env_var)
                
                # Convert numeric values
                if config_key in ['max_tokens']:
                    try:
                        env_config['aws']['bedrock'][config_key] = int(env_config['aws']['bedrock'][config_key])
                    except ValueError:
                        pass
                elif config_key in ['temperature', 'top_p']:
                    try:
                        env_config['aws']['bedrock'][config_key] = float(env_config['aws']['bedrock'][config_key])
                    except ValueError:
                        pass
        
        # Logging configuration
        if os.getenv('LOG_LEVEL'):
            env_config.setdefault('logging', {})['level'] = os.getenv('LOG_LEVEL')
        
        if os.getenv('LOG_FILE'):
            env_config.setdefault('logging', {})['file'] = os.getenv('LOG_FILE')
        
        # Output configuration
        if os.getenv('OUTPUT_DIR'):
            env_config.setdefault('output', {})['base_directory'] = os.getenv('OUTPUT_DIR')
        
        return env_config
    
    def _deep_merge(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deep merge two dictionaries.
        
        Args:
            base: Base dictionary
            override: Dictionary with override values
            
        Returns:
            Merged dictionary
        """
        result = base.copy()
        
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def _setup_logging(self):
        """Setup logging based on configuration."""
        log_config = self.config.get('logging', {})
        
        # Configure logging level
        level = getattr(logging, log_config.get('level', 'INFO').upper())
        logging.basicConfig(level=level)
        
        # Configure formatters
        formatter = logging.Formatter(log_config.get('format', 
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        
        # Get root logger
        root_logger = logging.getLogger()
        
        # Clear existing handlers
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # Add console handler if enabled
        if log_config.get('console', True):
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            root_logger.addHandler(console_handler)
        
        # Add file handler if specified
        if log_config.get('file'):
            try:
                log_file = Path(log_config['file'])
                log_file.parent.mkdir(parents=True, exist_ok=True)
                file_handler = logging.FileHandler(log_file)
                file_handler.setFormatter(formatter)
                root_logger.addHandler(file_handler)
            except Exception as e:
                logger.warning(f"Could not setup file logging: {str(e)}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.
        
        Args:
            key: Configuration key (e.g., 'aws.region')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any):
        """
        Set configuration value using dot notation.
        
        Args:
            key: Configuration key (e.g., 'aws.region')
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def get_aws_config(self) -> Dict[str, Any]:
        """Get AWS-specific configuration."""
        return self.config.get('aws', {})
    
    def get_bedrock_config(self) -> Dict[str, Any]:
        """Get Bedrock-specific configuration."""
        return self.config.get('aws', {}).get('bedrock', {})
    
    def get_converter_config(self) -> Dict[str, Any]:
        """Get converter-specific configuration."""
        return self.config.get('converter', {})
    
    def get_analyzer_config(self) -> Dict[str, Any]:
        """Get analyzer-specific configuration."""
        return self.config.get('analyzer', {})
    
    def get_output_config(self) -> Dict[str, Any]:
        """Get output-specific configuration."""
        return self.config.get('output', {})
    
    def save_config(self, output_file: Optional[Union[str, Path]] = None) -> bool:
        """
        Save current configuration to file.
        
        Args:
            output_file: Optional path to save configuration
            
        Returns:
            True if successful, False otherwise
        """
        try:
            output_file = Path(output_file) if output_file else self.config_file
            
            if not output_file:
                logger.error("No output file specified for saving configuration")
                return False
            
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                if output_file.suffix.lower() in ['.yml', '.yaml']:
                    yaml.safe_dump(self.config, f, default_flow_style=False, indent=2)
                else:
                    json.dump(self.config, f, indent=2)
            
            logger.info(f"Configuration saved to {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving configuration: {str(e)}")
            return False
    
    def create_sample_config(self, output_file: Union[str, Path]) -> bool:
        """
        Create a sample configuration file.
        
        Args:
            output_file: Path for the sample configuration file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            output_file = Path(output_file)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            sample_config = self.DEFAULT_CONFIG.copy()
            
            with open(output_file, 'w', encoding='utf-8') as f:
                if output_file.suffix.lower() in ['.yml', '.yaml']:
                    yaml.safe_dump(sample_config, f, default_flow_style=False, indent=2)
                else:
                    json.dump(sample_config, f, indent=2)
            
            logger.info(f"Sample configuration created at {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating sample configuration: {str(e)}")
            return False
    
    def validate_config(self) -> Dict[str, Any]:
        """
        Validate the current configuration.
        
        Returns:
            Validation results
        """
        issues = []
        warnings = []
        
        # Validate AWS configuration
        aws_config = self.get_aws_config()
        if not aws_config.get('region'):
            issues.append("AWS region not specified")
        
        # Validate Bedrock configuration
        bedrock_config = self.get_bedrock_config()
        if not bedrock_config.get('model_id'):
            issues.append("Bedrock model ID not specified")
        
        max_tokens = bedrock_config.get('max_tokens', 0)
        if max_tokens <= 0 or max_tokens > 4000:
            warnings.append(f"Max tokens value may be invalid: {max_tokens}")
        
        temperature = bedrock_config.get('temperature', 0)
        if temperature < 0 or temperature > 1:
            warnings.append(f"Temperature value should be between 0 and 1: {temperature}")
        
        # Validate output configuration
        output_config = self.get_output_config()
        output_dir = Path(output_config.get('base_directory', './output'))
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            if not output_dir.is_dir():
                issues.append(f"Output directory is not accessible: {output_dir}")
        except Exception as e:
            issues.append(f"Cannot create output directory: {str(e)}")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'warnings': warnings
        }


# Global configuration instance
_config_instance = None


def get_config(config_file: Optional[Union[str, Path]] = None) -> ConfigManager:
    """
    Get the global configuration instance.
    
    Args:
        config_file: Optional configuration file path
        
    Returns:
        ConfigManager instance
    """
    global _config_instance
    
    if _config_instance is None:
        _config_instance = ConfigManager(config_file)
    
    return _config_instance


def reload_config(config_file: Optional[Union[str, Path]] = None):
    """
    Reload the global configuration.
    
    Args:
        config_file: Optional configuration file path
    """
    global _config_instance
    _config_instance = ConfigManager(config_file)


if __name__ == "__main__":
    # Create sample configuration files
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'create-sample':
        config = ConfigManager()
        
        # Create JSON sample
        if config.create_sample_config('config.json'):
            print("✅ Created sample config.json")
        
        # Create YAML sample  
        if config.create_sample_config('config.yml'):
            print("✅ Created sample config.yml")
        
        print("\n📋 Sample configuration files created!")
        print("Edit them to customize your settings.")
        
    else:
        # Test configuration loading
        config = ConfigManager()
        validation = config.validate_config()
        
        print("🔧 Configuration Test")
        print("=" * 30)
        print(f"AWS Region: {config.get('aws.region')}")
        print(f"Bedrock Model: {config.get('aws.bedrock.model_id')}")
        print(f"Log Level: {config.get('logging.level')}")
        print(f"Output Dir: {config.get('output.base_directory')}")
        
        print(f"\n✅ Configuration Valid: {validation['valid']}")
        if validation['issues']:
            print("❌ Issues:")
            for issue in validation['issues']:
                print(f"  - {issue}")
        if validation['warnings']:
            print("⚠️  Warnings:")
            for warning in validation['warnings']:
                print(f"  - {warning}")
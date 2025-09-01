#!/usr/bin/env python3
"""
Simple test of monitoring functionality without emoji encoding issues
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

def simple_print(message):
    """Simple print without emojis for testing"""
    print(f"INFO: {message}")

def test_monitoring_import():
    """Test that we can import monitoring components"""
    try:
        # Import the monitoring config without triggering emoji issues
        import bedrock_kb_monitoring
        simple_print("Successfully imported monitoring module")
        
        # Test that the main components are available
        config_class = getattr(bedrock_kb_monitoring, 'MonitoringConfig', None)
        monitor_class = getattr(bedrock_kb_monitoring, 'BedrockKnowledgeBaseMonitor', None)
        
        if config_class and monitor_class:
            simple_print("All monitoring classes available")
            
            # Test creating config
            test_config = config_class(
                knowledge_base_id="test-kb-123",
                region="us-east-1"
            )
            simple_print(f"Created test config for KB: {test_config.knowledge_base_id}")
            
            return True
        else:
            simple_print("ERROR: Missing monitoring classes")
            return False
            
    except Exception as e:
        simple_print(f"ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    simple_print("Testing AWS Bedrock Knowledge Base Monitoring")
    success = test_monitoring_import()
    
    if success:
        simple_print("SUCCESS: Monitoring system is ready!")
        simple_print("To use:")
        simple_print("  python bedrock_kb_monitoring.py --knowledge-base-id YOUR_KB_ID --setup-monitoring")
        simple_print("  python bedrock_kb_monitoring.py --knowledge-base-id YOUR_KB_ID --status")
    else:
        simple_print("ERROR: Monitoring system has issues")
        sys.exit(1)

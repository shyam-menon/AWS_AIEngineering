#!/usr/bin/env python3
"""
Demo Script for Markdown Requirements Analyzer

This script demonstrates the complete workflow of the analyzer.
Note: Bedrock analysis requires AWS credentials to be configured.
"""

import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from markdown_converter import MarkdownConverter
from bedrock_analyzer import BedrockRequirementsAnalyzer
from config_manager import get_config
import utils


def demo_conversion():
    """Demonstrate markdown to JSON conversion."""
    print("🔄 DEMO: Markdown to JSON Conversion")
    print("=" * 50)
    
    # Convert a simple requirements file
    converter = MarkdownConverter()
    result = converter.convert_file('simple_requirements.md')
    
    if result['success']:
        utils.print_success("Conversion completed!")
        print(f"📊 Sections found: {result['metadata']['sections_count']}")
        print(f"📁 File size: {utils.format_file_size(result['metadata']['file_size'])}")
        
        # Display a sample of the converted JSON
        print("\n📋 Sample JSON Output:")
        sample_output = json.dumps(result['data'], indent=2)[:500] + "..."
        print(sample_output)
        
    else:
        utils.print_error(f"Conversion failed: {result['error']}")
    
    return result


def demo_analysis_structure():
    """Demonstrate the analysis structure (without actual Bedrock call)."""
    print("\n🤖 DEMO: Analysis Structure")
    print("=" * 50)
    
    # Load configuration
    config = get_config()
    
    utils.print_info(f"Configured region: {config.get('aws.region')}")
    utils.print_info(f"Configured model: {config.get('aws.bedrock.model_id')}")
    
    # Create analyzer instance (but don't call it without credentials)
    try:
        analyzer = BedrockRequirementsAnalyzer(
            region=config.get('aws.region'),
            model_id=config.get('aws.bedrock.model_id')
        )
        utils.print_success("Bedrock analyzer initialized successfully")
        utils.print_info("Note: Actual analysis requires AWS credentials")
        
        # Show what the analysis would look like
        sample_analysis = {
            "success": True,
            "analysis_type": "comprehensive",
            "model_used": config.get('aws.bedrock.model_id'),
            "analysis": {
                "completeness_score": 75,
                "quality_score": 82,
                "structure_score": 88,
                "missing_elements": [
                    "Detailed user acceptance criteria",
                    "Security requirements specification",
                    "Performance benchmarks"
                ],
                "strengths": [
                    "Clear feature definitions",
                    "Well-structured hierarchy",
                    "Specific technical requirements"
                ],
                "recommendations": [
                    "Add detailed security requirements",
                    "Include specific performance metrics",
                    "Define user acceptance criteria"
                ],
                "overall_assessment": "Good foundation with some areas for improvement"
            }
        }
        
        print("\n📊 Sample Analysis Output:")
        print(json.dumps(sample_analysis, indent=2))
        
    except Exception as e:
        utils.print_warning(f"Bedrock initialization issue (expected without AWS credentials): {str(e)}")
        utils.print_info("This is normal when AWS credentials are not configured")


def demo_batch_processing():
    """Demonstrate batch processing capabilities."""
    print("\n📂 DEMO: Batch Processing")
    print("=" * 50)
    
    converter = MarkdownConverter()
    
    # Process all markdown files in examples directory
    results = converter.convert_directory('.')
    
    successful = sum(1 for r in results if r['success'])
    total = len(results)
    
    utils.print_info(f"Batch processing results: {successful}/{total} files successful")
    
    for result in results:
        status = "✅" if result['success'] else "❌"
        filename = Path(result['file_path']).name
        
        if result['success']:
            sections = result['metadata']['sections_count']
            print(f"  {status} {filename} - {sections} sections")
        else:
            print(f"  {status} {filename} - Error: {result['error']}")


def demo_configuration():
    """Demonstrate configuration management."""
    print("\n⚙️  DEMO: Configuration Management")
    print("=" * 50)
    
    config = get_config()
    
    # Show key configuration values
    print("📋 Current Configuration:")
    print(f"  AWS Region: {config.get('aws.region')}")
    print(f"  Bedrock Model: {config.get('aws.bedrock.model_id')}")
    print(f"  Max Tokens: {config.get('aws.bedrock.max_tokens')}")
    print(f"  Temperature: {config.get('aws.bedrock.temperature')}")
    print(f"  Validation: {'Enabled' if config.get('converter.validate_structure') else 'Disabled'}")
    print(f"  Log Level: {config.get('logging.level')}")
    
    # Validate configuration
    validation = config.validate_config()
    if validation['valid']:
        utils.print_success("Configuration is valid")
    else:
        utils.print_warning("Configuration issues found:")
        for issue in validation['issues']:
            print(f"  - {issue}")


def main():
    """Run the complete demo."""
    print("🚀 Markdown Requirements Analyzer - Demo")
    print("=" * 60)
    print("This demo showcases the complete functionality of the analyzer.")
    print("Note: Bedrock analysis requires AWS credentials to be configured.\n")
    
    try:
        # Demo 1: Basic conversion
        conversion_result = demo_conversion()
        
        # Demo 2: Analysis structure (without actual Bedrock call)
        demo_analysis_structure()
        
        # Demo 3: Batch processing
        demo_batch_processing()
        
        # Demo 4: Configuration
        demo_configuration()
        
        # Summary
        print("\n" + "=" * 60)
        print("🎯 DEMO SUMMARY")
        print("=" * 60)
        
        print("✅ Core Features Demonstrated:")
        print("  • Markdown to JSON conversion")
        print("  • Batch processing capabilities")
        print("  • Configuration management")
        print("  • Analysis framework structure")
        
        print("\n🔧 To Test Bedrock Integration:")
        print("  1. Configure AWS credentials:")
        print("     aws configure")
        print("  2. Run with analysis:")
        print("     python ../main.py convert simple_requirements.md --analyze")
        print("  3. Try different analysis types:")
        print("     python ../main.py convert simple_requirements.md --analyze --analysis-type completeness")
        
        print("\n🎉 Demo completed successfully!")
        
    except Exception as e:
        utils.print_error(f"Demo failed: {str(e)}")
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
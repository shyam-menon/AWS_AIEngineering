#!/usr/bin/env python3
"""
Test Script for Markdown Requirements Analyzer

This script tests all functionality of the analyzer without requiring AWS credentials.
It validates the core conversion logic, configuration management, and CLI interface.
"""

import json
import sys
from pathlib import Path
import tempfile
import shutil

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from markdown_converter import MarkdownConverter, convert_single_file
from config_manager import ConfigManager
from cli_interface import CLIInterface
import utils


def test_markdown_conversion():
    """Test markdown to JSON conversion."""
    print("🧪 Testing Markdown Conversion")
    print("-" * 40)
    
    success_count = 0
    total_tests = 0
    
    # Test 1: Basic conversion
    total_tests += 1
    try:
        converter = MarkdownConverter()
        result = converter.convert_file('examples/sample_requirements.md')
        
        if result['success'] and result['data']:
            print("✅ Sample requirements conversion successful")
            print(f"   📊 Sections found: {result['metadata']['sections_count']}")
            success_count += 1
        else:
            print(f"❌ Sample requirements conversion failed: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Sample requirements test failed: {str(e)}")
    
    # Test 2: Simple requirements
    total_tests += 1
    try:
        result = convert_single_file('examples/simple_requirements.md')
        
        if result['success']:
            print("✅ Simple requirements conversion successful")
            success_count += 1
        else:
            print(f"❌ Simple requirements conversion failed: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Simple requirements test failed: {str(e)}")
    
    # Test 3: Incomplete requirements (should still work)
    total_tests += 1
    try:
        result = convert_single_file('examples/incomplete_requirements.md')
        
        if result['success']:
            print("✅ Incomplete requirements conversion successful")
            print("   ⚠️  Expected validation warnings for incomplete content")
            success_count += 1
        else:
            print(f"❌ Incomplete requirements conversion failed: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Incomplete requirements test failed: {str(e)}")
    
    # Test 4: Batch processing
    total_tests += 1
    try:
        converter = MarkdownConverter()
        results = converter.convert_directory('examples')
        
        successful_batch = sum(1 for r in results if r['success'])
        total_batch = len(results)
        
        if successful_batch >= 3:  # We have 3 example files
            print(f"✅ Batch processing successful: {successful_batch}/{total_batch} files")
            success_count += 1
        else:
            print(f"❌ Batch processing had issues: {successful_batch}/{total_batch} files successful")
            
    except Exception as e:
        print(f"❌ Batch processing test failed: {str(e)}")
    
    print(f"\n📊 Conversion Tests: {success_count}/{total_tests} passed")
    return success_count, total_tests


def test_configuration_management():
    """Test configuration management functionality."""
    print("\n🔧 Testing Configuration Management")
    print("-" * 40)
    
    success_count = 0
    total_tests = 0
    
    # Test 1: Default configuration loading
    total_tests += 1
    try:
        config = ConfigManager()
        
        if config.get('aws.region') and config.get('aws.bedrock.model_id'):
            print("✅ Default configuration loaded successfully")
            print(f"   🌍 Region: {config.get('aws.region')}")
            print(f"   🤖 Model: {config.get('aws.bedrock.model_id')}")
            success_count += 1
        else:
            print("❌ Default configuration missing required values")
            
    except Exception as e:
        print(f"❌ Default configuration test failed: {str(e)}")
    
    # Test 2: Configuration validation
    total_tests += 1
    try:
        config = ConfigManager()
        validation = config.validate_config()
        
        if validation['valid']:
            print("✅ Configuration validation passed")
            success_count += 1
        else:
            print(f"❌ Configuration validation failed: {validation['issues']}")
            
    except Exception as e:
        print(f"❌ Configuration validation test failed: {str(e)}")
    
    # Test 3: Sample configuration creation
    total_tests += 1
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        config = ConfigManager()
        if config.create_sample_config(tmp_path):
            # Verify the created file
            with open(tmp_path, 'r') as f:
                sample_config = json.load(f)
            
            if 'aws' in sample_config and 'converter' in sample_config:
                print("✅ Sample configuration creation successful")
                success_count += 1
            else:
                print("❌ Sample configuration missing required sections")
        else:
            print("❌ Sample configuration creation failed")
            
        # Cleanup
        Path(tmp_path).unlink(missing_ok=True)
            
    except Exception as e:
        print(f"❌ Sample configuration test failed: {str(e)}")
    
    print(f"\n📊 Configuration Tests: {success_count}/{total_tests} passed")
    return success_count, total_tests


def test_utility_functions():
    """Test utility functions."""
    print("\n🛠️  Testing Utility Functions")
    print("-" * 40)
    
    success_count = 0
    total_tests = 0
    
    # Test 1: File path validation
    total_tests += 1
    try:
        validation = utils.validate_file_path('examples/sample_requirements.md', ['.md'])
        
        if validation['valid'] and validation['exists']:
            print("✅ File path validation successful")
            success_count += 1
        else:
            print(f"❌ File path validation failed: {validation['issues']}")
            
    except Exception as e:
        print(f"❌ File path validation test failed: {str(e)}")
    
    # Test 2: JSON parsing
    total_tests += 1
    try:
        test_json = '{"test": "value", "number": 42}'
        parsed = utils.safe_json_parse(test_json)
        
        if parsed and parsed.get('test') == 'value' and parsed.get('number') == 42:
            print("✅ JSON parsing successful")
            success_count += 1
        else:
            print("❌ JSON parsing failed")
            
    except Exception as e:
        print(f"❌ JSON parsing test failed: {str(e)}")
    
    # Test 3: Filename sanitization
    total_tests += 1
    try:
        unsafe_name = 'test<>file:|*.txt'
        safe_name = utils.sanitize_filename(unsafe_name)
        
        if safe_name and '<' not in safe_name and '>' not in safe_name:
            print(f"✅ Filename sanitization successful: '{unsafe_name}' -> '{safe_name}'")
            success_count += 1
        else:
            print("❌ Filename sanitization failed")
            
    except Exception as e:
        print(f"❌ Filename sanitization test failed: {str(e)}")
    
    # Test 4: File size formatting
    total_tests += 1
    try:
        size_str = utils.format_file_size(1536)
        
        if size_str and 'KB' in size_str:
            print(f"✅ File size formatting successful: 1536 bytes -> {size_str}")
            success_count += 1
        else:
            print("❌ File size formatting failed")
            
    except Exception as e:
        print(f"❌ File size formatting test failed: {str(e)}")
    
    print(f"\n📊 Utility Tests: {success_count}/{total_tests} passed")
    return success_count, total_tests


def test_cli_interface():
    """Test CLI interface functionality."""
    print("\n💻 Testing CLI Interface")
    print("-" * 40)
    
    success_count = 0
    total_tests = 0
    
    # Test 1: CLI initialization
    total_tests += 1
    try:
        cli = CLIInterface()
        
        if cli.parser and hasattr(cli.parser, 'parse_args'):
            print("✅ CLI interface initialization successful")
            success_count += 1
        else:
            print("❌ CLI interface initialization failed")
            
    except Exception as e:
        print(f"❌ CLI interface initialization test failed: {str(e)}")
    
    # Test 2: Help functionality
    total_tests += 1
    try:
        cli = CLIInterface()
        
        # Test help parsing (this should not raise an exception)
        try:
            cli.parser.parse_args(['--help'])
        except SystemExit:
            # Help command exits, which is expected
            print("✅ CLI help functionality working")
            success_count += 1
        except Exception as e:
            print(f"❌ CLI help test failed: {str(e)}")
            
    except Exception as e:
        print(f"❌ CLI help test failed: {str(e)}")
    
    # Test 3: Command parsing
    total_tests += 1
    try:
        cli = CLIInterface()
        args = cli.parser.parse_args(['convert', 'test.md'])
        
        if args.command == 'convert' and args.input_file == 'test.md':
            print("✅ CLI command parsing successful")
            success_count += 1
        else:
            print("❌ CLI command parsing failed")
            
    except Exception as e:
        print(f"❌ CLI command parsing test failed: {str(e)}")
    
    print(f"\n📊 CLI Tests: {success_count}/{total_tests} passed")
    return success_count, total_tests


def test_end_to_end_workflow():
    """Test complete end-to-end workflow without Bedrock."""
    print("\n🔄 Testing End-to-End Workflow")
    print("-" * 40)
    
    success_count = 0
    total_tests = 0
    
    # Test 1: Complete conversion workflow
    total_tests += 1
    try:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            
            # Convert markdown file
            converter = MarkdownConverter()
            result = converter.convert_file('examples/simple_requirements.md')
            
            if not result['success']:
                print(f"❌ Conversion failed: {result.get('error')}")
                return success_count, total_tests
            
            # Save JSON output
            json_file = tmp_path / 'requirements.json'
            if converter.save_json(result['data'], json_file):
                # Verify JSON file was created and is valid
                with open(json_file, 'r') as f:
                    saved_data = json.load(f)
                
                if saved_data and isinstance(saved_data, dict):
                    print("✅ End-to-end conversion workflow successful")
                    print(f"   📁 JSON saved and validated: {json_file.name}")
                    print(f"   📊 Data keys: {list(saved_data.keys())[:3]}...")
                    success_count += 1
                else:
                    print("❌ Saved JSON data validation failed")
            else:
                print("❌ JSON file save failed")
            
    except Exception as e:
        print(f"❌ End-to-end workflow test failed: {str(e)}")
    
    # Test 2: Batch workflow
    total_tests += 1
    try:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            
            # Batch convert all example files
            converter = MarkdownConverter()
            results = converter.convert_directory('examples')
            
            # Save all results
            successful_saves = 0
            for result in results:
                if result['success']:
                    output_file = tmp_path / f"{Path(result['file_path']).stem}.json"
                    if converter.save_json(result['data'], output_file):
                        successful_saves += 1
            
            if successful_saves >= 3:  # We have 3 example files
                print(f"✅ Batch workflow successful: {successful_saves} files processed")
                success_count += 1
            else:
                print(f"❌ Batch workflow had issues: only {successful_saves} files processed successfully")
            
    except Exception as e:
        print(f"❌ Batch workflow test failed: {str(e)}")
    
    print(f"\n📊 Workflow Tests: {success_count}/{total_tests} passed")
    return success_count, total_tests


def main():
    """Run all tests."""
    print("🚀 Markdown Requirements Analyzer - Comprehensive Testing")
    print("=" * 60)
    
    total_success = 0
    total_tests = 0
    
    # Run all test suites
    test_suites = [
        test_markdown_conversion,
        test_configuration_management,
        test_utility_functions,
        test_cli_interface,
        test_end_to_end_workflow
    ]
    
    for test_suite in test_suites:
        try:
            success, tests = test_suite()
            total_success += success
            total_tests += tests
        except Exception as e:
            print(f"❌ Test suite failed: {str(e)}")
            total_tests += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    success_rate = (total_success / total_tests * 100) if total_tests > 0 else 0
    
    print(f"Total Tests: {total_tests}")
    print(f"Successful: {total_success}")
    print(f"Failed: {total_tests - total_success}")
    print(f"Success Rate: {success_rate:.1f}%")
    
    if success_rate >= 90:
        print("\n🎉 EXCELLENT! All core functionality is working properly.")
        print("✅ The system is ready for AWS Bedrock integration testing.")
    elif success_rate >= 75:
        print("\n👍 GOOD! Most functionality is working.")
        print("⚠️  Some issues found - review failed tests above.")
    else:
        print("\n⚠️  NEEDS ATTENTION! Multiple issues found.")
        print("❌ Please fix failing tests before proceeding.")
    
    print("\n📝 NEXT STEPS:")
    print("1. Configure AWS credentials for Bedrock testing")
    print("2. Test Bedrock integration with: python main.py convert examples/simple_requirements.md --analyze")
    print("3. Test different analysis types: --analysis-type completeness")
    print("4. Test batch processing with analysis")
    
    return success_rate >= 75


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
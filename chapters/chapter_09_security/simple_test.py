#!/usr/bin/env python3
"""
Simple Test Runner for Security Examples

This script performs basic validation of the security code examples
without making expensive API calls.
"""

import os
import sys
import importlib.util

def test_module_structure(module_name, expected_functions):
    """Test that a module has expected functions/classes"""
    try:
        # Load the module
        spec = importlib.util.spec_from_file_location(module_name, f"{module_name}.py")
        module = importlib.util.module_from_spec(spec)
        
        # Mock the strands import before executing
        import types
        mock_strands = types.ModuleType('strands')
        mock_strands.Agent = lambda **kwargs: type('MockAgent', (), {'run': lambda self, *args, **kwargs: 'mock response'})()
        mock_strands.ModelProvider = type('MockModelProvider', (), {'bedrock': lambda x: f'mock-{x}'})()
        sys.modules['strands'] = mock_strands
        
        spec.loader.exec_module(module)
        
        # Check for expected functions
        missing = []
        found = []
        
        for func_name in expected_functions:
            if hasattr(module, func_name):
                found.append(func_name)
            else:
                missing.append(func_name)
        
        return {
            'success': len(missing) == 0,
            'found': found,
            'missing': missing,
            'module': module
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'found': [],
            'missing': expected_functions
        }

def main():
    """Run all tests"""
    print("🧪 Security Examples Test Runner")
    print("=" * 50)
    
    # Define expected structure for each module
    test_modules = {
        'secure_prompt_engineering': [
            'create_secure_documentation_agent',
            'create_structured_input_agent',
            'create_context_management_agent',
            'create_adversarial_defense_agent',
            'create_validation_agent'
        ],
        'prompt_injection_defense': [
            'PromptInjectionDefense',
            'create_advanced_defense_agent'
        ],
        'input_validation_agent': [
            'InputValidator',
            'create_secure_processing_agent'
        ],
        'adversarial_testing': [
            'AdversarialTester', 
            'create_hardened_agent'
        ],
        'security_validation_agent': [
            'SecurityValidator',
            'create_secure_processing_agent'
        ]
    }
    
    results = {}
    
    for module_name, expected_functions in test_modules.items():
        print(f"\n🔍 Testing {module_name}...")
        
        if not os.path.exists(f"{module_name}.py"):
            print(f"❌ File {module_name}.py not found")
            results[module_name] = {'success': False, 'error': 'File not found'}
            continue
        
        result = test_module_structure(module_name, expected_functions)
        results[module_name] = result
        
        if result['success']:
            print(f"✅ {module_name}: All {len(expected_functions)} functions/classes found")
        else:
            print(f"❌ {module_name}: Issues found")
            if result.get('missing'):
                print(f"   Missing: {', '.join(result['missing'])}")
            if result.get('error'):
                print(f"   Error: {result['error']}")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary")
    print("=" * 50)
    
    successful_modules = sum(1 for r in results.values() if r['success'])
    total_modules = len(results)
    
    for module_name, result in results.items():
        status = "✅ PASS" if result['success'] else "❌ FAIL"
        print(f"{module_name}: {status}")
    
    print(f"\nOverall: {successful_modules}/{total_modules} modules passed")
    
    if successful_modules == total_modules:
        print("🎉 All security examples are ready for check-in!")
        return True
    else:
        print("⚠️  Some issues found. Please review before check-in.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

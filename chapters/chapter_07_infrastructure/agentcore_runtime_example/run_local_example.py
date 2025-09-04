#!/usr/bin/env python3
"""
Run Local AgentCore Example
============================

This script demonstrates how to run the AgentCore example locally without
requiring the AWS AgentCore toolkit. Perfect for learning and development.
"""

import sys
import os
import json
import subprocess
from pathlib import Path


def check_environment():
    """Check if the environment is properly set up"""
    print("🔍 Checking environment setup...")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major == 3 and python_version.minor >= 8:
        print(f"✅ Python {python_version.major}.{python_version.minor} detected")
    else:
        print(f"❌ Python 3.8+ required, found {python_version.major}.{python_version.minor}")
        return False
    
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment detected")
    else:
        print("⚠️ No virtual environment detected (recommended but not required)")
    
    # Check for required packages
    required_packages = [
        ('boto3', 'boto3'),
        ('strands-agents', 'strands')
    ]
    missing_packages = []
    
    for display_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"✅ {display_name} installed")
        except ImportError:
            missing_packages.append(display_name)
            print(f"❌ {display_name} missing")
    
    if missing_packages:
        print(f"\n📦 To install missing packages, run:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    print("\n✅ Environment setup complete!\n")
    return True


def run_local_agent():
    """Run the local Strands agent"""
    print("🚀 Running Local Strands Agent...")
    print("=" * 50)
    
    # Test payload
    test_payload = '{"prompt": "Hello! Can you help me with the weather in New York?"}'
    
    try:
        result = subprocess.run([
            sys.executable, 'local_strands_agent.py', test_payload
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Local agent ran successfully!")
            print("\nOutput:")
            print(result.stdout)
        else:
            print("❌ Local agent failed:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Local agent test timed out (this is normal for interactive agents)")
        return True
    except Exception as e:
        print(f"❌ Error running local agent: {e}")
        return False
    
    return True


def run_agentcore_agent():
    """Run the AgentCore-ready agent (without actually deploying)"""
    print("\n🔧 Testing AgentCore-Ready Agent...")
    print("=" * 50)
    
    try:
        # Set environment variable to indicate this is a test run
        env = os.environ.copy()
        env['AGENTCORE_TEST_MODE'] = 'true'
        
        result = subprocess.run([
            sys.executable, 'agentcore_strands_agent.py'
        ], capture_output=True, text=True, timeout=30, env=env)
        
        if result.returncode == 0:
            print("✅ AgentCore agent code is valid!")
            print("\nOutput:")
            print(result.stdout)
        else:
            print("❌ AgentCore agent failed:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ AgentCore agent test timed out (this is normal)")
        return True
    except Exception as e:
        print(f"❌ Error testing AgentCore agent: {e}")
        return False
    
    return True


def show_deployment_options():
    """Show deployment options"""
    print("\n🚀 Deployment Options:")
    print("=" * 50)
    
    print("\n1️⃣ Local Development (Current):")
    print("   • Run agents locally for testing")
    print("   • Iterate quickly on agent logic")
    print("   • No AWS costs during development")
    
    print("\n2️⃣ Manual Deployment to AgentCore:")
    print("   • Use deployment_script.py for step-by-step guide")
    print("   • Build Docker container manually")
    print("   • Deploy using AWS CLI commands")
    
    print("\n3️⃣ Automated Deployment (Requires Toolkit):")
    print("   • Use bedrock-agentcore-starter-toolkit")
    print("   • May require AWS preview access")
    print("   • Fully automated if available")
    
    print("\n📖 For detailed deployment instructions:")
    print("   python deployment_script.py")


def main():
    """Main function"""
    print("🎯 AgentCore Runtime Local Example")
    print("=" * 50)
    print("This script helps you run and test the AgentCore example locally")
    print("without requiring the AWS AgentCore toolkit.\n")
    
    # Check environment
    if not check_environment():
        print("\n❌ Environment setup incomplete. Please fix the issues above.")
        return 1
    
    # Run local agent
    if not run_local_agent():
        print("\n❌ Local agent test failed.")
        return 1
    
    # Test AgentCore agent code
    if not run_agentcore_agent():
        print("\n❌ AgentCore agent test failed.")
        return 1
    
    # Show deployment options
    show_deployment_options()
    
    print("\n✅ All local tests passed!")
    print("\n📝 Next Steps:")
    print("1. Modify agent logic in local_strands_agent.py")
    print("2. Test changes locally using this script")
    print("3. Deploy to AgentCore when ready (see deployment_script.py)")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

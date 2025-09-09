#!/usr/bin/env python3
"""
Quick test to verify Strands agents can be created with nova-lite model
"""

from secure_prompt_engineering import create_secure_documentation_agent
from prompt_injection_defense import create_advanced_defense_agent
from input_validation_agent import create_secure_application_agent
from adversarial_testing import create_hardened_agent
from security_validation_agent import create_secure_processing_agent

def test_agent_creation():
    """Test that all security agents can be created successfully"""
    
    print("🧪 Testing Agent Creation with Nova Lite Model")
    print("=" * 50)
    
    agents_to_test = [
        ("Secure Documentation Agent", create_secure_documentation_agent),
        ("Advanced Defense Agent", create_advanced_defense_agent),
        ("Secure Application Agent", create_secure_application_agent),
        ("Hardened Agent", create_hardened_agent),
        ("Secure Processing Agent", create_secure_processing_agent),
    ]
    
    success_count = 0
    total_count = len(agents_to_test)
    
    for agent_name, create_func in agents_to_test:
        try:
            agent = create_func()
            print(f"✅ {agent_name}: Created successfully")
            print(f"   Agent Name: {agent.name}")
            print(f"   Model: {agent.model}")
            success_count += 1
        except Exception as e:
            print(f"❌ {agent_name}: Failed to create")
            print(f"   Error: {str(e)}")
    
    print(f"\n📊 Results: {success_count}/{total_count} agents created successfully")
    
    if success_count == total_count:
        print("🎉 All security agents are working with Nova Lite model!")
        return True
    else:
        print("⚠️  Some agents failed to initialize")
        return False

if __name__ == "__main__":
    test_agent_creation()

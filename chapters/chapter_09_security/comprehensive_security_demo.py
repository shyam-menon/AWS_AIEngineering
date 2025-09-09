#!/usr/bin/env python3
"""
Comprehensive Security Demo

This script demonstrates all the security concepts covered in Chapter 9,
providing a complete end-to-end example of implementing guardrails with
Strands Agents in various modes and configurations.

Prerequisites:
1. AWS credentials configured
2. Bedrock model access enabled  
3. Bedrock guardrail created in AWS Console
4. Strands Agents library installed

Usage:
    python comprehensive_security_demo.py

Author: AWS AI Engineering Course
Date: September 2025
"""

import os
import sys
import json
import time
from datetime import datetime

# Import our security modules
from basic_bedrock_guardrails import basic_guardrail_example, demonstrate_guardrail_metrics
from shadow_mode_guardrails import demonstrate_shadow_mode_guardrails
from guardrail_evaluation import run_comprehensive_evaluation
from production_monitoring import demonstrate_production_monitoring


def print_banner(title: str, char: str = "="):
    """Print a formatted banner."""
    print(f"\n{char * 80}")
    print(f"{title:^80}")
    print(f"{char * 80}")


def check_prerequisites():
    """Check if all prerequisites are met."""
    print_banner("Prerequisites Check", "=")
    
    prerequisites = {
        "AWS Credentials": False,
        "Strands Agents": False,
        "Guardrail Configuration": False
    }
    
    # Check AWS credentials
    try:
        import boto3
        session = boto3.Session()
        credentials = session.get_credentials()
        if credentials:
            prerequisites["AWS Credentials"] = True
            print("✅ AWS credentials configured")
        else:
            print("❌ AWS credentials not found")
    except Exception as e:
        print(f"❌ AWS credentials error: {str(e)}")
    
    # Check Strands Agents
    try:
        from strands import Agent
        Model
        prerequisites["Strands Agents"] = True
        print("✅ Strands Agents library available")
    except ImportError as e:
        print(f"❌ Strands Agents import error: {str(e)}")
    
    # Check guardrail configuration
    guardrail_id = os.getenv("BEDROCK_GUARDRAIL_ID")
    if guardrail_id and guardrail_id != "your-guardrail-id-here":
        prerequisites["Guardrail Configuration"] = True
        print(f"✅ Guardrail configured: {guardrail_id}")
    else:
        print("⚠️  Guardrail ID not configured in environment")
        
        # First, check if there are existing guardrails we can reuse
        if prerequisites["AWS Credentials"]:
            existing_guardrail = find_existing_guardrail()
            if existing_guardrail:
                guardrail_id, version = existing_guardrail
                print(f"✅ Found existing guardrail: {guardrail_id}")
                print(f"   Reusing instead of creating new one")
                
                # Set environment variables for this session
                os.environ["BEDROCK_GUARDRAIL_ID"] = guardrail_id
                os.environ["BEDROCK_GUARDRAIL_VERSION"] = version
                prerequisites["Guardrail Configuration"] = True
            else:
                print("   Would you like to create a guardrail automatically? (Recommended)")
                create_choice = input("   Create guardrail now? (y/N): ").strip().lower()
                if create_choice == 'y':
                    try:
                        guardrail_id, version = auto_create_guardrail()
                        if guardrail_id:
                            print(f"✅ Guardrail created automatically: {guardrail_id}")
                            prerequisites["Guardrail Configuration"] = True
                            
                            # Set environment variables for this session
                            os.environ["BEDROCK_GUARDRAIL_ID"] = guardrail_id
                            os.environ["BEDROCK_GUARDRAIL_VERSION"] = version
                            
                            print("✅ Environment variables set for this session")
                    except Exception as e:
                        print(f"❌ Failed to create guardrail: {str(e)}")
        
        if not prerequisites["Guardrail Configuration"]:
            print("   Alternative setup options:")
            print("   • Run: python quick_setup_guardrails.py")
            print("   • Run: python setup_guardrails.py") 
            print("   • Set BEDROCK_GUARDRAIL_ID environment variable manually")
    
    # Summary
    all_ready = all(prerequisites.values())
    if all_ready:
        print("\n🎉 All prerequisites met! Ready to run demos.")
    else:
        print("\n⚠️  Some prerequisites missing. Demos may not work fully.")
    
    return all_ready


def find_existing_guardrail():
    """Find an existing guardrail that can be reused."""
    try:
        import boto3
        
        bedrock = boto3.client("bedrock", region_name="us-east-1")
        response = bedrock.list_guardrails()
        
        guardrails = response.get("guardrails", [])
        
        # Look for course-related guardrails first
        for guardrail in guardrails:
            if guardrail.get("status") == "READY":
                name = guardrail.get("name", "").lower()
                if "course" in name or "demo" in name or "test" in name:
                    guardrail_id = guardrail["id"]
                    
                    # Get detailed info to ensure it's fully ready
                    detail = bedrock.get_guardrail(guardrailIdentifier=guardrail_id)
                    if detail.get("status") == "READY":
                        print(f"   Found suitable guardrail: {name}")
                        return guardrail_id, detail.get("version", "DRAFT")
        
        # If no course-specific guardrail, use any ready guardrail
        for guardrail in guardrails:
            if guardrail.get("status") == "READY":
                guardrail_id = guardrail["id"]
                detail = bedrock.get_guardrail(guardrailIdentifier=guardrail_id)
                if detail.get("status") == "READY":
                    name = guardrail.get("name", guardrail_id)
                    print(f"   Found available guardrail: {name}")
                    return guardrail_id, detail.get("version", "DRAFT")
        
        return None
        
    except Exception as e:
        print(f"   Error checking existing guardrails: {str(e)}")
        return None


def auto_create_guardrail():
    """Automatically create a basic guardrail for the demos."""
    print("\n🛡️ Auto-Creating Guardrail...")
    
    try:
        import boto3
        from datetime import datetime
        
        bedrock = boto3.client("bedrock", region_name="us-east-1")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name = f"auto-course-guardrail-{timestamp}"
        
        print(f"📋 Creating: {name}")
        
        response = bedrock.create_guardrail(
            name=name,
            description="Auto-created guardrail for AI Engineering Course",
            
            contentPolicyConfig={
                "filtersConfig": [
                    {"type": "HATE", "inputStrength": "HIGH", "outputStrength": "HIGH"},
                    {"type": "VIOLENCE", "inputStrength": "HIGH", "outputStrength": "HIGH"},
                    {"type": "MISCONDUCT", "inputStrength": "HIGH", "outputStrength": "HIGH"}
                ]
            },
            
            sensitiveInformationPolicyConfig={
                "piiEntitiesConfig": [
                    {"type": "EMAIL", "action": "BLOCK"},
                    {"type": "US_SOCIAL_SECURITY_NUMBER", "action": "BLOCK"},
                    {"type": "CREDIT_DEBIT_CARD_NUMBER", "action": "BLOCK"}
                ]
            },
            
            blockedInputMessaging="Request blocked by guardrails.",
            blockedOutputsMessaging="Response blocked by guardrails."
        )
        
        guardrail_id = response["guardrailId"]
        version = response["version"]
        
        print(f"✅ Created: {guardrail_id}")
        print("⏳ Waiting for guardrail to be ready...")
        print("   This may take 1-2 minutes...")
        
        # Wait for ready status with longer timeout and better feedback
        import time
        max_attempts = 60  # Wait up to 10 minutes
        for attempt in range(max_attempts):
            try:
                status_response = bedrock.get_guardrail(
                    guardrailIdentifier=guardrail_id,
                    guardrailVersion=version
                )
                
                current_status = status_response["status"]
                
                if current_status == "READY":
                    print("✅ Guardrail is ready!")
                    # Additional wait to ensure full propagation
                    print("   Waiting 30 seconds for full propagation...")
                    time.sleep(30)
                    return guardrail_id, version
                elif current_status in ["FAILED", "DELETED"]:
                    raise Exception(f"Guardrail creation failed: {current_status}")
                else:
                    # Show progress every 30 seconds
                    if attempt % 3 == 0:
                        print(f"   Status: {current_status} (attempt {attempt+1}/{max_attempts})")
                
                time.sleep(10)
                
            except Exception as status_error:
                if "does not exist" in str(status_error):
                    # Guardrail might still be creating
                    if attempt < 10:  # Give it more time initially
                        time.sleep(10)
                        continue
                raise status_error
        
        raise Exception("Guardrail creation timed out after 10 minutes")
        
    except Exception as e:
        print(f"❌ Auto-creation failed: {str(e)}")
        return None, None


def run_interactive_demo():
    """Run an interactive demo with user choices."""
    print_banner("Chapter 9: Security - Interactive Demo Menu")
    
    demos = {
        "1": {
            "name": "Basic Bedrock Guardrails",
            "description": "Learn basic guardrail implementation with automatic input/output filtering",
            "function": basic_guardrail_example
        },
        "2": {
            "name": "Shadow Mode Monitoring", 
            "description": "Implement shadow mode guardrails for safe testing and tuning",
            "function": demonstrate_shadow_mode_guardrails
        },
        "3": {
            "name": "Comprehensive Evaluation",
            "description": "Systematic testing and evaluation of guardrail effectiveness",
            "function": run_comprehensive_evaluation
        },
        "4": {
            "name": "Production Monitoring",
            "description": "Real-time monitoring and observability for production systems",
            "function": demonstrate_production_monitoring
        },
        "5": {
            "name": "Run All Demos",
            "description": "Execute all security demonstrations in sequence",
            "function": None  # Special case
        },
        "6": {
            "name": "Quick Guardrail Setup",
            "description": "Automatically create a guardrail for testing",
            "function": quick_guardrail_setup
        }
    }
    
    while True:
        print("\n🛡️  Security Demonstrations Available:")
        print("-" * 50)
        
        for key, demo in demos.items():
            print(f"{key}. {demo['name']}")
            print(f"   {demo['description']}")
            print()
        
        print("0. Exit")
        print()
        
        choice = input("Select a demo to run (0-6): ").strip()
        
        if choice == "0":
            print("👋 Goodbye! Thank you for learning about AI security.")
            break
        elif choice == "5":
            # Run all demos
            run_all_demos()
        elif choice == "6":
            # Quick setup
            quick_guardrail_setup()
        elif choice in demos and demos[choice]["function"]:
            demo = demos[choice]
            print_banner(f"Running: {demo['name']}")
            
            try:
                start_time = time.time()
                demo["function"]()
                duration = time.time() - start_time
                print(f"\n✅ Demo completed in {duration:.1f} seconds")
            except Exception as e:
                print(f"\n❌ Demo failed: {str(e)}")
                print("💡 Check prerequisites and configuration")
            
            input("\nPress Enter to return to menu...")
        else:
            print("❌ Invalid choice. Please select 0-6.")


def quick_guardrail_setup():
    """Quick setup function for creating a guardrail."""
    print_banner("Quick Guardrail Setup", "=")
    
    # Check if already configured
    existing_id = os.getenv("BEDROCK_GUARDRAIL_ID")
    if existing_id and existing_id != "your-guardrail-id-here":
        print(f"✅ Guardrail already configured: {existing_id}")
        choice = input("Create a new one anyway? (y/N): ").strip().lower()
        if choice != 'y':
            return
    
    # First, check for existing guardrails
    print("🔍 Checking for existing guardrails...")
    existing_guardrail = find_existing_guardrail()
    if existing_guardrail:
        guardrail_id, version = existing_guardrail
        use_existing = input(f"   Use existing guardrail {guardrail_id}? (Y/n): ").strip().lower()
        if use_existing != 'n':
            # Set environment variables for this session
            os.environ["BEDROCK_GUARDRAIL_ID"] = guardrail_id
            os.environ["BEDROCK_GUARDRAIL_VERSION"] = version
            
            print(f"\n🎉 Setup complete using existing guardrail!")
            print(f"   Guardrail ID: {guardrail_id}")
            print(f"   Version: {version}")
            print("   Environment variables set for this session.")
            print("\n💡 To make this permanent, add to your .env file:")
            print(f"   BEDROCK_GUARDRAIL_ID={guardrail_id}")
            print(f"   BEDROCK_GUARDRAIL_VERSION={version}")
            return
    
    # If no existing guardrail or user wants to create new one
    print("🆕 Creating new guardrail...")
    try:
        guardrail_id, version = auto_create_guardrail()
        if guardrail_id:
            # Set environment variables for this session
            os.environ["BEDROCK_GUARDRAIL_ID"] = guardrail_id
            os.environ["BEDROCK_GUARDRAIL_VERSION"] = version
            
            print(f"\n🎉 Setup complete!")
            print(f"   Guardrail ID: {guardrail_id}")
            print(f"   Version: {version}")
            print("   Environment variables set for this session.")
            print("\n💡 To make this permanent, add to your .env file:")
            print(f"   BEDROCK_GUARDRAIL_ID={guardrail_id}")
            print(f"   BEDROCK_GUARDRAIL_VERSION={version}")
        else:
            print("❌ Failed to create guardrail. Try manual setup.")
            
    except Exception as e:
        print(f"❌ Setup failed: {str(e)}")
        print("\n💡 Alternative options:")
        print("   • Run: python quick_setup_guardrails.py")
        print("   • Run: python setup_guardrails.py")
        print("   • Check AWS credentials and permissions")


def run_all_demos():
    """Run all demonstrations in sequence."""
    print_banner("Running All Security Demonstrations")
    
    demos = [
        ("Basic Bedrock Guardrails", basic_guardrail_example),
        ("Shadow Mode Monitoring", demonstrate_shadow_mode_guardrails),
        ("Comprehensive Evaluation", run_comprehensive_evaluation),
        ("Production Monitoring", demonstrate_production_monitoring)
    ]
    
    results = []
    total_start_time = time.time()
    
    for i, (name, function) in enumerate(demos, 1):
        print_banner(f"Demo {i}/4: {name}", "-")
        
        try:
            start_time = time.time()
            function()
            duration = time.time() - start_time
            results.append({"name": name, "status": "✅ Success", "duration": duration})
            print(f"\n✅ {name} completed in {duration:.1f} seconds")
        except Exception as e:
            duration = time.time() - start_time
            results.append({"name": name, "status": f"❌ Failed: {str(e)}", "duration": duration})
            print(f"\n❌ {name} failed after {duration:.1f} seconds: {str(e)}")
        
        if i < len(demos):
            print("\n⏸️  Pausing 3 seconds before next demo...")
            time.sleep(3)
    
    # Summary
    total_duration = time.time() - total_start_time
    print_banner("All Demos Complete - Summary")
    
    for result in results:
        print(f"{result['status']} {result['name']} ({result['duration']:.1f}s)")
    
    print(f"\n🏁 Total execution time: {total_duration:.1f} seconds")
    
    success_count = sum(1 for r in results if "Success" in r["status"])
    print(f"📊 Success rate: {success_count}/{len(results)} ({success_count/len(results)*100:.0f}%)")


def create_getting_started_guide():
    """Create a getting started guide for students."""
    guide = {
        "title": "Chapter 9: Security - Getting Started Guide",
        "overview": "This chapter demonstrates how to implement AI guardrails and security measures using Strands Agents.",
        "learning_objectives": [
            "Understand AI safety and security principles",
            "Implement Amazon Bedrock guardrails with Strands Agents",
            "Use shadow mode for safe guardrail testing",
            "Evaluate guardrail effectiveness systematically",
            "Monitor guardrails in production environments"
        ],
        "prerequisites": {
            "aws_setup": [
                "AWS account with programmatic access",
                "AWS CLI configured with appropriate credentials",
                "Amazon Bedrock service access enabled",
                "At least one Bedrock guardrail created"
            ],
            "environment": [
                "Python 3.8+ installed",
                "Strands Agents library installed",
                "Required Python packages from requirements.txt"
            ]
        },
        "demo_files": {
            "basic_bedrock_guardrails.py": "Basic guardrail implementation with Bedrock",
            "shadow_mode_guardrails.py": "Shadow mode monitoring and testing",
            "guardrail_evaluation.py": "Comprehensive evaluation framework",
            "production_monitoring.py": "Production monitoring and observability",
            "comprehensive_security_demo.py": "Interactive demo runner (this file)"
        },
        "configuration_steps": [
            "Set BEDROCK_GUARDRAIL_ID environment variable",
            "Set BEDROCK_GUARDRAIL_VERSION environment variable (optional, defaults to '1')",
            "Ensure AWS region is configured (defaults to us-west-2)",
            "Test AWS connectivity with: aws bedrock list-guardrails"
        ],
        "common_issues": {
            "access_denied": "Ensure your AWS credentials have Bedrock permissions",
            "guardrail_not_found": "Verify guardrail ID and that it exists in your AWS account",
            "model_access": "Ensure you have access to the required Bedrock models",
            "rate_limits": "Be aware of Bedrock API rate limits during testing"
        },
        "next_steps": [
            "Experiment with different guardrail policies",
            "Integrate monitoring into your production systems",
            "Develop custom evaluation test suites",
            "Implement automated alerting and response"
        ]
    }
    
    # Save to file
    with open("GETTING_STARTED.json", "w") as f:
        json.dump(guide, f, indent=2)
    
    return guide


def main():
    """Main function to run the comprehensive security demo."""
    print("🛡️ Chapter 9: Security - Comprehensive Security Demo")
    print("🎯 Learning AI Safety and Security with Strands Agents")
    print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check prerequisites first
    prerequisites_ok = check_prerequisites()
    
    # Create getting started guide
    guide = create_getting_started_guide()
    print(f"\n📖 Getting started guide saved to: GETTING_STARTED.json")
    
    if not prerequisites_ok:
        print_banner("⚠️  Setup Required", "!")
        print("Some prerequisites are missing. Please review the setup requirements:")
        print()
        
        print("🔧 Configuration Steps:")
        for step in guide["configuration_steps"]:
            print(f"   • {step}")
        
        print("\n❓ Common Issues:")
        for issue, solution in guide["common_issues"].items():
            print(f"   • {issue}: {solution}")
        
        print("\n💡 You can still run the demos, but they may not work fully.")
        
        proceed = input("\nProceed anyway? (y/N): ").strip().lower()
        if proceed != 'y':
            print("👋 Setup complete and try again!")
            return
    
    # Run interactive demo
    try:
        run_interactive_demo()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        print("💡 Please check your configuration and try again.")
    
    print(f"\n🎓 Demo session ended at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Thank you for learning about AI security with Strands Agents!")


if __name__ == "__main__":
    main()

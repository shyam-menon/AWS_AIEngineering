#!/usr/bin/env python3
"""
Quick Guardrails Setup

A simple script to quickly create a basic guardrail for testing the security examples.
This creates a minimal but functional guardrail configuration.

Usage:
    python quick_setup_guardrails.py

Author: AWS AI Engineering Course
Date: September 2025
"""

import boto3
import json
import time
from datetime import datetime


def create_basic_guardrail():
    """Create a basic guardrail quickly for testing."""
    print("🚀 Quick Guardrail Setup for Chapter 9 Examples")
    print("=" * 50)
    
    try:
        # Connect to Bedrock
        bedrock = boto3.client("bedrock", region_name="us-east-1")
        print("✅ Connected to AWS Bedrock")
        
        # Create basic guardrail
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name = f"course-guardrail-{timestamp}"
        
        print(f"📋 Creating guardrail: {name}")
        
        response = bedrock.create_guardrail(
            name=name,
            description="Basic guardrail for AI Engineering Course examples",
            
            # Basic content filtering
            contentPolicyConfig={
                "filtersConfig": [
                    {"type": "HATE", "inputStrength": "HIGH", "outputStrength": "HIGH"},
                    {"type": "VIOLENCE", "inputStrength": "HIGH", "outputStrength": "HIGH"},
                    {"type": "SEXUAL", "inputStrength": "MEDIUM", "outputStrength": "MEDIUM"},
                    {"type": "MISCONDUCT", "inputStrength": "HIGH", "outputStrength": "HIGH"}
                ]
            },
            
            # Basic PII detection
            sensitiveInformationPolicyConfig={
                "piiEntitiesConfig": [
                    {"type": "EMAIL", "action": "BLOCK"},
                    {"type": "PHONE", "action": "BLOCK"},
                    {"type": "US_SOCIAL_SECURITY_NUMBER", "action": "BLOCK"},
                    {"type": "CREDIT_DEBIT_CARD_NUMBER", "action": "BLOCK"}
                ]
            },
            
            # Basic topic restrictions
            topicPolicyConfig={
                "topicsConfig": [
                    {
                        "name": "Harmful Content",
                        "definition": "Content that could cause harm including violence, illegal activities, or dangerous instructions.",
                        "examples": ["How to make weapons", "Illegal drug information"],
                        "type": "DENY"
                    }
                ]
            },
            
            blockedInputMessaging="I cannot process this request due to content policy.",
            blockedOutputsMessaging="I cannot provide this information due to content policy.",
            
            tags=[
                {"key": "Project", "value": "AIEngineeringCourse"},
                {"key": "Purpose", "value": "QuickDemo"}
            ]
        )
        
        guardrail_id = response["guardrailId"]
        version = response["version"]
        
        print(f"✅ Guardrail created!")
        print(f"   ID: {guardrail_id}")
        print(f"   Version: {version}")
        
        # Wait for it to be ready
        print("⏳ Waiting for guardrail to be ready...")
        while True:
            status_response = bedrock.get_guardrail(
                guardrailIdentifier=guardrail_id,
                guardrailVersion=version
            )
            
            status = status_response["status"]
            print(f"   Status: {status}")
            
            if status == "READY":
                break
            elif status in ["FAILED", "DELETED"]:
                raise Exception(f"Guardrail creation failed: {status}")
            
            time.sleep(10)
        
        # Save configuration
        config = {
            "guardrail_id": guardrail_id,
            "version": version,
            "name": name,
            "created_at": datetime.now().isoformat()
        }
        
        with open("quick_guardrail_config.json", "w") as f:
            json.dump(config, f, indent=2)
        
        print("\n🎯 SUCCESS! Your guardrail is ready.")
        print("\n🔧 Set these environment variables:")
        print(f'$env:BEDROCK_GUARDRAIL_ID="{guardrail_id}"')
        print(f'$env:BEDROCK_GUARDRAIL_VERSION="{version}"')
        
        print(f"\n🚀 Now you can run the security examples!")
        
        return guardrail_id, version
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None, None


if __name__ == "__main__":
    create_basic_guardrail()

#!/usr/bin/env python3
"""
AWS Bedrock Guardrails Setup Script

This script automatically creates a comprehensive guardrail configuration in AWS Bedrock
using boto3. It sets up content filters, topic policies, and PII detection suitable
for the Chapter 9 security examples.

Prerequisites:
1. AWS credentials configured with appropriate permissions
2. boto3 installed
3. Access to Amazon Bedrock service

Usage:
    python setup_guardrails.py

The script will:
1. Create a new guardrail with comprehensive safety policies
2. Configure content filters for harmful content
3. Set up topic restrictions
4. Enable PII detection
5. Output the guardrail ID for use in examples

Author: AWS AI Engineering Course
Date: September 2025
"""

import boto3
import json
import time
import os
from datetime import datetime
from typing import Dict, Any, Optional


class GuardrailSetup:
    """
    Class to handle automated guardrail creation in AWS Bedrock.
    """
    
    def __init__(self, region: str = "us-east-1"):
        """
        Initialize the guardrail setup client.
        
        Args:
            region: AWS region to create the guardrail in
        """
        self.region = region
        try:
            self.bedrock_client = boto3.client("bedrock", region_name=region)
            print(f"✅ Connected to AWS Bedrock in region: {region}")
        except Exception as e:
            print(f"❌ Failed to connect to AWS Bedrock: {str(e)}")
            raise
    
    def create_comprehensive_guardrail(self, name: str = None) -> Dict[str, Any]:
        """
        Create a comprehensive guardrail with all necessary policies.
        
        Args:
            name: Custom name for the guardrail (optional)
            
        Returns:
            Dictionary containing guardrail details
        """
        if not name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name = f"ai-engineering-course-guardrail-{timestamp}"
        
        print(f"🛡️ Creating guardrail: {name}")
        print("=" * 60)
        
        # Define comprehensive guardrail configuration
        guardrail_config = {
            "name": name,
            "description": "Comprehensive guardrail for AI Engineering Course Chapter 9 examples",
            "topicPolicyConfig": self._get_topic_policy_config(),
            "contentPolicyConfig": self._get_content_policy_config(),
            "wordPolicyConfig": self._get_word_policy_config(),
            "sensitiveInformationPolicyConfig": self._get_pii_policy_config(),
            "blockedInputMessaging": "I cannot process this request as it violates our content policy.",
            "blockedOutputsMessaging": "I cannot provide this information as it violates our content policy.",
            "kmsKeyId": None,  # Use default AWS managed key
            "tags": [
                {"key": "Project", "value": "AIEngineeringCourse"},
                {"key": "Chapter", "value": "Chapter9Security"},
                {"key": "Purpose", "value": "EducationalDemo"}
            ]
        }
        
        try:
            print("📋 Guardrail Configuration:")
            print(f"   Name: {name}")
            print(f"   Description: {guardrail_config['description']}")
            print("   Policies: Content, Topic, Word, PII Detection")
            print()
            
            # Create the guardrail
            print("🚀 Creating guardrail in AWS...")
            response = self.bedrock_client.create_guardrail(**guardrail_config)
            
            guardrail_id = response["guardrailId"]
            guardrail_arn = response["guardrailArn"]
            version = response["version"]
            
            print(f"✅ Guardrail created successfully!")
            print(f"   ID: {guardrail_id}")
            print(f"   ARN: {guardrail_arn}")
            print(f"   Version: {version}")
            
            # Wait for guardrail to be ready
            print("\n⏳ Waiting for guardrail to become ready...")
            self._wait_for_guardrail_ready(guardrail_id, version)
            
            # Get final details
            final_details = self.bedrock_client.get_guardrail(
                guardrailIdentifier=guardrail_id,
                guardrailVersion=version
            )
            
            result = {
                "guardrail_id": guardrail_id,
                "guardrail_arn": guardrail_arn,
                "version": version,
                "name": name,
                "status": final_details["status"],
                "created_at": final_details["createdAt"].isoformat(),
                "region": self.region
            }
            
            print(f"🎉 Guardrail is ready for use!")
            print(f"   Status: {result['status']}")
            
            return result
            
        except Exception as e:
            print(f"❌ Failed to create guardrail: {str(e)}")
            raise
    
    def _get_content_policy_config(self) -> Dict[str, Any]:
        """Define content filtering policies."""
        return {
            "filtersConfig": [
                {
                    "type": "SEXUAL",
                    "inputStrength": "HIGH",
                    "outputStrength": "HIGH"
                },
                {
                    "type": "VIOLENCE",
                    "inputStrength": "HIGH", 
                    "outputStrength": "HIGH"
                },
                {
                    "type": "HATE",
                    "inputStrength": "HIGH",
                    "outputStrength": "HIGH"
                },
                {
                    "type": "INSULTS",
                    "inputStrength": "MEDIUM",
                    "outputStrength": "MEDIUM"
                },
                {
                    "type": "MISCONDUCT",
                    "inputStrength": "HIGH",
                    "outputStrength": "HIGH"
                },
                {
                    "type": "PROMPT_ATTACK",
                    "inputStrength": "HIGH",
                    "outputStrength": "NONE"
                }
            ]
        }
    
    def _get_topic_policy_config(self) -> Dict[str, Any]:
        """Define topic restriction policies."""
        return {
            "topicsConfig": [
                {
                    "name": "Illegal Activities",
                    "definition": "Content related to illegal activities, including but not limited to drug trafficking, weapons manufacturing, fraud, and other criminal activities.",
                    "examples": [
                        "How to make explosives",
                        "Drug trafficking methods",
                        "Credit card fraud techniques"
                    ],
                    "type": "DENY"
                },
                {
                    "name": "Harmful Instructions",
                    "definition": "Instructions that could cause physical or psychological harm to individuals or groups.",
                    "examples": [
                        "Self-harm methods",
                        "Dangerous pranks",
                        "Harmful chemical combinations"
                    ],
                    "type": "DENY"
                },
                {
                    "name": "Financial Fraud",
                    "definition": "Content related to financial fraud, scams, or deceptive financial practices.",
                    "examples": [
                        "Ponzi scheme setup",
                        "Identity theft methods",
                        "Fake document creation"
                    ],
                    "type": "DENY"
                },
                {
                    "name": "Privacy Violations",
                    "definition": "Content that could lead to privacy violations or unauthorized access to personal information.",
                    "examples": [
                        "Hacking techniques",
                        "Social engineering methods",
                        "Personal data extraction"
                    ],
                    "type": "DENY"
                }
            ]
        }
    
    def _get_word_policy_config(self) -> Dict[str, Any]:
        """Define custom word filtering policies."""
        return {
            "wordsConfig": [
                {"text": "bomb"},
                {"text": "explosive"},
                {"text": "hack"},
                {"text": "exploit"},
                {"text": "malware"},
                {"text": "virus"},
                {"text": "phishing"},
                {"text": "scam"}
            ],
            "managedWordListsConfig": [
                {"type": "PROFANITY"}
            ]
        }
    
    def _get_pii_policy_config(self) -> Dict[str, Any]:
        """Define PII detection and handling policies."""
        return {
            "piiEntitiesConfig": [
                {
                    "type": "EMAIL",
                    "action": "BLOCK"
                },
                {
                    "type": "PHONE",
                    "action": "BLOCK"
                },
                {
                    "type": "US_SOCIAL_SECURITY_NUMBER",
                    "action": "BLOCK"
                },
                {
                    "type": "CREDIT_DEBIT_CARD_NUMBER",
                    "action": "BLOCK"
                },
                {
                    "type": "US_BANK_ACCOUNT_NUMBER",
                    "action": "BLOCK"
                },
                {
                    "type": "NAME",
                    "action": "ANONYMIZE"
                },
                {
                    "type": "ADDRESS",
                    "action": "ANONYMIZE"
                },
                {
                    "type": "USERNAME",
                    "action": "ANONYMIZE"
                },
                {
                    "type": "PASSWORD",
                    "action": "BLOCK"
                },
                {
                    "type": "DRIVER_ID",
                    "action": "BLOCK"
                },
                {
                    "type": "US_PASSPORT_NUMBER",
                    "action": "BLOCK"
                }
            ],
            "regexesConfig": [
                {
                    "name": "API_Key_Pattern",
                    "description": "Detect API keys and tokens",
                    "pattern": r"[Aa][Pp][Ii]_?[Kk][Ee][Yy].*[A-Za-z0-9]{20,}",
                    "action": "BLOCK"
                },
                {
                    "name": "AWS_Access_Key",
                    "description": "Detect AWS access keys",
                    "pattern": r"AKIA[0-9A-Z]{16}",
                    "action": "BLOCK"
                }
            ]
        }
    
    def _wait_for_guardrail_ready(self, guardrail_id: str, version: str, max_wait_time: int = 300):
        """
        Wait for guardrail to become ready.
        
        Args:
            guardrail_id: The guardrail ID
            version: The guardrail version
            max_wait_time: Maximum time to wait in seconds
        """
        start_time = time.time()
        
        while time.time() - start_time < max_wait_time:
            try:
                response = self.bedrock_client.get_guardrail(
                    guardrailIdentifier=guardrail_id,
                    guardrailVersion=version
                )
                
                status = response["status"]
                print(f"   Status: {status}")
                
                if status == "READY":
                    return
                elif status in ["FAILED", "DELETED"]:
                    raise Exception(f"Guardrail creation failed with status: {status}")
                
                time.sleep(10)  # Wait 10 seconds before checking again
                
            except Exception as e:
                if "ThrottlingException" in str(e):
                    print("   Rate limited, waiting longer...")
                    time.sleep(30)
                else:
                    raise
        
        raise Exception(f"Guardrail did not become ready within {max_wait_time} seconds")
    
    def list_existing_guardrails(self) -> list:
        """List existing guardrails in the account."""
        try:
            response = self.bedrock_client.list_guardrails()
            return response.get("guardrails", [])
        except Exception as e:
            print(f"Failed to list guardrails: {str(e)}")
            return []
    
    def delete_guardrail(self, guardrail_id: str) -> bool:
        """
        Delete a guardrail.
        
        Args:
            guardrail_id: The guardrail ID to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.bedrock_client.delete_guardrail(guardrailIdentifier=guardrail_id)
            print(f"✅ Guardrail {guardrail_id} deleted successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to delete guardrail {guardrail_id}: {str(e)}")
            return False


def save_guardrail_config(guardrail_info: Dict[str, Any], filename: str = "guardrail_config.json"):
    """Save guardrail configuration to a file."""
    with open(filename, "w") as f:
        json.dump(guardrail_info, f, indent=2)
    print(f"📁 Guardrail configuration saved to: {filename}")


def update_environment_variables(guardrail_info: Dict[str, Any]):
    """Update environment variables with guardrail information."""
    guardrail_id = guardrail_info["guardrail_id"]
    version = guardrail_info["version"]
    
    # For Windows PowerShell
    print("\n🔧 Environment Variable Setup:")
    print("Copy and run these commands in PowerShell:")
    print(f'$env:BEDROCK_GUARDRAIL_ID="{guardrail_id}"')
    print(f'$env:BEDROCK_GUARDRAIL_VERSION="{version}"')
    
    # For Linux/Mac
    print("\nOr for Linux/Mac (Bash):")
    print(f'export BEDROCK_GUARDRAIL_ID="{guardrail_id}"')
    print(f'export BEDROCK_GUARDRAIL_VERSION="{version}"')
    
    # For .env file
    print(f"\nOr add to .env file:")
    print(f'BEDROCK_GUARDRAIL_ID={guardrail_id}')
    print(f'BEDROCK_GUARDRAIL_VERSION={version}')


def main():
    """Main function to set up guardrails."""
    print("🛡️ AWS Bedrock Guardrails Setup for AI Engineering Course")
    print("=" * 70)
    
    try:
        # Initialize setup
        setup = GuardrailSetup()
        
        # Check existing guardrails
        print("\n📋 Checking existing guardrails...")
        existing = setup.list_existing_guardrails()
        
        if existing:
            print(f"Found {len(existing)} existing guardrail(s):")
            for i, guardrail in enumerate(existing, 1):
                print(f"   {i}. {guardrail['name']} (ID: {guardrail['id']})")
            
            # Ask if user wants to use existing or create new
            choice = input("\nWould you like to (c)reate a new guardrail or (u)se existing? [c/u]: ").lower().strip()
            
            if choice == 'u' and existing:
                # Use existing guardrail
                if len(existing) == 1:
                    selected = existing[0]
                else:
                    print("\nSelect guardrail to use:")
                    for i, guardrail in enumerate(existing, 1):
                        print(f"   {i}. {guardrail['name']}")
                    
                    while True:
                        try:
                            selection = int(input("Enter number: ")) - 1
                            if 0 <= selection < len(existing):
                                selected = existing[selection]
                                break
                            else:
                                print("Invalid selection. Try again.")
                        except ValueError:
                            print("Please enter a valid number.")
                
                guardrail_info = {
                    "guardrail_id": selected["id"],
                    "guardrail_arn": selected["arn"],
                    "version": "DRAFT",  # Use DRAFT version for existing
                    "name": selected["name"],
                    "status": selected["status"],
                    "created_at": selected["createdAt"].isoformat(),
                    "region": setup.region
                }
                
                print(f"\n✅ Using existing guardrail: {selected['name']}")
                print(f"   ID: {selected['id']}")
                
            else:
                # Create new guardrail
                guardrail_info = setup.create_comprehensive_guardrail()
        else:
            print("No existing guardrails found. Creating new one...")
            guardrail_info = setup.create_comprehensive_guardrail()
        
        # Save configuration
        save_guardrail_config(guardrail_info)
        
        # Show environment setup
        update_environment_variables(guardrail_info)
        
        print(f"\n🎉 Setup Complete!")
        print(f"Your guardrail is ready for use in the Chapter 9 security examples.")
        print(f"\nNext steps:")
        print(f"1. Set the environment variables shown above")
        print(f"2. Run the security examples: python comprehensive_security_demo.py")
        print(f"3. Or run individual examples: python basic_bedrock_guardrails.py")
        
    except Exception as e:
        print(f"\n❌ Setup failed: {str(e)}")
        print("\nTroubleshooting:")
        print("- Ensure AWS credentials are configured")
        print("- Verify Bedrock service access in your region")
        print("- Check IAM permissions for Bedrock operations")
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

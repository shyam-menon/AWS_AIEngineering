#!/usr/bin/env python3
"""
Customer Support Agent with Intent Classification and Human Handoff

This example demonstrates a sophisticated customer support workflow using Strands Agents:

1. Intent Classification - Uses Amazon Nova Lite to analyze customer queries
2. Knowledge Lookup - Mock implementation of AWS Bedrock Knowledge Base
3. Escalation Check - Determines if human intervention is needed  
4. Human Handoff - Routes complex/angry customers to human agents
5. Response Generation - Creates appropriate responses based on context

Workflow:
Customer Query → Intent Classification → (Knowledge Lookup + Escala            tools=[
                classify_customer_intent, 
                lookup_knowledge_base, 
                check_escalation_needed,
                prepare_human_handoff,
                generate_customer_response,
                handoff_to_user  # Re-added for proper HITL flow
            ],ck) → 
                → Human Handoff OR Response Generation

Author: AWS AI Engineering Course  
Date: September 2025
"""

import json
from typing import Dict, List, Any, Optional
from datetime import datetime

try:
    from strands import Agent
    from strands.tools import tool
    import boto3
    
    # Custom non-blocking handoff for web UI
    @tool
    def handoff_to_user(message: str) -> str:
        """
        Custom handoff that signals completion without blocking.
        The web UI will handle the actual human interaction separately.
        """
        print(f"🔄 HANDOFF INITIATED: {message[:100]}...")
        # Return a signal that handoff was initiated (not blocking)
        return "HANDOFF_INITIATED: Human agent intervention requested. Awaiting web-based feedback."
    
    print("✅ All required libraries imported successfully!")
    
    # Initialize AWS Bedrock client
    bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')
    
    # === INTENT CLASSIFICATION TOOL ===
    @tool
    def classify_customer_intent(customer_query: str) -> Dict[str, Any]:
        """
        Classify customer intent using Amazon Nova Lite model via AWS Bedrock.
        
        Analyzes customer query for:
        - Intent categories (RETURNS_REFUNDS, TECHNICAL_SUPPORT, BILLING, etc.)
        - Emotional state (happy, neutral, frustrated, angry)
        - Urgency level (low, medium, high)
        - Confidence score
        
        Args:
            customer_query (str): Raw customer query text
            
        Returns:
            Dict containing intent classification results
        """
        try:
            # Construct prompt for intent classification
            classification_prompt = f"""
You are a customer service intent classifier. Analyze the following customer message and provide a structured classification.

Customer message: "{customer_query}"

Analyze for:
1. Primary intent (choose one): RETURNS_REFUNDS, TECHNICAL_SUPPORT, BILLING, GENERAL_INQUIRY, COMPLAINT, PRODUCT_INFO
2. Customer emotion (choose one): happy, satisfied, neutral, concerned, frustrated, angry
3. Urgency level (choose one): low, medium, high
4. Key indicators that led to your classification

Provide your response in this exact JSON format:
{{
  "intent": "CATEGORY_NAME",
  "confidence": 0.95,
  "reasoning": "Brief explanation of classification decision",
  "urgency": "level",
  "customer_emotion": "emotion",
  "key_phrases": ["phrase1", "phrase2"],
  "escalation_triggers": ["trigger1", "trigger2"]
}}

Focus on detecting escalation triggers like:
- Negative product language ("garbage", "terrible", "awful")
- Demand language ("NOW!", "immediately", "right now")
- Emotional expressions ("!!!", "frustrated", "angry")
- Refund/money demands
"""
            
            # Call Amazon Nova Lite model
            response = bedrock_client.invoke_model(
                modelId="amazon.nova-lite-v1:0",
                body=json.dumps({
                    "schemaVersion": "messages-v1",
                    "messages": [
                        {
                            "role": "user",
                            "content": [{"text": classification_prompt}]
                        }
                    ],
                    "inferenceConfig": {
                        "maxTokens": 1000,
                        "temperature": 0.1
                    }
                })
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            classification_text = response_body['output']['message']['content'][0]['text']
            
            # Extract JSON from response
            start_idx = classification_text.find('{')
            end_idx = classification_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                classification_json = json.loads(classification_text[start_idx:end_idx])
                
                # Add timestamp and processing info
                classification_json.update({
                    "timestamp": datetime.now().isoformat(),
                    "model_used": "amazon.nova-lite-v1:0",
                    "processing_status": "success"
                })
                
                print(f"🎯 Intent Classification: {classification_json['intent']}")
                print(f"😊 Customer Emotion: {classification_json['customer_emotion']}")
                print(f"⚡ Urgency Level: {classification_json['urgency']}")
                
                return classification_json
            else:
                raise ValueError("Could not parse JSON from model response")
                
        except Exception as e:
            print(f"❌ Error in intent classification: {e}")
            # Return fallback classification
            return {
                "intent": "GENERAL_INQUIRY",
                "confidence": 0.5,
                "reasoning": f"Classification failed: {str(e)}",
                "urgency": "medium",
                "customer_emotion": "neutral",
                "key_phrases": [],
                "escalation_triggers": [],
                "timestamp": datetime.now().isoformat(),
                "model_used": "amazon.nova-lite-v1:0",
                "processing_status": "error"
            }
    
    # === KNOWLEDGE LOOKUP TOOL ===
    @tool
    def lookup_knowledge_base(intent_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mock implementation of AWS Bedrock Knowledge Base lookup.
        
        In production, this would query a real knowledge base with company policies,
        procedures, and relevant documentation based on the classified intent.
        
        Args:
            intent_data (Dict): Intent classification results
            
        Returns:
            Dict containing relevant knowledge base articles and procedures
        """
        try:
            intent = intent_data.get("intent", "GENERAL_INQUIRY")
            customer_emotion = intent_data.get("customer_emotion", "neutral")
            
            print(f"🔍 Looking up knowledge for intent: {intent}")
            
            # Mock knowledge base responses based on intent
            knowledge_base = {
                "RETURNS_REFUNDS": {
                    "relevant_articles": [
                        "30-day return policy",
                        "Refund processing procedures", 
                        "Product quality guarantee",
                        "Return shipping guidelines"
                    ],
                    "procedures": [
                        "Verify purchase date within 30 days",
                        "Check product condition requirements",
                        "Process refund request in system",
                        "Send return shipping label via email",
                        "Follow up within 48 hours"
                    ],
                    "policies": "Full refund available within 30 days of purchase for any reason. Refunds processed within 5-7 business days after item received. No restocking fee for defective items.",
                    "escalation_triggers": [
                        "Customer expressing extreme dissatisfaction",
                        "Product quality complaints",
                        "Immediate refund demands",
                        "Multiple previous contacts about same issue"
                    ]
                },
                "TECHNICAL_SUPPORT": {
                    "relevant_articles": [
                        "Product troubleshooting guide",
                        "Common technical issues",
                        "Setup and installation help",
                        "Warranty coverage details"
                    ],
                    "procedures": [
                        "Gather device/software information",
                        "Walk through basic troubleshooting steps",
                        "Escalate to technical specialists if needed",
                        "Schedule callback if issue persists"
                    ],
                    "policies": "Free technical support for 90 days. Extended support available with warranty. Remote assistance available.",
                    "escalation_triggers": [
                        "Complex technical issues",
                        "Customer frustration with multiple attempts",
                        "Hardware replacement needed"
                    ]
                },
                "BILLING": {
                    "relevant_articles": [
                        "Billing cycle information",
                        "Payment methods accepted",
                        "Dispute resolution process",
                        "Account management"
                    ],
                    "procedures": [
                        "Verify customer identity",
                        "Review billing history",
                        "Explain charges if needed",
                        "Process adjustments if warranted"
                    ],
                    "policies": "Billing disputes reviewed within 24 hours. Adjustments made for legitimate errors. Payment plans available for large amounts.",
                    "escalation_triggers": [
                        "Disputed charges over $100",
                        "Multiple billing complaints",
                        "Payment processing errors"
                    ]
                }
            }
            
            # Get knowledge for specific intent or default
            knowledge = knowledge_base.get(intent, {
                "relevant_articles": ["General FAQ", "Contact information"],
                "procedures": ["Listen to customer needs", "Provide appropriate guidance"],
                "policies": "We're here to help with any questions or concerns.",
                "escalation_triggers": ["Complex requests", "Customer dissatisfaction"]
            })
            
            # Add context-aware information
            knowledge.update({
                "intent_context": intent,
                "customer_emotion_context": customer_emotion,
                "retrieval_timestamp": datetime.now().isoformat(),
                "knowledge_source": "mock_bedrock_kb",
                "confidence_score": 0.92
            })
            
            print(f"📚 Found {len(knowledge['relevant_articles'])} relevant articles")
            
            return knowledge
            
        except Exception as e:
            print(f"❌ Error in knowledge lookup: {e}")
            return {
                "relevant_articles": ["General support"],
                "procedures": ["Contact customer service"],
                "policies": "Standard support policies apply",
                "escalation_triggers": [],
                "error": str(e),
                "retrieval_timestamp": datetime.now().isoformat()
            }
    
    # === ESCALATION CHECK TOOL ===
    @tool  
    def check_escalation_needed(intent_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate whether customer query requires human escalation.
        
        Analyzes multiple factors:
        - Customer emotional state
        - Urgency indicators  
        - Intent complexity
        - Escalation triggers from intent classification
        
        Args:
            intent_data (Dict): Intent classification results
            
        Returns:
            Dict containing escalation decision and reasoning
        """
        try:
            print("🚨 Evaluating escalation criteria...")
            
            # Extract key factors
            emotion = intent_data.get("customer_emotion", "neutral")
            urgency = intent_data.get("urgency", "low") 
            intent = intent_data.get("intent", "GENERAL_INQUIRY")
            escalation_triggers = intent_data.get("escalation_triggers", [])
            confidence = intent_data.get("confidence", 0.0)
            
            # Define escalation rules
            escalation_score = 0
            escalation_reasons = []
            
            # Emotion-based escalation
            emotion_weights = {
                "angry": 4,
                "frustrated": 3,
                "concerned": 2,
                "neutral": 1,
                "satisfied": 0,
                "happy": 0
            }
            emotion_score = emotion_weights.get(emotion, 1)
            escalation_score += emotion_score
            
            if emotion in ["angry", "frustrated"]:
                escalation_reasons.append(f"Customer emotion is '{emotion}' - requires empathetic handling")
            
            # Urgency-based escalation
            urgency_weights = {"high": 3, "medium": 1, "low": 0}
            urgency_score = urgency_weights.get(urgency, 0)
            escalation_score += urgency_score
            
            if urgency == "high":
                escalation_reasons.append("High urgency request - immediate attention needed")
            
            # Intent-based escalation
            high_risk_intents = ["RETURNS_REFUNDS", "COMPLAINT", "BILLING"]
            if intent in high_risk_intents and emotion in ["angry", "frustrated"]:
                escalation_score += 2
                escalation_reasons.append(f"High-risk intent ({intent}) combined with negative emotion")
            
            # Escalation trigger keywords
            if escalation_triggers:
                escalation_score += len(escalation_triggers)
                escalation_reasons.append(f"Escalation triggers detected: {', '.join(escalation_triggers)}")
            
            # Determine final escalation decision
            escalate = escalation_score >= 4  # Threshold for escalation
            
            # Determine priority and department
            if escalate:
                if escalation_score >= 6:
                    priority_level = "critical"
                    suggested_department = "management"
                elif escalation_score >= 5:
                    priority_level = "high" 
                    suggested_department = "senior_support"
                else:
                    priority_level = "medium"
                    suggested_department = "standard_support"
            else:
                priority_level = "low"
                suggested_department = "automated"
            
            # Build escalation response
            escalation_result = {
                "escalate": escalate,
                "escalation_score": escalation_score,
                "escalation_reason": "; ".join(escalation_reasons) if escalation_reasons else "No escalation triggers detected",
                "priority_level": priority_level,
                "suggested_department": suggested_department,
                "customer_context": f"Customer with {emotion} emotion, {urgency} urgency, {intent} intent",
                "decision_timestamp": datetime.now().isoformat(),
                "factors_analyzed": {
                    "emotion": emotion,
                    "urgency": urgency,
                    "intent": intent,
                    "triggers": escalation_triggers,
                    "confidence": confidence
                }
            }
            
            if escalate:
                print(f"🚨 ESCALATION REQUIRED - Score: {escalation_score}")
                print(f"📋 Priority: {priority_level.upper()}")
                print(f"🏢 Department: {suggested_department}")
            else:
                print(f"✅ No escalation needed - Score: {escalation_score}")
            
            return escalation_result
            
        except Exception as e:
            print(f"❌ Error in escalation check: {e}")
            return {
                "escalate": True,  # Default to escalation on error
                "escalation_reason": f"Error in automated processing: {str(e)}",
                "priority_level": "high",
                "suggested_department": "technical_support", 
                "customer_context": "System error during escalation evaluation",
                "error": str(e),
                "decision_timestamp": datetime.now().isoformat()
            }
    
    # === HUMAN HANDOFF TOOL ===
    @tool
    def prepare_human_handoff(escalation_data: Dict[str, Any], intent_data: Dict[str, Any], knowledge_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare comprehensive handoff package for human agents.
        
        Combines all analysis results into a structured handoff that provides
        human agents with full context and suggested actions.
        
        Args:
            escalation_data (Dict): Escalation analysis results
            intent_data (Dict): Intent classification results  
            knowledge_data (Dict): Knowledge base lookup results
            
        Returns:
            Dict containing complete handoff package
        """
        try:
            print("👥 Preparing human handoff package...")
            
            # Extract key information
            priority = escalation_data.get("priority_level", "medium")
            department = escalation_data.get("suggested_department", "support")
            customer_emotion = intent_data.get("customer_emotion", "neutral")
            intent = intent_data.get("intent", "UNKNOWN")
            urgency = intent_data.get("urgency", "medium")
            
            # Create priority prefix
            priority_prefix = {
                "critical": "🚨 CRITICAL PRIORITY",
                "high": "⚠️ HIGH PRIORITY", 
                "medium": "📋 MEDIUM PRIORITY",
                "low": "📝 LOW PRIORITY"
            }.get(priority, "📋 PRIORITY")
            
            # Generate handoff message
            handoff_message = f"""{priority_prefix} - Customer Support Escalation

Customer Profile:
• Emotional State: {customer_emotion.upper()}
• Request Type: {intent}
• Urgency Level: {urgency.upper()}
• Escalation Reason: {escalation_data.get('escalation_reason', 'System escalation')}

{escalation_data.get('customer_context', 'Customer requires human assistance')}

Immediate Action Required: This customer needs {priority} attention from the {department} team with empathetic, solution-focused approach."""

            # Compile customer summary
            customer_summary = f"""Customer is experiencing {customer_emotion} emotions regarding a {intent.lower().replace('_', ' ')} issue. 
Escalation score: {escalation_data.get('escalation_score', 'N/A')}/10. 
Key concerns: {', '.join(intent_data.get('key_phrases', ['General inquiry']))}.
Requires careful, empathetic handling with focus on immediate resolution."""

            # Identify attempted solutions
            attempted_solutions = [
                "Automated intent classification completed",
                "Knowledge base accessed for relevant policies",
                "Escalation criteria evaluated"
            ]
            
            if knowledge_data.get("relevant_articles"):
                attempted_solutions.append(f"Found {len(knowledge_data['relevant_articles'])} relevant help articles")
            
            # Create comprehensive handoff package
            handoff_package = {
                "handoff_message": handoff_message,
                "customer_summary": customer_summary,
                "priority": priority,
                "department": department,
                "attempted_solutions": attempted_solutions,
                "recommended_actions": [
                    f"Address customer with empathetic {customer_emotion} emotion handling",
                    "Review provided knowledge base articles for context",
                    "Focus on immediate resolution to prevent further escalation",
                    "Follow up within 24 hours to ensure satisfaction"
                ],
                "knowledge_context": {
                    "relevant_policies": knowledge_data.get("policies", "Standard policies apply"),
                    "available_procedures": knowledge_data.get("procedures", []),
                    "escalation_triggers": knowledge_data.get("escalation_triggers", [])
                },
                "technical_details": {
                    "classification_confidence": intent_data.get("confidence", 0.0),
                    "escalation_score": escalation_data.get("escalation_score", 0),
                    "processing_timestamp": datetime.now().isoformat(),
                    "model_used": intent_data.get("model_used", "amazon.nova-lite-v1:0")
                }
            }
            
            print(f"✅ Handoff package prepared for {department} team")
            print(f"📊 Package includes {len(attempted_solutions)} attempted solutions")
            
            # Initiate the actual handoff
            handoff_result = handoff_to_user(handoff_message)
            handoff_package["handoff_initiated"] = handoff_result
            
            return handoff_package
            
        except Exception as e:
            print(f"❌ Error preparing handoff: {e}")
            return {
                "handoff_message": f"PRIORITY: System Error - Customer requires immediate human attention due to processing error: {str(e)}",
                "customer_summary": "System error occurred during automated processing. Customer needs human assistance.",
                "priority": "high",
                "department": "technical_support",
                "attempted_solutions": ["Automated processing attempted but failed"],
                "error": str(e),
                "processing_timestamp": datetime.now().isoformat()
            }
    
    # === RESPONSE GENERATION TOOL ===
    @tool
    def generate_customer_response(intent_data: Dict[str, Any], knowledge_data: Dict[str, Any], escalation_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate appropriate customer response based on all available context.
        
        Creates empathetic, solution-focused responses that acknowledge customer
        emotions and provide clear next steps.
        
        Args:
            intent_data (Dict): Intent classification results
            knowledge_data (Dict): Knowledge base results
            escalation_data (Dict): Escalation analysis results
            
        Returns:
            Dict containing generated response and metadata
        """
        try:
            print("💬 Generating customer response...")
            
            # Extract context
            intent = intent_data.get("intent", "GENERAL_INQUIRY")
            emotion = intent_data.get("customer_emotion", "neutral")
            urgency = intent_data.get("urgency", "medium")
            escalate = escalation_data.get("escalate", False) if escalation_data else False
            policies = knowledge_data.get("policies", "")
            
            # Response templates based on emotion and intent
            if emotion in ["angry", "frustrated"]:
                empathy_opener = "I sincerely apologize that our product/service didn't meet your expectations. I completely understand your frustration, and I want to make this right immediately."
            elif emotion == "concerned":
                empathy_opener = "I understand your concerns and I'm here to help resolve this for you."
            else:
                empathy_opener = "Thank you for contacting us. I'm happy to help you with your request."
            
            # Intent-specific response content
            if intent == "RETURNS_REFUNDS":
                if escalate:
                    response_content = f"""{empathy_opener}

Let me connect you with our management team who can process your request right away and ensure you have a better experience with us.

While I'm getting them for you, here's what I can tell you about our return policy:
{policies}

Someone from our management team will be with you within 2 minutes to personally handle your refund request."""
                else:
                    response_content = f"""{empathy_opener}

I'd be happy to help you with your return/refund request. Here's our policy:
{policies}

To process your return, I'll need your order number and I can get this started right away. Would you prefer a full refund or would you like to exchange for a different product?"""
                    
            elif intent == "TECHNICAL_SUPPORT":
                if escalate:
                    response_content = f"""{empathy_opener}

I'm connecting you with one of our technical specialists who can provide detailed assistance with your issue. They'll be able to work through this step-by-step with you.

In the meantime, our technical support policy includes:
{policies}"""
                else:
                    response_content = f"""{empathy_opener}

I'm here to help troubleshoot your technical issue. Let me walk you through some steps that often resolve similar problems, and if needed, I can connect you with our technical specialists for more advanced support."""
                    
            else:  # General inquiry or other intents
                response_content = f"""{empathy_opener}

Based on your inquiry, here's the relevant information:
{policies}

Is there anything specific I can help clarify or any additional questions you have?"""
            
            # Determine tone and follow-up needs
            if emotion in ["angry", "frustrated"]:
                tone = "empathetic_urgent"
                follow_up_needed = True
                resolution_time = "immediate" if escalate else "within 2 hours"
            elif urgency == "high":
                tone = "professional_urgent" 
                follow_up_needed = True
                resolution_time = "within 1 hour"
            else:
                tone = "friendly_helpful"
                follow_up_needed = False
                resolution_time = "standard processing time"
            
            # Build response object
            response_result = {
                "response_text": response_content,
                "tone": tone,
                "includes_solution": True,
                "follow_up_needed": follow_up_needed,
                "estimated_resolution_time": resolution_time,
                "response_type": "escalated_holding" if escalate else "standard_response",
                "personalization_level": "high" if emotion in ["angry", "frustrated"] else "standard",
                "generation_metadata": {
                    "intent_considered": intent,
                    "emotion_considered": emotion,
                    "urgency_considered": urgency,
                    "escalation_status": "escalated" if escalate else "automated",
                    "timestamp": datetime.now().isoformat()
                }
            }
            
            print(f"✅ Response generated with {tone} tone")
            print(f"⏰ Estimated resolution: {resolution_time}")
            
            return response_result
            
        except Exception as e:
            print(f"❌ Error generating response: {e}")
            return {
                "response_text": "I apologize, but I'm experiencing a technical issue. Let me connect you with a human representative who can assist you right away.",
                "tone": "apologetic",
                "includes_solution": False,
                "follow_up_needed": True,
                "estimated_resolution_time": "immediate - human handoff",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    # === MAIN CUSTOMER SUPPORT AGENT ===
    def create_customer_support_agent():
        """Create and configure the customer support agent with all tools."""
        
        agent = Agent(
            tools=[
                classify_customer_intent,
                lookup_knowledge_base, 
                check_escalation_needed,
                prepare_human_handoff,
                generate_customer_response
                # handoff_to_user removed - handled by UI system instead
            ],
            model="amazon.nova-lite-v1:0"
        )
        
        return agent
    
    if __name__ == "__main__":
        print("🎯 Customer Support Agent - Core Implementation")
        print("=" * 50)
        print("This file contains the core customer support agent implementation.")
        print("For examples and demonstrations, run:")
        print("   python customer_support_examples.py")
        print("=" * 50)
        print()
        print("✅ Available tools:")
        print("   • classify_customer_intent")
        print("   • lookup_knowledge_base") 
        print("   • check_escalation_needed")
        print("   • prepare_human_handoff")
        print("   • generate_customer_response")
        print()
        print("✅ Agent creation function:")
        print("   • create_customer_support_agent()")
        print("=" * 50)

except ImportError as e:
    print("❌ Required libraries not available.")
    print(f"   Error: {e}")
    print("   Please install with:")
    print("   pip install strands-agents strands-agents-tools boto3")
    
except Exception as e:
    print(f"❌ Error setting up customer support agent: {e}")
    print("\n🔧 Troubleshooting:")
    print("   1. Check AWS credentials are configured")
    print("   2. Ensure Bedrock model access is enabled for amazon.nova-lite-v1:0")
    print("   3. Verify network connectivity")
    print("   4. Check AWS region settings (should be us-east-1 or configured region)")

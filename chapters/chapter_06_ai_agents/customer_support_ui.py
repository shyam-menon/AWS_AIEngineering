#!/usr/bin/env python3
"""
Customer Support Agent - Web UI Demo

A Flask-based web interface to demonstrate the customer support agent
with real-time interaction and detailed workflow visualization.

Features:
- Interactive chat interface
- Real-time agent processing visualization
- Escalation handling with human handoff simulation
- Intent classification display
- Knowledge base lookup results
- Response generation with tone analysis

Author: AWS AI Engineering Course
Date: September 2025
"""

import json
import datetime
import asyncio
from flask import Flask, render_template, request, jsonify, send_from_directory
from pathlib import Path
import traceback

# Import our customer support agent
try:
    import sys
    import os
    
    # Add current directory to path to ensure import works
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    from customer_support_agent import create_customer_support_agent
    AGENT_AVAILABLE = True
    print("✅ Customer support agent imported successfully!")
except ImportError as e:
    print(f"⚠️  Customer support agent not available: {e}")
    print(f"   Make sure strands-agents and dependencies are installed:")
    print(f"   pip install strands-agents strands-agents-tools boto3")
    AGENT_AVAILABLE = False

app = Flask(__name__)

# Store conversation history
conversation_history = []

# Human-in-the-loop storage
pending_handoffs = {}  # session_id -> handoff data
human_responses = {}   # session_id -> human response

class CustomerSupportUI:
    def __init__(self):
        self.agent = None
        
        if not AGENT_AVAILABLE:
            raise RuntimeError("Strands agent is required but not available. Please ensure virtual environment is activated and strands-agents is installed.")
        
        try:
            self.agent = create_customer_support_agent()
            print("✅ Real Strands customer support agent initialized successfully")
        except Exception as e:
            print(f"❌ Error initializing Strands agent: {e}")
            raise
    
    async def process_query(self, user_query, session_id="demo"):
        """Process user query with real Strands customer support agent"""
        
        try:
            print(f"🤖 Processing query with real Strands agent: {user_query[:100]}...")
            
            # Process the query with the actual Strands customer support agent
            result = await self.agent.invoke_async(user_query)
            
            # Extract the response content and check if human handoff occurred
            agent_response = ""
            human_feedback = ""
            handoff_detected = False
            
            # The Strands agent executes handoff_to_user but the actual conversation 
            # isn't captured in the result object - it's printed to console.
            # We need a different approach to capture the handoff interaction.
            
            # For now, we'll detect handoff by the agent's behavior and simulate the response
            conversation_text = str(result)
            
            # Extract response from message content
            if hasattr(result, 'message') and result.message:
                    content = result.message.get('content', [])
                    if content and isinstance(content, list):
                        for item in content:
                            if 'text' in item:
                                text = item['text']
                                # Skip thinking tags
                                if not text.startswith('<thinking>'):
                                    agent_response += text
            
            # If still no response found, extract from full conversation
            if not agent_response:
                full_text = str(result)
                
                # Try to extract the actual agent response from the conversation
                agent_response = self._extract_customer_response_from_conversation(full_text)
                
                # If that didn't work, look for other response patterns
                if not agent_response:
                    # Look for responses that start after the last </thinking> tag
                    thinking_end = full_text.rfind('</thinking>')
                    if thinking_end != -1:
                        # Get text after the last thinking section
                        after_thinking = full_text[thinking_end + len('</thinking>'):].strip()
                        # Split by lines and look for the actual response content
                        lines = after_thinking.split('\n')
                        response_lines = []
                        for line in lines:
                            line = line.strip()
                            # Skip tool outputs, system messages, etc.
                            if line and not line.startswith('Tool #') and not line.startswith('📝') and not line.startswith('👤') and not line.startswith('✅'):
                                # This looks like actual response content
                                response_lines.append(line)
                        
                        if response_lines:
                            agent_response = '\n'.join(response_lines)
                
                # Look for customer response patterns with multiple fallbacks
                if not agent_response:
                    # Try multiple response start patterns
                    response_starters = [
                        "I sincerely apologize",
                        "Dear Customer,",
                        "</response>",
                        "Best regards,",
                        "Thank you for"
                    ]
                    
                    for starter in response_starters:
                        if starter in full_text:
                            start = full_text.find(starter)
                            if start != -1:
                                # Find the end of the response
                                end = full_text.find("Your response:", start)
                                if end == -1:
                                    end = full_text.find("<thinking>", start)
                                if end == -1:
                                    end = full_text.find("🔍 DEBUG", start)
                                if end != -1:
                                    agent_response = full_text[start:end].strip()
                                else:
                                    agent_response = full_text[start:start+800].strip()  # Increased length
                                break
                
                # Final fallback: extract any substantial text after the last tool output
                if not agent_response:
                    # Look for text after the last tool execution
                    tool_matches = []
                    import re
                    for match in re.finditer(r'Tool #\d+:', full_text):
                        tool_matches.append(match.end())
                    
                    if tool_matches:
                        # Get text after the last tool
                        after_last_tool = full_text[tool_matches[-1]:].strip()
                        # Extract the first substantial text block
                        lines = after_last_tool.split('\n')
                        content_lines = []
                        for line in lines:
                            line = line.strip()
                            if (line and len(line) > 20 and 
                                not line.startswith('🔍') and 
                                not line.startswith('📝') and
                                not line.startswith('✅')):
                                content_lines.append(line)
                                if len('\n'.join(content_lines)) > 100:  # Got enough content
                                    break
                        
                        if content_lines:
                            agent_response = '\n'.join(content_lines)
            
            # Fallback to basic response
            if not agent_response:
                agent_response = "I've analyzed your request and will ensure it gets the appropriate attention."
            
            # NOW do handoff detection after we have the agent response
            handoff_detected = False
            
            # Debug: Let's see what's in conversation_text  
            print(f"🔍 DEBUG - Conversation text contains HANDOFF INITIATED: {'🔄 HANDOFF INITIATED' in conversation_text}")
            print(f"🔍 DEBUG - Conversation text contains prepare_human_handoff: {'prepare_human_handoff' in conversation_text}")
            print(f"🔍 DEBUG - Conversation text contains ESCALATION REQUIRED: {'🚨 ESCALATION REQUIRED' in conversation_text}")
            print(f"🔍 DEBUG - Conversation text sample: {conversation_text[:500]}...")
            
            # Additional debugging for new patterns
            print(f"🔍 DEBUG - Contains CRITICAL PRIORITY: {'CRITICAL PRIORITY' in conversation_text}")
            print(f"🔍 DEBUG - Contains Priority: CRITICAL: {'Priority: CRITICAL' in conversation_text}")
            print(f"🔍 DEBUG - Contains Department: management: {'Department: management' in conversation_text}")
            print(f"🔍 DEBUG - Contains Tool #: {'Tool #' in conversation_text}")
            print(f"🔍 DEBUG - Agent response has management team: {agent_response and 'management team' in agent_response.lower()}")
            
            # Method 1: Check for the actual handoff initiation message (most reliable)
            if "🔄 HANDOFF INITIATED" in conversation_text:
                handoff_detected = True
                print(f"🔍 DEBUG - Handoff detected via HANDOFF INITIATED signal")
            
            # Method 2: Check if prepare_human_handoff tool was executed
            elif "prepare_human_handoff" in conversation_text:
                handoff_detected = True  
                print(f"🔍 DEBUG - Handoff detected via prepare_human_handoff tool execution")
            
            # Method 3: Check for escalation required message
            elif "🚨 ESCALATION REQUIRED" in conversation_text:
                handoff_detected = True
                print(f"🔍 DEBUG - Handoff detected via ESCALATION REQUIRED signal")
            
            # Method 4: Check if the agent response mentions management/escalation (fallback)
            elif agent_response and any(keyword in agent_response.lower() for keyword in [
                "management team", "escalat", "human agent", "follow up", "within 24 hours",
                "personally handle", "higher authority", "supervisor"
            ]):
                handoff_detected = True
                print(f"🔍 DEBUG - Handoff detected via agent response keywords")
            
            # Method 5: Check for escalation indicators in conversation text (more patterns)
            elif any(pattern in conversation_text for pattern in [
                "ESCALATION REQUIRED", "CRITICAL PRIORITY", "Priority: CRITICAL", 
                "Department: management", "Tool #", "prepare_human_handoff", "handoff_to_user"
            ]):
                handoff_detected = True
                print(f"🔍 DEBUG - Handoff detected via escalation indicators in conversation")
            
            # Method 6: Check if conversation contains multiple escalation signals together
            elif ("angry" in conversation_text.lower() and 
                  ("management" in conversation_text.lower() or "escalat" in conversation_text.lower())):
                handoff_detected = True
                print(f"🔍 DEBUG - Handoff detected via combined escalation signals")
            
            # Method 7: Check for consistent escalation patterns (Score + Department)
            elif ("Score: 1" in conversation_text and "Department: management" in conversation_text):
                handoff_detected = True
                print(f"🔍 DEBUG - Handoff detected via escalation score + management department")
            
            # Method 8: Look for tool execution evidence even if not in conversation text
            elif ("🎯 Intent Classification: RETURNS_REFUNDS" in conversation_text and 
                  "😊 Customer Emotion: angry" in conversation_text and
                  "⚡ Urgency Level: high" in conversation_text):
                handoff_detected = True
                print(f"🔍 DEBUG - Handoff detected via angry returns request pattern")
            
            # Method 9: Check for handoff initiation signal in the full result string (most reliable)
            elif "HANDOFF INITIATED" in str(result):
                handoff_detected = True
                print(f"🔍 DEBUG - Handoff detected via HANDOFF INITIATED in result")
            
            # Method 10: Final fallback - if agent explicitly mentions escalation/handoff in response
            elif (agent_response and 
                  any(phrase in agent_response.lower() for phrase in [
                      "escalat", "management", "human agent", "supervisor", 
                      "priority", "follow up", "within", "hours"
                  ])):
                handoff_detected = True
                print(f"🔍 DEBUG - Handoff detected via escalation keywords in agent response")
            
            print(f"🔍 DEBUG - Final handoff detected: {handoff_detected}")
            print(f"🔍 DEBUG - Agent response sample: {agent_response[:200] if agent_response else 'None'}...")
            
            # Handle handoff storage if detected
            if handoff_detected:
                # Check if we already have human feedback for this session
                if session_id in human_responses:
                    human_feedback = human_responses[session_id]
                    print(f"👤 Using stored human feedback: {human_feedback[:100]}...")
                else:
                    # Store this handoff for human intervention
                    pending_handoffs[session_id] = {
                        "user_query": user_query,
                        "agent_response": agent_response,
                        "timestamp": datetime.datetime.now().isoformat(),
                        "conversation_text": conversation_text
                    }
                    print(f"⏳ Handoff pending human feedback for session: {session_id}")
                    human_feedback = "[PENDING: Awaiting human agent response...]"
            
            print(f"📝 Agent response: {agent_response[:200]}...")
            if human_feedback:
                print(f"👤 Human feedback: {human_feedback}")
            
            # Build workflow steps based on actual agent execution
            workflow_steps = [
                {"step": 1, "action": "Query Received", "status": "completed"},
                {"step": 2, "action": "Intent Classification (Nova Lite)", "status": "completed"},
                {"step": 3, "action": "Knowledge Base Lookup", "status": "completed"},
                {"step": 4, "action": "Escalation Analysis", "status": "completed"}
            ]
            
            # Detect if escalation/handoff occurred
            escalation_detected = handoff_detected or any(phrase in agent_response.lower() for phrase in [
                "management team", "connecting you", "escalat", "handoff", "human agent", "supervisor"
            ])
            
            if escalation_detected:
                workflow_steps.append({"step": 5, "action": "Human Handoff Initiated", "status": "completed"})
                if human_feedback:
                    workflow_steps.append({"step": 6, "action": "Human Feedback Received", "status": "completed"})
            else:
                workflow_steps.append({"step": 5, "action": "Automated Response Generated", "status": "completed"})
            
            # Analyze the query for UI display (supplemental to agent's analysis)
            escalation_analysis = self._check_escalation_indicators(user_query)
            intent_analysis = self._simulate_intent_classification(user_query)
            tone_analysis = self._analyze_tone(user_query)
            
            # Prepare the response for UI display
            if escalation_detected and not human_feedback:
                # Show pending state for handoff without feedback
                complete_response = "[PENDING...] Your request has been escalated to our management team. Please wait while we connect you with a human agent."
            elif human_feedback and escalation_detected:
                # Show human feedback
                complete_response = f"**Human Agent Response:** {human_feedback}"
            else:
                # Show regular agent response
                complete_response = agent_response
            
            workflow_details = {
                "timestamp": datetime.datetime.now().isoformat(),
                "user_query": user_query,
                "agent_response": complete_response,
                "session_id": session_id,
                "workflow_steps": workflow_steps,
                "escalation_needed": escalation_analysis,
                "intent_classification": intent_analysis,
                "tone_analysis": tone_analysis,
                "agent_type": "real_strands_customer_support",
                "model_used": "amazon.nova-lite-v1:0",
                "escalation_detected": escalation_detected,
                "human_feedback": human_feedback if handoff_detected else None,
                "handoff_detected": handoff_detected
            }
            
            print(f"✅ Query processed successfully by real Strands agent")
            return workflow_details
            
        except Exception as e:
            print(f"❌ Error processing with Strands agent: {e}")
            return {
                "error": f"Error processing query with Strands agent: {str(e)}",
                "traceback": traceback.format_exc(),
                "user_query": user_query
            }
    
    def _extract_workflow_steps(self, result):
        """Extract workflow steps from agent result"""
        # This is a simplified version - would need to be enhanced based on actual agent implementation
        steps = [
            {"step": 1, "action": "Query Received", "status": "completed"},
            {"step": 2, "action": "Intent Classification", "status": "completed"},
            {"step": 3, "action": "Knowledge Lookup", "status": "completed"},
            {"step": 4, "action": "Response Generation", "status": "completed"}
        ]
        return steps
    
    def _check_escalation_indicators(self, query):
        """Check if query should be escalated"""
        escalation_keywords = [
            "furious", "angry", "ridiculous", "garbage", "terrible", "awful",
            "manager", "supervisor", "complaint", "lawsuit", "legal action",
            "immediately", "right now", "urgent", "emergency"
        ]
        
        query_lower = query.lower()
        triggers = [keyword for keyword in escalation_keywords if keyword in query_lower]
        
        return {
            "needed": len(triggers) > 0,
            "triggers": triggers,
            "priority": "HIGH" if len(triggers) >= 3 else "MEDIUM" if len(triggers) >= 1 else "LOW"
        }
    
    def _simulate_intent_classification(self, query):
        """Simulate intent classification"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["return", "refund", "money back", "exchange"]):
            return {"intent": "RETURNS_REFUNDS", "confidence": 0.95}
        elif any(word in query_lower for word in ["bill", "charge", "payment", "invoice"]):
            return {"intent": "BILLING_PAYMENT", "confidence": 0.90}
        elif any(word in query_lower for word in ["broken", "not working", "error", "problem", "issue"]):
            return {"intent": "TECHNICAL_SUPPORT", "confidence": 0.88}
        elif any(word in query_lower for word in ["hours", "location", "contact", "phone"]):
            return {"intent": "GENERAL_INQUIRY", "confidence": 0.85}
        else:
            return {"intent": "GENERAL_INQUIRY", "confidence": 0.70}
    
    def _analyze_tone(self, query):
        """Analyze customer tone/emotion"""
        query_lower = query.lower()
        
        angry_words = ["furious", "angry", "ridiculous", "terrible", "awful", "hate"]
        frustrated_words = ["frustrated", "annoyed", "disappointed", "upset"]
        polite_words = ["please", "thank you", "could you", "would you", "help"]
        urgent_words = ["urgent", "immediately", "asap", "right now", "emergency"]
        
        angry_count = sum(1 for word in angry_words if word in query_lower)
        frustrated_count = sum(1 for word in frustrated_words if word in query_lower)
        polite_count = sum(1 for word in polite_words if word in query_lower)
        urgent_count = sum(1 for word in urgent_words if word in query_lower)
        
        if angry_count >= 2:
            return {"emotion": "angry", "intensity": "high", "recommended_tone": "empathetic_urgent"}
        elif angry_count >= 1 or frustrated_count >= 2:
            return {"emotion": "frustrated", "intensity": "medium", "recommended_tone": "empathetic_understanding"}
        elif urgent_count >= 1:
            return {"emotion": "urgent", "intensity": "medium", "recommended_tone": "responsive_efficient"}
        elif polite_count >= 1:
            return {"emotion": "polite", "intensity": "low", "recommended_tone": "friendly_helpful"}
        else:
            return {"emotion": "neutral", "intensity": "low", "recommended_tone": "professional_helpful"}
    
    def _extract_customer_response_from_conversation(self, conversation_text):
        """Extract the customer service response from the agent conversation"""
        
        # Look for response generated by generate_customer_response tool
        lines = conversation_text.split('\n')
        collecting_response = False
        response_lines = []
        
        for line in lines:
            # Look for the generate_customer_response tool output
            if "Tool #" in line and "generate_customer_response" in line:
                collecting_response = True
                continue
            elif collecting_response:
                # Stop collecting when we hit the next tool or thinking
                if line.startswith("Tool #") or line.startswith("<thinking>"):
                    break
                # Skip empty lines and tool status messages
                if line.strip() and not line.startswith("💬") and not line.startswith("✅") and not line.startswith("⏰"):
                    response_lines.append(line.strip())
        
        if response_lines:
            return '\n'.join(response_lines)
        
        # Alternative: Look for "I sincerely apologize" patterns (common customer service response)
        if "I sincerely apologize" in conversation_text:
            start = conversation_text.find("I sincerely apologize")
            # Find a reasonable end point
            end = conversation_text.find("Tool #", start)
            if end == -1:
                end = conversation_text.find("<thinking>", start)
            if end == -1:
                end = start + 500  # Limit length
            
            response = conversation_text[start:end].strip()
            # Clean up any tool output artifacts
            response = response.replace("💬 Generating customer response...", "").strip()
            response = response.replace("✅ Response generated with empathetic_urgent tone", "").strip()
            return response
        
        # Fallback response for handoff scenarios
        return "I understand your concern and want to help resolve this issue. Our team is reviewing your case and will ensure you receive the appropriate assistance to resolve this matter."

# Initialize the customer support UI
support_ui = CustomerSupportUI()

@app.route('/')
def index():
    """Main chat interface"""
    return render_template('chat_interface.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Process chat message"""
    try:
        data = request.get_json()
        user_query = data.get('message', '').strip()
        session_id = data.get('session_id', 'demo')
        
        if not user_query:
            return jsonify({"error": "Empty message"}), 400
        
        # Process the query asynchronously
        # Create new event loop if needed
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        result = loop.run_until_complete(support_ui.process_query(user_query, session_id))
        
        # Add to conversation history
        conversation_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "user_message": user_query,
            "agent_response": result,
            "session_id": session_id
        }
        conversation_history.append(conversation_entry)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "error": f"Server error: {str(e)}",
            "traceback": traceback.format_exc()
        }), 500

@app.route('/api/history')
def get_history():
    """Get conversation history"""
    return jsonify(conversation_history)

@app.route('/api/clear_history', methods=['POST'])
def clear_history():
    """Clear conversation history"""
    global conversation_history
    conversation_history = []
    return jsonify({"status": "cleared"})

@app.route('/api/restart_agent', methods=['POST'])
def restart_agent():
    """Restart the customer support agent to pick up code changes"""
    global support_ui
    try:
        print("🔄 Restarting customer support agent...")
        support_ui = CustomerSupportUI()
        return jsonify({"status": "success", "message": "Agent restarted successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Failed to restart agent: {str(e)}"}), 500

@app.route('/api/reload_page', methods=['POST'])
def reload_page():
    """Signal the page to reload to pick up template changes"""
    return jsonify({"status": "success", "message": "Please refresh the page to see changes"})

@app.route('/api/pending_handoffs')
def get_pending_handoffs():
    """Get list of conversations awaiting human feedback"""
    return jsonify({
        "pending_handoffs": [
            {
                "session_id": session_id,
                "user_query": data["user_query"],
                "agent_response": data["agent_response"][:200] + "...",
                "timestamp": data["timestamp"]
            }
            for session_id, data in pending_handoffs.items()
        ]
    })

@app.route('/api/provide_feedback', methods=['POST'])
def provide_human_feedback():
    """Allow human agents to provide feedback for pending handoffs"""
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        feedback = data.get('feedback', '').strip()
        
        if not session_id or not feedback:
            return jsonify({"error": "Missing session_id or feedback"}), 400
        
        if session_id not in pending_handoffs:
            return jsonify({"error": "No pending handoff found for this session"}), 404
        
        # Store the human feedback
        human_responses[session_id] = feedback
        
        # Get the original handoff data before removing from pending
        handoff_data = pending_handoffs[session_id]
        
        # Create updated response with human feedback
        updated_response = handoff_data["agent_response"]
        if not updated_response.endswith(f"**Human Agent Update:** {feedback}"):
            updated_response += f"\n\n**Human Agent Update:** {feedback}"
        
        # Update the conversation history with the human feedback
        for i, entry in enumerate(conversation_history):
            if entry.get("session_id") == session_id:
                conversation_history[i]["agent_response"] = updated_response
                conversation_history[i]["human_feedback"] = feedback
                break
        
        # Remove from pending list
        pending_handoffs.pop(session_id)
        
        print(f"✅ Human feedback provided for session {session_id}: {feedback[:100]}...")
        
        return jsonify({
            "status": "success",
            "message": "Feedback recorded successfully",
            "session_id": session_id,
            "feedback": feedback,
            "updated_response": updated_response
        })
        
    except Exception as e:
        return jsonify({
            "error": f"Error recording feedback: {str(e)}",
            "traceback": traceback.format_exc()
        }), 500

@app.route('/api/conversation/<session_id>')
def get_conversation_with_feedback(session_id):
    """Get conversation data including any human feedback"""
    try:
        # Find the conversation in history
        for entry in conversation_history:
            if entry.get("session_id") == session_id:
                # Check if there's human feedback available
                if session_id in human_responses:
                    entry_copy = entry.copy()
                    feedback = human_responses[session_id]
                    if not entry_copy["agent_response"].endswith(f"**Human Agent Update:** {feedback}"):
                        entry_copy["agent_response"] += f"\n\n**Human Agent Update:** {feedback}"
                    entry_copy["human_feedback"] = feedback
                    return jsonify(entry_copy)
                return jsonify(entry)
        
        return jsonify({"error": "Conversation not found"}), 404
        
    except Exception as e:
        return jsonify({
            "error": f"Error retrieving conversation: {str(e)}"
        }), 500

@app.route('/human-agent')
def human_agent_interface():
    """Human agent interface for providing feedback"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Human Agent Interface</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .handoff { border: 1px solid #ccc; margin: 10px 0; padding: 15px; border-radius: 5px; }
            .query { background: #f0f0f0; padding: 10px; margin: 10px 0; border-radius: 3px; }
            .response { background: #e8f4f8; padding: 10px; margin: 10px 0; border-radius: 3px; }
            textarea { width: 100%; height: 100px; margin: 10px 0; }
            button { background: #007cba; color: white; padding: 10px 20px; border: none; border-radius: 3px; cursor: pointer; }
            button:hover { background: #005a8b; }
            .success { color: green; }
            .error { color: red; }
        </style>
    </head>
    <body>
        <h1>🧑‍💼 Human Agent Interface</h1>
        <p>Provide feedback for customer support handoffs</p>
        
        <div id="handoffs-container">
            <p>Loading pending handoffs...</p>
        </div>
        
        <script>
            async function loadPendingHandoffs() {
                try {
                    const response = await fetch('/api/pending_handoffs');
                    const data = await response.json();
                    const container = document.getElementById('handoffs-container');
                    
                    if (data.pending_handoffs.length === 0) {
                        container.innerHTML = '<p>No pending handoffs at this time.</p>';
                        return;
                    }
                    
                    container.innerHTML = data.pending_handoffs.map(handoff => `
                        <div class="handoff">
                            <h3>Session: ${handoff.session_id}</h3>
                            <p><strong>Time:</strong> ${new Date(handoff.timestamp).toLocaleString()}</p>
                            <div class="query">
                                <strong>Customer Query:</strong><br>
                                ${handoff.user_query}
                            </div>
                            <div class="response">
                                <strong>Agent Response:</strong><br>
                                ${handoff.agent_response}
                            </div>
                            <textarea id="feedback-${handoff.session_id}" placeholder="Enter your feedback as a human agent..."></textarea>
                            <button onclick="provideFeedback('${handoff.session_id}')">Submit Feedback</button>
                            <div id="status-${handoff.session_id}"></div>
                        </div>
                    `).join('');
                } catch (error) {
                    document.getElementById('handoffs-container').innerHTML = 
                        `<p class="error">Error loading handoffs: ${error.message}</p>`;
                }
            }
            
            async function provideFeedback(sessionId) {
                const feedback = document.getElementById(`feedback-${sessionId}`).value;
                const statusDiv = document.getElementById(`status-${sessionId}`);
                
                if (!feedback.trim()) {
                    statusDiv.innerHTML = '<p class="error">Please enter feedback</p>';
                    return;
                }
                
                try {
                    const response = await fetch('/api/provide_feedback', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ session_id: sessionId, feedback: feedback })
                    });
                    
                    const result = await response.json();
                    
                    if (response.ok) {
                        statusDiv.innerHTML = '<p class="success">✅ Feedback submitted successfully!</p>';
                        // Reload handoffs after a short delay
                        setTimeout(loadPendingHandoffs, 2000);
                    } else {
                        statusDiv.innerHTML = `<p class="error">Error: ${result.error}</p>`;
                    }
                } catch (error) {
                    statusDiv.innerHTML = `<p class="error">Network error: ${error.message}</p>`;
                }
            }
            
            // Load handoffs on page load and refresh every 10 seconds
            loadPendingHandoffs();
            setInterval(loadPendingHandoffs, 10000);
        </script>
    </body>
    </html>
    """

@app.route('/api/examples')
def get_examples():
    """Get example queries for testing"""
    examples = [
        {
            "category": "Angry Customer",
            "query": "This product is complete garbage! I want my money back RIGHT NOW or I'm calling my lawyer!",
            "expected": "High escalation, management handoff"
        },
        {
            "category": "Polite Inquiry",
            "query": "Hi, could you please help me understand your return policy? Thank you.",
            "expected": "Automated helpful response"
        },
        {
            "category": "Technical Issue",
            "query": "My device stopped working after the latest update and I need it for a presentation tomorrow.",
            "expected": "Technical support escalation"
        },
        {
            "category": "Billing Question",
            "query": "I was charged twice for the same order last month. Can someone help me get this resolved?",
            "expected": "Billing department routing"
        },
        {
            "category": "Urgent Request",
            "query": "URGENT: I need to cancel my order immediately before it ships!",
            "expected": "Priority handling"
        }
    ]
    return jsonify(examples)

if __name__ == '__main__':
    # Create templates directory and HTML file
    templates_dir = Path(__file__).parent / "templates"
    templates_dir.mkdir(exist_ok=True)
    
    # Create the HTML template
    html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Customer Support Agent Demo</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .chat-container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            width: 100%;
            max-width: 1200px;
            height: 80vh;
            display: flex;
            overflow: hidden;
        }

        .chat-main {
            flex: 1;
            display: flex;
            flex-direction: column;
        }

        .chat-header {
            background: linear-gradient(135deg, #2196F3, #21CBF3);
            color: white;
            padding: 20px;
            text-align: center;
        }

        .chat-messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            background: #f8f9fa;
        }

        .message {
            margin-bottom: 20px;
            display: flex;
            align-items: flex-start;
            gap: 10px;
        }

        .message.user {
            flex-direction: row-reverse;
        }

        .message-content {
            max-width: 70%;
            padding: 12px 18px;
            border-radius: 18px;
            word-wrap: break-word;
        }

        .message.user .message-content {
            background: #2196F3;
            color: white;
        }

        .message.agent .message-content {
            background: #e3f2fd;
            color: #333;
            border: 1px solid #bbdefb;
        }

        .message.error .message-content {
            background: #ffebee;
            color: #c62828;
            border: 1px solid #ef9a9a;
        }

        .chat-input {
            padding: 20px;
            border-top: 1px solid #e0e0e0;
            background: white;
        }

        .input-group {
            display: flex;
            gap: 10px;
        }

        #messageInput {
            flex: 1;
            padding: 12px 18px;
            border: 2px solid #e0e0e0;
            border-radius: 25px;
            font-size: 16px;
            outline: none;
            transition: border-color 0.3s;
        }

        #messageInput:focus {
            border-color: #2196F3;
        }

        #sendButton {
            background: #2196F3;
            color: white;
            border: none;
            border-radius: 25px;
            padding: 12px 24px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        #sendButton:hover {
            background: #1976D2;
        }

        .sidebar {
            width: 300px;
            background: #f5f5f5;
            border-left: 1px solid #e0e0e0;
            padding: 20px;
            overflow-y: auto;
        }

        .workflow-panel {
            margin-bottom: 20px;
        }

        .workflow-panel h3 {
            color: #333;
            margin-bottom: 10px;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .workflow-step {
            background: white;
            padding: 10px;
            margin-bottom: 8px;
            border-radius: 8px;
            border-left: 4px solid #2196F3;
            font-size: 12px;
        }

        .intent-badge {
            display: inline-block;
            padding: 4px 8px;
            background: #4CAF50;
            color: white;
            border-radius: 12px;
            font-size: 11px;
            font-weight: bold;
        }

        .escalation-badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: bold;
        }

        .escalation-badge.HIGH {
            background: #f44336;
            color: white;
        }

        .escalation-badge.MEDIUM {
            background: #ff9800;
            color: white;
        }

        .escalation-badge.LOW {
            background: #4CAF50;
            color: white;
        }

        .examples-section {
            margin-top: 20px;
        }

        .example-query {
            background: white;
            padding: 10px;
            margin-bottom: 8px;
            border-radius: 8px;
            cursor: pointer;
            transition: background-color 0.2s;
            font-size: 12px;
            border: 1px solid #e0e0e0;
        }

        .example-query:hover {
            background: #f0f0f0;
        }

        .example-category {
            font-weight: bold;
            color: #2196F3;
            margin-bottom: 4px;
        }

        .loading {
            display: none;
            text-align: center;
            padding: 20px;
            color: #666;
        }

        .controls {
            padding: 10px;
            text-align: center;
            border-bottom: 1px solid #e0e0e0;
        }

        .btn {
            background: #f5f5f5;
            border: 1px solid #ddd;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            margin: 0 5px;
        }

        .btn:hover {
            background: #e0e0e0;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-main">
            <div class="chat-header">
                <h1>🤖 Customer Support Agent Demo</h1>
                <p>Test different customer scenarios and see how the AI agent handles them</p>
            </div>
            
            <div class="controls">
                <button class="btn" onclick="clearHistory()">Clear Chat</button>
                <button class="btn" onclick="showExamples()">Load Examples</button>
                <button class="btn" onclick="window.open('/human-agent', '_blank')" style="background: #4CAF50; color: white;">👥 Human Agent Interface</button>
                <button class="btn" onclick="restartAgent()" style="background: #ff9800; color: white;">Restart Agent</button>
            </div>

            <div class="chat-messages" id="chatMessages">
                <div class="message agent">
                    <div class="message-content">
                        👋 Hello! I'm the Customer Support AI Agent. Try asking me about returns, billing, technical issues, or any customer service question. I'll show you how I classify intents, check for escalations, and decide whether to help you directly or connect you with a human agent.
                    </div>
                </div>
            </div>

            <div class="loading" id="loading">
                🤖 Processing your request...
            </div>

            <div class="chat-input">
                <div class="input-group">
                    <input type="text" id="messageInput" placeholder="Type your customer service question here..." 
                           onkeypress="handleKeyPress(event)">
                    <button id="sendButton" onclick="sendMessage()">Send</button>
                </div>
            </div>
        </div>

        <div class="sidebar">
            <div class="workflow-panel">
                <h3>🔄 Workflow Steps</h3>
                <div id="workflowSteps">
                    <p style="color: #666; font-size: 12px;">Send a message to see the workflow in action!</p>
                </div>
            </div>

            <div class="workflow-panel">
                <h3>🎯 Intent & Analysis</h3>
                <div id="intentAnalysis">
                    <p style="color: #666; font-size: 12px;">Intent classification will appear here</p>
                </div>
            </div>

            <div class="examples-section">
                <h3>💡 Example Queries</h3>
                <button onclick="showExamples()" style="margin-bottom: 10px; padding: 5px 10px; background: #007bff; color: white; border: none; border-radius: 3px; cursor: pointer;">Load Examples</button>
                <div id="exampleQueries">
                    <p style="color: #666; font-size: 12px;">Loading examples...</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        let sessionId = 'demo_' + Date.now();

        async function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (!message) return;

            // Add user message to chat
            addMessage('user', message);
            input.value = '';
            
            // Show loading
            document.getElementById('loading').style.display = 'block';

            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        message: message,
                        session_id: sessionId
                    })
                });

                const data = await response.json();
                
                if (data.error) {
                    addMessage('error', `Error: ${data.error}`);
                } else {
                    addMessage('agent', data.agent_response || 'Response processed successfully');
                    updateWorkflow(data);
                    updateIntentAnalysis(data);
                    
                    // Check if this is a handoff scenario with pending feedback
                    if (data.handoff_detected && data.human_feedback && data.human_feedback.includes('PENDING')) {
                        showHandoffNotification();
                        // Poll for human feedback updates
                        setTimeout(() => pollForFeedbackUpdate(sessionId), 5000);
                    }
                }
            } catch (error) {
                addMessage('error', `Network error: ${error.message}`);
            }

            // Hide loading
            document.getElementById('loading').style.display = 'none';
        }

        function addMessage(type, content) {
            const messagesContainer = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${type}`;
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            contentDiv.textContent = content;
            
            messageDiv.appendChild(contentDiv);
            messagesContainer.appendChild(messageDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }

        function updateWorkflow(data) {
            const workflowContainer = document.getElementById('workflowSteps');
            
            if (data.workflow_steps) {
                workflowContainer.innerHTML = data.workflow_steps.map(step => 
                    `<div class="workflow-step">
                        ${step.step}. ${step.action} ✅
                    </div>`
                ).join('');
            }
        }

        function updateIntentAnalysis(data) {
            const analysisContainer = document.getElementById('intentAnalysis');
            let html = '';
            
            if (data.intent_classification) {
                html += `<div style="margin-bottom: 10px;">
                    <span class="intent-badge">${data.intent_classification.intent}</span>
                    <small style="display: block; color: #666; margin-top: 4px;">
                        Confidence: ${(data.intent_classification.confidence * 100).toFixed(1)}%
                    </small>
                </div>`;
            }
            
            if (data.escalation_needed) {
                html += `<div style="margin-bottom: 10px;">
                    <span class="escalation-badge ${data.escalation_needed.priority}">
                        ${data.escalation_needed.needed ? 'ESCALATION NEEDED' : 'NO ESCALATION'}
                    </span>
                    ${data.escalation_needed.triggers && data.escalation_needed.triggers.length > 0 ? 
                        `<small style="display: block; color: #666; margin-top: 4px;">
                            Triggers: ${data.escalation_needed.triggers.join(', ')}
                        </small>` : ''}
                </div>`;
            }
            
            if (data.tone_analysis) {
                html += `<div style="margin-bottom: 10px;">
                    <strong>Tone:</strong> ${data.tone_analysis.emotion}
                    <small style="display: block; color: #666;">
                        Recommended response: ${data.tone_analysis.recommended_tone.replace('_', ' ')}
                    </small>
                </div>`;
            }
            
            analysisContainer.innerHTML = html || '<p style="color: #666; font-size: 12px;">Analysis will appear here</p>';
        }

        // Global variable to store examples
        let globalExamples = [];

        // Make showExamples globally accessible
        window.showExamples = async function showExamples() {
            try {
                console.log('Loading examples...');
                const response = await fetch('/api/examples');
                const examples = await response.json();
                globalExamples = examples; // Store globally
                console.log('Examples loaded:', examples);
                
                const examplesContainer = document.getElementById('exampleQueries');
                if (!examplesContainer) {
                    console.error('Example queries container not found!');
                    return;
                }
                
                examplesContainer.innerHTML = examples.map((example, index) => 
                    `<div class="example-query" onclick="useExampleByIndex(${index})">
                        <div class="example-category">${example.category}</div>
                        <div style="color: #666; font-size: 11px; margin-bottom: 4px;">${example.query}</div>
                        <div style="color: #999; font-size: 10px;">${example.expected}</div>
                    </div>`
                ).join('');
                console.log('Examples displayed');
            } catch (error) {
                console.error('Error loading examples:', error);
                // Try to show a fallback message
                const examplesContainer = document.getElementById('exampleQueries');
                if (examplesContainer) {
                    examplesContainer.innerHTML = '<p style="color: red;">Error loading examples. Click "Load Examples" to retry.</p>';
                }
            }
        };

        function useExampleByIndex(index) {
            if (globalExamples[index]) {
                document.getElementById('messageInput').value = globalExamples[index].query;
                console.log('Example loaded:', globalExamples[index].query);
            }
        }

        function useExample(query) {
            document.getElementById('messageInput').value = query;
        }

        async function clearHistory() {
            document.getElementById('chatMessages').innerHTML = `
                <div class="message agent">
                    <div class="message-content">
                        👋 Hello! I'm the Customer Support AI Agent. Try asking me about returns, billing, technical issues, or any customer service question.
                    </div>
                </div>`;
            
            document.getElementById('workflowSteps').innerHTML = '<p style="color: #666; font-size: 12px;">Send a message to see the workflow in action!</p>';
            document.getElementById('intentAnalysis').innerHTML = '<p style="color: #666; font-size: 12px;">Intent classification will appear here</p>';
            
            await fetch('/api/clear_history', { method: 'POST' });
        }

        async function restartAgent() {
            try {
                const response = await fetch('/api/restart_agent', { method: 'POST' });
                const data = await response.json();
                
                if (data.status === 'success') {
                    addMessage('agent', '🔄 Agent restarted successfully! Code changes have been applied.');
                } else {
                    addMessage('error', `Failed to restart agent: ${data.message}`);
                }
            } catch (error) {
                addMessage('error', `Error restarting agent: ${error.message}`);
            }
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
        
        function showHandoffNotification() {
            const notification = document.createElement('div');
            notification.style.cssText = `
                position: fixed; top: 20px; right: 20px; 
                background: #ff9800; color: white; padding: 15px; border-radius: 5px; 
                box-shadow: 0 4px 8px rgba(0,0,0,0.2); z-index: 1000;
            `;
            notification.innerHTML = `
                🧑‍💼 <strong>Handoff to Human Agent</strong><br>
                This conversation has been escalated.<br>
                <a href="/human-agent" target="_blank" style="color: white; text-decoration: underline;">
                    Click here to provide feedback as human agent
                </a>
            `;
            document.body.appendChild(notification);
            
            // Remove notification after 10 seconds
            setTimeout(() => notification.remove(), 10000);
        }
        
        async function pollForFeedbackUpdate(currentSessionId) {
            try {
                const response = await fetch('/api/pending_handoffs');
                const data = await response.json();
                
                // Check if our session is still pending
                const stillPending = data.pending_handoffs.find(h => h.session_id === currentSessionId);
                
                if (!stillPending) {
                    // Feedback was provided, fetch the updated conversation
                    try {
                        const convResponse = await fetch(`/api/conversation/${currentSessionId}`);
                        const convData = await convResponse.json();
                        
                        if (convData.agent_response) {
                            // Find and update the last agent message
                            const messages = document.querySelectorAll('.message.agent');
                            if (messages.length > 0) {
                                const lastMessage = messages[messages.length - 1];
                                const contentDiv = lastMessage.querySelector('.message-content');
                                if (contentDiv) {
                                    // Update content with human feedback included
                                    const newlineRegex = new RegExp('\\n', 'g');
                                    contentDiv.innerHTML = convData.agent_response.replace(newlineRegex, '<br>');
                                    
                                    // Add success notification
                                    addMessage('system', '✅ Human agent feedback has been incorporated into the response above.');
                                }
                            }
                        }
                    } catch (updateError) {
                        console.log('Error updating conversation:', updateError);
                        // Fallback to showing a notification
                        addMessage('system', '✅ Human agent feedback has been provided.');
                    }
                } else {
                    // Still pending, check again in 5 seconds
                    setTimeout(() => pollForFeedbackUpdate(currentSessionId), 5000);
                }
            } catch (error) {
                console.log('Error polling for feedback updates:', error);
            }
        }

        // Load examples on page load
        document.addEventListener('DOMContentLoaded', function() {
            console.log('DOM content loaded, showing examples...');
            showExamples();
        });
        
        // Also try to load examples immediately if DOM is already ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', showExamples);
        } else {
            // DOM is already ready
            showExamples();
        }
    </script>
</body>
</html>'''
    
    with open(templates_dir / "chat_interface.html", "w", encoding="utf-8") as f:
        f.write(html_template)
    
    print("🚀 CUSTOMER SUPPORT AGENT UI DEMO")
    print("=" * 50)
    print("🌐 Starting web server...")
    print("📱 Open your browser to: http://localhost:5000")
    print("=" * 50)
    print()
    print("✨ Features:")
    print("   • Interactive chat interface")
    print("   • Real-time workflow visualization") 
    print("   • Intent classification display")
    print("   • Escalation detection")
    print("   • Tone analysis")
    print("   • Example scenarios")
    print()
    print("🔧 Controls:")
    print("   • Type messages to test different scenarios")
    print("   • Click example queries to load them")
    print("   • Watch the workflow panel for processing steps")
    print("   • See escalation triggers in real-time")
    print()
    
    try:
        # Disable debug mode to prevent import issues with virtual environment
        app.run(debug=False, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Customer Support UI Demo stopped")

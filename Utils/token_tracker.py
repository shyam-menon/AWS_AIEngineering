#!/usr/bin/env python3
"""
Real-Time AI Token Tracker

A simple utility to track token usage and costs for your current AI session.
This complements the main usage monitor by providing immediate feedback
on your token consumption.

Author: AWS AI Engineering Course
Date: August 2025
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path


class TokenTracker:
    """Track tokens and costs for the current session."""
    
    def __init__(self, session_file: Optional[str] = None):
        """Initialize the token tracker."""
        self.session_file = session_file or "ai_session_log.json"
        self.session_data = self._load_session()
        
        # Pricing per 1K tokens (as of August 2025) - in dollars
        self.pricing = {
            'amazon.nova-lite-v1:0': {
                'input': 0.06,      # $0.06 per 1K input tokens
                'output': 0.24      # $0.24 per 1K output tokens
            },
            'anthropic.claude-3-5-sonnet-20241022-v2:0': {
                'input': 3.00,      # $3.00 per 1K input tokens
                'output': 15.00     # $15.00 per 1K output tokens
            },
            'anthropic.claude-3-5-haiku-20241022-v1:0': {
                'input': 0.25,      # $0.25 per 1K input tokens
                'output': 1.25      # $1.25 per 1K output tokens
            }
        }
    
    def _load_session(self) -> Dict:
        """Load existing session data or create new session."""
        session_path = Path(self.session_file)
        
        if session_path.exists():
            try:
                with open(session_path, 'r') as f:
                    data = json.load(f)
                print(f"📊 Loaded existing session: {len(data.get('requests', []))} previous requests")
                return data
            except Exception as e:
                print(f"⚠️  Could not load session file: {e}")
        
        # Create new session
        new_session = {
            'session_start': datetime.now().isoformat(),
            'requests': [],
            'summary': {
                'total_input_tokens': 0,
                'total_output_tokens': 0,
                'total_cost': 0.0,
                'request_count': 0
            }
        }
        print("🆕 Created new tracking session")
        return new_session
    
    def _save_session(self) -> None:
        """Save session data to file."""
        try:
            with open(self.session_file, 'w') as f:
                json.dump(self.session_data, f, indent=2)
        except Exception as e:
            print(f"⚠️  Could not save session: {e}")
    
    def track_request(self, model_id: str, input_tokens: int, output_tokens: int, 
                     prompt: str = "", response: str = "") -> Dict:
        """
        Track a single AI request.
        
        Args:
            model_id (str): The model identifier
            input_tokens (int): Number of input tokens
            output_tokens (int): Number of output tokens
            prompt (str): The input prompt (optional, for logging)
            response (str): The model response (optional, for logging)
            
        Returns:
            Dict: Request summary with cost calculation
        """
        timestamp = datetime.now().isoformat()
        
        # Calculate costs
        cost_data = self._calculate_cost(model_id, input_tokens, output_tokens)
        
        # Create request record
        request_record = {
            'timestamp': timestamp,
            'model_id': model_id,
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'total_tokens': input_tokens + output_tokens,
            'input_cost': cost_data['input_cost'],
            'output_cost': cost_data['output_cost'],
            'total_cost': cost_data['total_cost'],
            'prompt_preview': prompt[:100] + "..." if len(prompt) > 100 else prompt,
            'response_preview': response[:100] + "..." if len(response) > 100 else response
        }
        
        # Add to session
        self.session_data['requests'].append(request_record)
        
        # Update summary
        summary = self.session_data['summary']
        summary['total_input_tokens'] += input_tokens
        summary['total_output_tokens'] += output_tokens
        summary['total_cost'] += cost_data['total_cost']
        summary['request_count'] += 1
        summary['last_updated'] = timestamp
        
        # Save session
        self._save_session()
        
        return request_record
    
    def _calculate_cost(self, model_id: str, input_tokens: int, output_tokens: int) -> Dict:
        """Calculate cost for a request."""
        if model_id not in self.pricing:
            return {
                'input_cost': 0.0,
                'output_cost': 0.0,
                'total_cost': 0.0,
                'note': f'Pricing not available for {model_id}'
            }
        
        pricing = self.pricing[model_id]
        input_cost = (input_tokens / 1000.0) * pricing['input']
        output_cost = (output_tokens / 1000.0) * pricing['output']
        
        return {
            'input_cost': input_cost,
            'output_cost': output_cost,
            'total_cost': input_cost + output_cost
        }
    
    def get_session_summary(self) -> Dict:
        """Get current session summary."""
        return self.session_data['summary'].copy()
    
    def print_session_summary(self) -> None:
        """Print a formatted session summary."""
        summary = self.session_data['summary']
        
        print("\n" + "=" * 50)
        print("🎯 CURRENT SESSION SUMMARY")
        print("=" * 50)
        
        print(f"📅 Session Start: {self.session_data['session_start']}")
        print(f"🔢 Total Requests: {summary['request_count']}")
        print(f"📝 Input Tokens: {summary['total_input_tokens']:,}")
        print(f"📄 Output Tokens: {summary['total_output_tokens']:,}")
        print(f"🔢 Total Tokens: {summary['total_input_tokens'] + summary['total_output_tokens']:,}")
        print(f"💰 Total Cost: ${summary['total_cost']:.4f}")
        
        if summary['request_count'] > 0:
            avg_cost = summary['total_cost'] / summary['request_count']
            avg_tokens = (summary['total_input_tokens'] + summary['total_output_tokens']) / summary['request_count']
            print(f"📊 Avg Cost/Request: ${avg_cost:.4f}")
            print(f"📊 Avg Tokens/Request: {avg_tokens:.0f}")
    
    def print_recent_requests(self, count: int = 5) -> None:
        """Print recent requests."""
        requests = self.session_data['requests']
        recent = requests[-count:] if len(requests) > count else requests
        
        if not recent:
            print("\n📝 No requests in current session")
            return
        
        print(f"\n📋 RECENT REQUESTS (Last {len(recent)})")
        print("-" * 50)
        
        for i, req in enumerate(recent, 1):
            timestamp = datetime.fromisoformat(req['timestamp']).strftime('%H:%M:%S')
            print(f"\n{i}. {timestamp} | {req['model_id']}")
            print(f"   Tokens: {req['input_tokens']}→{req['output_tokens']} | Cost: ${req['total_cost']:.4f}")
            if req['prompt_preview']:
                print(f"   Prompt: {req['prompt_preview']}")
    
    def export_session(self, filename: Optional[str] = None) -> str:
        """Export session data to a file."""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"ai_session_export_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(self.session_data, f, indent=2)
            print(f"📁 Session exported to: {filename}")
            return filename
        except Exception as e:
            print(f"❌ Export failed: {e}")
            return ""
    
    def reset_session(self) -> None:
        """Reset the current session."""
        self.session_data = {
            'session_start': datetime.now().isoformat(),
            'requests': [],
            'summary': {
                'total_input_tokens': 0,
                'total_output_tokens': 0,
                'total_cost': 0.0,
                'request_count': 0
            }
        }
        self._save_session()
        print("🔄 Session reset")


def estimate_tokens(text: str) -> int:
    """
    Rough estimation of token count for text.
    
    Note: This is an approximation. Actual token counts may vary by model.
    """
    # Rough approximation: 1 token ≈ 4 characters for English text
    return len(text) // 4


def demo_tracker():
    """Demonstrate the token tracker functionality."""
    print("🤖 AI Token Tracker Demo")
    print("=" * 40)
    
    tracker = TokenTracker("demo_session.json")
    
    # Simulate some AI requests
    demo_requests = [
        {
            'model': 'amazon.nova-lite-v1:0',
            'prompt': 'What is the capital of France?',
            'response': 'The capital of France is Paris.',
            'input_tokens': 8,
            'output_tokens': 12
        },
        {
            'model': 'amazon.nova-lite-v1:0',
            'prompt': 'Explain machine learning in simple terms.',
            'response': 'Machine learning is a way for computers to learn patterns from data without being explicitly programmed.',
            'input_tokens': 12,
            'output_tokens': 24
        }
    ]
    
    for req in demo_requests:
        print(f"\n📝 Tracking request: {req['prompt']}")
        result = tracker.track_request(
            req['model'], 
            req['input_tokens'], 
            req['output_tokens'],
            req['prompt'],
            req['response']
        )
        print(f"   Cost: ${result['total_cost']:.4f}")
    
    # Show summary
    tracker.print_session_summary()
    tracker.print_recent_requests()


if __name__ == "__main__":
    demo_tracker()

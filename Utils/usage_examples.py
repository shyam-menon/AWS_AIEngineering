#!/usr/bin/env python3
"""
Usage Examples for AI Token Tracking

This file shows how to integrate token tracking into your existing Bedrock code.

Author: AWS AI Engineering Course
Date: August 2025
"""

from token_tracker import TokenTracker
from bedrock_with_tracking import BedrockWithTracking
import json


def example_1_simple_tracking():
    """Example 1: Simple manual token tracking"""
    print("🔍 Example 1: Simple Manual Tracking")
    print("-" * 40)
    
    tracker = TokenTracker("example1_session.json")
    
    # Simulate some AI requests with manual tracking
    tracker.track_request(
        model_id="amazon.nova-lite-v1:0",
        input_tokens=15,
        output_tokens=45,
        prompt="What is machine learning?",
        response="Machine learning is a subset of artificial intelligence..."
    )
    
    tracker.track_request(
        model_id="amazon.nova-lite-v1:0", 
        input_tokens=25,
        output_tokens=120,
        prompt="Explain neural networks in simple terms",
        response="Neural networks are computing systems inspired by biological neural networks..."
    )
    
    # Show summary
    tracker.print_session_summary()
    print()


def example_2_automatic_tracking():
    """Example 2: Automatic tracking with Bedrock integration"""
    print("🤖 Example 2: Automatic Bedrock Tracking")
    print("-" * 40)
    
    client = BedrockWithTracking(session_file="example2_session.json")
    
    # Make some AI calls with automatic tracking
    prompts = [
        "What are the key features of AWS Lambda?",
        "How does Amazon S3 ensure data durability?"
    ]
    
    for prompt in prompts:
        print(f"📝 Query: {prompt}")
        result = client.invoke_with_tracking(
            model_id="amazon.nova-lite-v1:0",
            prompt=prompt,
            max_tokens=200
        )
        
        if result.get('content'):
            print(f"✅ Response: {result['content'][:100]}...")
            print(f"💰 Cost: ${result['tracking']['total_cost']:.4f}")
            print()
    
    # Show session summary
    client.print_summary()
    print()


def example_3_cost_comparison():
    """Example 3: Comparing costs across different models"""
    print("📊 Example 3: Model Cost Comparison")
    print("-" * 40)
    
    tracker = TokenTracker("cost_comparison.json")
    
    # Same request with different models
    prompt = "Explain the differences between supervised and unsupervised learning"
    input_tokens = 15
    output_tokens = 200
    
    models = [
        "amazon.nova-lite-v1:0",
        "anthropic.claude-3-5-haiku-20241022-v1:0",
        "anthropic.claude-3-5-sonnet-20241022-v2:0"
    ]
    
    print(f"Prompt: {prompt}")
    print(f"Token usage: {input_tokens} input → {output_tokens} output\n")
    
    for model in models:
        result = tracker.track_request(
            model_id=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            prompt=prompt,
            response="[Model response would be here]"
        )
        
        print(f"Model: {model}")
        print(f"Cost: ${result['total_cost']:.4f}")
        print()
    
    # Show cost comparison
    tracker.print_recent_requests(3)


def example_4_session_management():
    """Example 4: Managing multiple sessions"""
    print("📁 Example 4: Session Management")
    print("-" * 40)
    
    # Different sessions for different projects
    sessions = {
        "learning": TokenTracker("learning_session.json"),
        "project_a": TokenTracker("project_a_session.json"),
        "experiments": TokenTracker("experiments_session.json")
    }
    
    # Simulate work on different projects
    sessions["learning"].track_request(
        "amazon.nova-lite-v1:0", 20, 80,
        "What is AWS?", "AWS is Amazon Web Services..."
    )
    
    sessions["project_a"].track_request(
        "amazon.nova-lite-v1:0", 50, 200,
        "Generate API documentation", "Here's the API documentation..."
    )
    
    sessions["experiments"].track_request(
        "anthropic.claude-3-5-haiku-20241022-v1:0", 30, 150,
        "Test prompt engineering", "Here are some prompt engineering techniques..."
    )
    
    # Show summaries for each session
    for session_name, tracker in sessions.items():
        print(f"\n📊 {session_name.title()} Session:")
        summary = tracker.get_session_summary()
        print(f"  Requests: {summary['request_count']}")
        print(f"  Total Cost: ${summary['total_cost']:.4f}")
        print(f"  Total Tokens: {summary['total_input_tokens'] + summary['total_output_tokens']}")


def example_5_budget_monitoring():
    """Example 5: Budget monitoring and alerts"""
    print("💰 Example 5: Budget Monitoring")
    print("-" * 40)
    
    tracker = TokenTracker("budget_session.json")
    
    # Set budget alert threshold
    budget_limit = 1.00  # $1.00 budget
    
    # Simulate AI usage
    test_requests = [
        {"tokens_in": 50, "tokens_out": 200, "prompt": "Code review request"},
        {"tokens_in": 30, "tokens_out": 150, "prompt": "Documentation help"},
        {"tokens_in": 40, "tokens_out": 300, "prompt": "Bug fixing assistance"},
        {"tokens_in": 60, "tokens_out": 250, "prompt": "Feature implementation"}
    ]
    
    print(f"💳 Budget limit: ${budget_limit:.2f}\n")
    
    for i, req in enumerate(test_requests, 1):
        result = tracker.track_request(
            "amazon.nova-lite-v1:0",
            req["tokens_in"], 
            req["tokens_out"],
            req["prompt"],
            "Response for " + req["prompt"]
        )
        
        summary = tracker.get_session_summary()
        print(f"Request {i}: {req['prompt']}")
        print(f"  Cost: ${result['total_cost']:.4f}")
        print(f"  Running total: ${summary['total_cost']:.4f}")
        
        # Budget check
        if summary['total_cost'] > budget_limit:
            print(f"  ⚠️  WARNING: Budget exceeded! (${summary['total_cost']:.4f} > ${budget_limit:.2f})")
        elif summary['total_cost'] > budget_limit * 0.8:
            print(f"  🔔 Alert: 80% of budget used")
        
        print()
    
    tracker.print_session_summary()


if __name__ == "__main__":
    print("🎯 AI Token Tracking Usage Examples")
    print("=" * 50)
    
    examples = [
        example_1_simple_tracking,
        example_2_automatic_tracking,
        example_3_cost_comparison,
        example_4_session_management,
        example_5_budget_monitoring
    ]
    
    for example in examples:
        try:
            example()
            print("\n" + "=" * 50)
        except Exception as e:
            print(f"❌ Error in {example.__name__}: {e}")
            print()
    
    print("✅ All examples completed!")
    print("\n💡 Tips:")
    print("- Use different session files for different projects")
    print("- Monitor costs regularly with print_session_summary()")
    print("- Set budget alerts for cost control")
    print("- Export sessions for record keeping")
    print("- Compare model costs before making bulk requests")

#!/usr/bin/env python3
"""
Simple Prompt Caching Example for Beginners

This is a simplified version demonstrating the core concepts of prompt caching:
1. Store responses to avoid repeated API calls
2. Check cache before making new requests
3. Calculate cost and time savings

Perfect for students learning the fundamentals of prompt caching.
"""

import boto3
import json
import time
import hashlib
from datetime import datetime, timedelta


class SimplePromptCache:
    """A basic prompt caching implementation for learning purposes."""
    
    def __init__(self):
        """Initialize the simple cache."""
        # In-memory storage for cached responses
        self.cache = {}
        
        # Track statistics
        self.total_requests = 0
        self.cache_hits = 0
        self.cost_saved = 0.0
        
        # Initialize Bedrock client
        self.bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
        
        print("✅ Simple prompt cache initialized!")
    
    def create_cache_key(self, prompt, model_id):
        """Create a unique key for the cache based on prompt and model."""
        # Combine prompt and model into a single string
        cache_string = f"{prompt}_{model_id}"
        
        # Create a hash to make it a consistent length
        return hashlib.md5(cache_string.encode()).hexdigest()
    
    def get_from_cache(self, prompt, model_id):
        """Check if we have this prompt cached."""
        cache_key = self.create_cache_key(prompt, model_id)
        
        if cache_key in self.cache:
            print("💚 Found in cache! Using cached response.")
            self.cache_hits += 1
            self.cost_saved += 0.01  # Approximate cost savings
            return self.cache[cache_key]
        
        print("🔴 Not in cache. Will call API.")
        return None
    
    def store_in_cache(self, prompt, model_id, response):
        """Store the response in cache for future use."""
        cache_key = self.create_cache_key(prompt, model_id)
        
        # Store with timestamp
        self.cache[cache_key] = {
            'response': response,
            'timestamp': datetime.now(),
            'prompt': prompt
        }
        
        print("💾 Stored response in cache.")
    
    def ask_bedrock(self, prompt, model_id="amazon.nova-lite-v1:0"):
        """
        Ask Bedrock a question with caching.
        
        This method:
        1. Checks cache first
        2. If not cached, calls Bedrock API
        3. Stores the response in cache
        4. Returns the response
        """
        self.total_requests += 1
        start_time = time.time()
        
        # Step 1: Check cache
        cached_result = self.get_from_cache(prompt, model_id)
        if cached_result:
            return {
                'answer': cached_result['response'],
                'from_cache': True,
                'time_taken': time.time() - start_time
            }
        
        # Step 2: Not in cache, call API
        try:
            # Prepare the request for Nova Lite
            request_body = {
                "schemaVersion": "messages-v1",
                "messages": [
                    {
                        "role": "user",
                        "content": [{"text": prompt}]
                    }
                ],
                "inferenceConfig": {
                    "maxTokens": 500,
                    "temperature": 0.7
                }
            }
            
            # Call Bedrock
            print("🔄 Calling Bedrock API...")
            response = self.bedrock.invoke_model(
                modelId=model_id,
                body=json.dumps(request_body),
                contentType='application/json'
            )
            
            # Parse the response
            response_body = json.loads(response['body'].read())
            answer = response_body['output']['message']['content'][0]['text']
            
            # Step 3: Store in cache
            self.store_in_cache(prompt, model_id, answer)
            
            return {
                'answer': answer,
                'from_cache': False,
                'time_taken': time.time() - start_time
            }
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return {
                'error': str(e),
                'from_cache': False,
                'time_taken': time.time() - start_time
            }
    
    def print_stats(self):
        """Print cache statistics."""
        hit_rate = (self.cache_hits / self.total_requests * 100) if self.total_requests > 0 else 0
        
        print("\n" + "="*40)
        print("📊 CACHE STATISTICS")
        print("="*40)
        print(f"Total questions asked: {self.total_requests}")
        print(f"Answered from cache: {self.cache_hits}")
        print(f"Cache hit rate: {hit_rate:.1f}%")
        print(f"Estimated cost saved: ${self.cost_saved:.3f}")
        print(f"Cache size: {len(self.cache)} items")
        print("="*40)


def learning_demo():
    """A step-by-step demo for students to understand caching."""
    print("🎓 PROMPT CACHING LEARNING DEMO")
    print("=" * 50)
    print("This demo shows how caching works step by step.\n")
    
    # Create our cache
    cache = SimplePromptCache()
    
    # Questions to ask (notice some repeats!)
    questions = [
        "What is machine learning?",
        "How does cloud computing work?", 
        "What is machine learning?",  # Same as #1 - should be cached!
        "What are the benefits of AI?",
        "How does cloud computing work?",  # Same as #2 - should be cached!
        "What is machine learning?"  # Same as #1 and #3 - should be cached!
    ]
    
    print("We'll ask 6 questions, but notice some are repeated...")
    print("The repeated questions should come from cache!\n")
    
    for i, question in enumerate(questions, 1):
        print(f"\n--- Question {i}: {question} ---")
        
        result = cache.ask_bedrock(question)
        
        if 'error' not in result:
            print(f"📝 Answer: {result['answer'][:100]}...")
            print(f"⚡ From cache: {result['from_cache']}")
            print(f"⏱️  Time taken: {result['time_taken']:.2f} seconds")
        else:
            print(f"❌ Error: {result['error']}")
        
        # Pause for learning
        if i < len(questions):
            input("\nPress Enter to continue to next question...")
    
    # Show final statistics
    cache.print_stats()
    
    print("\n🎯 KEY LEARNING POINTS:")
    print("1. First time asking = API call (slower, costs money)")
    print("2. Repeated questions = cache hit (faster, free!)")
    print("3. Cache saves both time and money")
    print("4. More cache hits = better performance")


def quick_test():
    """Quick test of the caching system."""
    print("🚀 Quick Caching Test\n")
    
    cache = SimplePromptCache()
    
    # Ask the same question twice
    question = "What is artificial intelligence?"
    
    print("1. First time asking (should call API):")
    result1 = cache.ask_bedrock(question)
    print(f"   From cache: {result1['from_cache']}")
    print(f"   Time: {result1['time_taken']:.2f}s")
    
    print("\n2. Second time asking same question (should use cache):")
    result2 = cache.ask_bedrock(question)
    print(f"   From cache: {result2['from_cache']}")
    print(f"   Time: {result2['time_taken']:.3f}s")
    
    cache.print_stats()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        quick_test()
    else:
        learning_demo()

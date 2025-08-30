#!/usr/bin/env python3
"""
Redis-Based Prompt Caching for Production Use

This example demonstrates how to implement prompt caching using Redis
for production environments where:
- Multiple applications need to share the cache
- Cache needs to persist across application restarts
- Cache needs to be distributed across multiple servers

Requirements:
    pip install redis

Note: This example assumes you have Redis running locally.
For AWS environments, consider using ElastiCache for Redis.
"""

import boto3
import json
import time
import hashlib
import pickle
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    print("⚠️  Redis not available. Install with: pip install redis")


class RedisPromptCache:
    """Production-ready prompt caching using Redis."""
    
    def __init__(self, 
                 redis_host: str = 'localhost',
                 redis_port: int = 6379,
                 redis_db: int = 0,
                 ttl_seconds: int = 3600,
                 key_prefix: str = 'bedrock:cache:'):
        """
        Initialize Redis-based prompt cache.
        
        Args:
            redis_host: Redis server hostname
            redis_port: Redis server port
            redis_db: Redis database number
            ttl_seconds: Default TTL for cache entries
            key_prefix: Prefix for all cache keys
        """
        if not REDIS_AVAILABLE:
            raise ImportError("Redis is required. Install with: pip install redis")
        
        self.ttl_seconds = ttl_seconds
        self.key_prefix = key_prefix
        
        # Connect to Redis
        try:
            self.redis_client = redis.Redis(
                host=redis_host,
                port=redis_port,
                db=redis_db,
                decode_responses=False  # We'll handle encoding ourselves
            )
            
            # Test connection
            self.redis_client.ping()
            print(f"✅ Connected to Redis at {redis_host}:{redis_port}")
            
        except redis.ConnectionError:
            print(f"❌ Could not connect to Redis at {redis_host}:{redis_port}")
            print("   Make sure Redis is running or use in-memory caching instead.")
            raise
        
        # Initialize Bedrock client
        self.bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')
        
        # Statistics (stored in Redis)
        self.stats_key = f"{key_prefix}stats"
        self._init_stats()
        
        print(f"🚀 Redis prompt cache ready (TTL: {ttl_seconds}s)")
    
    def _init_stats(self):
        """Initialize cache statistics in Redis."""
        if not self.redis_client.exists(self.stats_key):
            initial_stats = {
                'total_requests': 0,
                'cache_hits': 0,
                'cache_misses': 0,
                'total_cost_saved': 0.0,
                'created_at': datetime.now().isoformat()
            }
            self.redis_client.set(
                self.stats_key,
                pickle.dumps(initial_stats),
                ex=None  # Stats don't expire
            )
    
    def _get_stats(self) -> Dict[str, Any]:
        """Get current statistics from Redis."""
        stats_data = self.redis_client.get(self.stats_key)
        if stats_data:
            return pickle.loads(stats_data)
        return {}
    
    def _update_stats(self, updates: Dict[str, Any]):
        """Update statistics in Redis."""
        stats = self._get_stats()
        stats.update(updates)
        stats['updated_at'] = datetime.now().isoformat()
        
        self.redis_client.set(
            self.stats_key,
            pickle.dumps(stats),
            ex=None  # Stats don't expire
        )
    
    def _generate_cache_key(self, prompt: str, model_id: str, **kwargs) -> str:
        """Generate Redis key for the cache entry."""
        # Create unique cache key based on all parameters
        cache_data = {
            'prompt': prompt,
            'model_id': model_id,
            'temperature': kwargs.get('temperature', 0.7),
            'max_tokens': kwargs.get('max_tokens', 1000),
            'top_p': kwargs.get('top_p', 0.9)
        }
        
        # Create hash
        cache_string = json.dumps(cache_data, sort_keys=True)
        cache_hash = hashlib.sha256(cache_string.encode()).hexdigest()
        
        return f"{self.key_prefix}{cache_hash}"
    
    def get_cached_response(self, prompt: str, model_id: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Get cached response from Redis."""
        cache_key = self._generate_cache_key(prompt, model_id, **kwargs)
        
        try:
            cached_data = self.redis_client.get(cache_key)
            
            if cached_data:
                # Cache hit!
                cache_entry = pickle.loads(cached_data)
                
                # Update statistics
                stats = self._get_stats()
                stats['cache_hits'] = stats.get('cache_hits', 0) + 1
                stats['total_requests'] = stats.get('total_requests', 0) + 1
                
                # Calculate cost savings
                cost_saved = cache_entry.get('original_cost', 0.01)
                stats['total_cost_saved'] = stats.get('total_cost_saved', 0.0) + cost_saved
                
                self._update_stats(stats)
                
                print(f"💚 Redis cache HIT! Saved ${cost_saved:.4f}")
                
                return {
                    'response': cache_entry['response'],
                    'cached': True,
                    'cache_key': cache_key,
                    'cached_at': cache_entry.get('cached_at'),
                    'cost_saved': cost_saved
                }
            
        except Exception as e:
            print(f"⚠️  Error reading from Redis cache: {e}")
        
        return None
    
    def store_response(self, prompt: str, response: str, model_id: str, 
                      input_tokens: int, output_tokens: int, cost: float, **kwargs):
        """Store response in Redis cache."""
        cache_key = self._generate_cache_key(prompt, model_id, **kwargs)
        
        cache_entry = {
            'prompt': prompt,
            'response': response,
            'model_id': model_id,
            'input_tokens': input_tokens,
            'output_tokens': output_tokens,
            'original_cost': cost,
            'cached_at': datetime.now().isoformat(),
            'cache_version': '1.0'
        }
        
        try:
            # Store with TTL
            self.redis_client.set(
                cache_key,
                pickle.dumps(cache_entry),
                ex=self.ttl_seconds
            )
            
            print(f"💾 Stored in Redis cache (TTL: {self.ttl_seconds}s, cost: ${cost:.4f})")
            
        except Exception as e:
            print(f"⚠️  Error storing to Redis cache: {e}")
    
    def invoke_with_caching(self, prompt: str, model_id: str = "amazon.nova-lite-v1:0", **kwargs) -> Dict[str, Any]:
        """Invoke Bedrock with Redis caching."""
        start_time = time.time()
        
        # Check Redis cache first
        cached_result = self.get_cached_response(prompt, model_id, **kwargs)
        if cached_result:
            cached_result['response_time'] = time.time() - start_time
            return cached_result
        
        # Cache miss - call API
        print("🔴 Redis cache MISS - calling Bedrock API")
        
        # Update miss statistics
        stats = self._get_stats()
        stats['cache_misses'] = stats.get('cache_misses', 0) + 1
        stats['total_requests'] = stats.get('total_requests', 0) + 1
        self._update_stats(stats)
        
        try:
            # Prepare request for Nova Lite
            request_body = {
                "schemaVersion": "messages-v1",
                "messages": [{"role": "user", "content": [{"text": prompt}]}],
                "inferenceConfig": {
                    "maxTokens": kwargs.get('max_tokens', 1000),
                    "temperature": kwargs.get('temperature', 0.7),
                    "topP": kwargs.get('top_p', 0.9)
                }
            }
            
            # Call Bedrock
            response = self.bedrock_runtime.invoke_model(
                modelId=model_id,
                body=json.dumps(request_body),
                contentType='application/json'
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            content = response_body['output']['message']['content'][0]['text']
            usage = response_body.get('usage', {})
            input_tokens = usage.get('inputTokens', 0)
            output_tokens = usage.get('outputTokens', 0)
            
            # Calculate cost (Nova Lite pricing)
            cost = (input_tokens / 1000 * 0.06) + (output_tokens / 1000 * 0.24)
            
            # Store in Redis cache
            self.store_response(prompt, content, model_id, input_tokens, output_tokens, cost, **kwargs)
            
            return {
                'response': content,
                'cached': False,
                'cache_key': self._generate_cache_key(prompt, model_id, **kwargs),
                'response_time': time.time() - start_time,
                'cost': cost,
                'input_tokens': input_tokens,
                'output_tokens': output_tokens
            }
            
        except Exception as e:
            print(f"❌ Error calling Bedrock: {e}")
            return {
                'error': str(e),
                'cached': False,
                'response_time': time.time() - start_time
            }
    
    def get_cache_info(self) -> Dict[str, Any]:
        """Get Redis cache information."""
        try:
            # Get Redis info
            redis_info = self.redis_client.info()
            
            # Count cache entries
            cache_keys = self.redis_client.keys(f"{self.key_prefix}*")
            cache_count = len([k for k in cache_keys if not k.decode().endswith('stats')])
            
            # Get statistics
            stats = self._get_stats()
            
            # Calculate hit rate
            total_requests = stats.get('total_requests', 0)
            cache_hits = stats.get('cache_hits', 0)
            hit_rate = (cache_hits / total_requests * 100) if total_requests > 0 else 0
            
            return {
                'redis_version': redis_info.get('redis_version'),
                'redis_memory_used': redis_info.get('used_memory_human'),
                'cache_entries': cache_count,
                'total_requests': total_requests,
                'cache_hits': cache_hits,
                'cache_misses': stats.get('cache_misses', 0),
                'hit_rate': hit_rate,
                'total_cost_saved': stats.get('total_cost_saved', 0.0),
                'cache_ttl': self.ttl_seconds
            }
            
        except Exception as e:
            return {'error': f"Could not get Redis info: {e}"}
    
    def print_cache_info(self):
        """Print formatted cache information."""
        info = self.get_cache_info()
        
        print("\n" + "=" * 60)
        print("📊 REDIS PROMPT CACHE INFORMATION")
        print("=" * 60)
        
        if 'error' in info:
            print(f"❌ {info['error']}")
            return
        
        print(f"🔧 Redis Version: {info.get('redis_version', 'Unknown')}")
        print(f"💾 Memory Used: {info.get('redis_memory_used', 'Unknown')}")
        print(f"📦 Cache Entries: {info['cache_entries']}")
        print(f"🔄 Total Requests: {info['total_requests']}")
        print(f"✅ Cache Hits: {info['cache_hits']}")
        print(f"❌ Cache Misses: {info['cache_misses']}")
        print(f"📈 Hit Rate: {info['hit_rate']:.1f}%")
        print(f"💰 Cost Saved: ${info['total_cost_saved']:.4f}")
        print(f"⏰ Cache TTL: {info['cache_ttl']} seconds")
        print("=" * 60)
    
    def clear_cache(self):
        """Clear all cache entries (but keep stats)."""
        try:
            cache_keys = self.redis_client.keys(f"{self.key_prefix}*")
            stats_key_bytes = self.stats_key.encode()
            
            # Delete all cache keys except stats
            for key in cache_keys:
                if key != stats_key_bytes:
                    self.redis_client.delete(key)
            
            print("🧹 Redis cache cleared")
            
        except Exception as e:
            print(f"⚠️  Error clearing cache: {e}")


def demo_redis_caching():
    """Demonstrate Redis caching functionality."""
    print("🚀 Redis Prompt Caching Demo")
    print("=" * 50)
    
    try:
        # Initialize Redis cache
        cache = RedisPromptCache(
            redis_host='localhost',
            redis_port=6379,
            ttl_seconds=300  # 5 minutes for demo
        )
        
        # Test prompts
        test_prompts = [
            "What is distributed computing?",
            "Explain microservices architecture.",
            "What is distributed computing?",  # Repeat for cache test
            "How does Redis work?",
            "Explain microservices architecture."  # Another repeat
        ]
        
        print(f"\n🧪 Testing with {len(test_prompts)} prompts...")
        
        for i, prompt in enumerate(test_prompts, 1):
            print(f"\n--- Request {i}: {prompt[:40]}... ---")
            
            result = cache.invoke_with_caching(
                prompt=prompt,
                max_tokens=200,
                temperature=0.7
            )
            
            if 'error' not in result:
                print(f"📝 Response: {result['response'][:80]}...")
                print(f"⚡ Cached: {result['cached']}")
                print(f"⏱️  Time: {result['response_time']:.2f}s")
                print(f"💰 Cost: ${result.get('cost', 0):.4f}")
            else:
                print(f"❌ Error: {result['error']}")
        
        # Show cache information
        cache.print_cache_info()
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("Make sure Redis is running locally:")
        print("  - Install Redis: https://redis.io/download")
        print("  - Start Redis: redis-server")
        print("  - Or use Docker: docker run -d -p 6379:6379 redis")


if __name__ == "__main__":
    if not REDIS_AVAILABLE:
        print("Redis is not installed. Install it with:")
        print("  pip install redis")
        print("\nThen make sure Redis server is running:")
        print("  redis-server")
    else:
        demo_redis_caching()

# Prompt Caching Examples for AWS Bedrock

This directory contains comprehensive examples of implementing prompt caching with AWS Bedrock, designed to teach students the fundamental concepts and advanced implementations of caching for LLM applications.

## 📚 Learning Objectives

After working through these examples, students will understand:

1. **Why Prompt Caching Matters**
   - Reduce API response latency (2-10x faster)
   - Significantly lower costs by avoiding duplicate API calls
   - Improve application reliability and user experience
   - Enable better scalability for production applications

2. **Core Caching Concepts**
   - Cache key generation and uniqueness
   - Time-to-Live (TTL) and cache expiration
   - Cache hit vs. cache miss scenarios
   - Cost-benefit analysis of caching strategies

3. **Implementation Patterns**
   - In-memory caching for single applications
   - File-based persistent caching
   - Distributed caching with Redis for production

## 🗂️ Files Overview

### 1. `simple_prompt_cache.py` - Beginner Level
**Perfect starting point for students new to caching concepts.**

- ✅ Easy to understand in-memory cache
- ✅ Step-by-step interactive demo
- ✅ Clear statistics and cost tracking
- ✅ Educational comments explaining each step

```bash
# Run the interactive learning demo
python simple_prompt_cache.py

# Quick test with immediate comparison
python simple_prompt_cache.py quick
```

**Key Learning Points:**
- How cache keys are generated
- The difference between cache hits and misses
- Immediate cost and time savings visualization

### 2. `prompt_caching_example.py` - Advanced Level
**Comprehensive production-ready implementation with multiple backends.**

- ✅ Multiple cache backends (memory, file, Redis)
- ✅ TTL-based cache expiration
- ✅ Cache size management and cleanup
- ✅ Detailed cost calculation and tracking
- ✅ Command-line interface for testing

```bash
# Run comprehensive demo
python prompt_caching_example.py --demo

# Test cache expiration (5-second TTL)
python prompt_caching_example.py --test-expiration

# Test single prompt with custom settings
python prompt_caching_example.py --prompt "What is machine learning?" --model "amazon.nova-lite-v1:0"

# Use memory cache with custom TTL
python prompt_caching_example.py --prompt "Explain AI" --cache-type memory --ttl 1800
```

**Key Features:**
- Persistent file-based caching
- Automatic cache cleanup and size management
- Comprehensive cost tracking across models
- Production-ready error handling

### 3. `redis_prompt_cache.py` - Production Level
**Enterprise-grade distributed caching for scalable applications.**

- ✅ Redis-based distributed caching
- ✅ Shared cache across multiple applications
- ✅ Persistent statistics and analytics
- ✅ Production monitoring and management
- ✅ Scalable for high-traffic applications

```bash
# First, start Redis (requires Docker or local Redis installation)
docker run -d -p 6379:6379 redis

# Install Redis Python client
pip install redis

# Run Redis caching demo
python redis_prompt_cache.py
```

**When to Use Redis Caching:**
- Multiple applications sharing the same cache
- Need for cache persistence across restarts
- High-traffic production environments
- Distributed systems requiring shared state

## 🚀 Quick Start Guide

### Prerequisites
1. **AWS Configuration**
   ```bash
   aws configure
   # Ensure you have Bedrock access in us-east-1
   ```

2. **Python Dependencies**
   ```bash
   # Basic examples (simple and advanced)
   pip install boto3

   # For Redis example only
   pip install redis
   ```

### Running Your First Cache Example

1. **Start with the Simple Example:**
   ```bash
   python simple_prompt_cache.py
   ```
   
   This will run an interactive demo showing:
   - 6 questions (with intentional repeats)
   - Clear indication of cache hits vs. misses
   - Real-time cost and time savings

2. **Explore Advanced Features:**
   ```bash
   python prompt_caching_example.py --demo
   ```
   
   This demonstrates:
   - File-based persistent caching
   - Automatic cache management
   - Detailed statistics and cost tracking

3. **Try Production Redis Caching:**
   ```bash
   # Start Redis first
   docker run -d -p 6379:6379 redis
   
   # Install Redis client
   pip install redis
   
   # Run Redis demo
   python redis_prompt_cache.py
   ```

## 📊 Understanding Cache Performance

### Cost Savings Example
With Nova Lite pricing (as of August 2025):
- Input tokens: $0.06 per 1K tokens
- Output tokens: $0.24 per 1K tokens

**Example Calculation:**
- Original API call: 100 input + 200 output tokens = $0.054
- Cache hit: $0.00 (instant response)
- **Savings per cache hit: $0.054**

For 1000 repeated questions:
- Without cache: $54.00
- With 80% cache hit rate: $10.80
- **Total savings: $43.20 (80% cost reduction)**

### Performance Improvements
- **API call:** 2-5 seconds average response time
- **Cache hit:** 0.001-0.01 seconds (200-500x faster)
- **Network bandwidth:** Reduced by 80-95% for cached responses

## 🎓 Educational Exercises

### Exercise 1: Basic Cache Understanding
1. Run `simple_prompt_cache.py`
2. Observe the cache hit/miss patterns
3. Calculate manual cost savings based on the statistics

### Exercise 2: Cache Expiration
1. Run `prompt_caching_example.py --test-expiration`
2. Understand how TTL affects cache behavior
3. Experiment with different TTL values

### Exercise 3: Production Scaling
1. Set up Redis using Docker
2. Run multiple instances of `redis_prompt_cache.py`
3. Observe how they share the same cache

### Exercise 4: Custom Implementation
1. Modify `simple_prompt_cache.py` to add your own features:
   - Different cache key strategies
   - Custom cost calculation
   - Cache warming (pre-populating common queries)

## 🔧 Configuration Options

### Cache Backend Comparison

| Feature | Memory | File | Redis |
|---------|--------|------|-------|
| **Speed** | Fastest | Fast | Fast |
| **Persistence** | No | Yes | Yes |
| **Sharing** | No | Limited | Yes |
| **Scalability** | Low | Medium | High |
| **Setup Complexity** | None | Low | Medium |
| **Best For** | Development | Single app | Production |

### Recommended Settings

**Development/Learning:**
```python
cache = SimplePromptCache()  # Start here
```

**Single Application:**
```python
cache = BedrockPromptCache(
    cache_type="file",
    ttl_seconds=3600,  # 1 hour
    max_cache_size=1000
)
```

**Production Environment:**
```python
cache = RedisPromptCache(
    redis_host="your-redis-host",
    ttl_seconds=7200,  # 2 hours
    key_prefix="myapp:cache:"
)
```

## 🛡️ Best Practices

### Cache Key Design
- ✅ Include all parameters that affect the response
- ✅ Use consistent ordering for parameters
- ✅ Consider model-specific settings
- ❌ Don't include timestamps or random data

### TTL Strategy
- **Short TTL (5-30 minutes):** Rapidly changing content
- **Medium TTL (1-6 hours):** General Q&A, explanations
- **Long TTL (12-24 hours):** Static content, definitions
- **No TTL:** Mathematical calculations, code generation

### Security Considerations
- 🔐 Don't cache sensitive or personal information
- 🔐 Use appropriate Redis authentication in production
- 🔐 Consider encryption for cached data
- 🔐 Implement proper access controls

### Monitoring and Maintenance
- 📊 Track cache hit rates (aim for >70%)
- 📊 Monitor cache size and memory usage
- 📊 Set up alerts for cache failures
- 🧹 Implement regular cache cleanup

## 🐛 Common Issues and Solutions

### Issue: Low Cache Hit Rate
**Symptoms:** < 50% cache hit rate
**Causes:** 
- Inconsistent parameter ordering
- Including dynamic data in cache keys
- TTL too short for use patterns

**Solutions:**
- Review cache key generation
- Normalize parameters before hashing
- Analyze actual usage patterns

### Issue: High Memory Usage
**Symptoms:** Application running out of memory
**Causes:**
- No cache size limits
- Very large responses being cached
- Memory leaks in cache implementation

**Solutions:**
- Set `max_cache_size` limits
- Implement LRU eviction
- Monitor cache entry sizes

### Issue: Stale Data
**Symptoms:** Outdated responses being served
**Causes:**
- TTL too long for dynamic content
- No cache invalidation strategy

**Solutions:**
- Reduce TTL for dynamic content
- Implement manual cache invalidation
- Use versioned cache keys

## 📈 Performance Metrics

Track these key metrics to optimize your caching:

1. **Cache Hit Rate** - Percentage of requests served from cache
2. **Average Response Time** - Including both cached and API calls
3. **Cost Savings** - Total cost avoided through caching
4. **Cache Size** - Number of entries and memory usage
5. **Error Rate** - Failed cache operations

**Target Goals:**
- Cache Hit Rate: > 70%
- Response Time Improvement: > 5x for cache hits
- Cost Reduction: > 50% for repeated queries
- Error Rate: < 1%

## 🔗 Related Resources

- [AWS Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/)
- [Redis Documentation](https://redis.io/documentation)
- [AWS ElastiCache for Redis](https://aws.amazon.com/elasticache/redis/)
- [Course.md - Complete curriculum reference](../../Course.md)

## 💡 Next Steps

After mastering prompt caching:

1. **Chapter 3:** Explore advanced prompt engineering techniques
2. **Chapter 4:** Learn about fine-tuning and model customization
3. **Utils Directory:** Implement comprehensive cost monitoring
4. **Production:** Deploy caching in real applications

Remember: Effective caching is often the difference between a prototype and a production-ready AI application! 🚀

#!/usr/bin/env python3
"""
Tool Use with Strands Agents - Comprehensive Example
Chapter 3: Model Adaptation

This module demonstrates advanced tool use patterns with Strands Agents, showing how to:
1. Define custom tools for various tasks
2. Integrate with AWS services  
3. Handle tool execution and error cases
4. Build practical AI applications with external capabilities

Author: AWS AI Engineering Course
Version: 1.0
"""

import json
import boto3
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import time

try:
    from strands import Agent
    from strands.tools import tool
    STRANDS_AVAILABLE = True
except ImportError:
    STRANDS_AVAILABLE = False

# Mock tool decorator if Strands is not available (for demonstration)
if not STRANDS_AVAILABLE:
    def tool(func):
        """Mock tool decorator for demonstration when Strands is not available."""
        func._is_tool = True
        return func


class StrandsToolDemo:
    """
    Comprehensive demonstration of tool use with Strands Agents.
    
    This class showcases various types of tools and how they work together
    to create powerful AI applications.
    """
    
    def __init__(self):
        """Initialize the demo with AWS clients and tool configurations."""
        self.agent = None
        self.tools = []
        
        # Initialize AWS clients
        try:
            self.bedrock = boto3.client('bedrock-runtime')
            self.s3 = boto3.client('s3')
            self.cloudwatch = boto3.client('cloudwatch')
            print("✅ AWS clients initialized successfully")
        except Exception as e:
            print(f"⚠️  AWS clients not available: {e}")
    
    def setup_tools(self):
        """Define and register all available tools."""
        
        # === UTILITY TOOLS ===
        
        @tool
        def get_current_time(timezone: str = "UTC") -> str:
            """
            Get the current time in a specified timezone.
            
            Args:
                timezone: The timezone to get time for (default: UTC)
                
            Returns:
                Current time as formatted string
            """
            try:
                now = datetime.now()
                return f"Current time ({timezone}): {now.strftime('%Y-%m-%d %H:%M:%S')}"
            except Exception as e:
                return f"Error getting time: {str(e)}"
        
        @tool
        def calculate_business_days(start_date: str, end_date: str) -> Dict[str, Any]:
            """
            Calculate business days between two dates.
            
            Args:
                start_date: Start date in YYYY-MM-DD format
                end_date: End date in YYYY-MM-DD format
                
            Returns:
                Dictionary with calculation results
            """
            try:
                from datetime import datetime
                start = datetime.strptime(start_date, '%Y-%m-%d')
                end = datetime.strptime(end_date, '%Y-%m-%d')
                
                # Calculate business days (Mon-Fri)
                business_days = 0
                current = start
                while current <= end:
                    if current.weekday() < 5:  # Monday = 0, Friday = 4
                        business_days += 1
                    current += timedelta(days=1)
                
                total_days = (end - start).days + 1
                weekend_days = total_days - business_days
                
                return {
                    "start_date": start_date,
                    "end_date": end_date,
                    "total_days": total_days,
                    "business_days": business_days,
                    "weekend_days": weekend_days,
                    "weeks": round(business_days / 5, 1)
                }
            except Exception as e:
                return {"error": f"Date calculation failed: {str(e)}"}
        
        # === AWS INTEGRATION TOOLS ===
        
        @tool
        def check_s3_bucket_size(bucket_name: str) -> Dict[str, Any]:
            """
            Get the size and object count of an S3 bucket.
            
            Args:
                bucket_name: Name of the S3 bucket to check
                
            Returns:
                Dictionary with bucket statistics
            """
            try:
                # Get bucket metrics from CloudWatch
                response = self.cloudwatch.get_metric_statistics(
                    Namespace='AWS/S3',
                    MetricName='BucketSizeBytes',
                    Dimensions=[
                        {'Name': 'BucketName', 'Value': bucket_name},
                        {'Name': 'StorageType', 'Value': 'StandardStorage'}
                    ],
                    StartTime=datetime.now() - timedelta(days=2),
                    EndTime=datetime.now(),
                    Period=86400,  # 24 hours
                    Statistics=['Average']
                )
                
                if response['Datapoints']:
                    size_bytes = response['Datapoints'][-1]['Average']
                    size_gb = round(size_bytes / (1024**3), 2)
                    
                    return {
                        "bucket_name": bucket_name,
                        "size_bytes": int(size_bytes),
                        "size_gb": size_gb,
                        "status": "active",
                        "last_updated": response['Datapoints'][-1]['Timestamp'].isoformat()
                    }
                else:
                    return {
                        "bucket_name": bucket_name,
                        "status": "empty_or_no_metrics",
                        "message": "No metrics available - bucket may be empty or newly created"
                    }
                    
            except Exception as e:
                return {
                    "bucket_name": bucket_name,
                    "error": f"Failed to get bucket size: {str(e)}",
                    "status": "error"
                }
        
        @tool
        def estimate_bedrock_cost(model_id: str, input_tokens: int, output_tokens: int) -> Dict[str, Any]:
            """
            Estimate the cost of a Bedrock model invocation.
            
            Args:
                model_id: The Bedrock model ID
                input_tokens: Number of input tokens
                output_tokens: Number of output tokens
                
            Returns:
                Cost estimation breakdown
            """
            try:
                # Simplified pricing for common models (as of 2024)
                pricing = {
                    "amazon.nova-lite-v1:0": {"input": 0.00006, "output": 0.00024},  # per 1K tokens
                    "amazon.nova-pro-v1:0": {"input": 0.0008, "output": 0.0032},
                    "amazon.titan-text-express-v1": {"input": 0.0008, "output": 0.0016},
                    "anthropic.claude-3-haiku-20240307-v1:0": {"input": 0.00025, "output": 0.00125}
                }
                
                if model_id not in pricing:
                    return {
                        "model_id": model_id,
                        "error": "Pricing not available for this model",
                        "available_models": list(pricing.keys())
                    }
                
                model_pricing = pricing[model_id]
                input_cost = (input_tokens / 1000) * model_pricing["input"]
                output_cost = (output_tokens / 1000) * model_pricing["output"]
                total_cost = input_cost + output_cost
                
                return {
                    "model_id": model_id,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "input_cost_usd": round(input_cost, 6),
                    "output_cost_usd": round(output_cost, 6),
                    "total_cost_usd": round(total_cost, 6),
                    "pricing_per_1k_tokens": model_pricing
                }
                
            except Exception as e:
                return {"error": f"Cost estimation failed: {str(e)}"}
        
        # === EXTERNAL API TOOLS ===
        
        @tool
        def get_weather_info(city: str, country_code: str = "US") -> Dict[str, Any]:
            """
            Get current weather information for a city.
            
            Args:
                city: Name of the city
                country_code: Country code (default: US)
                
            Returns:
                Weather information dictionary
            """
            try:
                # Using a free weather API (OpenWeatherMap - requires API key)
                # For demo purposes, return mock data
                import random
                
                temperatures = [15, 18, 22, 25, 28, 32, 35]
                conditions = ["sunny", "cloudy", "partly cloudy", "rainy", "clear"]
                
                return {
                    "city": city,
                    "country": country_code,
                    "temperature_celsius": random.choice(temperatures),
                    "condition": random.choice(conditions),
                    "humidity": random.randint(30, 80),
                    "timestamp": datetime.now().isoformat(),
                    "note": "Demo data - replace with real API in production"
                }
                
            except Exception as e:
                return {
                    "city": city,
                    "error": f"Weather lookup failed: {str(e)}"
                }
        
        @tool
        def search_web_content(query: str, max_results: int = 3) -> Dict[str, Any]:
            """
            Search for web content (mock implementation for demo).
            
            Args:
                query: Search query string
                max_results: Maximum number of results to return
                
            Returns:
                Search results dictionary
            """
            try:
                # Mock search results for demonstration
                mock_results = [
                    {
                        "title": f"Result about {query} - AWS Documentation",
                        "url": f"https://docs.aws.amazon.com/search?q={query}",
                        "snippet": f"Learn about {query} in AWS services and best practices.",
                        "relevance": 0.95
                    },
                    {
                        "title": f"{query} - Technical Guide",
                        "url": f"https://example.com/{query.lower().replace(' ', '-')}",
                        "snippet": f"Comprehensive guide to understanding and implementing {query}.",
                        "relevance": 0.87
                    },
                    {
                        "title": f"Best Practices for {query}",
                        "url": f"https://bestpractices.com/{query}",
                        "snippet": f"Industry best practices and real-world examples of {query}.",
                        "relevance": 0.82
                    }
                ]
                
                return {
                    "query": query,
                    "results": mock_results[:max_results],
                    "total_found": len(mock_results),
                    "search_time": "0.12 seconds",
                    "note": "Demo data - replace with real search API in production"
                }
                
            except Exception as e:
                return {
                    "query": query,
                    "error": f"Search failed: {str(e)}"
                }
        
        # === DATA PROCESSING TOOLS ===
        
        @tool
        def analyze_text_metrics(text: str) -> Dict[str, Any]:
            """
            Analyze various metrics of a text string.
            
            Args:
                text: The text to analyze
                
            Returns:
                Text analysis metrics
            """
            try:
                import re
                
                # Basic text analysis
                word_count = len(text.split())
                char_count = len(text)
                char_count_no_spaces = len(text.replace(' ', ''))
                sentence_count = len(re.split(r'[.!?]+', text.strip()))
                paragraph_count = len([p for p in text.split('\n\n') if p.strip()])
                
                # Reading time estimation (average 200 words per minute)
                reading_time_minutes = round(word_count / 200, 1)
                
                # Most common words (excluding common stop words)
                stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'}
                words = [word.lower().strip('.,!?";') for word in text.split()]
                word_freq = {}
                for word in words:
                    if word not in stop_words and len(word) > 2:
                        word_freq[word] = word_freq.get(word, 0) + 1
                
                top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
                
                return {
                    "text_preview": text[:100] + "..." if len(text) > 100 else text,
                    "word_count": word_count,
                    "character_count": char_count,
                    "character_count_no_spaces": char_count_no_spaces,
                    "sentence_count": sentence_count,
                    "paragraph_count": paragraph_count,
                    "reading_time_minutes": reading_time_minutes,
                    "average_words_per_sentence": round(word_count / max(sentence_count, 1), 1),
                    "top_words": top_words,
                    "analysis_timestamp": datetime.now().isoformat()
                }
                
            except Exception as e:
                return {"error": f"Text analysis failed: {str(e)}"}
        
        # Store tools for later reference
        self.tools = [
            get_current_time,
            calculate_business_days,
            check_s3_bucket_size,
            estimate_bedrock_cost,
            get_weather_info,
            search_web_content,
            analyze_text_metrics
        ]
        
        return self.tools
    
    def create_agent(self):
        """Create a Strands agent with all the defined tools."""
        if not STRANDS_AVAILABLE:
            print("❌ Strands Agents library not available.")
            print("   Install with: pip install strands-agents")
            return None
        
        try:
            tools = self.setup_tools()
            
            # Create agent with Nova Lite model and all tools
            self.agent = Agent(
                tools=tools,
                model="amazon.nova-lite-v1:0"
            )
            
            print("✅ Strands Agent created successfully!")
            print(f"🔧 Agent has access to {len(tools)} tools:")
            for i, tool in enumerate(tools, 1):
                print(f"   {i}. {tool.__name__} - {tool.__doc__.split('.')[0] if tool.__doc__ else 'No description'}")
            
            return self.agent
            
        except Exception as e:
            print(f"❌ Error creating agent: {e}")
            return None
    
    def demonstrate_single_tool_use(self):
        """Demonstrate how the agent uses individual tools."""
        if not self.agent:
            print("❌ Agent not available")
            return
        
        print("=" * 80)
        print("🔧 DEMONSTRATION 1: SINGLE TOOL USE")
        print("=" * 80)
        print()
        
        test_cases = [
            {
                "query": "What time is it right now?",
                "expected_tool": "get_current_time"
            },
            {
                "query": "How many business days are there between 2024-08-01 and 2024-08-15?",
                "expected_tool": "calculate_business_days"
            },
            {
                "query": "What's the weather like in Seattle?",
                "expected_tool": "get_weather_info"
            },
            {
                "query": "How much would it cost to use amazon.nova-lite-v1:0 with 500 input tokens and 200 output tokens?",
                "expected_tool": "estimate_bedrock_cost"
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"🎯 Test Case {i}: {test_case['expected_tool']}")
            print(f"Query: \"{test_case['query']}\"")
            print()
            print("Agent Response:")
            print("-" * 40)
            
            try:
                response = self.agent(test_case['query'])
                print(response)
            except Exception as e:
                print(f"❌ Error: {e}")
            
            print()
            print("-" * 80)
            print()
            time.sleep(1)  # Brief pause between demonstrations
    
    def demonstrate_multi_tool_use(self):
        """Demonstrate how the agent uses multiple tools in sequence."""
        if not self.agent:
            print("❌ Agent not available")
            return
        
        print("=" * 80)
        print("🔧 DEMONSTRATION 2: MULTI-TOOL USE")
        print("=" * 80)
        print()
        
        complex_queries = [
            """I need to plan a project timeline. Please help me with the following:
            1. What's the current time?
            2. How many business days are between 2024-09-01 and 2024-10-15?
            3. What would be the cost to process this analysis using amazon.nova-lite-v1:0 with approximately 1000 input tokens and 500 output tokens?""",
            
            """I'm analyzing some content for a presentation. Can you help me:
            1. Analyze this text: "Artificial Intelligence is transforming how we work and live. Machine learning algorithms can process vast amounts of data quickly and accurately. AI systems are becoming more sophisticated and capable of handling complex tasks."
            2. Search for information about "AI best practices"
            3. What's the weather like in San Francisco for my presentation location?"""
        ]
        
        for i, query in enumerate(complex_queries, 1):
            print(f"🎯 Complex Query {i}:")
            print(f"\"{query}\"")
            print()
            print("Agent Response:")
            print("-" * 40)
            
            try:
                response = self.agent(query)
                print(response)
            except Exception as e:
                print(f"❌ Error: {e}")
            
            print()
            print("-" * 80)
            print()
            time.sleep(2)  # Pause between complex demonstrations
    
    def demonstrate_tool_error_handling(self):
        """Demonstrate how the agent handles tool errors gracefully."""
        if not self.agent:
            print("❌ Agent not available")
            return
        
        print("=" * 80)
        print("🔧 DEMONSTRATION 3: ERROR HANDLING")
        print("=" * 80)
        print()
        
        error_test_cases = [
            {
                "query": "How many business days between invalid-date and 2024-08-15?",
                "description": "Invalid date format"
            },
            {
                "query": "Check the size of a bucket named 'non-existent-bucket-12345'",
                "description": "Non-existent S3 bucket"
            },
            {
                "query": "Estimate cost for model 'invalid-model-id' with 100 tokens",
                "description": "Invalid model ID"
            }
        ]
        
        for i, test_case in enumerate(error_test_cases, 1):
            print(f"🎯 Error Test {i}: {test_case['description']}")
            print(f"Query: \"{test_case['query']}\"")
            print()
            print("Agent Response:")
            print("-" * 40)
            
            try:
                response = self.agent(test_case['query'])
                print(response)
            except Exception as e:
                print(f"❌ Agent Error: {e}")
            
            print()
            print("-" * 80)
            print()
            time.sleep(1)
    
    def demonstrate_tool_inspection(self):
        """Show how to inspect and understand the available tools."""
        print("=" * 80)
        print("🔍 TOOL INSPECTION AND CAPABILITIES")
        print("=" * 80)
        print()
        
        if not self.tools:
            self.setup_tools()
        
        for i, tool in enumerate(self.tools, 1):
            print(f"🔧 Tool {i}: {tool.__name__}")
            print(f"   Description: {tool.__doc__.strip() if tool.__doc__ else 'No description'}")
            
            # Get function signature
            import inspect
            sig = inspect.signature(tool)
            print(f"   Parameters: {list(sig.parameters.keys())}")
            
            # Show parameter details
            for param_name, param in sig.parameters.items():
                param_type = param.annotation if param.annotation != inspect.Parameter.empty else "Any"
                default = f" = {param.default}" if param.default != inspect.Parameter.empty else ""
                print(f"     - {param_name}: {param_type}{default}")
            
            print()
    
    def run_complete_demo(self):
        """Run the complete tool use demonstration."""
        print("🔥 AWS AI ENGINEERING COURSE")
        print("Chapter 3: Model Adaptation - Tool Use with Strands Agents")
        print("=" * 80)
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        if not STRANDS_AVAILABLE:
            print("❌ Strands Agents library not available.")
            print("   Please install with: pip install strands-agents strands-agents-tools")
            print()
            print("🔍 Showing tool definitions for educational purposes...")
            self.demonstrate_tool_inspection()
            return
        
        # Create the agent
        print("🚀 Setting up Strands Agent with custom tools...")
        agent = self.create_agent()
        
        if not agent:
            print("❌ Failed to create agent. Please check AWS credentials and Bedrock access.")
            return
        
        print()
        
        # Run all demonstrations
        self.demonstrate_tool_inspection()
        
        self.demonstrate_single_tool_use()
        
        self.demonstrate_multi_tool_use()
        
        self.demonstrate_tool_error_handling()
        
        # Summary
        print("=" * 80)
        print("📊 DEMONSTRATION SUMMARY")
        print("=" * 80)
        print()
        print("Key Learning Points:")
        print("1. 🔧 Tool Definition: Use @tool decorator to define capabilities")
        print("2. 🤖 Agent Creation: Register tools with Agent() constructor")
        print("3. 🧠 Automatic Decision: Agent decides when and which tools to use")
        print("4. 🔗 Tool Chaining: Agent can use multiple tools to solve complex tasks")
        print("5. ⚠️  Error Handling: Tools should handle errors gracefully")
        print("6. 🎯 Real-world Integration: Connect to AWS services, APIs, and data sources")
        print()
        print("💡 Best Practices:")
        print("   - Write clear tool descriptions and docstrings")
        print("   - Include proper type hints for parameters")
        print("   - Handle errors gracefully within tools")
        print("   - Return structured data when possible")
        print("   - Test tools independently before agent integration")
        print()
        print("🚀 Next Steps:")
        print("   - Customize tools for your specific use cases")
        print("   - Integrate with your organization's APIs and databases")
        print("   - Build multi-agent systems with tool sharing")
        print("   - Implement monitoring and observability for tool usage")


def main():
    """Main function to run the tool use demonstration."""
    try:
        demo = StrandsToolDemo()
        demo.run_complete_demo()
        
        print()
        print("✅ Tool Use demonstration completed!")
        print()
        print("📝 To explore further:")
        print("- Modify the tools to fit your specific needs")
        print("- Add new tools for your domain-specific tasks")
        print("- Integrate with your organization's APIs and services")
        print("- Experiment with different tool combinations")
        print("- Build multi-agent systems with specialized tools")
        
    except Exception as e:
        print(f"❌ Error running demonstration: {str(e)}")
        print()
        print("🔧 Troubleshooting:")
        print("- Ensure Strands Agents library is installed: pip install strands-agents")
        print("- Check AWS credentials are configured")
        print("- Verify AWS Bedrock model access permissions")
        print("- Check network connectivity for external APIs")


if __name__ == "__main__":
    main()

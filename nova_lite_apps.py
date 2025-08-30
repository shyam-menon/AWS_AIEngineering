#!/usr/bin/env python3
"""
Amazon Nova Lite - Specialized Applications

A collection of specialized applications built on top of Amazon Nova Lite
for specific use cases like content creation, code assistance, and analysis.
"""

import boto3
import json
import argparse
from datetime import datetime
from typing import List, Dict, Optional


class NovaLiteApps:
    """Specialized applications using Nova Lite."""
    
    def __init__(self, region='us-east-1'):
        """Initialize Nova Lite applications."""
        self.client = boto3.client("bedrock-runtime", region_name=region)
        self.model_id = "us.amazon.nova-lite-v1:0"
    
    def _invoke(self, messages: List[Dict], system_prompt: str = None, 
                max_tokens: int = 1000, temperature: float = 0.7, stream: bool = False):
        """Internal method to invoke Nova Lite."""
        system_list = []
        if system_prompt:
            system_list.append({"text": system_prompt})
        
        request_body = {
            "schemaVersion": "messages-v1",
            "messages": messages,
            "inferenceConfig": {
                "maxTokens": max_tokens,
                "temperature": temperature,
                "topP": 0.9,
                "topK": 20
            }
        }
        
        if system_list:
            request_body["system"] = system_list
        
        if stream:
            return self._stream_response(request_body)
        else:
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body)
            )
            response_body = json.loads(response['body'].read())
            return response_body['output']['message']['content'][0]['text']
    
    def _stream_response(self, request_body):
        """Stream response from Nova Lite."""
        response = self.client.invoke_model_with_response_stream(
            modelId=self.model_id,
            body=json.dumps(request_body)
        )
        
        full_response = ""
        stream = response.get("body")
        
        if stream:
            for event in stream:
                chunk = event.get("chunk")
                if chunk:
                    chunk_json = json.loads(chunk.get("bytes").decode())
                    content_block_delta = chunk_json.get("contentBlockDelta")
                    if content_block_delta:
                        text = content_block_delta.get("delta").get("text")
                        if text:
                            print(text, end="", flush=True)
                            full_response += text
        
        print()  # New line
        return full_response
    
    def content_creator(self, content_type: str, topic: str, style: str = "professional", 
                       length: str = "medium", stream: bool = True):
        """
        Create various types of content.
        
        Args:
            content_type: blog, article, email, social, story, poem, script
            topic: The main topic or subject
            style: professional, casual, creative, technical, humorous
            length: short, medium, long
            stream: Whether to stream the response
        """
        length_tokens = {"short": 300, "medium": 800, "long": 1500}
        max_tokens = length_tokens.get(length, 800)
        
        style_prompts = {
            "professional": "Write in a professional, authoritative tone with clear structure.",
            "casual": "Write in a friendly, conversational tone that's easy to read.",
            "creative": "Write with creativity and flair, using vivid descriptions and engaging language.",
            "technical": "Write with technical accuracy and precision, using appropriate terminology.",
            "humorous": "Write with humor and wit while maintaining informativeness."
        }
        
        content_templates = {
            "blog": "Write a compelling blog post about {topic}. Include an engaging introduction, well-structured main points, and a strong conclusion. Make it informative and engaging for readers.",
            "article": "Write a comprehensive article about {topic}. Provide in-depth information, expert insights, and actionable takeaways.",
            "email": "Write a professional email about {topic}. Include appropriate subject line, greeting, clear main message, and professional closing.",
            "social": "Write social media content about {topic}. Make it engaging, shareable, and appropriate for social platforms. Include relevant hashtags.",
            "story": "Write an engaging short story with {topic} as the central theme. Include compelling characters, plot development, and a satisfying conclusion.",
            "poem": "Write a creative poem about {topic}. Use vivid imagery, rhythm, and emotional depth.",
            "script": "Write a script or dialogue about {topic}. Include character interactions, scene descriptions, and engaging dialogue."
        }
        
        system_prompt = f"""You are an expert content creator. {style_prompts.get(style, style_prompts['professional'])} 
        Focus on creating high-quality, engaging content that provides value to the reader. 
        Structure your content appropriately for the format requested."""
        
        user_prompt = content_templates.get(content_type, 
            f"Create {content_type} content about {{topic}}").format(topic=topic)
        
        messages = [{"role": "user", "content": [{"text": user_prompt}]}]
        
        print(f"🎯 Creating {length} {content_type} content about '{topic}' in {style} style...")
        print("=" * 60)
        
        return self._invoke(messages, system_prompt, max_tokens, 0.8, stream)
    
    def code_assistant(self, request: str, language: str = "python", 
                      include_tests: bool = False, stream: bool = True):
        """
        Provide coding assistance.
        
        Args:
            request: What you want help with
            language: Programming language
            include_tests: Whether to include test cases
            stream: Whether to stream the response
        """
        system_prompt = f"""You are an expert {language} programmer. Provide clean, well-commented, 
        and efficient code that follows best practices. Include error handling where appropriate.
        Explain your code and provide usage examples."""
        
        if include_tests:
            system_prompt += " Also include unit tests for the code you write."
        
        user_prompt = f"Help me with this {language} programming request: {request}"
        
        messages = [{"role": "user", "content": [{"text": user_prompt}]}]
        
        print(f"💻 {language.title()} Code Assistant")
        print("=" * 30)
        
        return self._invoke(messages, system_prompt, 1200, 0.3, stream)
    
    def research_analyst(self, topic: str, analysis_type: str = "comprehensive", 
                        focus_areas: List[str] = None, stream: bool = True):
        """
        Provide research and analysis.
        
        Args:
            topic: Topic to analyze
            analysis_type: comprehensive, summary, comparison, pros_cons
            focus_areas: Specific areas to focus on
            stream: Whether to stream the response
        """
        focus_text = ""
        if focus_areas:
            focus_text = f" Pay special attention to: {', '.join(focus_areas)}."
        
        analysis_prompts = {
            "comprehensive": f"Provide a comprehensive analysis of {topic}. Cover all major aspects, implications, and considerations.{focus_text}",
            "summary": f"Provide a clear, concise summary of {topic}. Hit the key points without excessive detail.{focus_text}",
            "comparison": f"Compare and contrast different aspects of {topic}. Highlight similarities, differences, and relative advantages.{focus_text}",
            "pros_cons": f"Analyze the pros and cons of {topic}. Provide balanced perspective on advantages and disadvantages.{focus_text}"
        }
        
        system_prompt = """You are a research analyst with expertise across multiple domains. 
        Provide objective, well-researched analysis backed by logical reasoning. 
        Structure your analysis clearly with headings and bullet points where appropriate."""
        
        user_prompt = analysis_prompts.get(analysis_type, analysis_prompts["comprehensive"])
        
        messages = [{"role": "user", "content": [{"text": user_prompt}]}]
        
        print(f"🔍 Research Analysis: {topic}")
        print("=" * 40)
        
        return self._invoke(messages, system_prompt, 1200, 0.4, stream)
    
    def business_consultant(self, business_topic: str, consultation_type: str = "advice", 
                           industry: str = None, stream: bool = True):
        """
        Provide business consultation.
        
        Args:
            business_topic: The business topic or problem
            consultation_type: advice, strategy, plan, analysis
            industry: Specific industry context
            stream: Whether to stream the response
        """
        industry_text = f" in the {industry} industry" if industry else ""
        
        consultation_prompts = {
            "advice": f"Provide practical business advice for {business_topic}{industry_text}. Focus on actionable recommendations.",
            "strategy": f"Develop a strategic approach for {business_topic}{industry_text}. Include short-term and long-term considerations.",
            "plan": f"Create a detailed business plan for {business_topic}{industry_text}. Include steps, timelines, and success metrics.",
            "analysis": f"Analyze the business implications of {business_topic}{industry_text}. Consider risks, opportunities, and market factors."
        }
        
        system_prompt = """You are an experienced business consultant with expertise across various industries. 
        Provide practical, actionable advice that considers real-world constraints and opportunities. 
        Focus on value creation and implementable solutions."""
        
        user_prompt = consultation_prompts.get(consultation_type, consultation_prompts["advice"])
        
        messages = [{"role": "user", "content": [{"text": user_prompt}]}]
        
        print(f"💼 Business Consultation: {business_topic}")
        if industry:
            print(f"🏢 Industry: {industry}")
        print("=" * 40)
        
        return self._invoke(messages, system_prompt, 1000, 0.5, stream)
    
    def creative_writer(self, writing_type: str, theme: str, genre: str = "general", 
                       length: str = "medium", stream: bool = True):
        """
        Creative writing assistant.
        
        Args:
            writing_type: story, poem, script, dialogue, description
            theme: The main theme or prompt
            genre: fiction, mystery, romance, scifi, fantasy, horror, drama
            length: short, medium, long
            stream: Whether to stream the response
        """
        length_tokens = {"short": 400, "medium": 800, "long": 1500}
        max_tokens = length_tokens.get(length, 800)
        
        genre_styles = {
            "fiction": "realistic fiction with relatable characters",
            "mystery": "suspenseful mystery with clues and intrigue", 
            "romance": "romantic story with emotional depth",
            "scifi": "science fiction with futuristic elements",
            "fantasy": "fantasy with magical or supernatural elements",
            "horror": "horror with atmospheric tension",
            "drama": "dramatic story with emotional conflict"
        }
        
        system_prompt = f"""You are a creative writing expert specializing in {genre_styles.get(genre, 'engaging storytelling')}. 
        Write with vivid descriptions, compelling characters, and engaging plot development. 
        Use literary devices to create atmosphere and emotional impact."""
        
        user_prompt = f"Write a {length} {writing_type} in the {genre} genre with the theme: {theme}"
        
        messages = [{"role": "user", "content": [{"text": user_prompt}]}]
        
        print(f"✍️  Creative Writing: {writing_type.title()}")
        print(f"🎭 Genre: {genre.title()}, Theme: {theme}")
        print("=" * 40)
        
        return self._invoke(messages, system_prompt, max_tokens, 0.9, stream)


def main():
    """Main CLI application."""
    parser = argparse.ArgumentParser(description='Nova Lite Specialized Applications')
    subparsers = parser.add_subparsers(dest='app', help='Available applications')
    
    # Content Creator
    content_parser = subparsers.add_parser('content', help='Content creation')
    content_parser.add_argument('type', choices=['blog', 'article', 'email', 'social', 'story', 'poem', 'script'])
    content_parser.add_argument('topic', help='Content topic')
    content_parser.add_argument('--style', default='professional', 
                               choices=['professional', 'casual', 'creative', 'technical', 'humorous'])
    content_parser.add_argument('--length', default='medium', choices=['short', 'medium', 'long'])
    
    # Code Assistant
    code_parser = subparsers.add_parser('code', help='Programming assistance')
    code_parser.add_argument('request', help='What you need help with')
    code_parser.add_argument('--language', default='python', help='Programming language')
    code_parser.add_argument('--tests', action='store_true', help='Include unit tests')
    
    # Research Analyst
    research_parser = subparsers.add_parser('research', help='Research and analysis')
    research_parser.add_argument('topic', help='Topic to analyze')
    research_parser.add_argument('--type', default='comprehensive',
                                choices=['comprehensive', 'summary', 'comparison', 'pros_cons'])
    research_parser.add_argument('--focus', nargs='+', help='Specific focus areas')
    
    # Business Consultant
    business_parser = subparsers.add_parser('business', help='Business consultation')
    business_parser.add_argument('topic', help='Business topic or problem')
    business_parser.add_argument('--type', default='advice',
                                choices=['advice', 'strategy', 'plan', 'analysis'])
    business_parser.add_argument('--industry', help='Specific industry')
    
    # Creative Writer
    creative_parser = subparsers.add_parser('creative', help='Creative writing')
    creative_parser.add_argument('type', choices=['story', 'poem', 'script', 'dialogue', 'description'])
    creative_parser.add_argument('theme', help='Writing theme or prompt')
    creative_parser.add_argument('--genre', default='general',
                                choices=['fiction', 'mystery', 'romance', 'scifi', 'fantasy', 'horror', 'drama'])
    creative_parser.add_argument('--length', default='medium', choices=['short', 'medium', 'long'])
    
    # Global options
    parser.add_argument('--no-stream', action='store_true', help='Disable streaming output')
    parser.add_argument('--region', default='us-east-1', help='AWS region')
    
    args = parser.parse_args()
    
    if not args.app:
        parser.print_help()
        return
    
    # Initialize applications
    apps = NovaLiteApps(region=args.region)
    stream = not args.no_stream
    
    try:
        if args.app == 'content':
            apps.content_creator(args.type, args.topic, args.style, args.length, stream)
        
        elif args.app == 'code':
            apps.code_assistant(args.request, args.language, args.tests, stream)
        
        elif args.app == 'research':
            apps.research_analyst(args.topic, args.type, args.focus, stream)
        
        elif args.app == 'business':
            apps.business_consultant(args.topic, args.type, args.industry, stream)
        
        elif args.app == 'creative':
            apps.creative_writer(args.type, args.theme, args.genre, args.length, stream)
    
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Prompt Engineering Example - Key Principles Implementation
Chapter 3: Model Adaptation

This module demonstrates the key principles of prompt engineering as outlined in the course:
1. Clarity and Specificity
2. Persona Assignment
3. Few-Shot Learning (Examples)
4. Chain of Thought Reasoning

Author: AWS AI Engineering Course
Version: 1.0
"""

import boto3
import json
import time
from typing import Dict, List, Any
from datetime import datetime


class PromptEngineeringDemo:
    """
    A comprehensive demonstration of prompt engineering principles using AWS Bedrock.
    
    This class showcases how different prompting techniques can dramatically improve
    the quality and consistency of LLM outputs.
    """
    
    def __init__(self, model_id: str = "us.amazon.nova-lite-v1:0"):
        """
        Initialize the Prompt Engineering Demo.
        
        Args:
            model_id: The AWS Bedrock model to use for demonstrations
        """
        self.bedrock = boto3.client('bedrock-runtime')
        self.model_id = model_id
        
    def invoke_model(self, prompt: str, temperature: float = 0.3, max_tokens: int = 500) -> str:
        """
        Invoke the AWS Bedrock model with the given prompt.
        
        Args:
            prompt: The input prompt
            temperature: Controls randomness (0.0 = deterministic, 1.0 = creative)
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated response text
        """
        try:
            request_body = {
                "schemaVersion": "messages-v1",
                "messages": [
                    {
                        "role": "user",
                        "content": [{"text": prompt}]
                    }
                ],
                "inferenceConfig": {
                    "temperature": temperature,
                    "maxTokens": max_tokens,
                    "topP": 0.9,
                    "topK": 20
                }
            }
            
            response = self.bedrock.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body)
            )
            
            result = json.loads(response['body'].read())
            return result['output']['message']['content'][0]['text']
            
        except Exception as e:
            return f"Error invoking model: {str(e)}"
    
    def demonstrate_clarity_specificity(self):
        """
        Demonstrate the importance of clarity and specificity in prompts.
        
        Shows the difference between vague and specific prompts.
        """
        print("=" * 80)
        print("🎯 PRINCIPLE 1: CLARITY AND SPECIFICITY")
        print("=" * 80)
        print()
        
        # Poor example - vague and unclear
        poor_prompt = "Write about running shoes."
        
        print("❌ POOR PROMPT (Vague):")
        print(f"'{poor_prompt}'")
        print()
        print("Response:")
        poor_response = self.invoke_model(poor_prompt)
        print(poor_response)
        print()
        print("-" * 80)
        print()
        
        # Good example - clear and specific
        good_prompt = """Write a compelling product description for a new pair of running shoes called "The Velocity."

Requirements:
- Target audience: Serious runners looking for racing shoes
- Tone: Exciting and persuasive
- Length: Exactly 150 words
- Include key features: ultra-lightweight (7 ounces), responsive cushioning, breathable mesh, durable rubber outsole
- Focus on performance benefits for competitive runners"""

        print("✅ IMPROVED PROMPT (Clear & Specific):")
        print(f"'{good_prompt}'")
        print()
        print("Response:")
        good_response = self.invoke_model(good_prompt)
        print(good_response)
        print()
        
        return {"poor": poor_response, "good": good_response}
    
    def demonstrate_persona_assignment(self):
        """
        Demonstrate how persona assignment affects response tone and style.
        
        Shows the same task performed by different personas.
        """
        print("=" * 80)
        print("🎭 PRINCIPLE 2: PERSONA ASSIGNMENT")
        print("=" * 80)
        print()
        
        base_task = "Explain why regular exercise is important for health."
        
        personas = [
            {
                "name": "Medical Professional",
                "prompt": f"You are a medical doctor speaking to patients. {base_task} Use professional medical terminology and cite health benefits.",
                "description": "Professional, authoritative, medical focus"
            },
            {
                "name": "Fitness Enthusiast",
                "prompt": f"You are an energetic fitness coach talking to beginners. {base_task} Be motivational and encouraging!",
                "description": "Enthusiastic, motivational, accessible"
            },
            {
                "name": "Scientific Researcher",
                "prompt": f"You are a research scientist writing for an academic audience. {base_task} Include specific studies and statistical data.",
                "description": "Academic, data-driven, evidence-based"
            }
        ]
        
        responses = {}
        
        for persona in personas:
            print(f"🎭 PERSONA: {persona['name']} ({persona['description']})")
            print(f"Prompt: '{persona['prompt']}'")
            print()
            print("Response:")
            response = self.invoke_model(persona['prompt'])
            responses[persona['name']] = response
            print(response)
            print()
            print("-" * 80)
            print()
        
        return responses
    
    def demonstrate_few_shot_learning(self):
        """
        Demonstrate few-shot learning with examples.
        
        Shows how providing examples improves task performance.
        """
        print("=" * 80)
        print("📚 PRINCIPLE 3: FEW-SHOT LEARNING (EXAMPLES)")
        print("=" * 80)
        print()
        
        # Zero-shot example (no examples provided)
        zero_shot_prompt = """Convert the following customer review into a structured sentiment analysis:

"The product arrived quickly and the quality is amazing. However, the packaging was damaged and customer service was slow to respond."

Provide the analysis in JSON format."""

        print("❌ ZERO-SHOT (No Examples):")
        print(f"'{zero_shot_prompt}'")
        print()
        print("Response:")
        zero_shot_response = self.invoke_model(zero_shot_prompt)
        print(zero_shot_response)
        print()
        print("-" * 80)
        print()
        
        # Few-shot example (with examples)
        few_shot_prompt = """Convert customer reviews into structured sentiment analysis. Here are some examples:

Example 1:
Review: "Great product, fast delivery, but expensive."
Analysis: {
    "overall_sentiment": "positive",
    "sentiment_score": 0.6,
    "aspects": {
        "product_quality": {"sentiment": "positive", "score": 0.9},
        "delivery": {"sentiment": "positive", "score": 0.8},
        "price": {"sentiment": "negative", "score": -0.7}
    }
}

Example 2:
Review: "Poor quality, broke after one week, terrible experience."
Analysis: {
    "overall_sentiment": "negative",
    "sentiment_score": -0.8,
    "aspects": {
        "product_quality": {"sentiment": "negative", "score": -0.9},
        "durability": {"sentiment": "negative", "score": -0.9},
        "overall_experience": {"sentiment": "negative", "score": -0.8}
    }
}

Now analyze this review:
"The product arrived quickly and the quality is amazing. However, the packaging was damaged and customer service was slow to respond."

Analysis:"""

        print("✅ FEW-SHOT (With Examples):")
        print(f"'{few_shot_prompt}'")
        print()
        print("Response:")
        few_shot_response = self.invoke_model(few_shot_prompt, max_tokens=300)
        print(few_shot_response)
        print()
        
        return {"zero_shot": zero_shot_response, "few_shot": few_shot_response}
    
    def demonstrate_chain_of_thought(self):
        """
        Demonstrate Chain of Thought reasoning.
        
        Shows how asking for step-by-step thinking improves complex reasoning.
        """
        print("=" * 80)
        print("🔗 PRINCIPLE 4: CHAIN OF THOUGHT REASONING")
        print("=" * 80)
        print()
        
        problem = """A software development team needs to estimate project timeline. They have:
- 5 developers (3 senior, 2 junior)
- Senior developers code 50 lines/day, junior developers code 30 lines/day
- Project needs 8,000 lines of code
- Team works 5 days per week
- They want 20% buffer time for testing and debugging

How many weeks will the project take?"""
        
        # Direct answer (no reasoning)
        direct_prompt = f"{problem}\n\nProvide the answer:"
        
        print("❌ DIRECT ANSWER (No Reasoning):")
        print(f"'{direct_prompt}'")
        print()
        print("Response:")
        direct_response = self.invoke_model(direct_prompt)
        print(direct_response)
        print()
        print("-" * 80)
        print()
        
        # Chain of thought (step-by-step)
        cot_prompt = f"""{problem}

Think through this step-by-step:

1. First, calculate the daily coding capacity
2. Then, determine how many days of coding are needed
3. Convert to weeks
4. Add the buffer time
5. Provide the final answer

Please show your work for each step:"""

        print("✅ CHAIN OF THOUGHT (Step-by-Step Reasoning):")
        print(f"'{cot_prompt}'")
        print()
        print("Response:")
        cot_response = self.invoke_model(cot_prompt, max_tokens=600)
        print(cot_response)
        print()
        
        return {"direct": direct_response, "chain_of_thought": cot_response}
    
    def demonstrate_combined_techniques(self):
        """
        Demonstrate all principles combined in a single, powerful prompt.
        
        Shows how multiple techniques work together for optimal results.
        """
        print("=" * 80)
        print("🚀 COMBINED TECHNIQUES: ALL PRINCIPLES TOGETHER")
        print("=" * 80)
        print()
        
        combined_prompt = """You are an expert technical product manager with 10+ years of experience in software development and agile methodologies.

Your task: Create a comprehensive project risk assessment for a new mobile app development project.

Here are examples of good risk assessments:

Example 1:
Project: E-commerce Website
Key Risks:
- Technical: Legacy system integration (High probability, High impact)
- Timeline: Q4 holiday deadline pressure (Medium probability, High impact)
- Resource: Lead developer vacation in month 2 (High probability, Medium impact)

Example 2:
Project: Data Analytics Dashboard
Key Risks:
- Technical: Data quality issues (Medium probability, High impact)
- Business: Changing requirements from stakeholders (High probability, Medium impact)
- External: Third-party API reliability (Low probability, High impact)

Now, analyze this project step-by-step:

Project Details:
- Mobile app for food delivery
- Team: 1 iOS dev, 1 Android dev, 1 backend dev, 1 designer
- Timeline: 4 months
- Key features: GPS tracking, payment processing, real-time notifications
- Target: Launch before summer season

Please think through this systematically:
1. Identify technical risks
2. Assess timeline and resource risks
3. Consider external dependencies
4. Evaluate business/market risks
5. Prioritize risks by probability and impact

Provide your analysis in the same format as the examples, with clear reasoning for each risk assessment."""

        print("🎯 COMBINED PROMPT (All Principles):")
        print("- ✅ Persona: Expert technical product manager")
        print("- ✅ Clarity: Specific task and format requirements")
        print("- ✅ Examples: Two concrete risk assessment examples")
        print("- ✅ Chain of Thought: Step-by-step analysis requested")
        print()
        print(f"Full Prompt:\n'{combined_prompt}'")
        print()
        print("Response:")
        combined_response = self.invoke_model(combined_prompt, temperature=0.2, max_tokens=800)
        print(combined_response)
        print()
        
        return combined_response
    
    def run_complete_demo(self):
        """
        Run the complete prompt engineering demonstration.
        
        Executes all principle demonstrations and provides a summary.
        """
        print("🔥 AWS AI ENGINEERING COURSE")
        print("Chapter 3: Model Adaptation - Prompt Engineering Principles")
        print("=" * 80)
        print(f"Using Model: {self.model_id}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        results = {}
        
        # Run all demonstrations
        print("🚀 Starting Prompt Engineering Demonstrations...")
        print()
        
        results['clarity'] = self.demonstrate_clarity_specificity()
        time.sleep(1)  # Brief pause between demonstrations
        
        results['persona'] = self.demonstrate_persona_assignment()
        time.sleep(1)
        
        results['few_shot'] = self.demonstrate_few_shot_learning()
        time.sleep(1)
        
        results['chain_of_thought'] = self.demonstrate_chain_of_thought()
        time.sleep(1)
        
        results['combined'] = self.demonstrate_combined_techniques()
        
        # Summary
        print("=" * 80)
        print("📊 DEMONSTRATION SUMMARY")
        print("=" * 80)
        print()
        print("Key Takeaways:")
        print("1. 🎯 Clarity & Specificity: Specific prompts yield better, more relevant responses")
        print("2. 🎭 Persona Assignment: Different personas produce different tones and styles")
        print("3. 📚 Few-Shot Learning: Examples dramatically improve task performance")
        print("4. 🔗 Chain of Thought: Step-by-step reasoning improves complex problem solving")
        print("5. 🚀 Combined Techniques: Multiple principles together maximize effectiveness")
        print()
        print("💡 Best Practice: Always consider your specific use case and combine techniques")
        print("   appropriately for optimal results with AWS Bedrock models.")
        print()
        
        return results


def main():
    """
    Main function to run the prompt engineering demonstration.
    """
    try:
        demo = PromptEngineeringDemo()
        results = demo.run_complete_demo()
        
        print("✅ Demonstration completed successfully!")
        print()
        print("📝 To explore further:")
        print("- Modify the prompts and observe how responses change")
        print("- Try different temperature settings for varied creativity")
        print("- Experiment with different personas for your use cases")
        print("- Apply these principles to your own AI applications")
        
    except Exception as e:
        print(f"❌ Error running demonstration: {str(e)}")
        print()
        print("🔧 Troubleshooting:")
        print("- Ensure AWS credentials are configured")
        print("- Check AWS Bedrock model access permissions")
        print("- Verify the model ID is available in your region")


if __name__ == "__main__":
    main()

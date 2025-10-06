#!/usr/bin/env python3
"""
Bedrock Requirements Analyzer

This module integrates with AWS Bedrock LLM to analyze business requirements
for completeness and provide feedback and suggestions.
"""

import json
import logging
from typing import Dict, Any, List, Optional
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

logger = logging.getLogger(__name__)


class BedrockRequirementsAnalyzer:
    """
    Analyzes business requirements using AWS Bedrock LLM models.
    
    Provides completeness analysis, feedback, and improvement suggestions
    for business requirements converted from markdown to JSON.
    """
    
    def __init__(self, region: str = 'us-east-1', model_id: str = 'amazon.nova-lite-v1:0'):
        """
        Initialize the Bedrock analyzer.
        
        Args:
            region: AWS region for Bedrock service
            model_id: Bedrock model ID to use for analysis
        """
        self.region = region
        self.model_id = model_id
        
        try:
            self.bedrock_runtime = boto3.client('bedrock-runtime', region_name=region)
            self.bedrock = boto3.client('bedrock', region_name=region)
            logger.info(f"Initialized Bedrock analyzer with model: {model_id}")
        except NoCredentialsError:
            logger.error("AWS credentials not configured")
            raise
        except Exception as e:
            logger.error(f"Error initializing Bedrock client: {str(e)}")
            raise
    
    def analyze_requirements(self, requirements_json: Dict[str, Any], 
                           analysis_type: str = 'comprehensive') -> Dict[str, Any]:
        """
        Analyze business requirements for completeness and quality.
        
        Args:
            requirements_json: JSON data containing business requirements
            analysis_type: Type of analysis ('comprehensive', 'completeness', 'quality')
            
        Returns:
            Analysis results with feedback and suggestions
        """
        try:
            logger.info(f"Starting {analysis_type} analysis of requirements")
            
            # Create analysis prompt based on type
            prompt = self._create_analysis_prompt(requirements_json, analysis_type)
            
            # Get analysis from Bedrock
            analysis_response = self._invoke_bedrock_model(prompt)
            
            # Parse and structure the response
            structured_analysis = self._parse_analysis_response(analysis_response, analysis_type)
            
            return {
                'success': True,
                'analysis_type': analysis_type,
                'model_used': self.model_id,
                'analysis': structured_analysis,
                'raw_response': analysis_response
            }
            
        except Exception as e:
            logger.error(f"Error analyzing requirements: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'analysis_type': analysis_type
            }
    
    def check_completeness(self, requirements_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check requirements for completeness.
        
        Args:
            requirements_json: JSON data containing business requirements
            
        Returns:
            Completeness analysis results
        """
        return self.analyze_requirements(requirements_json, 'completeness')
    
    def suggest_improvements(self, requirements_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Suggest improvements for business requirements.
        
        Args:
            requirements_json: JSON data containing business requirements
            
        Returns:
            Improvement suggestions
        """
        return self.analyze_requirements(requirements_json, 'improvements')
    
    def validate_structure(self, requirements_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate the structure and organization of requirements.
        
        Args:
            requirements_json: JSON data containing business requirements
            
        Returns:
            Structure validation results
        """
        return self.analyze_requirements(requirements_json, 'structure')
    
    def _create_analysis_prompt(self, requirements_json: Dict[str, Any], 
                               analysis_type: str) -> str:
        """
        Create the appropriate prompt for the analysis type.
        
        Args:
            requirements_json: JSON data to analyze
            analysis_type: Type of analysis to perform
            
        Returns:
            Formatted prompt string
        """
        # Convert JSON to a readable format for the prompt
        requirements_text = json.dumps(requirements_json, indent=2)[:4000]  # Limit size
        
        base_prompt = f"""
You are an expert business analyst reviewing business requirements. 
Analyze the following requirements data that was converted from markdown format:

{requirements_text}

"""
        
        if analysis_type == 'comprehensive':
            prompt = base_prompt + """
Provide a comprehensive analysis covering:
1. Completeness assessment
2. Quality evaluation
3. Structure review
4. Missing elements identification
5. Improvement recommendations

Please respond with valid JSON in the following format:
{
    "completeness_score": <number 0-100>,
    "quality_score": <number 0-100>,
    "structure_score": <number 0-100>,
    "missing_elements": ["element1", "element2"],
    "strengths": ["strength1", "strength2"],
    "weaknesses": ["weakness1", "weakness2"],
    "recommendations": ["recommendation1", "recommendation2"],
    "critical_gaps": ["gap1", "gap2"],
    "overall_assessment": "text description"
}
"""
        
        elif analysis_type == 'completeness':
            prompt = base_prompt + """
Focus specifically on completeness. Identify:
1. What key business requirement elements are present
2. What essential elements are missing
3. Areas that need more detail
4. Questions that should be addressed

Please respond with valid JSON in the following format:
{
    "completeness_score": <number 0-100>,
    "present_elements": ["element1", "element2"],
    "missing_elements": ["element1", "element2"],
    "incomplete_sections": ["section1", "section2"],
    "questions_to_address": ["question1", "question2"],
    "recommendations": ["rec1", "rec2"]
}
"""
        
        elif analysis_type == 'improvements':
            prompt = base_prompt + """
Focus on improvement suggestions:
1. How to enhance clarity and specificity
2. Additional details that would be valuable
3. Better organization or structure
4. Industry best practices to incorporate

Please respond with valid JSON in the following format:
{
    "priority_improvements": ["improvement1", "improvement2"],
    "clarity_enhancements": ["enhancement1", "enhancement2"],
    "additional_details_needed": ["detail1", "detail2"],
    "structural_improvements": ["structure1", "structure2"],
    "best_practices": ["practice1", "practice2"],
    "quick_wins": ["win1", "win2"]
}
"""
        
        elif analysis_type == 'structure':
            prompt = base_prompt + """
Focus on structural and organizational aspects:
1. Logical flow and organization
2. Hierarchy and categorization
3. Consistency in format and style
4. Accessibility and readability

Please respond with valid JSON in the following format:
{
    "structure_score": <number 0-100>,
    "organization_quality": "excellent/good/fair/poor",
    "hierarchy_issues": ["issue1", "issue2"],
    "consistency_problems": ["problem1", "problem2"],
    "readability_score": <number 0-100>,
    "structural_recommendations": ["rec1", "rec2"]
}
"""
        
        return prompt
    
    def _invoke_bedrock_model(self, prompt: str, max_tokens: int = 1000) -> str:
        """
        Invoke the Bedrock model with the given prompt.
        
        Args:
            prompt: The prompt to send to the model
            max_tokens: Maximum tokens to generate
            
        Returns:
            Model response text
        """
        try:
            if "nova-lite" in self.model_id:
                request_body = {
                    "schemaVersion": "messages-v1",
                    "messages": [
                        {
                            "role": "user",
                            "content": [{"text": prompt}]
                        }
                    ],
                    "inferenceConfig": {
                        "max_new_tokens": max_tokens,
                        "temperature": 0.1,
                        "top_p": 0.9
                    }
                }
            elif "claude" in self.model_id:
                request_body = {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": max_tokens,
                    "temperature": 0.1,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                }
            else:
                # Generic format
                request_body = {
                    "prompt": prompt,
                    "max_tokens": max_tokens,
                    "temperature": 0.1
                }
            
            response = self.bedrock_runtime.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body),
                contentType='application/json',
                accept='application/json'
            )
            
            response_body = json.loads(response['body'].read())
            
            # Extract text based on model type
            if "nova-lite" in self.model_id:
                return response_body['output']['message']['content'][0]['text']
            elif "claude" in self.model_id:
                return response_body['content'][0]['text']
            else:
                # Try common response formats
                if 'completion' in response_body:
                    return response_body['completion']
                elif 'outputs' in response_body:
                    return response_body['outputs'][0]['text']
                else:
                    return str(response_body)
                    
        except ClientError as e:
            logger.error(f"Bedrock API error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error invoking Bedrock model: {str(e)}")
            raise
    
    def _parse_analysis_response(self, response: str, analysis_type: str) -> Dict[str, Any]:
        """
        Parse and validate the analysis response from Bedrock.
        
        Args:
            response: Raw response from Bedrock
            analysis_type: Type of analysis performed
            
        Returns:
            Parsed and validated analysis data
        """
        try:
            # Clean the response text
            cleaned_response = response.strip()
            
            # Remove markdown code blocks if present
            if cleaned_response.startswith('```json'):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.startswith('```'):
                cleaned_response = cleaned_response[3:]
            if cleaned_response.endswith('```'):
                cleaned_response = cleaned_response[:-3]
            
            cleaned_response = cleaned_response.strip()
            
            # Find JSON content
            start_idx = cleaned_response.find('{')
            end_idx = cleaned_response.rfind('}')
            
            if start_idx != -1 and end_idx != -1:
                json_str = cleaned_response[start_idx:end_idx + 1]
                parsed_data = json.loads(json_str)
                
                # Validate required fields based on analysis type
                validated_data = self._validate_analysis_data(parsed_data, analysis_type)
                return validated_data
            else:
                # Fallback: create structured response from text
                return self._create_fallback_analysis(response, analysis_type)
                
        except json.JSONDecodeError as e:
            logger.warning(f"Could not parse JSON response: {str(e)}")
            return self._create_fallback_analysis(response, analysis_type)
        except Exception as e:
            logger.error(f"Error parsing analysis response: {str(e)}")
            return self._create_fallback_analysis(response, analysis_type)
    
    def _validate_analysis_data(self, data: Dict[str, Any], analysis_type: str) -> Dict[str, Any]:
        """
        Validate and ensure required fields are present in analysis data.
        
        Args:
            data: Parsed analysis data
            analysis_type: Type of analysis
            
        Returns:
            Validated analysis data
        """
        # Add default values for missing fields based on analysis type
        if analysis_type == 'comprehensive':
            defaults = {
                'completeness_score': 0,
                'quality_score': 0,
                'structure_score': 0,
                'missing_elements': [],
                'strengths': [],
                'weaknesses': [],
                'recommendations': [],
                'critical_gaps': [],
                'overall_assessment': 'Analysis completed'
            }
        elif analysis_type == 'completeness':
            defaults = {
                'completeness_score': 0,
                'present_elements': [],
                'missing_elements': [],
                'incomplete_sections': [],
                'questions_to_address': [],
                'recommendations': []
            }
        elif analysis_type == 'improvements':
            defaults = {
                'priority_improvements': [],
                'clarity_enhancements': [],
                'additional_details_needed': [],
                'structural_improvements': [],
                'best_practices': [],
                'quick_wins': []
            }
        elif analysis_type == 'structure':
            defaults = {
                'structure_score': 0,
                'organization_quality': 'unknown',
                'hierarchy_issues': [],
                'consistency_problems': [],
                'readability_score': 0,
                'structural_recommendations': []
            }
        else:
            defaults = {}
        
        # Merge with defaults
        for key, default_value in defaults.items():
            if key not in data:
                data[key] = default_value
        
        return data
    
    def _create_fallback_analysis(self, response: str, analysis_type: str) -> Dict[str, Any]:
        """
        Create a fallback analysis when JSON parsing fails.
        
        Args:
            response: Raw response text
            analysis_type: Type of analysis
            
        Returns:
            Fallback analysis structure
        """
        return {
            'analysis_type': analysis_type,
            'raw_analysis': response,
            'parsed_successfully': False,
            'summary': 'Analysis completed but response format was non-standard',
            'recommendations': ['Review the raw analysis for detailed insights']
        }


# Convenience functions
def analyze_requirements_json(requirements_json: Dict[str, Any], 
                             region: str = 'us-east-1',
                             model_id: str = 'amazon.nova-lite-v1:0') -> Dict[str, Any]:
    """
    Convenience function to analyze requirements JSON.
    
    Args:
        requirements_json: JSON data to analyze
        region: AWS region
        model_id: Bedrock model ID
        
    Returns:
        Analysis results
    """
    analyzer = BedrockRequirementsAnalyzer(region=region, model_id=model_id)
    return analyzer.analyze_requirements(requirements_json)


if __name__ == "__main__":
    # Simple test when run directly
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python bedrock_analyzer.py <json_file>")
        sys.exit(1)
    
    json_file = sys.argv[1]
    
    try:
        with open(json_file, 'r') as f:
            requirements_json = json.load(f)
        
        result = analyze_requirements_json(requirements_json)
        
        if result['success']:
            print("✅ Analysis successful!")
            print(json.dumps(result['analysis'], indent=2))
        else:
            print(f"❌ Analysis failed: {result['error']}")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)
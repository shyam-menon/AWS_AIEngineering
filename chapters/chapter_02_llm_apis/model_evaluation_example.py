#!/usr/bin/env python3
"""
Comprehensive Model Evaluation for AWS Bedrock LLMs

This example demonstrates various evaluation techniques for Large Language Models,
covering both traditional ML metrics and LLM-specific evaluation methods.

Learning Objectives:
1. Understand different types of evaluation metrics
2. Implement practical evaluation for LLM applications
3. Compare model performance across different tasks
4. Use AWS Bedrock's evaluation capabilities
5. Create custom evaluation frameworks

Author: AWS AI Engineering Course
Date: August 2025
"""

import boto3
import json
import time
import statistics
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import re
import math


@dataclass
class EvaluationResult:
    """Represents the result of a model evaluation."""
    model_id: str
    task_type: str
    prompt: str
    response: str
    expected_answer: Optional[str]
    metrics: Dict[str, float]
    response_time: float
    cost: float
    timestamp: datetime


class LLMEvaluator:
    """
    Comprehensive evaluation framework for LLM applications.
    
    Supports multiple evaluation approaches:
    - Task-based evaluation with ground truth
    - Quality assessment without ground truth
    - Performance metrics (cost, latency)
    - LLM-specific metrics (coherence, relevance)
    """
    
    def __init__(self, region_name: str = 'us-east-1'):
        """Initialize the evaluator with AWS Bedrock client."""
        self.bedrock_runtime = boto3.client('bedrock-runtime', region_name=region_name)
        self.bedrock = boto3.client('bedrock', region_name=region_name)
        
        # Pricing per 1K tokens (as of August 2025)
        self.pricing = {
            'amazon.nova-lite-v1:0': {'input': 0.06, 'output': 0.24},
            'anthropic.claude-3-5-sonnet-20241022-v2:0': {'input': 3.00, 'output': 15.00},
            'anthropic.claude-3-5-haiku-20241022-v1:0': {'input': 0.25, 'output': 1.25}
        }
        
        self.evaluation_results: List[EvaluationResult] = []
        
        print("🔍 LLM Evaluator initialized")
    
    def _estimate_tokens(self, text: str) -> int:
        """Rough estimation of token count."""
        return len(text) // 4  # Approximate: 1 token ≈ 4 characters
    
    def _calculate_cost(self, model_id: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate the cost of a request."""
        if model_id not in self.pricing:
            return 0.0
        
        pricing = self.pricing[model_id]
        input_cost = (input_tokens / 1000) * pricing['input']
        output_cost = (output_tokens / 1000) * pricing['output']
        return input_cost + output_cost
    
    def invoke_model(self, prompt: str, model_id: str = "amazon.nova-lite-v1:0", **kwargs) -> Dict[str, Any]:
        """
        Invoke a Bedrock model and measure performance.
        
        Returns response with timing and cost information.
        """
        start_time = time.time()
        
        try:
            # Prepare request based on model
            if 'nova' in model_id.lower():
                request_body = {
                    "schemaVersion": "messages-v1",
                    "messages": [{"role": "user", "content": [{"text": prompt}]}],
                    "inferenceConfig": {
                        "maxTokens": kwargs.get('max_tokens', 1000),
                        "temperature": kwargs.get('temperature', 0.7),
                        "topP": kwargs.get('top_p', 0.9)
                    }
                }
            else:
                # For Claude models
                request_body = {
                    "anthropic_version": "bedrock-2023-05-31",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": kwargs.get('max_tokens', 1000),
                    "temperature": kwargs.get('temperature', 0.7)
                }
            
            # Make API call
            response = self.bedrock_runtime.invoke_model(
                modelId=model_id,
                body=json.dumps(request_body),
                contentType='application/json'
            )
            
            response_time = time.time() - start_time
            
            # Parse response
            response_body = json.loads(response['body'].read())
            
            if 'nova' in model_id.lower():
                content = response_body['output']['message']['content'][0]['text']
                usage = response_body.get('usage', {})
                input_tokens = usage.get('inputTokens', 0)
                output_tokens = usage.get('outputTokens', 0)
            else:
                content = response_body['content'][0]['text']
                usage = response_body.get('usage', {})
                input_tokens = usage.get('input_tokens', 0)
                output_tokens = usage.get('output_tokens', 0)
            
            # Calculate cost
            cost = self._calculate_cost(model_id, input_tokens, output_tokens)
            
            return {
                'response': content,
                'response_time': response_time,
                'cost': cost,
                'input_tokens': input_tokens,
                'output_tokens': output_tokens,
                'success': True
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'response_time': time.time() - start_time,
                'cost': 0.0,
                'success': False
            }
    
    def evaluate_accuracy(self, response: str, expected_answer: str, task_type: str = "general") -> Dict[str, float]:
        """
        Evaluate accuracy based on expected answer.
        
        Different strategies for different task types:
        - exact_match: Exact string matching
        - contains: Expected answer is contained in response
        - semantic: Basic semantic similarity
        """
        metrics = {}
        
        # Clean and normalize strings
        response_clean = response.strip().lower()
        expected_clean = expected_answer.strip().lower()
        
        # Exact match accuracy
        metrics['exact_match'] = 1.0 if response_clean == expected_clean else 0.0
        
        # Contains accuracy (for factual questions)
        metrics['contains_answer'] = 1.0 if expected_clean in response_clean else 0.0
        
        # Token overlap (simple Jaccard similarity)
        response_tokens = set(response_clean.split())
        expected_tokens = set(expected_clean.split())
        
        if len(response_tokens) > 0 and len(expected_tokens) > 0:
            intersection = len(response_tokens.intersection(expected_tokens))
            union = len(response_tokens.union(expected_tokens))
            metrics['token_overlap'] = intersection / union if union > 0 else 0.0
        else:
            metrics['token_overlap'] = 0.0
        
        # Length similarity (penalize very short or very long responses)
        len_ratio = min(len(response), len(expected_answer)) / max(len(response), len(expected_answer))
        metrics['length_similarity'] = len_ratio
        
        # Overall accuracy score (weighted combination)
        metrics['overall_accuracy'] = (
            metrics['contains_answer'] * 0.4 +
            metrics['token_overlap'] * 0.3 +
            metrics['length_similarity'] * 0.3
        )
        
        return metrics
    
    def evaluate_quality_without_ground_truth(self, prompt: str, response: str) -> Dict[str, float]:
        """
        Evaluate response quality without ground truth answers.
        
        Uses heuristic measures to assess:
        - Completeness
        - Coherence
        - Relevance
        - Helpfulness
        """
        metrics = {}
        
        # Response length (indicates completeness)
        response_length = len(response)
        metrics['response_length'] = response_length
        
        # Completeness score based on length (normalized)
        if response_length < 50:
            metrics['completeness'] = 0.2  # Very short, likely incomplete
        elif response_length < 200:
            metrics['completeness'] = 0.6  # Moderate length
        elif response_length < 500:
            metrics['completeness'] = 1.0  # Good length
        else:
            metrics['completeness'] = 0.8  # Very long, might be verbose
        
        # Coherence (basic checks)
        sentences = response.split('.')
        metrics['sentence_count'] = len(sentences)
        
        # Check for repetition (indicates poor coherence)
        words = response.lower().split()
        unique_words = len(set(words))
        total_words = len(words)
        metrics['word_diversity'] = unique_words / total_words if total_words > 0 else 0.0
        
        # Relevance to prompt (keyword overlap)
        prompt_words = set(prompt.lower().split())
        response_words = set(response.lower().split())
        common_words = prompt_words.intersection(response_words)
        metrics['prompt_relevance'] = len(common_words) / len(prompt_words) if len(prompt_words) > 0 else 0.0
        
        # Structure quality (presence of punctuation, capitalization)
        has_proper_capitalization = any(c.isupper() for c in response)
        has_punctuation = any(p in response for p in '.!?')
        metrics['structural_quality'] = (
            (1.0 if has_proper_capitalization else 0.0) +
            (1.0 if has_punctuation else 0.0)
        ) / 2.0
        
        # Overall quality score
        metrics['overall_quality'] = (
            metrics['completeness'] * 0.3 +
            metrics['word_diversity'] * 0.2 +
            metrics['prompt_relevance'] * 0.3 +
            metrics['structural_quality'] * 0.2
        )
        
        return metrics
    
    def calculate_bleu_score(self, candidate: str, reference: str) -> float:
        """
        Calculate a simplified BLEU score.
        
        Note: This is a simplified version for educational purposes.
        For production use, consider using libraries like nltk or sacrebleu.
        """
        # Tokenize
        candidate_tokens = candidate.lower().split()
        reference_tokens = reference.lower().split()
        
        if len(candidate_tokens) == 0:
            return 0.0
        
        # Calculate precision for n-grams (simplified, using only 1-grams and 2-grams)
        precisions = []
        
        for n in [1, 2]:
            # Generate n-grams
            candidate_ngrams = [tuple(candidate_tokens[i:i+n]) for i in range(len(candidate_tokens)-n+1)]
            reference_ngrams = [tuple(reference_tokens[i:i+n]) for i in range(len(reference_tokens)-n+1)]
            
            if len(candidate_ngrams) == 0:
                precisions.append(0.0)
                continue
            
            # Count matches
            matches = 0
            for ngram in candidate_ngrams:
                if ngram in reference_ngrams:
                    matches += 1
            
            precision = matches / len(candidate_ngrams)
            precisions.append(precision)
        
        # Brevity penalty
        candidate_length = len(candidate_tokens)
        reference_length = len(reference_tokens)
        
        if candidate_length > reference_length:
            bp = 1.0
        else:
            bp = math.exp(1 - reference_length / candidate_length) if candidate_length > 0 else 0.0
        
        # Geometric mean of precisions
        if all(p > 0 for p in precisions):
            geometric_mean = math.exp(sum(math.log(p) for p in precisions) / len(precisions))
        else:
            geometric_mean = 0.0
        
        bleu = bp * geometric_mean
        return bleu
    
    def calculate_rouge_score(self, candidate: str, reference: str) -> Dict[str, float]:
        """
        Calculate simplified ROUGE scores (ROUGE-1 and ROUGE-L).
        
        Note: Simplified version for educational purposes.
        """
        candidate_tokens = candidate.lower().split()
        reference_tokens = reference.lower().split()
        
        # ROUGE-1 (unigram overlap)
        candidate_unigrams = set(candidate_tokens)
        reference_unigrams = set(reference_tokens)
        
        overlap = len(candidate_unigrams.intersection(reference_unigrams))
        
        rouge_1_precision = overlap / len(candidate_unigrams) if len(candidate_unigrams) > 0 else 0.0
        rouge_1_recall = overlap / len(reference_unigrams) if len(reference_unigrams) > 0 else 0.0
        rouge_1_f1 = (2 * rouge_1_precision * rouge_1_recall) / (rouge_1_precision + rouge_1_recall) if (rouge_1_precision + rouge_1_recall) > 0 else 0.0
        
        # ROUGE-L (Longest Common Subsequence - simplified)
        # For simplicity, we'll use sentence-level comparison
        candidate_sentences = candidate.split('.')
        reference_sentences = reference.split('.')
        
        max_lcs = 0
        for c_sent in candidate_sentences:
            for r_sent in reference_sentences:
                # Simple word overlap as proxy for LCS
                c_words = set(c_sent.lower().split())
                r_words = set(r_sent.lower().split())
                lcs = len(c_words.intersection(r_words))
                max_lcs = max(max_lcs, lcs)
        
        rouge_l = max_lcs / max(len(candidate_tokens), len(reference_tokens)) if max(len(candidate_tokens), len(reference_tokens)) > 0 else 0.0
        
        return {
            'rouge_1_precision': rouge_1_precision,
            'rouge_1_recall': rouge_1_recall,
            'rouge_1_f1': rouge_1_f1,
            'rouge_l': rouge_l
        }
    
    def evaluate_single_prompt(self, prompt: str, expected_answer: str = None, 
                              model_id: str = "amazon.nova-lite-v1:0", 
                              task_type: str = "general", **kwargs) -> EvaluationResult:
        """
        Evaluate a single prompt comprehensively.
        
        Args:
            prompt: Input prompt
            expected_answer: Ground truth answer (optional)
            model_id: Bedrock model to evaluate
            task_type: Type of task for evaluation strategy
            **kwargs: Additional model parameters
        """
        print(f"🔍 Evaluating: {prompt[:50]}...")
        
        # Get model response
        result = self.invoke_model(prompt, model_id, **kwargs)
        
        if not result['success']:
            print(f"❌ Model invocation failed: {result['error']}")
            return None
        
        response = result['response']
        
        # Calculate all metrics
        metrics = {}
        
        # Performance metrics
        metrics['response_time'] = result['response_time']
        metrics['cost'] = result['cost']
        metrics['input_tokens'] = result['input_tokens']
        metrics['output_tokens'] = result['output_tokens']
        
        # Quality metrics without ground truth
        quality_metrics = self.evaluate_quality_without_ground_truth(prompt, response)
        metrics.update(quality_metrics)
        
        # Accuracy metrics (if ground truth available)
        if expected_answer:
            accuracy_metrics = self.evaluate_accuracy(response, expected_answer, task_type)
            metrics.update(accuracy_metrics)
            
            # LLM-specific metrics
            metrics['bleu_score'] = self.calculate_bleu_score(response, expected_answer)
            rouge_scores = self.calculate_rouge_score(response, expected_answer)
            metrics.update(rouge_scores)
        
        # Create evaluation result
        eval_result = EvaluationResult(
            model_id=model_id,
            task_type=task_type,
            prompt=prompt,
            response=response,
            expected_answer=expected_answer,
            metrics=metrics,
            response_time=result['response_time'],
            cost=result['cost'],
            timestamp=datetime.now()
        )
        
        self.evaluation_results.append(eval_result)
        
        print(f"✅ Evaluation complete - Quality: {metrics.get('overall_quality', 0):.2f}")
        
        return eval_result
    
    def compare_models(self, prompts: List[Dict[str, str]], 
                      models: List[str] = None) -> Dict[str, Any]:
        """
        Compare multiple models on the same set of prompts.
        
        Args:
            prompts: List of {"prompt": str, "expected": str} dicts
            models: List of model IDs to compare
        """
        if models is None:
            models = ["amazon.nova-lite-v1:0", "anthropic.claude-3-5-haiku-20241022-v1:0"]
        
        print(f"🔀 Comparing {len(models)} models on {len(prompts)} prompts...")
        
        comparison_results = {model: [] for model in models}
        
        for i, prompt_data in enumerate(prompts):
            prompt = prompt_data['prompt']
            expected = prompt_data.get('expected')
            
            print(f"\n--- Prompt {i+1}/{len(prompts)}: {prompt[:40]}... ---")
            
            for model in models:
                result = self.evaluate_single_prompt(
                    prompt=prompt,
                    expected_answer=expected,
                    model_id=model,
                    task_type=prompt_data.get('task_type', 'general')
                )
                
                if result:
                    comparison_results[model].append(result)
        
        # Calculate aggregate statistics
        aggregated_results = {}
        
        for model in models:
            results = comparison_results[model]
            if not results:
                continue
            
            # Calculate averages
            avg_metrics = {}
            metric_names = results[0].metrics.keys() if results else []
            
            for metric in metric_names:
                values = [r.metrics[metric] for r in results if metric in r.metrics]
                if values:
                    avg_metrics[f'avg_{metric}'] = statistics.mean(values)
                    avg_metrics[f'std_{metric}'] = statistics.stdev(values) if len(values) > 1 else 0.0
            
            aggregated_results[model] = {
                'total_evaluations': len(results),
                'total_cost': sum(r.cost for r in results),
                'total_time': sum(r.response_time for r in results),
                'avg_metrics': avg_metrics
            }
        
        return {
            'individual_results': comparison_results,
            'aggregated_results': aggregated_results,
            'comparison_summary': self._generate_comparison_summary(aggregated_results)
        }
    
    def _generate_comparison_summary(self, aggregated_results: Dict[str, Any]) -> Dict[str, str]:
        """Generate a summary comparing model performance."""
        summary = {}
        
        # Find best model for each metric
        metrics_to_compare = ['avg_overall_quality', 'avg_response_time', 'avg_cost', 'avg_overall_accuracy']
        
        for metric in metrics_to_compare:
            best_model = None
            best_value = None
            
            for model, results in aggregated_results.items():
                if metric in results['avg_metrics']:
                    value = results['avg_metrics'][metric]
                    
                    # For cost and time, lower is better
                    if 'cost' in metric or 'time' in metric:
                        if best_value is None or value < best_value:
                            best_value = value
                            best_model = model
                    else:
                        # For quality and accuracy, higher is better
                        if best_value is None or value > best_value:
                            best_value = value
                            best_model = model
            
            if best_model:
                summary[metric] = f"{best_model} ({best_value:.3f})"
        
        return summary
    
    def print_evaluation_summary(self, result: EvaluationResult):
        """Print a formatted summary of an evaluation result."""
        print(f"\n{'='*80}")
        print(f"📊 EVALUATION SUMMARY - {result.model_id}")
        print(f"{'='*80}")
        
        print(f"🎯 Task Type: {result.task_type}")
        print(f"📝 Prompt: {result.prompt[:100]}...")
        print(f"🤖 Response: {result.response[:200]}...")
        
        if result.expected_answer:
            print(f"✅ Expected: {result.expected_answer[:100]}...")
        
        print(f"\n📈 PERFORMANCE METRICS:")
        print(f"   Response Time: {result.response_time:.3f}s")
        print(f"   Cost: ${result.cost:.4f}")
        print(f"   Input Tokens: {result.metrics.get('input_tokens', 0)}")
        print(f"   Output Tokens: {result.metrics.get('output_tokens', 0)}")
        
        print(f"\n🎯 QUALITY METRICS:")
        print(f"   Overall Quality: {result.metrics.get('overall_quality', 0):.3f}")
        print(f"   Completeness: {result.metrics.get('completeness', 0):.3f}")
        print(f"   Prompt Relevance: {result.metrics.get('prompt_relevance', 0):.3f}")
        print(f"   Word Diversity: {result.metrics.get('word_diversity', 0):.3f}")
        
        if result.expected_answer:
            print(f"\n✅ ACCURACY METRICS:")
            print(f"   Overall Accuracy: {result.metrics.get('overall_accuracy', 0):.3f}")
            print(f"   Contains Answer: {result.metrics.get('contains_answer', 0):.3f}")
            print(f"   Token Overlap: {result.metrics.get('token_overlap', 0):.3f}")
            print(f"   BLEU Score: {result.metrics.get('bleu_score', 0):.3f}")
            print(f"   ROUGE-1 F1: {result.metrics.get('rouge_1_f1', 0):.3f}")
        
        print(f"{'='*80}\n")
    
    def print_comparison_summary(self, comparison_results: Dict[str, Any]):
        """Print a formatted comparison summary."""
        print(f"\n{'='*100}")
        print(f"🔀 MODEL COMPARISON SUMMARY")
        print(f"{'='*100}")
        
        aggregated = comparison_results['aggregated_results']
        summary = comparison_results['comparison_summary']
        
        # Print aggregated statistics
        for model, results in aggregated.items():
            print(f"\n🤖 {model}:")
            print(f"   Total Evaluations: {results['total_evaluations']}")
            print(f"   Total Cost: ${results['total_cost']:.4f}")
            print(f"   Total Time: {results['total_time']:.2f}s")
            print(f"   Avg Quality: {results['avg_metrics'].get('avg_overall_quality', 0):.3f}")
            print(f"   Avg Response Time: {results['avg_metrics'].get('avg_response_time', 0):.3f}s")
            print(f"   Avg Cost per Query: ${results['avg_metrics'].get('avg_cost', 0):.4f}")
            
            if 'avg_overall_accuracy' in results['avg_metrics']:
                print(f"   Avg Accuracy: {results['avg_metrics']['avg_overall_accuracy']:.3f}")
        
        # Print best performers
        print(f"\n🏆 BEST PERFORMERS:")
        for metric, winner in summary.items():
            metric_name = metric.replace('avg_', '').replace('_', ' ').title()
            print(f"   {metric_name}: {winner}")
        
        print(f"{'='*100}\n")


def demo_basic_evaluation():
    """Demonstrate basic model evaluation."""
    print("🎓 BASIC MODEL EVALUATION DEMO")
    print("="*60)
    
    evaluator = LLMEvaluator()
    
    # Test cases with expected answers
    test_cases = [
        {
            "prompt": "What is the capital of France?",
            "expected": "Paris",
            "task_type": "factual"
        },
        {
            "prompt": "Explain what machine learning is in simple terms.",
            "expected": "Machine learning is a type of artificial intelligence where computers learn to make predictions or decisions by finding patterns in data, without being explicitly programmed for each specific task.",
            "task_type": "explanation"
        },
        {
            "prompt": "Write a haiku about technology.",
            "expected": "Circuits pulse with life,\nData flows through silicon veins,\nFuture born in code.",
            "task_type": "creative"
        }
    ]
    
    print(f"Testing {len(test_cases)} examples with Nova Lite...\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"=== Test Case {i}: {test_case['task_type'].title()} Task ===")
        
        result = evaluator.evaluate_single_prompt(
            prompt=test_case['prompt'],
            expected_answer=test_case['expected'],
            model_id="amazon.nova-lite-v1:0",
            task_type=test_case['task_type']
        )
        
        if result:
            evaluator.print_evaluation_summary(result)


def demo_model_comparison():
    """Demonstrate model comparison."""
    print("🔀 MODEL COMPARISON DEMO")
    print("="*60)
    
    evaluator = LLMEvaluator()
    
    # Test prompts for comparison
    comparison_prompts = [
        {
            "prompt": "Explain the concept of cloud computing in 2-3 sentences.",
            "expected": "Cloud computing is the delivery of computing services over the internet, allowing users to access servers, storage, databases, and software without owning physical hardware. It provides scalability, cost-effectiveness, and accessibility from anywhere with an internet connection.",
            "task_type": "explanation"
        },
        {
            "prompt": "What are the main benefits of using renewable energy?",
            "expected": "Renewable energy offers environmental benefits by reducing greenhouse gas emissions, economic advantages through job creation and energy independence, and sustainability by using naturally replenishing resources like solar and wind power.",
            "task_type": "factual"
        }
    ]
    
    # Compare Nova Lite with Claude Haiku
    models_to_compare = [
        "amazon.nova-lite-v1:0",
        "anthropic.claude-3-5-haiku-20241022-v1:0"
    ]
    
    print(f"Comparing {len(models_to_compare)} models on {len(comparison_prompts)} prompts...\n")
    
    comparison_results = evaluator.compare_models(
        prompts=comparison_prompts,
        models=models_to_compare
    )
    
    evaluator.print_comparison_summary(comparison_results)


def demo_quality_assessment():
    """Demonstrate quality assessment without ground truth."""
    print("📊 QUALITY ASSESSMENT DEMO (No Ground Truth)")
    print("="*60)
    
    evaluator = LLMEvaluator()
    
    # Test prompts without expected answers
    open_ended_prompts = [
        "What do you think about the future of artificial intelligence?",
        "Describe your ideal vacation destination.",
        "How would you solve traffic congestion in major cities?"
    ]
    
    print(f"Evaluating {len(open_ended_prompts)} open-ended prompts...\n")
    
    for i, prompt in enumerate(open_ended_prompts, 1):
        print(f"=== Open-ended Question {i} ===")
        
        result = evaluator.evaluate_single_prompt(
            prompt=prompt,
            expected_answer=None,  # No ground truth
            model_id="amazon.nova-lite-v1:0",
            task_type="open_ended"
        )
        
        if result:
            evaluator.print_evaluation_summary(result)


def main():
    """Main function with command-line interface."""
    import argparse
    
    parser = argparse.ArgumentParser(description='LLM Model Evaluation Demo')
    parser.add_argument('--basic', action='store_true', help='Run basic evaluation demo')
    parser.add_argument('--comparison', action='store_true', help='Run model comparison demo')
    parser.add_argument('--quality', action='store_true', help='Run quality assessment demo')
    parser.add_argument('--all', action='store_true', help='Run all demos')
    
    args = parser.parse_args()
    
    if args.all:
        demo_basic_evaluation()
        demo_model_comparison()
        demo_quality_assessment()
    elif args.basic:
        demo_basic_evaluation()
    elif args.comparison:
        demo_model_comparison()
    elif args.quality:
        demo_quality_assessment()
    else:
        print("Choose a demo mode:")
        print("  --basic         Basic evaluation with ground truth")
        print("  --comparison    Compare multiple models")
        print("  --quality       Quality assessment without ground truth")
        print("  --all           Run all demos")
        print("\nExample: python model_evaluation_example.py --basic")


if __name__ == "__main__":
    main()

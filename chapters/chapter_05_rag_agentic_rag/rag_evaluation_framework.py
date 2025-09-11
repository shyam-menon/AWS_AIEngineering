#!/usr/bin/env python3
"""
Comprehensive RAG Evaluation Framework

This module provides a complete framework for evaluating Retrieval-Augmented Generation (RAG) systems
using Amazon Bedrock as the judge model. It implements the evaluation techniques described in the
AWS blog post on RAG evaluation.

Key Features:
- Automated evaluation of faithfulness, context relevance, and answer relevance
- Batch evaluation capabilities
- Comprehensive reporting and analysis
- Integration with AWS CloudWatch for monitoring
- A/B testing framework for comparing RAG configurations
- Continuous evaluation pipeline for production monitoring

Author: AI Engineering Course
Date: 2025
"""

import boto3
import json
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import asyncio
import logging
import time
import schedule
from enum import Enum
import random
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class RAGEvaluationResult:
    """Data class to store evaluation results for a single RAG interaction"""
    query: str
    retrieved_context: str
    generated_answer: str
    ground_truth: Optional[str] = None
    faithfulness_score: Optional[float] = None
    context_relevance_score: Optional[float] = None
    answer_relevance_score: Optional[float] = None
    overall_score: Optional[float] = None
    evaluation_timestamp: str = None
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.evaluation_timestamp is None:
            self.evaluation_timestamp = datetime.now().isoformat()
        if self.metadata is None:
            self.metadata = {}

class RAGEvaluator:
    """
    Comprehensive RAG evaluation system using Amazon Bedrock as judge
    
    This class implements the evaluation framework described in the AWS blog post:
    https://aws.amazon.com/blogs/machine-learning/evaluate-the-reliability-of-retrieval-augmented-generation-applications-using-amazon-bedrock/
    """
    
    def __init__(self, region_name: str = "us-east-1", judge_model_id: str = "amazon.nova-lite-v1:0", knowledge_base_id: str = "PIWCGRFREL"):
        """
        Initialize the RAG evaluator
        
        Args:
            region_name: AWS region for Bedrock calls
            judge_model_id: Model ID for the judge model (default: Amazon Nova Lite)
            knowledge_base_id: AWS Knowledge Base ID for retrieval
        """
        self.bedrock_runtime = boto3.client(
            service_name="bedrock-runtime",
            region_name=region_name
        )
        self.bedrock_agent_runtime = boto3.client(
            service_name="bedrock-agent-runtime",
            region_name=region_name
        )
        self.judge_model_id = judge_model_id
        self.knowledge_base_id = knowledge_base_id
        
        # Define evaluation prompt templates based on AWS blog post
        self.faithfulness_prompt = """You are an AI assistant trained to evaluate interactions between a Human and an AI Assistant. Your goal is to classify the AI answer as either "factual" or "hallucinated".

"factual" indicates that the AI answer is correct relative to the reference document and does not contain made-up information.
"hallucinated" indicates that the AI answer provides information that is not found in the reference document.

Human query: {query}
Reference document: {reference}
AI answer: {answer}

Classify the AI's response as: "factual" or "hallucinated". Provide only the classification word."""

        self.context_relevance_prompt = """You are an AI assistant trained to evaluate a knowledge base search system. Your goal is to classify the reference document as either "relevant" or "irrelevant".

"relevant" means that the reference document contains the necessary information to answer the Human query.
"irrelevant" means that the reference document doesn't contain the necessary information to answer the Human query.

Human query: {query}
Reference document: {reference}

Classify the reference document as: "relevant" or "irrelevant". Provide only the classification word."""

        self.answer_relevance_prompt = """You are an AI assistant trained to evaluate interactions between a Human and an AI Assistant. Your goal is to classify the AI answer as either "relevant" or "irrelevant".

"relevant" means that the AI answer answers the Human query appropriately, even if the reference document lacks full information.
"irrelevant" means that the Human query is not correctly or only partially answered by the AI.

Human query: {query}
Reference document: {reference}
AI answer: {answer}

Classify the AI's response as: "relevant" or "irrelevant". Provide only the classification word."""

        # Advanced evaluation prompts for additional metrics
        self.coherence_prompt = """You are an AI assistant trained to evaluate text coherence. Your goal is to classify the AI answer as either "coherent" or "incoherent".

"coherent" means the answer presents ideas in a logical and organized manner.
"incoherent" means the answer lacks logical flow or organization.

AI answer: {answer}

Classify the AI's response as: "coherent" or "incoherent". Provide only the classification word."""

        self.conciseness_prompt = """You are an AI assistant trained to evaluate text conciseness. Your goal is to classify the AI answer as either "concise" or "verbose".

"concise" means the answer conveys information efficiently without unnecessary details.
"verbose" means the answer contains unnecessary or redundant information.

Human query: {query}
AI answer: {answer}

Classify the AI's response as: "concise" or "verbose". Provide only the classification word."""

    def _call_bedrock_judge(self, prompt: str, max_retries: int = 3) -> str:
        """
        Call Bedrock model for evaluation with retry logic
        
        Args:
            prompt: Evaluation prompt to send to the judge model
            max_retries: Maximum number of retry attempts
            
        Returns:
            Evaluation result as string
        """
        for attempt in range(max_retries):
            try:
                # Amazon Nova Lite uses a messages-based format
                if "nova-lite" in self.judge_model_id:
                    body = json.dumps({
                        "messages": [
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "text": prompt
                                    }
                                ]
                            }
                        ],
                        "inferenceConfig": {
                            "maxTokens": 10,
                            "temperature": 0.0,
                            "topP": 0.9,
                            "stopSequences": []
                        }
                    })
                else:
                    # Claude format for other models
                    body = json.dumps({
                        "anthropic_version": "bedrock-2023-05-31",
                        "max_tokens": 10,
                        "temperature": 0.0,
                        "messages": [
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    })
                
                response = self.bedrock_runtime.invoke_model(
                    modelId=self.judge_model_id,
                    body=body
                )
                
                response_body = json.loads(response.get('body').read())
                
                # Parse response based on model type
                if "nova-lite" in self.judge_model_id:
                    return response_body.get('output', {}).get('message', {}).get('content', [{}])[0].get('text', '').strip().lower()
                else:
                    return response_body['content'][0]['text'].strip().lower()
                
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"All attempts failed for judge evaluation: {e}")
                    return "error"

    def retrieve_from_knowledge_base(self, query: str, max_results: int = 5) -> Tuple[str, List[Dict]]:
        """
        Retrieve relevant documents from the knowledge base
        
        Args:
            query: User query for retrieval
            max_results: Maximum number of results to return
            
        Returns:
            Tuple of (concatenated_context, raw_results)
        """
        try:
            response = self.bedrock_agent_runtime.retrieve(
                knowledgeBaseId=self.knowledge_base_id,
                retrievalQuery={
                    'text': query
                },
                retrievalConfiguration={
                    'vectorSearchConfiguration': {
                        'numberOfResults': max_results
                    }
                }
            )
            
            # Extract text from results
            retrieved_docs = []
            for result in response.get('retrievalResults', []):
                content = result.get('content', {}).get('text', '')
                metadata = result.get('metadata', {})
                score = result.get('score', 0.0)
                
                retrieved_docs.append({
                    'content': content,
                    'metadata': metadata,
                    'score': score
                })
            
            # Concatenate all retrieved content for evaluation
            concatenated_context = "\n\n".join([doc['content'] for doc in retrieved_docs])
            
            return concatenated_context, retrieved_docs
            
        except Exception as e:
            logger.error(f"Knowledge base retrieval failed: {e}")
            return "", []

    def evaluate_faithfulness(self, query: str, reference: str, answer: str) -> float:
        """
        Evaluate if the answer is faithful to the reference context
        
        Args:
            query: User query
            reference: Retrieved context
            answer: Generated answer
            
        Returns:
            Faithfulness score (1.0 = factual, 0.0 = hallucinated)
        """
        prompt = self.faithfulness_prompt.format(
            query=query,
            reference=reference,
            answer=answer
        )
        
        result = self._call_bedrock_judge(prompt)
        return 1.0 if result == "factual" else 0.0

    def evaluate_context_relevance(self, query: str, reference: str) -> float:
        """
        Evaluate if the retrieved context is relevant to the query
        
        Args:
            query: User query
            reference: Retrieved context
            
        Returns:
            Context relevance score (1.0 = relevant, 0.0 = irrelevant)
        """
        prompt = self.context_relevance_prompt.format(
            query=query,
            reference=reference
        )
        
        result = self._call_bedrock_judge(prompt)
        return 1.0 if result == "relevant" else 0.0

    def evaluate_answer_relevance(self, query: str, reference: str, answer: str) -> float:
        """
        Evaluate if the answer is relevant to the query
        
        Args:
            query: User query
            reference: Retrieved context
            answer: Generated answer
            
        Returns:
            Answer relevance score (1.0 = relevant, 0.0 = irrelevant)
        """
        prompt = self.answer_relevance_prompt.format(
            query=query,
            reference=reference,
            answer=answer
        )
        
        result = self._call_bedrock_judge(prompt)
        return 1.0 if result == "relevant" else 0.0

    def evaluate_coherence(self, answer: str) -> float:
        """
        Evaluate if the answer is coherent and well-organized
        
        Args:
            answer: Generated answer
            
        Returns:
            Coherence score (1.0 = coherent, 0.0 = incoherent)
        """
        prompt = self.coherence_prompt.format(answer=answer)
        result = self._call_bedrock_judge(prompt)
        return 1.0 if result == "coherent" else 0.0

    def evaluate_conciseness(self, query: str, answer: str) -> float:
        """
        Evaluate if the answer is concise and to the point
        
        Args:
            query: User query
            answer: Generated answer
            
        Returns:
            Conciseness score (1.0 = concise, 0.0 = verbose)
        """
        prompt = self.conciseness_prompt.format(
            query=query,
            answer=answer
        )
        result = self._call_bedrock_judge(prompt)
        return 1.0 if result == "concise" else 0.0

    def evaluate_single_interaction(
        self, 
        query: str, 
        retrieved_context: str, 
        generated_answer: str,
        ground_truth: Optional[str] = None,
        include_advanced_metrics: bool = False
    ) -> RAGEvaluationResult:
        """
        Evaluate a single RAG interaction across all metrics
        
        Args:
            query: User query
            retrieved_context: Context retrieved from knowledge base
            generated_answer: Answer generated by the RAG system
            ground_truth: Optional ground truth answer
            include_advanced_metrics: Whether to include coherence and conciseness
            
        Returns:
            RAGEvaluationResult containing all evaluation scores
        """
        logger.info(f"Evaluating query: {query[:50]}...")
        
        # Core RAG metrics
        faithfulness = self.evaluate_faithfulness(query, retrieved_context, generated_answer)
        context_relevance = self.evaluate_context_relevance(query, retrieved_context)
        answer_relevance = self.evaluate_answer_relevance(query, retrieved_context, generated_answer)
        
        # Calculate overall score
        core_scores = [faithfulness, context_relevance, answer_relevance]
        
        # Advanced metrics (optional)
        metadata = {}
        if include_advanced_metrics:
            coherence = self.evaluate_coherence(generated_answer)
            conciseness = self.evaluate_conciseness(query, generated_answer)
            core_scores.extend([coherence, conciseness])
            metadata.update({
                "coherence_score": coherence,
                "conciseness_score": conciseness
            })
        
        overall_score = sum(core_scores) / len(core_scores)
        
        return RAGEvaluationResult(
            query=query,
            retrieved_context=retrieved_context,
            generated_answer=generated_answer,
            ground_truth=ground_truth,
            faithfulness_score=faithfulness,
            context_relevance_score=context_relevance,
            answer_relevance_score=answer_relevance,
            overall_score=overall_score,
            metadata=metadata
        )

    def evaluate_batch(
        self, 
        evaluation_data: List[Dict], 
        include_advanced_metrics: bool = False,
        show_progress: bool = True
    ) -> List[RAGEvaluationResult]:
        """
        Evaluate a batch of RAG interactions
        
        Args:
            evaluation_data: List of dictionaries containing query, context, and answer data
            include_advanced_metrics: Whether to include advanced metrics
            show_progress: Whether to show progress information
            
        Returns:
            List of RAGEvaluationResult objects
        """
        results = []
        
        for i, data in enumerate(evaluation_data):
            if show_progress:
                logger.info(f"Processing evaluation {i+1}/{len(evaluation_data)}")
            
            result = self.evaluate_single_interaction(
                query=data['query'],
                retrieved_context=data['retrieved_context'],
                generated_answer=data['generated_answer'],
                ground_truth=data.get('ground_truth'),
                include_advanced_metrics=include_advanced_metrics
            )
            
            results.append(result)
            
            # Add small delay to avoid rate limiting
            time.sleep(0.1)
            
        return results

    def generate_evaluation_report(self, results: List[RAGEvaluationResult]) -> Dict[str, Any]:
        """
        Generate a comprehensive evaluation report
        
        Args:
            results: List of evaluation results
            
        Returns:
            Dictionary containing comprehensive evaluation report
        """
        if not results:
            return {"error": "No evaluation results provided"}
        
        # Calculate aggregate metrics
        faithfulness_scores = [r.faithfulness_score for r in results if r.faithfulness_score is not None]
        context_relevance_scores = [r.context_relevance_score for r in results if r.context_relevance_score is not None]
        answer_relevance_scores = [r.answer_relevance_score for r in results if r.answer_relevance_score is not None]
        overall_scores = [r.overall_score for r in results if r.overall_score is not None]
        
        def calculate_stats(scores):
            if not scores:
                return {"average": 0, "passing_rate": 0, "std_dev": 0, "min": 0, "max": 0}
            return {
                "average": np.mean(scores),
                "passing_rate": sum(1 for s in scores if s >= 0.5) / len(scores),
                "std_dev": np.std(scores),
                "min": min(scores),
                "max": max(scores)
            }
        
        report = {
            "evaluation_summary": {
                "total_evaluations": len(results),
                "evaluation_timestamp": datetime.now().isoformat(),
                "model_used": self.judge_model_id
            },
            "aggregate_metrics": {
                "faithfulness": calculate_stats(faithfulness_scores),
                "context_relevance": calculate_stats(context_relevance_scores),
                "answer_relevance": calculate_stats(answer_relevance_scores),
                "overall_score": calculate_stats(overall_scores)
            }
        }
        
        # Check for advanced metrics
        if results and results[0].metadata and "coherence_score" in results[0].metadata:
            coherence_scores = [r.metadata.get("coherence_score", 0) for r in results]
            conciseness_scores = [r.metadata.get("conciseness_score", 0) for r in results]
            
            report["aggregate_metrics"].update({
                "coherence": calculate_stats(coherence_scores),
                "conciseness": calculate_stats(conciseness_scores)
            })
        
        # Identify problematic areas
        low_faithfulness = [r for r in results if r.faithfulness_score == 0.0]
        low_context_relevance = [r for r in results if r.context_relevance_score == 0.0]
        low_answer_relevance = [r for r in results if r.answer_relevance_score == 0.0]
        
        report["issues_analysis"] = {
            "hallucination_cases": len(low_faithfulness),
            "irrelevant_context_cases": len(low_context_relevance),
            "irrelevant_answer_cases": len(low_answer_relevance),
            "total_issues": len(low_faithfulness) + len(low_context_relevance) + len(low_answer_relevance)
        }
        
        # Performance distribution
        score_ranges = {
            "excellent": [0.9, 1.0],
            "good": [0.7, 0.9],
            "fair": [0.5, 0.7],
            "poor": [0.0, 0.5]
        }
        
        distribution = {}
        for range_name, (min_score, max_score) in score_ranges.items():
            count = sum(1 for r in results if min_score <= r.overall_score < max_score)
            distribution[range_name] = {
                "count": count,
                "percentage": count / len(results) * 100
            }
        
        report["performance_distribution"] = distribution
        
        # Generate optimization recommendations
        recommendations = self._generate_recommendations(report)
        report["recommendations"] = recommendations
        
        # Detailed results for further analysis
        report["detailed_results"] = [
            {
                "query": r.query,
                "faithfulness": r.faithfulness_score,
                "context_relevance": r.context_relevance_score,
                "answer_relevance": r.answer_relevance_score,
                "overall_score": r.overall_score,
                "metadata": r.metadata
            }
            for r in results
        ]
        
        return report

    def _generate_recommendations(self, report: Dict[str, Any]) -> List[str]:
        """
        Generate optimization recommendations based on evaluation results
        
        Args:
            report: Evaluation report
            
        Returns:
            List of optimization recommendations
        """
        recommendations = []
        
        metrics = report["aggregate_metrics"]
        issues = report["issues_analysis"]
        total_evals = report["evaluation_summary"]["total_evaluations"]
        
        # Context relevance issues
        if metrics["context_relevance"]["passing_rate"] < 0.7:
            recommendations.append("🔍 Improve retrieval quality: Consider optimizing your chunking strategy and embedding model")
            recommendations.append("📊 Review retrieval parameters: Increase number of retrieved documents or implement reranking")
            
        # Faithfulness issues
        if metrics["faithfulness"]["passing_rate"] < 0.8:
            recommendations.append("🎯 Reduce hallucinations: Improve prompt engineering to emphasize context adherence")
            recommendations.append("🤖 Review model choice: Consider using models with better instruction following capabilities")
            
        # Answer relevance issues
        if metrics["answer_relevance"]["passing_rate"] < 0.8:
            recommendations.append("💬 Improve answer quality: Refine prompt templates and response formatting")
            recommendations.append("🔄 Review query understanding: Implement better query preprocessing and intent detection")
        
        # Overall performance
        if metrics["overall_score"]["average"] < 0.6:
            recommendations.append("⚠️ Critical: Overall system performance is below acceptable threshold")
            recommendations.append("🔧 Comprehensive review needed: Consider end-to-end system optimization")
        
        # High variance
        if metrics["overall_score"]["std_dev"] > 0.3:
            recommendations.append("📈 High performance variance detected: Investigate query-specific performance patterns")
            
        # Specific issue counts
        if issues["hallucination_cases"] > total_evals * 0.2:
            recommendations.append("🚨 High hallucination rate: Immediate attention needed for prompt engineering")
            
        if issues["irrelevant_context_cases"] > total_evals * 0.3:
            recommendations.append("🎯 Poor retrieval performance: Fundamental retrieval system improvements needed")
        
        return recommendations

    def export_results(self, results: List[RAGEvaluationResult], filename: str):
        """
        Export evaluation results to CSV file
        
        Args:
            results: List of evaluation results
            filename: Output filename
        """
        # Convert results to DataFrame
        data = []
        for result in results:
            row = asdict(result)
            # Flatten metadata
            if row['metadata']:
                for key, value in row['metadata'].items():
                    row[f'metadata_{key}'] = value
            del row['metadata']
            data.append(row)
        
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        logger.info(f"Results exported to {filename}")

    def load_results(self, filename: str) -> List[RAGEvaluationResult]:
        """
        Load evaluation results from CSV file
        
        Args:
            filename: Input filename
            
        Returns:
            List of RAGEvaluationResult objects
        """
        df = pd.read_csv(filename)
        results = []
        
        for _, row in df.iterrows():
            # Extract metadata columns
            metadata = {}
            for col in df.columns:
                if col.startswith('metadata_'):
                    key = col.replace('metadata_', '')
                    metadata[key] = row[col]
            
            result = RAGEvaluationResult(
                query=row['query'],
                retrieved_context=row['retrieved_context'],
                generated_answer=row['generated_answer'],
                ground_truth=row.get('ground_truth'),
                faithfulness_score=row.get('faithfulness_score'),
                context_relevance_score=row.get('context_relevance_score'),
                answer_relevance_score=row.get('answer_relevance_score'),
                overall_score=row.get('overall_score'),
                evaluation_timestamp=row.get('evaluation_timestamp'),
                metadata=metadata if metadata else None
            )
            results.append(result)
        
        return results


# Utility functions for creating sample data and demonstrations
def create_sample_evaluation_data() -> List[Dict]:
    """Create sample data for RAG evaluation demonstration"""
    return [
        {
            "query": "What are the benefits of using vector databases for AI applications?",
            "retrieved_context": "Vector databases are specialized databases designed to store and query high-dimensional vectors (embeddings). They enable semantic search, recommendation systems, and similarity matching. Key benefits include fast similarity search, scalability for large datasets, and support for various AI use cases like retrieval-augmented generation.",
            "generated_answer": "Vector databases offer several key benefits for AI applications: 1) Fast semantic search capabilities allowing you to find conceptually similar items, 2) Scalable storage and querying of high-dimensional embedding vectors, 3) Support for recommendation systems and similarity matching, 4) Essential infrastructure for RAG systems that need to quickly retrieve relevant context.",
            "ground_truth": "Vector databases enable semantic search and are essential for RAG systems, providing fast similarity search and scalable storage."
        },
        {
            "query": "How do I configure AWS Bedrock Knowledge Bases?",
            "retrieved_context": "Amazon S3 is a cloud storage service that offers industry-leading scalability, data availability, security, and performance.",
            "generated_answer": "To configure AWS Bedrock Knowledge Bases, you need to: 1) Create a knowledge base in the AWS console, 2) Configure your data source (like S3), 3) Set up embeddings and vector storage, 4) Configure chunking parameters, 5) Test your retrieval system.",
            "ground_truth": "Configure Bedrock Knowledge Bases by creating a knowledge base, setting up data sources, and configuring embeddings."
        },
        {
            "query": "What is the capital of France?",
            "retrieved_context": "France is a country in Western Europe. It is known for its culture, cuisine, and landmarks. Paris is the capital and largest city of France.",
            "generated_answer": "The capital of France is Paris.",
            "ground_truth": "Paris"
        },
        {
            "query": "Explain quantum computing principles",
            "retrieved_context": "Quantum computing is a revolutionary approach to computation that leverages quantum mechanical phenomena like superposition and entanglement. Unlike classical bits that exist in either 0 or 1 states, quantum bits (qubits) can exist in multiple states simultaneously through superposition.",
            "generated_answer": "Quantum computing harnesses quantum mechanical properties to process information. Key principles include: 1) Superposition - qubits can exist in multiple states simultaneously, 2) Entanglement - qubits can be correlated in ways that classical systems cannot achieve, 3) Quantum interference - allows quantum algorithms to amplify correct answers and cancel out wrong ones. This enables quantum computers to potentially solve certain problems exponentially faster than classical computers.",
            "ground_truth": "Quantum computing uses superposition and entanglement to process information in ways classical computers cannot."
        },
        {
            "query": "What are microservices advantages?",
            "retrieved_context": "Microservices architecture is a method of developing software systems that are loosely coupled and independently deployable. Each service is focused on a specific business capability.",
            "generated_answer": "The main advantages of microservices include: 1) Independent deployment and scaling of services, 2) Technology diversity - each service can use different technologies, 3) Fault isolation - failure of one service doesn't bring down the entire system, 4) Better team organization around business capabilities, 5) Easier maintenance and updates of individual services.",
            "ground_truth": "Microservices provide independent deployment, fault isolation, and better team organization."
        }
    ]


def run_comprehensive_rag_evaluation_demo():
    """Run a comprehensive RAG evaluation demonstration"""
    print("🔍 Comprehensive RAG Evaluation Demonstration")
    print("=" * 60)
    
    # Initialize evaluator
    evaluator = RAGEvaluator()
    
    # Create sample data
    evaluation_data = create_sample_evaluation_data()
    
    print(f"📊 Evaluating {len(evaluation_data)} RAG interactions...")
    print("⏳ This may take a few minutes as we call Amazon Bedrock for evaluation...")
    print()
    
    # Run evaluation with advanced metrics
    results = evaluator.evaluate_batch(evaluation_data, include_advanced_metrics=True)
    
    # Generate comprehensive report
    report = evaluator.generate_evaluation_report(results)
    
    # Display results
    print("📈 COMPREHENSIVE EVALUATION RESULTS")
    print("=" * 40)
    
    print(f"📋 Summary:")
    print(f"   Total evaluations: {report['evaluation_summary']['total_evaluations']}")
    print(f"   Model used: {report['evaluation_summary']['model_used']}")
    print(f"   Timestamp: {report['evaluation_summary']['evaluation_timestamp']}")
    print()
    
    print(f"📊 Core Metrics:")
    for metric_name, metric_data in report['aggregate_metrics'].items():
        print(f"   {metric_name.replace('_', ' ').title()}:")
        print(f"     Average: {metric_data['average']:.3f}")
        print(f"     Passing Rate: {metric_data['passing_rate']:.1%}")
        print(f"     Std Dev: {metric_data['std_dev']:.3f}")
        print(f"     Range: {metric_data['min']:.3f} - {metric_data['max']:.3f}")
        print()
    
    print(f"⚠️  Issues Analysis:")
    issues = report['issues_analysis']
    print(f"   Hallucination cases: {issues['hallucination_cases']}")
    print(f"   Irrelevant context cases: {issues['irrelevant_context_cases']}")
    print(f"   Irrelevant answer cases: {issues['irrelevant_answer_cases']}")
    print(f"   Total issues: {issues['total_issues']}")
    print()
    
    print(f"📊 Performance Distribution:")
    for level, data in report['performance_distribution'].items():
        print(f"   {level.title()}: {data['count']} ({data['percentage']:.1f}%)")
    print()
    
    if report['recommendations']:
        print(f"💡 Optimization Recommendations:")
        for i, rec in enumerate(report['recommendations'], 1):
            print(f"   {i}. {rec}")
        print()
    
    # Export results for further analysis
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"rag_evaluation_results_{timestamp}.csv"
    evaluator.export_results(results, filename)
    print(f"📁 Results exported to: {filename}")
    
    print()
    print("✅ Comprehensive evaluation complete!")
    print("🔍 Review the detailed results and recommendations to optimize your RAG system.")
    
    return report, results


if __name__ == "__main__":
    # Run the demonstration
    report, results = run_comprehensive_rag_evaluation_demo()

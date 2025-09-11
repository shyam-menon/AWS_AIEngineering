#!/usr/bin/env python3
"""
Demo: RAG Evaluation with AWS Knowledge Base

This script demonstrates how to use the RAG evaluation framework with your
existing AWS Knowledge Base containing the course content.

Knowledge Base ID: PIWCGRFREL
Model: amazon.nova-lite-v1:0

To run this demo:
1. Ensure AWS credentials are configured
2. Ensure Bedrock model access is enabled for Amazon Nova Lite
3. Run: python demo_rag_evaluation_with_knowledge_base.py

Author: AI Engineering Course
Date: September 2025
"""

import boto3
import json
import pandas as pd
from typing import List, Dict
from datetime import datetime
import time

try:
    from rag_evaluation_framework import RAGEvaluator, RAGEvaluationResult
    
    print("✅ RAG Evaluation Framework imported successfully!")
    print()
    
    # Initialize the evaluator with your knowledge base and Nova Lite model
    print("🔧 Initializing RAG Evaluator...")
    print(f"   Knowledge Base ID: PIWCGRFREL")
    print(f"   Judge Model: amazon.nova-lite-v1:0")
    print(f"   Region: us-east-1")
    
    evaluator = RAGEvaluator(
        region_name="us-east-1",
        judge_model_id="amazon.nova-lite-v1:0",
        knowledge_base_id="PIWCGRFREL"
    )
    
    print("✅ RAG Evaluator initialized successfully!")
    print()
    
    # Sample queries about your course content
    sample_queries = [
        "What is Amazon Bedrock and how is it used in AI engineering?",
        "Explain the concept of Retrieval-Augmented Generation (RAG)",
        "What are the key components of machine learning fundamentals?",
        "How do you implement agents using the Strands framework?",
        "What are the best practices for prompt engineering?"
    ]
    
    print("📝 Testing RAG evaluation with sample queries...")
    print("="*60)
    
    evaluation_results = []
    
    for i, query in enumerate(sample_queries, 1):
        print(f"\n🔍 Query {i}/5: {query}")
        print("-" * 50)
        
        try:
            # Step 1: Retrieve from knowledge base
            print("   📚 Retrieving from knowledge base...")
            retrieved_context, raw_results = evaluator.retrieve_from_knowledge_base(query, max_results=3)
            
            if not retrieved_context:
                print("   ❌ No content retrieved from knowledge base")
                continue
            
            print(f"   ✅ Retrieved {len(raw_results)} documents")
            print(f"   📄 Context length: {len(retrieved_context)} characters")
            
            # Show first document snippet
            if raw_results:
                first_doc = raw_results[0]['content'][:200] + "..."
                print(f"   📖 First document snippet: {first_doc}")
            
            # Step 2: Generate answer using Nova Lite (simulated - you can replace with actual generation)
            # For this demo, we'll create a simple answer based on the retrieved context
            generated_answer = f"Based on the course materials, {query.lower().replace('?', '').replace('what', 'this')} involves several key concepts mentioned in the documentation. The retrieved context provides relevant information about this topic from the AI engineering curriculum."
            
            print(f"   🤖 Generated answer: {generated_answer[:100]}...")
            
            # Step 3: Evaluate the RAG interaction
            print("   📊 Evaluating RAG performance...")
            
            # Evaluate faithfulness
            faithfulness_score = evaluator.evaluate_faithfulness(query, retrieved_context, generated_answer)
            print(f"   📈 Faithfulness Score: {faithfulness_score}")
            
            # Evaluate context relevance
            context_relevance_score = evaluator.evaluate_context_relevance(query, retrieved_context)
            print(f"   📈 Context Relevance Score: {context_relevance_score}")
            
            # Evaluate answer relevance
            answer_relevance_score = evaluator.evaluate_answer_relevance(query, retrieved_context, generated_answer)
            print(f"   📈 Answer Relevance Score: {answer_relevance_score}")
            
            # Calculate overall score
            overall_score = (faithfulness_score + context_relevance_score + answer_relevance_score) / 3
            print(f"   📈 Overall Score: {overall_score:.2f}")
            
            # Create evaluation result
            result = RAGEvaluationResult(
                query=query,
                retrieved_context=retrieved_context[:500] + "...",  # Truncated for storage
                generated_answer=generated_answer,
                faithfulness_score=faithfulness_score,
                context_relevance_score=context_relevance_score,
                answer_relevance_score=answer_relevance_score,
                overall_score=overall_score,
                metadata={
                    "num_retrieved_docs": len(raw_results),
                    "context_length": len(retrieved_context),
                    "retrieval_scores": [doc['score'] for doc in raw_results]
                }
            )
            
            evaluation_results.append(result)
            
            # Brief pause between evaluations
            time.sleep(2)
            
        except Exception as e:
            print(f"   ❌ Error evaluating query: {e}")
            continue
    
    print("\n" + "="*60)
    print("📊 EVALUATION SUMMARY")
    print("="*60)
    
    if evaluation_results:
        # Calculate average scores
        avg_faithfulness = sum(r.faithfulness_score for r in evaluation_results) / len(evaluation_results)
        avg_context_relevance = sum(r.context_relevance_score for r in evaluation_results) / len(evaluation_results)
        avg_answer_relevance = sum(r.answer_relevance_score for r in evaluation_results) / len(evaluation_results)
        avg_overall = sum(r.overall_score for r in evaluation_results) / len(evaluation_results)
        
        print(f"📈 Average Faithfulness Score: {avg_faithfulness:.2f}")
        print(f"📈 Average Context Relevance Score: {avg_context_relevance:.2f}")
        print(f"📈 Average Answer Relevance Score: {avg_answer_relevance:.2f}")
        print(f"📈 Average Overall Score: {avg_overall:.2f}")
        print()
        
        print(f"✅ Successfully evaluated {len(evaluation_results)} out of {len(sample_queries)} queries")
        
        # Performance interpretation
        if avg_overall >= 0.8:
            print("🎉 Excellent RAG performance!")
        elif avg_overall >= 0.6:
            print("👍 Good RAG performance with room for improvement")
        else:
            print("⚠️  RAG performance needs optimization")
        
        # Save detailed results
        print("\n💾 Saving evaluation results...")
        
        # Convert to pandas DataFrame for analysis
        df_data = []
        for result in evaluation_results:
            df_data.append({
                'query': result.query,
                'faithfulness_score': result.faithfulness_score,
                'context_relevance_score': result.context_relevance_score,
                'answer_relevance_score': result.answer_relevance_score,
                'overall_score': result.overall_score,
                'num_retrieved_docs': result.metadata.get('num_retrieved_docs', 0),
                'context_length': result.metadata.get('context_length', 0),
                'evaluation_timestamp': result.evaluation_timestamp
            })
        
        df = pd.DataFrame(df_data)
        
        # Save to CSV
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"rag_evaluation_results_{timestamp}.csv"
        df.to_csv(filename, index=False)
        print(f"   📁 Results saved to: {filename}")
        
        # Save detailed JSON
        json_filename = f"rag_evaluation_detailed_{timestamp}.json"
        with open(json_filename, 'w') as f:
            json.dump([{
                'query': r.query,
                'retrieved_context': r.retrieved_context,
                'generated_answer': r.generated_answer,
                'scores': {
                    'faithfulness': r.faithfulness_score,
                    'context_relevance': r.context_relevance_score,
                    'answer_relevance': r.answer_relevance_score,
                    'overall': r.overall_score
                },
                'metadata': r.metadata,
                'timestamp': r.evaluation_timestamp
            } for r in evaluation_results], f, indent=2)
        print(f"   📁 Detailed results saved to: {json_filename}")
        
    else:
        print("❌ No successful evaluations completed")
    
    print("\n🎓 RAG Evaluation Demo Complete!")
    print("\n💡 Next Steps:")
    print("   1. Review the evaluation results and identify areas for improvement")
    print("   2. Experiment with different retrieval configurations")
    print("   3. Try the continuous monitoring setup with actual production data")
    print("   4. Use the A/B testing framework to compare different RAG configurations")
    
except ImportError as e:
    print("❌ RAG Evaluation Framework not available.")
    print(f"   Error: {e}")
    print("   Please ensure rag_evaluation_framework.py is in the same directory")
    
except Exception as e:
    print(f"❌ Error running RAG evaluation demo: {e}")
    print("\n🔧 Troubleshooting:")
    print("   1. Check AWS credentials are configured")
    print("   2. Ensure Bedrock model access is enabled for Amazon Nova Lite")
    print("   3. Verify the knowledge base PIWCGRFREL exists and is accessible")
    print("   4. Check network connectivity")
    print("   5. Verify AWS region settings (us-east-1)")
    
    print(f"\n📋 Error details: {type(e).__name__}: {e}")

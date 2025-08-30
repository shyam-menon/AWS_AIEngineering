#!/usr/bin/env python3
"""
Simple Model Evaluation for Beginners

This is a simplified version demonstrating the fundamental concepts of evaluating
Large Language Models (LLMs). Perfect for students learning evaluation basics.

Key Learning Points:
1. What is model evaluation and why it matters
2. Basic evaluation metrics (accuracy, cost, speed)
3. How to compare different responses
4. Simple quality assessment techniques
"""

import boto3
import json
import time
from datetime import datetime


class SimpleModelEvaluator:
    """A basic model evaluator for learning purposes."""
    
    def __init__(self):
        """Initialize the simple evaluator."""
        self.bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
        
        # Keep track of all evaluations
        self.evaluations = []
        
        print("✅ Simple Model Evaluator initialized!")
        print("📚 Ready to learn about model evaluation!\n")
    
    def ask_model(self, question, model_id="amazon.nova-lite-v1:0"):
        """
        Ask the model a question and measure basic performance.
        
        Returns:
            Dict with response, timing, and basic metrics
        """
        print(f"❓ Question: {question}")
        
        start_time = time.time()
        
        try:
            # Prepare request for Nova Lite
            request_body = {
                "schemaVersion": "messages-v1",
                "messages": [
                    {
                        "role": "user",
                        "content": [{"text": question}]
                    }
                ],
                "inferenceConfig": {
                    "maxTokens": 300,
                    "temperature": 0.7
                }
            }
            
            # Call Bedrock
            response = self.bedrock.invoke_model(
                modelId=model_id,
                body=json.dumps(request_body),
                contentType='application/json'
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            answer = response_body['output']['message']['content'][0]['text']
            
            # Calculate time taken
            time_taken = time.time() - start_time
            
            print(f"🤖 Answer: {answer}")
            print(f"⏱️  Time taken: {time_taken:.2f} seconds")
            
            return {
                'question': question,
                'answer': answer,
                'time_taken': time_taken,
                'success': True,
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return {
                'question': question,
                'error': str(e),
                'time_taken': time.time() - start_time,
                'success': False,
                'timestamp': datetime.now()
            }
    
    def check_if_correct(self, answer, expected_answer):
        """
        Simple method to check if an answer is correct.
        
        This uses basic string matching - in real applications,
        you might use more sophisticated methods.
        """
        # Make both answers lowercase for comparison
        answer_clean = answer.lower().strip()
        expected_clean = expected_answer.lower().strip()
        
        # Check if the expected answer is contained in the response
        contains_answer = expected_clean in answer_clean
        
        # Check if they're exactly the same
        exact_match = answer_clean == expected_clean
        
        # Calculate a simple similarity score
        # Count how many words from expected answer appear in the actual answer
        expected_words = expected_clean.split()
        answer_words = answer_clean.split()
        
        matching_words = 0
        for word in expected_words:
            if word in answer_words:
                matching_words += 1
        
        similarity_score = matching_words / len(expected_words) if expected_words else 0
        
        return {
            'exact_match': exact_match,
            'contains_answer': contains_answer,
            'similarity_score': similarity_score,
            'is_correct': contains_answer or similarity_score > 0.5
        }
    
    def evaluate_response_quality(self, question, answer):
        """
        Evaluate the quality of a response without knowing the "right" answer.
        
        This is useful for open-ended questions where there's no single correct answer.
        """
        quality_scores = {}
        
        # 1. Length check - is the response a reasonable length?
        answer_length = len(answer)
        if answer_length < 20:
            quality_scores['length_score'] = 0.3  # Too short
        elif answer_length < 100:
            quality_scores['length_score'] = 0.7  # Reasonable
        elif answer_length < 300:
            quality_scores['length_score'] = 1.0  # Good length
        else:
            quality_scores['length_score'] = 0.8  # Might be too long
        
        # 2. Relevance check - does the answer relate to the question?
        question_words = set(question.lower().split())
        answer_words = set(answer.lower().split())
        common_words = question_words.intersection(answer_words)
        
        relevance_score = len(common_words) / len(question_words) if question_words else 0
        quality_scores['relevance_score'] = min(relevance_score, 1.0)
        
        # 3. Completeness check - does it seem like a complete answer?
        # Simple heuristic: complete answers usually have punctuation and proper structure
        has_punctuation = any(p in answer for p in '.!?')
        has_capital_letters = any(c.isupper() for c in answer)
        
        completeness_score = (
            (1.0 if has_punctuation else 0.0) +
            (1.0 if has_capital_letters else 0.0)
        ) / 2.0
        
        quality_scores['completeness_score'] = completeness_score
        
        # 4. Overall quality (average of all scores)
        overall_quality = sum(quality_scores.values()) / len(quality_scores)
        quality_scores['overall_quality'] = overall_quality
        
        return quality_scores
    
    def test_with_known_answers(self, test_cases):
        """
        Test the model with questions that have known correct answers.
        
        Args:
            test_cases: List of dictionaries with 'question' and 'expected_answer'
        """
        print("🧪 TESTING WITH KNOWN ANSWERS")
        print("="*50)
        
        results = []
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n--- Test {i}/{len(test_cases)} ---")
            
            # Ask the model
            response = self.ask_model(test_case['question'])
            
            if response['success']:
                # Check if the answer is correct
                correctness = self.check_if_correct(
                    response['answer'], 
                    test_case['expected_answer']
                )
                
                # Evaluate quality
                quality = self.evaluate_response_quality(
                    test_case['question'],
                    response['answer']
                )
                
                # Combine all results
                full_result = {
                    **response,
                    'expected_answer': test_case['expected_answer'],
                    'correctness': correctness,
                    'quality': quality
                }
                
                results.append(full_result)
                self.evaluations.append(full_result)
                
                # Show results
                print(f"✅ Expected: {test_case['expected_answer']}")
                print(f"🎯 Correct: {'Yes' if correctness['is_correct'] else 'No'}")
                print(f"📊 Similarity: {correctness['similarity_score']:.2f}")
                print(f"⭐ Quality: {quality['overall_quality']:.2f}")
            
            print()  # Empty line for readability
        
        return results
    
    def test_open_ended_questions(self, questions):
        """
        Test the model with open-ended questions (no "correct" answer).
        
        Args:
            questions: List of questions to ask
        """
        print("💭 TESTING OPEN-ENDED QUESTIONS")
        print("="*50)
        
        results = []
        
        for i, question in enumerate(questions, 1):
            print(f"\n--- Question {i}/{len(questions)} ---")
            
            # Ask the model
            response = self.ask_model(question)
            
            if response['success']:
                # Evaluate quality (no "correct" answer to compare against)
                quality = self.evaluate_response_quality(question, response['answer'])
                
                # Combine results
                full_result = {
                    **response,
                    'quality': quality
                }
                
                results.append(full_result)
                self.evaluations.append(full_result)
                
                # Show results
                print(f"⭐ Quality Score: {quality['overall_quality']:.2f}")
                print(f"📏 Length Score: {quality['length_score']:.2f}")
                print(f"🎯 Relevance Score: {quality['relevance_score']:.2f}")
            
            print()  # Empty line for readability
        
        return results
    
    def show_summary(self):
        """Show a summary of all evaluations."""
        if not self.evaluations:
            print("No evaluations to summarize yet!")
            return
        
        print("\n" + "="*60)
        print("📊 EVALUATION SUMMARY")
        print("="*60)
        
        total_tests = len(self.evaluations)
        successful_tests = len([e for e in self.evaluations if e['success']])
        
        print(f"Total Tests: {total_tests}")
        print(f"Successful Tests: {successful_tests}")
        
        if successful_tests > 0:
            # Calculate average response time
            times = [e['time_taken'] for e in self.evaluations if e['success']]
            avg_time = sum(times) / len(times)
            
            # Calculate average quality
            qualities = [e['quality']['overall_quality'] for e in self.evaluations if e['success'] and 'quality' in e]
            avg_quality = sum(qualities) / len(qualities) if qualities else 0
            
            # Count correct answers (for tests with known answers)
            correct_answers = [e for e in self.evaluations if e['success'] and 'correctness' in e and e['correctness']['is_correct']]
            accuracy = len(correct_answers) / len([e for e in self.evaluations if 'correctness' in e]) if any('correctness' in e for e in self.evaluations) else 0
            
            print(f"Average Response Time: {avg_time:.2f} seconds")
            print(f"Average Quality Score: {avg_quality:.2f}")
            
            if accuracy > 0:
                print(f"Accuracy (Known Answers): {accuracy:.2%}")
            
            # Performance rating
            if avg_quality >= 0.8:
                rating = "Excellent! 🌟"
            elif avg_quality >= 0.6:
                rating = "Good 👍"
            elif avg_quality >= 0.4:
                rating = "Fair 👌"
            else:
                rating = "Needs Improvement 📈"
            
            print(f"Overall Performance: {rating}")
        
        print("="*60)


def learning_demo():
    """A step-by-step demo to learn model evaluation."""
    print("🎓 MODEL EVALUATION LEARNING DEMO")
    print("="*60)
    print("Welcome! This demo will teach you the basics of evaluating AI models.")
    print("We'll test the model with different types of questions.\n")
    
    evaluator = SimpleModelEvaluator()
    
    # Phase 1: Test with questions that have clear correct answers
    factual_questions = [
        {
            "question": "What is the capital of Japan?",
            "expected_answer": "Tokyo"
        },
        {
            "question": "How many days are in a week?",
            "expected_answer": "7"
        },
        {
            "question": "What color do you get when you mix red and blue?",
            "expected_answer": "purple"
        }
    ]
    
    print("🔍 PHASE 1: Testing factual knowledge")
    print("These questions have clear 'correct' answers.\n")
    
    factual_results = evaluator.test_with_known_answers(factual_questions)
    
    input("Press Enter to continue to Phase 2...")
    
    # Phase 2: Test with open-ended questions
    open_questions = [
        "What do you think is the most important invention in human history?",
        "Describe your perfect day.",
        "What advice would you give to someone learning to code?"
    ]
    
    print("\n🤔 PHASE 2: Testing creative thinking")
    print("These questions don't have a single 'correct' answer.\n")
    
    open_results = evaluator.test_open_ended_questions(open_questions)
    
    # Show final summary
    evaluator.show_summary()
    
    print("\n🎯 KEY LEARNINGS:")
    print("1. Different types of questions need different evaluation approaches")
    print("2. For factual questions, we can check if the answer is correct")
    print("3. For open-ended questions, we evaluate quality and relevance")
    print("4. Response time and consistency are also important factors")
    print("5. No single metric tells the whole story - use multiple measures!")


def quick_comparison():
    """Quick demo comparing the same question asked multiple times."""
    print("🔄 QUICK CONSISTENCY TEST")
    print("="*40)
    print("Let's ask the same question multiple times to see how consistent the model is.\n")
    
    evaluator = SimpleModelEvaluator()
    
    question = "Explain what artificial intelligence is in one sentence."
    
    print(f"Asking: '{question}'\n")
    
    responses = []
    for i in range(3):
        print(f"--- Attempt {i+1} ---")
        result = evaluator.ask_model(question)
        if result['success']:
            quality = evaluator.evaluate_response_quality(question, result['answer'])
            responses.append({
                'answer': result['answer'],
                'quality': quality['overall_quality'],
                'time': result['time_taken']
            })
        print()
    
    if responses:
        print("📊 COMPARISON RESULTS:")
        for i, resp in enumerate(responses, 1):
            print(f"Response {i}: Quality {resp['quality']:.2f}, Time {resp['time']:.2f}s")
        
        # Calculate consistency
        qualities = [r['quality'] for r in responses]
        avg_quality = sum(qualities) / len(qualities)
        quality_std = (sum((q - avg_quality) ** 2 for q in qualities) / len(qualities)) ** 0.5
        
        print(f"\nAverage Quality: {avg_quality:.2f}")
        print(f"Consistency (lower std deviation = more consistent): {quality_std:.3f}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        quick_comparison()
    else:
        learning_demo()

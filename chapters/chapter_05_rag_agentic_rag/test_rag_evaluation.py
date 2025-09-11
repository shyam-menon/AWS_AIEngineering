#!/usr/bin/env python3
"""
Comprehensive Test Suite for RAG Evaluation Framework

This module provides comprehensive unit tests for the RAG evaluation framework,
including tests for all evaluation metrics, A/B testing, and CloudWatch integration.

Author: AI Engineering Course
Date: 2025
"""

import unittest
import json
import tempfile
import os
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock
import pandas as pd

# Import the modules to test
from rag_evaluation_framework import (
    RAGEvaluator, 
    RAGEvaluationResult, 
    create_sample_evaluation_data,
    run_comprehensive_rag_evaluation_demo
)
from advanced_rag_evaluation import (
    ContinuousRAGEvaluator,
    RAGABTester,
    RAGConfiguration,
    RAGVariant,
    create_sample_rag_configurations,
    simulate_user_interactions
)
from cloudwatch_integration import CloudWatchRAGMonitor

class TestRAGEvaluationResult(unittest.TestCase):
    """Test cases for RAGEvaluationResult data class"""
    
    def test_initialization(self):
        """Test RAGEvaluationResult initialization"""
        result = RAGEvaluationResult(
            query="Test query",
            retrieved_context="Test context",
            generated_answer="Test answer"
        )
        
        self.assertEqual(result.query, "Test query")
        self.assertEqual(result.retrieved_context, "Test context")
        self.assertEqual(result.generated_answer, "Test answer")
        self.assertIsNotNone(result.evaluation_timestamp)
        self.assertIsNotNone(result.metadata)
    
    def test_post_init(self):
        """Test __post_init__ method"""
        result = RAGEvaluationResult(
            query="Test",
            retrieved_context="Context",
            generated_answer="Answer"
        )
        
        # Check timestamp is set
        self.assertIsInstance(result.evaluation_timestamp, str)
        
        # Check metadata is initialized
        self.assertIsInstance(result.metadata, dict)


class TestRAGEvaluator(unittest.TestCase):
    """Test cases for RAGEvaluator class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.evaluator = RAGEvaluator()
        
        # Mock Bedrock calls to avoid actual API calls during testing
        self.bedrock_patcher = patch.object(self.evaluator, '_call_bedrock_judge')
        self.mock_bedrock = self.bedrock_patcher.start()
        
    def tearDown(self):
        """Clean up after tests"""
        self.bedrock_patcher.stop()
    
    def test_initialization(self):
        """Test RAGEvaluator initialization"""
        evaluator = RAGEvaluator(region_name="us-west-2")
        self.assertEqual(evaluator.judge_model_id, "amazon.nova-lite-v1:0")
        self.assertEqual(evaluator.knowledge_base_id, "PIWCGRFREL")
        self.assertIn("factual", evaluator.faithfulness_prompt)
        self.assertIn("relevant", evaluator.context_relevance_prompt)
    
    def test_evaluate_faithfulness(self):
        """Test faithfulness evaluation"""
        # Mock successful response
        self.mock_bedrock.return_value = "factual"
        
        score = self.evaluator.evaluate_faithfulness(
            query="Test query",
            reference="Test reference",
            answer="Test answer"
        )
        
        self.assertEqual(score, 1.0)
        
        # Test hallucination case
        self.mock_bedrock.return_value = "hallucinated"
        
        score = self.evaluator.evaluate_faithfulness(
            query="Test query",
            reference="Test reference",
            answer="Test answer"
        )
        
        self.assertEqual(score, 0.0)
    
    def test_evaluate_context_relevance(self):
        """Test context relevance evaluation"""
        # Mock relevant response
        self.mock_bedrock.return_value = "relevant"
        
        score = self.evaluator.evaluate_context_relevance(
            query="Test query",
            reference="Test reference"
        )
        
        self.assertEqual(score, 1.0)
        
        # Test irrelevant case
        self.mock_bedrock.return_value = "irrelevant"
        
        score = self.evaluator.evaluate_context_relevance(
            query="Test query",
            reference="Test reference"
        )
        
        self.assertEqual(score, 0.0)
    
    def test_evaluate_answer_relevance(self):
        """Test answer relevance evaluation"""
        # Mock relevant response
        self.mock_bedrock.return_value = "relevant"
        
        score = self.evaluator.evaluate_answer_relevance(
            query="Test query",
            reference="Test reference",
            answer="Test answer"
        )
        
        self.assertEqual(score, 1.0)
    
    def test_evaluate_single_interaction(self):
        """Test single interaction evaluation"""
        # Mock all responses as positive for consistent testing
        def mock_side_effect(prompt):
            if "factual" in prompt or "relevant" in prompt:
                return "factual" if "factual" in prompt else "relevant"
            return "relevant"  # Default positive response
        
        self.mock_bedrock.side_effect = mock_side_effect
        
        result = self.evaluator.evaluate_single_interaction(
            query="Test query",
            retrieved_context="Test context",
            generated_answer="Test answer"
        )
        
        self.assertIsInstance(result, RAGEvaluationResult)
        self.assertEqual(result.query, "Test query")
        # The exact scores may vary based on the actual Bedrock responses
        # so we just check that scores are within valid range
        self.assertGreaterEqual(result.faithfulness_score, 0.0)
        self.assertLessEqual(result.faithfulness_score, 1.0)
        self.assertGreaterEqual(result.context_relevance_score, 0.0)
        self.assertLessEqual(result.context_relevance_score, 1.0)
        self.assertGreaterEqual(result.answer_relevance_score, 0.0)
        self.assertLessEqual(result.answer_relevance_score, 1.0)
        self.assertGreaterEqual(result.overall_score, 0.0)
        self.assertLessEqual(result.overall_score, 1.0)
    
    def test_evaluate_batch(self):
        """Test batch evaluation"""
        # Mock positive responses
        self.mock_bedrock.return_value = "factual"
        
        evaluation_data = [
            {
                "query": "Query 1",
                "retrieved_context": "Context 1",
                "generated_answer": "Answer 1"
            },
            {
                "query": "Query 2",
                "retrieved_context": "Context 2",
                "generated_answer": "Answer 2"
            }
        ]
        
        results = self.evaluator.evaluate_batch(evaluation_data, show_progress=False)
        
        self.assertEqual(len(results), 2)
        self.assertIsInstance(results[0], RAGEvaluationResult)
        self.assertIsInstance(results[1], RAGEvaluationResult)
    
    def test_generate_evaluation_report(self):
        """Test evaluation report generation"""
        # Create mock results
        results = [
            RAGEvaluationResult(
                query="Query 1",
                retrieved_context="Context 1",
                generated_answer="Answer 1",
                faithfulness_score=1.0,
                context_relevance_score=0.8,
                answer_relevance_score=0.9,
                overall_score=0.9
            ),
            RAGEvaluationResult(
                query="Query 2",
                retrieved_context="Context 2",
                generated_answer="Answer 2",
                faithfulness_score=0.7,
                context_relevance_score=0.6,
                answer_relevance_score=0.8,
                overall_score=0.7
            )
        ]
        
        report = self.evaluator.generate_evaluation_report(results)
        
        # Check report structure
        self.assertIn("evaluation_summary", report)
        self.assertIn("aggregate_metrics", report)
        self.assertIn("issues_analysis", report)
        self.assertIn("performance_distribution", report)
        self.assertIn("recommendations", report)
        
        # Check metrics calculations
        self.assertEqual(report["evaluation_summary"]["total_evaluations"], 2)
        self.assertAlmostEqual(report["aggregate_metrics"]["overall_score"]["average"], 0.8, places=1)
    
    def test_export_and_load_results(self):
        """Test exporting and loading results"""
        # Create test results
        results = [
            RAGEvaluationResult(
                query="Test query",
                retrieved_context="Test context",
                generated_answer="Test answer",
                faithfulness_score=1.0,
                context_relevance_score=0.8,
                answer_relevance_score=0.9,
                overall_score=0.9
            )
        ]
        
        # Export to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            filename = f.name
        
        try:
            self.evaluator.export_results(results, filename)
            self.assertTrue(os.path.exists(filename))
            
            # Load results
            loaded_results = self.evaluator.load_results(filename)
            
            self.assertEqual(len(loaded_results), 1)
            self.assertEqual(loaded_results[0].query, "Test query")
            self.assertEqual(loaded_results[0].faithfulness_score, 1.0)
            
        finally:
            # Clean up
            if os.path.exists(filename):
                os.unlink(filename)


class TestContinuousRAGEvaluator(unittest.TestCase):
    """Test cases for ContinuousRAGEvaluator class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_evaluator = Mock(spec=RAGEvaluator)
        self.mock_data_source = Mock()
        
        self.continuous_evaluator = ContinuousRAGEvaluator(
            evaluator=self.mock_evaluator,
            data_source_func=self.mock_data_source
        )
    
    def test_initialization(self):
        """Test ContinuousRAGEvaluator initialization"""
        self.assertEqual(self.continuous_evaluator.evaluator, self.mock_evaluator)
        self.assertEqual(self.continuous_evaluator.data_source_func, self.mock_data_source)
        self.assertIsInstance(self.continuous_evaluator.alert_thresholds, dict)
    
    @patch('advanced_rag_evaluation.logger')
    def test_run_scheduled_evaluation_no_data(self, mock_logger):
        """Test scheduled evaluation with no data"""
        # Mock no data available
        self.mock_data_source.return_value = []
        
        result = self.continuous_evaluator.run_scheduled_evaluation()
        
        self.assertIsNone(result)
        mock_logger.info.assert_called_with("📭 No data available for evaluation")
    
    @patch('advanced_rag_evaluation.logger')
    def test_run_scheduled_evaluation_with_data(self, mock_logger):
        """Test scheduled evaluation with data"""
        # Mock data and evaluation results
        sample_data = [
            {
                "query": "Test query",
                "retrieved_context": "Test context",
                "generated_answer": "Test answer"
            }
        ]
        
        self.mock_data_source.return_value = sample_data
        self.mock_evaluator.evaluate_batch.return_value = [Mock()]
        self.mock_evaluator.generate_evaluation_report.return_value = {
            "aggregate_metrics": {
                "overall_score": {"average": 0.8}
            },
            "evaluation_summary": {"total_evaluations": 1},
            "issues_analysis": {"hallucination_cases": 0}
        }
        
        # Mock CloudWatch methods to avoid actual AWS calls
        with patch.object(self.continuous_evaluator, '_publish_metrics_to_cloudwatch'), \
             patch.object(self.continuous_evaluator, '_check_performance_alerts'):
            
            result = self.continuous_evaluator.run_scheduled_evaluation()
        
        self.assertIsNotNone(result)
        self.assertIn("timestamp", result)
        self.assertIn("report", result)
    
    def test_get_performance_trend_insufficient_data(self):
        """Test performance trend with insufficient data"""
        # No evaluation history
        trend = self.continuous_evaluator.get_performance_trend()
        
        self.assertIn("error", trend)
    
    def test_get_performance_trend_with_data(self):
        """Test performance trend with sufficient data"""
        # Add mock evaluation history
        now = datetime.now()
        self.continuous_evaluator.evaluation_history = [
            {
                "timestamp": (now - timedelta(hours=2)).isoformat(),
                "report": {
                    "aggregate_metrics": {
                        "overall_score": {"average": 0.7}
                    }
                }
            },
            {
                "timestamp": now.isoformat(),
                "report": {
                    "aggregate_metrics": {
                        "overall_score": {"average": 0.8}
                    }
                }
            }
        ]
        
        trend = self.continuous_evaluator.get_performance_trend(hours=24)
        
        self.assertNotIn("error", trend)
        self.assertEqual(trend["evaluations_count"], 2)
        self.assertEqual(trend["current_score"], 0.8)


class TestRAGABTester(unittest.TestCase):
    """Test cases for RAGABTester class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.control_config, self.treatment_config = create_sample_rag_configurations()
        self.mock_evaluator = Mock(spec=RAGEvaluator)
        
        self.ab_tester = RAGABTester(
            control_config=self.control_config,
            treatment_config=self.treatment_config,
            evaluator=self.mock_evaluator
        )
    
    def test_initialization(self):
        """Test RAGABTester initialization"""
        self.assertEqual(self.ab_tester.control_config, self.control_config)
        self.assertEqual(self.ab_tester.treatment_config, self.treatment_config)
        self.assertEqual(self.ab_tester.traffic_split, 0.5)
    
    def test_assign_variant_consistency(self):
        """Test that user variant assignment is consistent"""
        user_id = "test_user_123"
        
        # Get assignment multiple times
        variant1 = self.ab_tester.assign_variant(user_id)
        variant2 = self.ab_tester.assign_variant(user_id)
        variant3 = self.ab_tester.assign_variant(user_id)
        
        # Should be consistent
        self.assertEqual(variant1, variant2)
        self.assertEqual(variant2, variant3)
    
    def test_process_query(self):
        """Test query processing"""
        result = self.ab_tester.process_query(
            user_id="test_user",
            query="Test query"
        )
        
        self.assertIn("user_id", result)
        self.assertIn("query", result)
        self.assertIn("variant", result)
        self.assertIn("config_used", result)
        self.assertIn("timestamp", result)
        
        # Check that result is stored
        variant = RAGVariant(result["variant"])
        self.assertGreater(len(self.ab_tester.results[variant]), 0)
    
    def test_evaluate_experiment_insufficient_samples(self):
        """Test experiment evaluation with insufficient samples"""
        evaluation_result = self.ab_tester.evaluate_experiment(min_sample_size=100)
        
        self.assertIn("error", evaluation_result)
    
    def test_prepare_evaluation_data(self):
        """Test evaluation data preparation"""
        raw_results = [
            {
                "query": "Test query",
                "retrieved_context": "Test context",
                "generated_answer": "Test answer"
            }
        ]
        
        evaluation_data = self.ab_tester._prepare_evaluation_data(raw_results)
        
        self.assertEqual(len(evaluation_data), 1)
        self.assertEqual(evaluation_data[0]["query"], "Test query")


class TestCloudWatchRAGMonitor(unittest.TestCase):
    """Test cases for CloudWatchRAGMonitor class"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Mock AWS clients to avoid actual AWS calls
        with patch('cloudwatch_integration.boto3.client'):
            self.monitor = CloudWatchRAGMonitor(
                namespace="Test/RAG",
                region_name="us-east-1"
            )
    
    def test_initialization(self):
        """Test CloudWatchRAGMonitor initialization"""
        self.assertEqual(self.monitor.namespace, "Test/RAG")
        self.assertEqual(self.monitor.region_name, "us-east-1")
    
    @patch('cloudwatch_integration.logger')
    def test_publish_evaluation_metrics(self, mock_logger):
        """Test publishing evaluation metrics"""
        # Mock CloudWatch client
        self.monitor.cloudwatch = Mock()
        
        sample_report = {
            "evaluation_summary": {
                "total_evaluations": 10
            },
            "aggregate_metrics": {
                "overall_score": {
                    "average": 0.8,
                    "passing_rate": 0.9,
                    "std_dev": 0.1
                }
            },
            "issues_analysis": {
                "hallucination_cases": 2
            },
            "performance_distribution": {
                "excellent": {"count": 5, "percentage": 50.0}
            }
        }
        
        # Should not raise exception
        self.monitor.publish_evaluation_metrics(sample_report)
        
        # Verify CloudWatch was called
        self.monitor.cloudwatch.put_metric_data.assert_called()
    
    def test_create_rag_dashboard(self):
        """Test dashboard creation"""
        # Mock CloudWatch client
        self.monitor.cloudwatch = Mock()
        self.monitor.cloudwatch.put_dashboard.return_value = {}
        
        dashboard_arn = self.monitor.create_rag_dashboard("Test-Dashboard")
        
        self.assertIn("Test-Dashboard", dashboard_arn)
        self.monitor.cloudwatch.put_dashboard.assert_called_once()
    
    def test_create_performance_alarms(self):
        """Test alarm creation"""
        # Mock CloudWatch client
        self.monitor.cloudwatch = Mock()
        
        alarm_arns = self.monitor.create_performance_alarms(
            thresholds={
                "overall_score": 0.8,
                "faithfulness_rate": 80,
                "context_relevance_rate": 70,
                "hallucination_cases": 10,
                "poor_performance_rate": 20
            },
            alarm_prefix="Test"
        )
        
        self.assertIsInstance(alarm_arns, list)
        self.assertGreater(len(alarm_arns), 0)


class TestUtilityFunctions(unittest.TestCase):
    """Test cases for utility functions"""
    
    def test_create_sample_evaluation_data(self):
        """Test sample evaluation data creation"""
        data = create_sample_evaluation_data()
        
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        
        # Check structure of first item
        first_item = data[0]
        self.assertIn("query", first_item)
        self.assertIn("retrieved_context", first_item)
        self.assertIn("generated_answer", first_item)
    
    def test_create_sample_rag_configurations(self):
        """Test sample RAG configuration creation"""
        control, treatment = create_sample_rag_configurations()
        
        self.assertIsInstance(control, RAGConfiguration)
        self.assertIsInstance(treatment, RAGConfiguration)
        self.assertNotEqual(control.name, treatment.name)
    
    def test_simulate_user_interactions(self):
        """Test user interaction simulation"""
        control_config, treatment_config = create_sample_rag_configurations()
        mock_evaluator = Mock(spec=RAGEvaluator)
        
        ab_tester = RAGABTester(
            control_config=control_config,
            treatment_config=treatment_config,
            evaluator=mock_evaluator
        )
        
        interactions = simulate_user_interactions(ab_tester, num_interactions=10)
        
        self.assertEqual(len(interactions), 10)
        self.assertIsInstance(interactions[0], dict)


class TestIntegrationScenarios(unittest.TestCase):
    """Integration test scenarios"""
    
    @patch('rag_evaluation_framework.RAGEvaluator._call_bedrock_judge')
    def test_end_to_end_evaluation_workflow(self, mock_bedrock):
        """Test complete evaluation workflow"""
        # Mock Bedrock responses
        mock_bedrock.return_value = "factual"
        
        # Create evaluator
        evaluator = RAGEvaluator()
        
        # Get sample data
        evaluation_data = create_sample_evaluation_data()
        
        # Run evaluation
        results = evaluator.evaluate_batch(evaluation_data[:2], show_progress=False)
        
        # Generate report
        report = evaluator.generate_evaluation_report(results)
        
        # Verify results
        self.assertEqual(len(results), 2)
        self.assertIn("evaluation_summary", report)
        self.assertIn("aggregate_metrics", report)
    
    def test_ab_testing_workflow(self):
        """Test A/B testing workflow"""
        # Create configurations
        control_config, treatment_config = create_sample_rag_configurations()
        mock_evaluator = Mock(spec=RAGEvaluator)
        
        # Create A/B tester
        ab_tester = RAGABTester(
            control_config=control_config,
            treatment_config=treatment_config,
            evaluator=mock_evaluator
        )
        
        # Simulate interactions
        interactions = simulate_user_interactions(ab_tester, num_interactions=10)
        
        # Verify interactions were recorded
        total_results = len(ab_tester.results[RAGVariant.CONTROL]) + len(ab_tester.results[RAGVariant.TREATMENT])
        self.assertEqual(total_results, 10)


def run_tests():
    """Run all tests"""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestRAGEvaluationResult,
        TestRAGEvaluator,
        TestContinuousRAGEvaluator,
        TestRAGABTester,
        TestCloudWatchRAGMonitor,
        TestUtilityFunctions,
        TestIntegrationScenarios
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result

if __name__ == "__main__":
    print("🧪 Running RAG Evaluation Framework Tests")
    print("=" * 50)
    
    result = run_tests()
    
    print("\\n" + "=" * 50)
    if result.wasSuccessful():
        print("✅ All tests passed!")
    else:
        print(f"❌ {len(result.failures)} failures, {len(result.errors)} errors")
        
        if result.failures:
            print("\\nFailures:")
            for test, traceback in result.failures:
                print(f"- {test}: {traceback}")
        
        if result.errors:
            print("\\nErrors:")
            for test, traceback in result.errors:
                print(f"- {test}: {traceback}")

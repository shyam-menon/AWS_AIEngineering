#!/usr/bin/env python3
"""
Graph Multi-Agent Pattern Example

This example demonstrates the "Graph" pattern, where agents are organized as nodes
in a Directed Acyclic Graph (DAG) with explicit dependencies and deterministic execution order.

The Graph pattern provides:
- Deterministic execution order based on DAG structure
- Output propagation along edges between nodes
- Clear dependency management between agents
- Support for conditional edges and dynamic workflows
- Custom node types for business logic
- Multi-modal input support

Author: AI Engineering Course
Date: September 2025
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Enable Strands multiagent debug logging
graph_logger = logging.getLogger("strands.multiagent")
graph_logger.setLevel(logging.DEBUG)

try:
    from strands import Agent
    from strands.multiagent import GraphBuilder
    from strands.multiagent.base import MultiAgentBase, NodeResult, Status, MultiAgentResult
    from strands.agent.agent_result import AgentResult
    from strands.types.content import ContentBlock, Message
    from strands_tools import current_time, calculator, file_read
    
    logger.info("✅ Successfully imported Strands modules")
except ImportError as e:
    logger.error(f"❌ Failed to import Strands modules: {e}")
    logger.info("📝 This is a demonstration of Graph multi-agent patterns")
    logger.info("🔧 Install Strands with: pip install strands")
    exit(1)


# ===============================
# CUSTOM NODE TYPES
# ===============================

class DataValidationNode(MultiAgentBase):
    """Custom node for deterministic data validation."""
    
    def __init__(self, name: str = "data_validator"):
        super().__init__()
        self.name = name
    
    def __call__(self, task, **kwargs):
        """Synchronous execution wrapper."""
        import asyncio
        return asyncio.run(self.invoke_async(task, **kwargs))
    
    async def invoke_async(self, task, **kwargs):
        """Execute data validation logic."""
        start_time = datetime.now()
        
        try:
            # Extract text content from task
            if isinstance(task, str):
                content = task
            elif isinstance(task, list):
                content = " ".join([str(item) for item in task if isinstance(item, str)])
            else:
                content = str(task)
            
            # Perform validation
            validation_result = self._validate_data(content)
            
            # Create AgentResult
            agent_result = AgentResult(
                stop_reason="end_turn",
                message=Message(
                    role="assistant", 
                    content=[ContentBlock(text=validation_result)]
                ),
                usage={"input_tokens": len(content.split()), "output_tokens": len(validation_result.split())},
                metrics={"execution_time": (datetime.now() - start_time).total_seconds() * 1000}
            )
            
            # Return wrapped in MultiAgentResult
            return MultiAgentResult(
                status=Status.COMPLETED,
                results={self.name: NodeResult(
                    result=agent_result,
                    execution_status="COMPLETED",
                    execution_time=(datetime.now() - start_time).total_seconds() * 1000
                )},
                execution_time=(datetime.now() - start_time).total_seconds() * 1000
            )
            
        except Exception as e:
            logger.error(f"❌ Data validation failed: {e}")
            
            agent_result = AgentResult(
                stop_reason="error",
                message=Message(
                    role="assistant", 
                    content=[ContentBlock(text=f"❌ Validation failed: {str(e)}")]
                ),
                usage={"input_tokens": 0, "output_tokens": 0},
                metrics={"error": str(e)}
            )
            
            return MultiAgentResult(
                status=Status.FAILED,
                results={self.name: NodeResult(
                    result=agent_result,
                    execution_status="FAILED",
                    execution_time=(datetime.now() - start_time).total_seconds() * 1000
                )},
                execution_time=(datetime.now() - start_time).total_seconds() * 1000
            )
    
    def _validate_data(self, content: str) -> str:
        """Perform deterministic data validation."""
        if not content or not content.strip():
            return "❌ Validation failed: Empty or whitespace-only content"
        
        if len(content) < 10:
            return "⚠️ Validation warning: Content is very short (less than 10 characters)"
        
        # Basic content checks
        checks = {
            "length": len(content),
            "word_count": len(content.split()),
            "has_numbers": any(c.isdigit() for c in content),
            "has_punctuation": any(c in ".,!?;:" for c in content),
            "avg_word_length": sum(len(word) for word in content.split()) / len(content.split()) if content.split() else 0
        }
        
        validation_summary = f"""✅ Data Validation Completed
        
Content Statistics:
- Length: {checks['length']} characters
- Word count: {checks['word_count']} words
- Contains numbers: {checks['has_numbers']}
- Contains punctuation: {checks['has_punctuation']}
- Average word length: {checks['avg_word_length']:.1f} characters

Status: Content passes basic validation checks."""
        
        return validation_summary


class BusinessRulesNode(MultiAgentBase):
    """Custom node for deterministic business rule processing."""
    
    def __init__(self, rules: Dict[str, Any], name: str = "business_rules"):
        super().__init__()
        self.rules = rules
        self.name = name
    
    def __call__(self, task, **kwargs):
        """Synchronous execution wrapper."""
        import asyncio
        return asyncio.run(self.invoke_async(task, **kwargs))
    
    async def invoke_async(self, task, **kwargs):
        """Execute business rules logic."""
        start_time = datetime.now()
        
        try:
            # Extract and process content
            if isinstance(task, str):
                content = task
            else:
                content = str(task)
            
            # Apply business rules
            rules_result = self._apply_business_rules(content)
            
            # Create AgentResult
            agent_result = AgentResult(
                stop_reason="end_turn",
                message=Message(
                    role="assistant", 
                    content=[ContentBlock(text=rules_result)]
                ),
                usage={"input_tokens": len(content.split()), "output_tokens": len(rules_result.split())},
                metrics={"execution_time": (datetime.now() - start_time).total_seconds() * 1000}
            )
            
            return MultiAgentResult(
                status=Status.COMPLETED,
                results={self.name: NodeResult(
                    result=agent_result,
                    execution_status="COMPLETED",
                    execution_time=(datetime.now() - start_time).total_seconds() * 1000
                )},
                execution_time=(datetime.now() - start_time).total_seconds() * 1000
            )
            
        except Exception as e:
            logger.error(f"❌ Business rules processing failed: {e}")
            
            agent_result = AgentResult(
                stop_reason="error",
                message=Message(
                    role="assistant", 
                    content=[ContentBlock(text=f"❌ Business rules failed: {str(e)}")]
                ),
                usage={"input_tokens": 0, "output_tokens": 0},
                metrics={"error": str(e)}
            )
            
            return MultiAgentResult(
                status=Status.FAILED,
                results={self.name: NodeResult(
                    result=agent_result,
                    execution_status="FAILED",
                    execution_time=(datetime.now() - start_time).total_seconds() * 1000
                )},
                execution_time=(datetime.now() - start_time).total_seconds() * 1000
            )
    
    def _apply_business_rules(self, content: str) -> str:
        """Apply configured business rules."""
        results = []
        
        # Check content against business rules
        for rule_name, rule_config in self.rules.items():
            if rule_name == "min_length":
                if len(content) >= rule_config["value"]:
                    results.append(f"✅ {rule_name}: PASS (length: {len(content)} >= {rule_config['value']})")
                else:
                    results.append(f"❌ {rule_name}: FAIL (length: {len(content)} < {rule_config['value']})")
            
            elif rule_name == "required_keywords":
                found_keywords = [kw for kw in rule_config["keywords"] if kw.lower() in content.lower()]
                if found_keywords:
                    results.append(f"✅ {rule_name}: PASS (found: {found_keywords})")
                else:
                    results.append(f"❌ {rule_name}: FAIL (none of {rule_config['keywords']} found)")
            
            elif rule_name == "forbidden_terms":
                found_forbidden = [term for term in rule_config["terms"] if term.lower() in content.lower()]
                if not found_forbidden:
                    results.append(f"✅ {rule_name}: PASS (no forbidden terms)")
                else:
                    results.append(f"❌ {rule_name}: FAIL (found forbidden: {found_forbidden})")
        
        return f"""🔧 Business Rules Processing Results

{chr(10).join(results)}

Overall Status: {'✅ ALL RULES PASSED' if all('✅' in r for r in results) else '⚠️ SOME RULES FAILED'}"""


# ===============================
# GRAPH TOPOLOGY EXAMPLES
# ===============================

def create_research_analysis_graph():
    """
    Create a research and analysis graph with sequential pipeline topology.
    
    Topology: Research -> Analysis -> Fact-Check -> Report
    """
    
    # Create specialized research agents
    researcher = Agent(
        name="researcher",
        model="us.amazon.nova-lite-v1:0",
        system_prompt="""You are a Research Specialist focused on comprehensive information gathering.
        
        Your expertise:
        - Comprehensive research methodology
        - Source identification and verification
        - Data collection and organization
        - Research question formulation
        - Initial findings documentation
        
        When you receive a task:
        1. Break down the research question into key components
        2. Identify the types of information needed
        3. Gather relevant data and insights
        4. Organize findings systematically
        5. Provide comprehensive research foundation for analysis
        
        Deliver thorough, well-organized research that enables deep analysis.""",
        tools=[current_time, calculator]
    )
    
    analyst = Agent(
        name="analyst",
        model="us.amazon.nova-lite-v1:0",
        system_prompt="""You are a Data Analysis Specialist focused on insight extraction and pattern recognition.
        
        Your expertise:
        - Data analysis and interpretation
        - Pattern recognition and trend identification
        - Statistical analysis and correlation discovery
        - Insight synthesis and conclusion development
        - Analytical reasoning and logic application
        
        When you receive research data:
        1. Analyze the provided research thoroughly
        2. Identify key patterns, trends, and relationships
        3. Draw meaningful insights from the data
        4. Develop evidence-based conclusions
        5. Prepare analytical findings for fact-checking
        
        Provide deep, evidence-based analysis with clear reasoning.""",
        tools=[current_time, calculator]
    )
    
    fact_checker = Agent(
        name="fact_checker",
        model="us.amazon.nova-lite-v1:0",
        system_prompt="""You are a Fact-Checking Specialist focused on accuracy verification and validation.
        
        Your expertise:
        - Fact verification and accuracy checking
        - Source credibility assessment
        - Bias detection and mitigation
        - Logical consistency validation
        - Error identification and correction
        
        When you receive analysis results:
        1. Verify the accuracy of key claims and findings
        2. Check for logical consistency in conclusions
        3. Identify potential biases or errors
        4. Validate source credibility and reliability
        5. Provide accuracy assessment for final reporting
        
        Ensure high accuracy and reliability of all information.""",
        tools=[current_time, calculator]
    )
    
    report_writer = Agent(
        name="report_writer",
        model="us.amazon.nova-lite-v1:0",
        system_prompt="""You are a Report Writing Specialist focused on comprehensive documentation and presentation.
        
        Your expertise:
        - Professional report writing and structure
        - Clear communication and presentation
        - Executive summary creation
        - Data visualization recommendations
        - Stakeholder-focused content development
        
        When you receive verified analysis:
        1. Synthesize all previous work into a comprehensive report
        2. Structure information for maximum clarity and impact
        3. Create executive summaries and key findings
        4. Recommend visualizations and supporting materials
        5. Ensure professional presentation and readability
        
        Deliver polished, professional reports ready for stakeholders.""",
        tools=[current_time, calculator]
    )
    
    # Build the sequential pipeline graph
    builder = GraphBuilder()
    
    # Add nodes
    builder.add_node(researcher, "research")
    builder.add_node(analyst, "analysis")
    builder.add_node(fact_checker, "fact_check")
    builder.add_node(report_writer, "report")
    
    # Add sequential edges
    builder.add_edge("research", "analysis")
    builder.add_edge("analysis", "fact_check")
    builder.add_edge("fact_check", "report")
    
    # Set entry point
    builder.set_entry_point("research")
    
    return builder.build()


def create_parallel_processing_graph():
    """
    Create a parallel processing graph with coordination and aggregation.
    
    Topology: Coordinator -> [Worker1, Worker2, Worker3] -> Aggregator
    """
    
    # Coordinator agent
    coordinator = Agent(
        name="coordinator",
        model="us.amazon.nova-lite-v1:0",
        system_prompt="""You are a Task Coordination Specialist focused on work distribution and planning.
        
        Your expertise:
        - Task decomposition and work breakdown
        - Resource allocation and distribution
        - Parallel workflow design
        - Team coordination and management
        - Progress tracking and oversight
        
        When you receive a complex task:
        1. Analyze the task scope and requirements
        2. Break down the work into parallel workstreams
        3. Define clear objectives for each workstream
        4. Provide detailed instructions for parallel processing
        5. Set up coordination framework for team collaboration
        
        Organize work efficiently for parallel execution by specialist teams.""",
        tools=[current_time, calculator]
    )
    
    # Specialized worker agents
    technical_worker = Agent(
        name="technical_worker",
        model="us.amazon.nova-lite-v1:0",
        system_prompt="""You are a Technical Analysis Worker focused on technical aspects and implementation details.
        
        Your expertise:
        - Technical feasibility analysis
        - System architecture and design
        - Technology evaluation and selection
        - Implementation planning and requirements
        - Technical risk assessment
        
        Focus on technical dimensions of the assigned work.""",
        tools=[current_time, calculator, file_read]
    )
    
    business_worker = Agent(
        name="business_worker",
        model="us.amazon.nova-lite-v1:0",
        system_prompt="""You are a Business Analysis Worker focused on business value and strategy.
        
        Your expertise:
        - Business case development
        - Market analysis and positioning
        - ROI analysis and financial modeling
        - Stakeholder impact assessment
        - Business strategy alignment
        
        Focus on business dimensions of the assigned work.""",
        tools=[current_time, calculator]
    )
    
    operations_worker = Agent(
        name="operations_worker",
        model="us.amazon.nova-lite-v1:0",
        system_prompt="""You are an Operations Analysis Worker focused on operational efficiency and execution.
        
        Your expertise:
        - Process design and optimization
        - Resource planning and allocation
        - Operational risk management
        - Performance metrics and monitoring
        - Implementation logistics
        
        Focus on operational dimensions of the assigned work.""",
        tools=[current_time, calculator]
    )
    
    # Aggregator agent
    aggregator = Agent(
        name="aggregator",
        model="us.amazon.nova-lite-v1:0",
        system_prompt="""You are a Results Aggregation Specialist focused on synthesis and integration.
        
        Your expertise:
        - Multi-dimensional analysis synthesis
        - Cross-functional integration
        - Conflict resolution and harmonization
        - Comprehensive recommendation development
        - Strategic decision support
        
        When you receive parallel work results:
        1. Analyze all parallel workstream outputs
        2. Identify synergies and conflicts between approaches
        3. Synthesize findings into unified recommendations
        4. Develop integrated implementation strategy
        5. Provide comprehensive final assessment
        
        Create unified, actionable recommendations from diverse inputs.""",
        tools=[current_time, calculator]
    )
    
    # Build the parallel processing graph
    builder = GraphBuilder()
    
    # Add nodes
    builder.add_node(coordinator, "coordinator")
    builder.add_node(technical_worker, "technical_worker")
    builder.add_node(business_worker, "business_worker")
    builder.add_node(operations_worker, "operations_worker")
    builder.add_node(aggregator, "aggregator")
    
    # Add edges for parallel processing
    builder.add_edge("coordinator", "technical_worker")
    builder.add_edge("coordinator", "business_worker")
    builder.add_edge("coordinator", "operations_worker")
    
    # Aggregate results
    builder.add_edge("technical_worker", "aggregator")
    builder.add_edge("business_worker", "aggregator")
    builder.add_edge("operations_worker", "aggregator")
    
    # Set entry point
    builder.set_entry_point("coordinator")
    
    return builder.build()


def create_conditional_branching_graph():
    """
    Create a conditional branching graph with dynamic workflow routing.
    
    Topology: Classifier -> [Technical Path OR Business Path] -> Specialized Reports
    """
    
    # Classifier agent
    classifier = Agent(
        name="classifier",
        model="us.amazon.nova-lite-v1:0",
        system_prompt="""You are a Task Classification Specialist focused on intelligent workflow routing.
        
        Your expertise:
        - Task analysis and categorization
        - Domain identification and classification
        - Workflow routing decisions
        - Requirements assessment
        - Complexity evaluation
        
        When you receive a task:
        1. Analyze the task domain and requirements
        2. Determine if it's primarily TECHNICAL or BUSINESS focused
        3. Assess complexity and specialized needs
        4. Make clear routing recommendation
        5. Provide reasoning for classification decision
        
        IMPORTANT: Include either "TECHNICAL" or "BUSINESS" clearly in your response to indicate the routing decision.
        
        Make intelligent routing decisions for optimal workflow execution.""",
        tools=[current_time, calculator]
    )
    
    # Technical specialists
    technical_specialist = Agent(
        name="technical_specialist",
        model="us.amazon.nova-lite-v1:0",
        system_prompt="""You are a Technical Domain Specialist focused on deep technical analysis and solutions.
        
        Your expertise:
        - Advanced technical analysis
        - System design and architecture
        - Technology implementation planning
        - Technical risk assessment
        - Engineering best practices
        
        Handle complex technical tasks requiring specialized technical expertise.""",
        tools=[current_time, calculator, file_read]
    )
    
    business_specialist = Agent(
        name="business_specialist",
        model="us.amazon.nova-lite-v1:0",
        system_prompt="""You are a Business Domain Specialist focused on strategic business analysis and planning.
        
        Your expertise:
        - Strategic business analysis
        - Market research and competitive analysis
        - Business model development
        - Financial planning and ROI analysis
        - Stakeholder management
        
        Handle complex business tasks requiring specialized business expertise.""",
        tools=[current_time, calculator]
    )
    
    # Specialized report writers
    technical_reporter = Agent(
        name="technical_reporter",
        model="us.amazon.nova-lite-v1:0",
        system_prompt="""You are a Technical Report Writer specialized in technical documentation and communication.
        
        Create comprehensive technical reports with:
        - Detailed technical specifications
        - Implementation recommendations
        - Technical risk assessments
        - Architecture diagrams descriptions
        - Engineering guidelines
        
        Deliver technical reports for engineering and technical stakeholders.""",
        tools=[current_time, calculator]
    )
    
    business_reporter = Agent(
        name="business_reporter",
        model="us.amazon.nova-lite-v1:0",
        system_prompt="""You are a Business Report Writer specialized in executive communication and strategic documentation.
        
        Create comprehensive business reports with:
        - Executive summaries
        - Strategic recommendations
        - Financial projections
        - Business impact assessments
        - Implementation roadmaps
        
        Deliver business reports for executives and business stakeholders.""",
        tools=[current_time, calculator]
    )
    
    # Define conditional functions
    def is_technical_task(state):
        """Check if the classifier determined this is a technical task."""
        classifier_result = state.results.get("classifier")
        if not classifier_result:
            return False
        
        result_text = str(classifier_result.result)
        return "TECHNICAL" in result_text.upper()
    
    def is_business_task(state):
        """Check if the classifier determined this is a business task."""
        classifier_result = state.results.get("classifier")
        if not classifier_result:
            return False
        
        result_text = str(classifier_result.result)
        return "BUSINESS" in result_text.upper()
    
    # Build the conditional branching graph
    builder = GraphBuilder()
    
    # Add nodes
    builder.add_node(classifier, "classifier")
    builder.add_node(technical_specialist, "technical_specialist")
    builder.add_node(business_specialist, "business_specialist")
    builder.add_node(technical_reporter, "technical_reporter")
    builder.add_node(business_reporter, "business_reporter")
    
    # Add conditional edges
    builder.add_edge("classifier", "technical_specialist", condition=is_technical_task)
    builder.add_edge("classifier", "business_specialist", condition=is_business_task)
    builder.add_edge("technical_specialist", "technical_reporter")
    builder.add_edge("business_specialist", "business_reporter")
    
    # Set entry point
    builder.set_entry_point("classifier")
    
    return builder.build()


def create_hybrid_custom_nodes_graph():
    """
    Create a hybrid graph combining AI agents with custom deterministic nodes.
    
    Topology: AI Input Processing -> Data Validation -> Business Rules -> AI Output Generation
    """
    
    # AI input processor
    input_processor = Agent(
        name="input_processor",
        model="us.amazon.nova-lite-v1:0",
        system_prompt="""You are an Input Processing Specialist focused on preparing and structuring data for analysis.
        
        Your expertise:
        - Data preprocessing and cleaning
        - Input validation and formatting
        - Content structure analysis
        - Requirements extraction
        - Data preparation for downstream processing
        
        When you receive raw input:
        1. Analyze and understand the input content
        2. Extract key requirements and constraints
        3. Structure the data for downstream processing
        4. Identify any potential issues or concerns
        5. Prepare clean, well-formatted output for validation
        
        Ensure data is properly prepared for deterministic processing.""",
        tools=[current_time, calculator]
    )
    
    # AI output generator
    output_generator = Agent(
        name="output_generator",
        model="us.amazon.nova-lite-v1:0",
        system_prompt="""You are an Output Generation Specialist focused on creating final deliverables from processed data.
        
        Your expertise:
        - Professional output formatting
        - Comprehensive result synthesis
        - User-friendly presentation
        - Quality assurance and final review
        - Stakeholder communication
        
        When you receive validated and processed data:
        1. Synthesize all processing results into final output
        2. Ensure professional formatting and presentation
        3. Include validation results and business rule compliance
        4. Provide clear, actionable recommendations
        5. Create comprehensive final deliverable
        
        Deliver polished, professional final results.""",
        tools=[current_time, calculator]
    )
    
    # Custom deterministic nodes
    data_validator = DataValidationNode("data_validator")
    
    business_rules = BusinessRulesNode(
        rules={
            "min_length": {"value": 50},
            "required_keywords": {"keywords": ["analysis", "recommendation", "implementation"]},
            "forbidden_terms": {"terms": ["confidential", "internal", "secret"]}
        },
        name="business_rules"
    )
    
    # Build the hybrid graph
    builder = GraphBuilder()
    
    # Add nodes (mix of AI agents and custom nodes)
    builder.add_node(input_processor, "input_processor")
    builder.add_node(data_validator, "data_validator")
    builder.add_node(business_rules, "business_rules")
    builder.add_node(output_generator, "output_generator")
    
    # Add edges
    builder.add_edge("input_processor", "data_validator")
    builder.add_edge("data_validator", "business_rules")
    builder.add_edge("business_rules", "output_generator")
    
    # Set entry point
    builder.set_entry_point("input_processor")
    
    return builder.build()


# ===============================
# GRAPH ORCHESTRATOR
# ===============================

class GraphOrchestrator:
    """
    Orchestrator for managing different graph topologies and demonstrating Graph pattern capabilities.
    
    This class provides a unified interface for working with different graph configurations
    and shows how deterministic, dependency-based agent coordination works in practice.
    """
    
    def __init__(self):
        """Initialize the graph orchestrator with different graph types."""
        logger.info("📊 Initializing Graph Orchestrator...")
        
        # Create different graph topologies
        self.graphs = {
            "research_analysis": create_research_analysis_graph(),
            "parallel_processing": create_parallel_processing_graph(),
            "conditional_branching": create_conditional_branching_graph(),
            "hybrid_custom_nodes": create_hybrid_custom_nodes_graph()
        }
        
        logger.info(f"✅ Graph Orchestrator initialized with {len(self.graphs)} graph types")
    
    def execute_graph(self, graph_type: str, task: str) -> Dict[str, Any]:
        """
        Execute a specific graph type on a given task.
        
        Args:
            graph_type: Type of graph to execute
            task: Task description to process
            
        Returns:
            Dict containing execution results and metadata
        """
        if graph_type not in self.graphs:
            available_types = list(self.graphs.keys())
            raise ValueError(f"Unknown graph type: {graph_type}. Available: {available_types}")
        
        logger.info(f"📊 Executing {graph_type} graph on task: {task[:100]}...")
        
        try:
            # Execute the graph
            graph = self.graphs[graph_type]
            result = graph(task)
            
            # Extract execution information
            execution_info = {
                "status": str(result.status),
                "graph_type": graph_type,
                "task": task,
                "execution_order": [node.node_id for node in result.execution_order],
                "total_nodes": result.total_nodes,
                "completed_nodes": result.completed_nodes,
                "failed_nodes": result.failed_nodes,
                "execution_time_ms": getattr(result, 'execution_time', 0),
                "node_results": {},
                "final_output": ""
            }
            
            # Get individual node results
            if hasattr(result, 'results'):
                for node_id, node_result in result.results.items():
                    if hasattr(node_result, 'result'):
                        execution_info["node_results"][node_id] = str(node_result.result)
            
            # Extract final output (typically from the last executed node)
            if result.execution_order:
                last_node_id = result.execution_order[-1].node_id
                if last_node_id in execution_info["node_results"]:
                    execution_info["final_output"] = execution_info["node_results"][last_node_id]
            
            logger.info(f"✅ Graph execution completed: {result.status}")
            return execution_info
            
        except Exception as e:
            logger.error(f"❌ Error executing graph: {e}")
            return {
                "status": "FAILED",
                "error": str(e),
                "graph_type": graph_type,
                "task": task
            }
    
    async def execute_graph_async(self, graph_type: str, task: str) -> Dict[str, Any]:
        """
        Execute a graph asynchronously.
        
        Args:
            graph_type: Type of graph to execute
            task: Task description to process
            
        Returns:
            Dict containing execution results and metadata
        """
        if graph_type not in self.graphs:
            available_types = list(self.graphs.keys())
            raise ValueError(f"Unknown graph type: {graph_type}. Available: {available_types}")
        
        logger.info(f"📊 Executing {graph_type} graph async on task: {task[:100]}...")
        
        try:
            # Execute the graph asynchronously
            graph = self.graphs[graph_type]
            result = await graph.invoke_async(task)
            
            # Process results same as synchronous execution
            execution_info = {
                "status": str(result.status),
                "graph_type": graph_type,
                "task": task,
                "execution_order": [node.node_id for node in result.execution_order],
                "total_nodes": result.total_nodes,
                "completed_nodes": result.completed_nodes,
                "failed_nodes": result.failed_nodes,
                "execution_time_ms": getattr(result, 'execution_time', 0),
                "node_results": {},
                "final_output": ""
            }
            
            # Get individual node results
            if hasattr(result, 'results'):
                for node_id, node_result in result.results.items():
                    if hasattr(node_result, 'result'):
                        execution_info["node_results"][node_id] = str(node_result.result)
            
            # Extract final output
            if result.execution_order:
                last_node_id = result.execution_order[-1].node_id
                if last_node_id in execution_info["node_results"]:
                    execution_info["final_output"] = execution_info["node_results"][last_node_id]
            
            logger.info(f"✅ Async graph execution completed: {result.status}")
            return execution_info
            
        except Exception as e:
            logger.error(f"❌ Error executing async graph: {e}")
            return {
                "status": "FAILED",
                "error": str(e),
                "graph_type": graph_type,
                "task": task
            }
    
    def demonstrate_graphs(self):
        """Demonstrate different graph topologies with example tasks."""
        
        print("\n" + "="*80)
        print("📊 GRAPH MULTI-AGENT PATTERN DEMONSTRATIONS")
        print("="*80)
        
        demonstrations = [
            {
                "name": "Research Analysis Pipeline",
                "graph_type": "research_analysis",
                "task": "Research the impact of artificial intelligence on healthcare delivery and create a comprehensive analysis report",
                "description": "Sequential pipeline: Research → Analysis → Fact-Check → Report"
            },
            {
                "name": "Parallel Processing Workflow",
                "graph_type": "parallel_processing",
                "task": "Develop a comprehensive strategy for implementing AI-powered customer service platform",
                "description": "Parallel processing: Coordinator → [Technical, Business, Operations] → Aggregator"
            },
            {
                "name": "Conditional Branching Logic",
                "graph_type": "conditional_branching",
                "task": "Design a real-time fraud detection system for financial transactions",
                "description": "Conditional routing: Classifier → [Technical OR Business Path] → Specialized Reports"
            },
            {
                "name": "Hybrid Custom Nodes",
                "graph_type": "hybrid_custom_nodes",
                "task": "Process customer feedback data and generate actionable business recommendations with compliance validation",
                "description": "Hybrid workflow: AI Processing → Data Validation → Business Rules → AI Output"
            }
        ]
        
        for i, demo in enumerate(demonstrations, 1):
            print(f"\n📊 Demo {i}: {demo['name']}")
            print("─" * 50)
            print(f"📋 Task: {demo['task']}")
            print(f"🏗️ Topology: {demo['description']}")
            print(f"📊 Graph Type: {demo['graph_type']}")
            print("🔄 Starting graph execution...")
            
            try:
                result = self.execute_graph(demo['graph_type'], demo['task'])
                
                print(f"\n✅ Status: {result['status']}")
                print(f"📈 Execution Order: {' → '.join(result.get('execution_order', []))}")
                print(f"📊 Nodes Completed: {result.get('completed_nodes', 0)}/{result.get('total_nodes', 0)}")
                print(f"⏱️ Execution Time: {result.get('execution_time_ms', 0)}ms")
                
                if result['status'] == "COMPLETED" and result.get('final_output'):
                    print(f"\n🎯 Final Result Preview:")
                    output_preview = result['final_output'][:400] + "..." if len(result['final_output']) > 400 else result['final_output']
                    print(output_preview)
                
                print(f"\n{'✅ Demo completed successfully!' if result['status'] == 'COMPLETED' else '❌ Demo encountered issues!'}")
                
            except Exception as e:
                print(f"❌ Demo failed: {e}")
            
            if i < len(demonstrations):
                print("\n" + "─" * 50)
        
        print(f"\n{'='*80}")
        print("📊 All Graph Pattern Demonstrations Completed!")
        print("="*80)
    
    def interactive_mode(self):
        """Interactive mode for custom graph execution."""
        
        print("\n" + "="*60)
        print("🎮 INTERACTIVE GRAPH EXECUTION MODE")
        print("="*60)
        
        available_graphs = list(self.graphs.keys())
        print("\nAvailable Graph Types:")
        for i, graph_type in enumerate(available_graphs, 1):
            print(f"{i}. {graph_type}")
        
        while True:
            try:
                print(f"\n{'─'*40}")
                choice = input("\nSelect graph type (1-4) or 'quit' to exit: ").strip().lower()
                
                if choice in ['quit', 'q', 'exit']:
                    print("👋 Exiting interactive mode...")
                    break
                
                try:
                    graph_index = int(choice) - 1
                    if 0 <= graph_index < len(available_graphs):
                        selected_graph = available_graphs[graph_index]
                    else:
                        print("❌ Invalid choice. Please select 1-4.")
                        continue
                except ValueError:
                    print("❌ Invalid input. Please enter a number 1-4 or 'quit'.")
                    continue
                
                task = input(f"\nEnter task for {selected_graph} graph: ").strip()
                if not task:
                    print("❌ Task cannot be empty.")
                    continue
                
                print(f"\n🔄 Executing {selected_graph} graph...")
                result = self.execute_graph(selected_graph, task)
                
                print(f"\n✅ Status: {result['status']}")
                print(f"📈 Execution Order: {' → '.join(result.get('execution_order', []))}")
                print(f"⏱️ Execution Time: {result.get('execution_time_ms', 0)}ms")
                
                if result['status'] == "COMPLETED" and result.get('final_output'):
                    print(f"\n🎯 Final Result:")
                    print(result['final_output'])
                
            except KeyboardInterrupt:
                print("\n👋 Exiting interactive mode...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")


# ===============================
# MAIN EXECUTION
# ===============================

def main():
    """Main function to demonstrate Graph multi-agent patterns."""
    
    print("📊 Graph Multi-Agent Pattern Example")
    print("=" * 50)
    print("This example demonstrates deterministic, dependency-based agent coordination")
    print("using Directed Acyclic Graphs (DAGs) with multiple topology patterns.")
    print()
    
    try:
        # Initialize orchestrator
        orchestrator = GraphOrchestrator()
        
        # Run demonstrations
        orchestrator.demonstrate_graphs()
        
        # Interactive mode
        print(f"\n🎮 Ready for interactive mode!")
        print("You can now test custom tasks with different graph topologies.")
        
        orchestrator.interactive_mode()
        
    except KeyboardInterrupt:
        print("\n👋 Graph pattern demonstration interrupted by user")
    except Exception as e:
        logger.error(f"❌ Error in main execution: {e}")
        print(f"❌ An error occurred: {e}")


if __name__ == "__main__":
    main()

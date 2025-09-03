#!/usr/bin/env python3
"""
Simplified Workflow Multi-Agent Pattern Example
Demonstrates sequential task execution with minimal token usage
"""

import os
import sys
import json
import time
import logging
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)

# Import Strands components
try:
    from strands import Agent
    logger.info("✅ Successfully imported Strands modules")
except ImportError as e:
    logger.error(f"❌ Failed to import Strands: {e}")
    print("Please ensure Strands is installed: pip install strands")
    sys.exit(1)

class TaskStatus(Enum):
    """Task execution status"""
    PENDING = "pending"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class SimpleTask:
    """Simplified workflow task"""
    task_id: str
    description: str
    system_prompt: str
    dependencies: List[str]
    status: TaskStatus = TaskStatus.PENDING

@dataclass
class WorkflowResult:
    """Workflow execution result"""
    workflow_id: str
    status: str
    completed_tasks: int
    total_tasks: int
    execution_time_ms: float
    task_results: Dict[str, str]
    final_output: str

class SimpleWorkflowEngine:
    """Simplified workflow execution engine"""
    
    def __init__(self, workflow_id: str):
        self.workflow_id = workflow_id
        self.tasks: Dict[str, SimpleTask] = {}
        self.task_results: Dict[str, str] = {}
        self.execution_order: List[str] = []
        
        # Initialize shared agent
        self.agent = Agent(
            model="us.amazon.nova-lite-v1:0",
            system_prompt="You are a helpful assistant that provides concise, focused responses."
        )
        logger.info(f"🤖 Initialized workflow agent")
    
    def add_task(self, task: SimpleTask):
        """Add task to workflow"""
        self.tasks[task.task_id] = task
        logger.info(f"📋 Added task '{task.task_id}' to workflow")
    
    def get_ready_tasks(self) -> List[str]:
        """Get tasks ready for execution"""
        ready_tasks = []
        for task_id, task in self.tasks.items():
            if task.status == TaskStatus.PENDING:
                # Check if all dependencies are completed
                deps_satisfied = all(
                    self.tasks.get(dep_id, SimpleTask("", "", "", [])).status == TaskStatus.COMPLETED
                    for dep_id in task.dependencies
                )
                if deps_satisfied:
                    task.status = TaskStatus.READY
                    ready_tasks.append(task_id)
        return ready_tasks
    
    def build_context(self, task_id: str) -> str:
        """Build context from previous tasks"""
        task = self.tasks[task_id]
        if not task.dependencies:
            return task.description
        
        context_parts = [f"Previous results:"]
        for dep_id in task.dependencies:
            if dep_id in self.task_results:
                result = self.task_results[dep_id][:200]  # Limit context
                context_parts.append(f"- {dep_id}: {result}")
        
        context_parts.append(f"Current task: {task.description}")
        return "\n".join(context_parts)
    
    def execute_task(self, task_id: str) -> bool:
        """Execute a single task"""
        task = self.tasks[task_id]
        task.status = TaskStatus.RUNNING
        
        try:
            logger.info(f"🔄 Executing task '{task_id}'...")
            
            # Build context and execute
            context = self.build_context(task_id)
            self.agent.system_prompt = task.system_prompt
            
            result = self.agent(context)
            
            # Store result (limit length to save tokens)
            self.task_results[task_id] = str(result)[:500]
            task.status = TaskStatus.COMPLETED
            self.execution_order.append(task_id)
            
            logger.info(f"✅ Task '{task_id}' completed")
            return True
            
        except Exception as e:
            logger.error(f"❌ Task '{task_id}' failed: {e}")
            task.status = TaskStatus.FAILED
            return False
    
    def execute_workflow(self) -> WorkflowResult:
        """Execute the complete workflow"""
        start_time = time.time()
        logger.info(f"🚀 Starting workflow '{self.workflow_id}' execution...")
        
        # Execute tasks in dependency order
        while True:
            ready_tasks = self.get_ready_tasks()
            if not ready_tasks:
                break
            
            # Execute ready tasks (one at a time for simplicity)
            for task_id in ready_tasks:
                if not self.execute_task(task_id):
                    break
        
        # Build final result
        execution_time = (time.time() - start_time) * 1000
        completed_count = sum(1 for task in self.tasks.values() if task.status == TaskStatus.COMPLETED)
        
        # Create final output from last task
        final_output = ""
        if self.execution_order:
            last_task = self.execution_order[-1]
            final_output = self.task_results.get(last_task, "No output generated")
        
        result = WorkflowResult(
            workflow_id=self.workflow_id,
            status="completed" if completed_count == len(self.tasks) else "partial",
            completed_tasks=completed_count,
            total_tasks=len(self.tasks),
            execution_time_ms=execution_time,
            task_results=self.task_results,
            final_output=final_output
        )
        
        logger.info(f"🏁 Workflow '{self.workflow_id}' completed: {result.status}")
        return result

def create_simple_analysis_workflow() -> SimpleWorkflowEngine:
    """Create a simple 3-step analysis workflow"""
    workflow = SimpleWorkflowEngine("simple_analysis")
    
    # Step 1: Research
    research_task = SimpleTask(
        task_id="research",
        description="Research the topic and gather key information",
        system_prompt="You are a researcher. Provide a brief summary (2-3 sentences) of key findings about the topic. Be concise.",
        dependencies=[]
    )
    
    # Step 2: Analysis
    analysis_task = SimpleTask(
        task_id="analysis",
        description="Analyze the research findings",
        system_prompt="You are an analyst. Based on the research, provide 2-3 key insights or conclusions. Be concise.",
        dependencies=["research"]
    )
    
    # Step 3: Summary
    summary_task = SimpleTask(
        task_id="summary",
        description="Create a final summary",
        system_prompt="You are a summarizer. Create a brief final summary (2-3 sentences) combining the research and analysis. Be concise.",
        dependencies=["analysis"]
    )
    
    workflow.add_task(research_task)
    workflow.add_task(analysis_task)
    workflow.add_task(summary_task)
    
    return workflow

def create_simple_content_workflow() -> SimpleWorkflowEngine:
    """Create a simple 3-step content creation workflow"""
    workflow = SimpleWorkflowEngine("simple_content")
    
    # Step 1: Planning
    planning_task = SimpleTask(
        task_id="planning",
        description="Plan the content structure and key points",
        system_prompt="You are a content planner. Create a brief outline (3-4 key points) for the content. Be concise.",
        dependencies=[]
    )
    
    # Step 2: Writing
    writing_task = SimpleTask(
        task_id="writing",
        description="Write the content based on the plan",
        system_prompt="You are a writer. Based on the plan, write a brief piece of content (3-4 sentences). Be concise.",
        dependencies=["planning"]
    )
    
    # Step 3: Review
    review_task = SimpleTask(
        task_id="review",
        description="Review and finalize the content",
        system_prompt="You are an editor. Review the content and provide a final polished version (3-4 sentences). Be concise.",
        dependencies=["writing"]
    )
    
    workflow.add_task(planning_task)
    workflow.add_task(writing_task)
    workflow.add_task(review_task)
    
    return workflow

class SimpleWorkflowOrchestrator:
    """Simplified workflow orchestrator"""
    
    def __init__(self):
        logger.info("⚙️ Initializing Simple Workflow Orchestrator...")
        self.workflows = {}
        logger.info("✅ Simple Workflow Orchestrator ready")
    
    def run_analysis_workflow(self, task_description: str) -> Dict[str, Any]:
        """Run a simple analysis workflow"""
        workflow = create_simple_analysis_workflow()
        
        # Execute with the given task
        # Modify first task description
        workflow.tasks["research"].description = f"Research: {task_description}"
        
        result = workflow.execute_workflow()
        
        return {
            "workflow_id": result.workflow_id,
            "status": result.status,
            "completed_tasks": result.completed_tasks,
            "total_tasks": result.total_tasks,
            "execution_time_ms": result.execution_time_ms,
            "task_results": result.task_results,
            "execution_order": workflow.execution_order,
            "final_output": result.final_output
        }
    
    def run_content_workflow(self, task_description: str) -> Dict[str, Any]:
        """Run a simple content creation workflow"""
        workflow = create_simple_content_workflow()
        
        # Execute with the given task
        # Modify first task description
        workflow.tasks["planning"].description = f"Plan content for: {task_description}"
        
        result = workflow.execute_workflow()
        
        return {
            "workflow_id": result.workflow_id,
            "status": result.status,
            "completed_tasks": result.completed_tasks,
            "total_tasks": result.total_tasks,
            "execution_time_ms": result.execution_time_ms,
            "task_results": result.task_results,
            "execution_order": workflow.execution_order,
            "final_output": result.final_output
        }

def demo_simple_workflows():
    """Demonstrate simple workflow patterns"""
    print("\n" + "="*60)
    print("🔄 SIMPLE WORKFLOW PATTERN DEMONSTRATION")
    print("="*60)
    
    orchestrator = SimpleWorkflowOrchestrator()
    
    # Demo 1: Analysis Workflow
    print("\n⚙️ Demo 1: Simple Analysis Workflow")
    print("─" * 40)
    print("📋 Task: Analyze the benefits of renewable energy")
    print("🏗️ Pipeline: Research → Analysis → Summary")
    
    result1 = orchestrator.run_analysis_workflow("benefits of renewable energy")
    
    print(f"\n✅ Status: {result1['status'].upper()}")
    print(f"📈 Execution Order: {' → '.join(result1['execution_order'])}")
    print(f"📊 Tasks Completed: {result1['completed_tasks']}/{result1['total_tasks']}")
    print(f"⏱️ Execution Time: {result1['execution_time_ms']:.0f}ms")
    print(f"\n🎯 Final Result:\n{result1['final_output']}")
    
    # Demo 2: Content Workflow
    print("\n⚙️ Demo 2: Simple Content Creation Workflow")
    print("─" * 40)
    print("📋 Task: Create content about AI in healthcare")
    print("🏗️ Pipeline: Planning → Writing → Review")
    
    result2 = orchestrator.run_content_workflow("AI applications in healthcare")
    
    print(f"\n✅ Status: {result2['status'].upper()}")
    print(f"📈 Execution Order: {' → '.join(result2['execution_order'])}")
    print(f"📊 Tasks Completed: {result2['completed_tasks']}/{result2['total_tasks']}")
    print(f"⏱️ Execution Time: {result2['execution_time_ms']:.0f}ms")
    print(f"\n🎯 Final Result:\n{result2['final_output']}")
    
    print("\n" + "="*60)
    print("✨ WORKFLOW PATTERN FEATURES DEMONSTRATED:")
    print("• Sequential task execution with dependencies")
    print("• Context passing between workflow stages")
    print("• Task status tracking and monitoring")
    print("• Structured pipeline processing")
    print("• Minimal token usage for efficiency")
    print("="*60)

def interactive_mode():
    """Interactive workflow demonstration"""
    print("\n🎮 Interactive Workflow Mode")
    print("Choose a workflow type:")
    print("1. Analysis Workflow (Research → Analysis → Summary)")
    print("2. Content Workflow (Planning → Writing → Review)")
    print("3. Exit")
    
    orchestrator = SimpleWorkflowOrchestrator()
    
    while True:
        try:
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == "3":
                print("👋 Goodbye!")
                break
            elif choice in ["1", "2"]:
                task = input("Enter your task description: ").strip()
                if not task:
                    print("❌ Please provide a task description")
                    continue
                
                print(f"\n🚀 Executing workflow...")
                start_time = time.time()
                
                if choice == "1":
                    result = orchestrator.run_analysis_workflow(task)
                else:
                    result = orchestrator.run_content_workflow(task)
                
                duration = time.time() - start_time
                
                print(f"\n✅ Workflow completed in {duration:.1f}s")
                print(f"📊 Status: {result['status']}")
                print(f"📈 Pipeline: {' → '.join(result['execution_order'])}")
                print(f"\n🎯 Final Output:\n{result['final_output']}")
                
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
            interactive_mode()
        else:
            demo_simple_workflows()
            
    except KeyboardInterrupt:
        print("\n⚠️ Demo interrupted by user")
    except Exception as e:
        logger.error(f"💥 Unexpected error: {e}")
        print(f"❌ Error running workflow demo: {e}")

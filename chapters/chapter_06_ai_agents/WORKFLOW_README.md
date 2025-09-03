# Workflow Multi-Agent Pattern Example

This example demonstrates the **"Workflow"** pattern, where agents are organized in sequential processing pipelines with clear dependencies, structured task management, and coordinated information flow between stages.

**Note**: This implementation is optimized for token efficiency while maintaining educational value and demonstrating all key workflow concepts.

## ⚙️ Workflow Architecture Overview

```
Task Input
    ↓
🔄 Sequential Processing Pipeline
┌─────────────────────────────────────────┐
│  Task 1 → Task 2 → Task 3 → Task 4     │
│     ↓        ↓        ↓        ↓       │
│ Agent A  Agent B  Agent C  Agent D     │
│                                         │
│ Dependencies: A → B → C → D             │
│ Context Flow: Output becomes Input      │
└─────────────────────────────────────────┘
    ↓
Structured Result with Full Pipeline Context
```

### Key Workflow Characteristics

1. **Sequential Execution**: Tasks execute in defined order based on dependencies
2. **Context Preservation**: Output from one stage becomes input for the next
3. **Dependency Management**: Clear task relationships and execution prerequisites
4. **Status Tracking**: Comprehensive monitoring of task progress and completion
5. **Error Recovery**: Retry mechanisms and failure handling at task level

## 🔧 Workflow Components

### 1. WorkflowTask
Represents a single task in the workflow:
- **task_id**: Unique identifier for the task
- **description**: Clear description of task objectives
- **system_prompt**: Specialized instructions for the agent
- **dependencies**: List of prerequisite tasks
- **priority**: Execution priority (higher numbers = higher priority)
- **status**: Current execution status (PENDING, READY, RUNNING, COMPLETED, FAILED)

### 2. WorkflowEngine
Core execution engine that manages:
- **Task Dependencies**: Ensures tasks execute in correct order
- **Context Building**: Combines outputs from dependency tasks
- **Status Management**: Tracks progress and handles failures
- **Execution Coordination**: Orchestrates the entire pipeline

### 3. Task Status Management
```python
class TaskStatus(Enum):
    PENDING = "pending"      # Waiting for dependencies
    READY = "ready"          # Dependencies satisfied, ready to run
    RUNNING = "running"      # Currently executing
    COMPLETED = "completed"  # Successfully finished
    FAILED = "failed"        # Failed after retries
    SKIPPED = "skipped"      # Skipped due to conditions
```

## 🏗️ Workflow Templates Implemented

### 1. Data Analysis Workflow 📊

**Pipeline**: Data Extraction → Cleaning → Analysis → Visualization → Report

**Agents**:
- **Data Extraction Specialist**: Identifies and gathers relevant data sources
- **Data Cleaning Specialist**: Preprocesses and improves data quality
- **Data Analysis Specialist**: Performs statistical analysis and pattern recognition
- **Data Visualization Specialist**: Creates clear, impactful visual representations
- **Report Generation Specialist**: Synthesizes findings into professional reports

**Example Task**: "Analyze customer satisfaction survey data to identify improvement areas"

**Flow**:
```
Input: Customer satisfaction survey request
→ Data Extraction: Identify survey data sources and collection methods
→ Data Cleaning: Clean and preprocess survey responses
→ Data Analysis: Perform statistical analysis and identify patterns
→ Data Visualization: Create charts and visual summaries
→ Report Generation: Generate comprehensive analysis report
```

### 2. Content Production Workflow 📝

**Pipeline**: Research → Writing → Editing → Design → Publishing

**Agents**:
- **Content Research Specialist**: Topic research, audience analysis, and strategy
- **Content Writing Specialist**: Creates engaging, well-structured content
- **Content Editing Specialist**: Refines content for clarity and impact
- **Design and Layout Specialist**: Creates visual design and presentation
- **Content Publishing Specialist**: Develops distribution and promotion strategy

**Example Task**: "Create comprehensive blog post about AI trends in healthcare"

**Flow**:
```
Input: AI healthcare blog post request
→ Content Research: Research AI trends, audience needs, and competition
→ Content Writing: Create engaging, informative blog post content
→ Content Editing: Edit for clarity, accuracy, and style consistency
→ Design Layout: Design visual layout and select supporting images
→ Content Publishing: Develop distribution and social media strategy
```

### 3. Software Development Workflow 💻

**Pipeline**: Requirements → Design → Implementation → Testing → Deployment

**Agents**:
- **Requirements Analysis Specialist**: Gathers and documents software requirements
- **System Design Specialist**: Creates architecture and technical specifications
- **Implementation Specialist**: Develops software based on design specifications
- **Testing and QA Specialist**: Validates functionality and ensures quality
- **Deployment and Release Specialist**: Manages production deployment

**Example Task**: "Develop REST API for task management with user authentication"

**Flow**:
```
Input: Task management API development request
→ Requirements Analysis: Define functional and non-functional requirements
→ System Design: Create API architecture and database design
→ Implementation: Code the API endpoints and authentication system
→ Testing & QA: Test functionality, performance, and security
→ Deployment: Deploy to production with monitoring setup
```

## 🚀 Advanced Workflow Features

### Context Passing Between Tasks

```python
def build_task_context(self, task_id: str) -> str:
    """Build context from dependent tasks for the current task."""
    task = self.tasks[task_id]
    context_parts = []
    
    # Add results from dependency tasks
    for dep_id in task.dependencies:
        if dep_id in self.task_results:
            context_parts.append(f"Results from {dep_id}:\n{self.task_results[dep_id]}")
    
    # Build the complete prompt
    prompt = task.description
    if context_parts:
        context_section = "\n\n".join(context_parts)
        prompt = f"Previous task results:\n\n{context_section}\n\nCurrent task:\n{prompt}"
    
    return prompt
```

### Dependency Resolution

```python
def get_ready_tasks(self) -> List[str]:
    """Get tasks that are ready to execute (dependencies satisfied)."""
    ready_tasks = []
    
    for task_id, task in self.tasks.items():
        if task.status == TaskStatus.PENDING:
            # Check if all dependencies are completed
            deps_satisfied = all(
                self.tasks.get(dep_id).status == TaskStatus.COMPLETED
                for dep_id in task.dependencies
            )
            
            if deps_satisfied:
                task.status = TaskStatus.READY
                ready_tasks.append(task_id)
    
    # Sort by priority
    ready_tasks.sort(key=lambda t: self.tasks[t].priority, reverse=True)
    return ready_tasks
```

### Error Handling and Retry Logic

```python
# Automatic retries for failed tasks
task.retry_count += 1
if task.retry_count <= task.max_retries:
    task.status = TaskStatus.PENDING
    logger.warning(f"Task '{task_id}' failed, retrying ({task.retry_count}/{task.max_retries})")
else:
    task.status = TaskStatus.FAILED
    logger.error(f"Task '{task_id}' failed permanently")
```

### Performance Monitoring

```python
@dataclass
class WorkflowResult:
    workflow_id: str
    status: str
    total_tasks: int
    completed_tasks: int
    failed_tasks: int
    execution_time_ms: float
    task_results: Dict[str, Any]
    execution_order: List[str]
    final_output: Optional[str]
```

## 📋 Usage Examples

### Basic Workflow Execution

```bash
python workflow_example.py
```

### What You'll See

1. **Data Analysis Demo**: Customer satisfaction survey analysis pipeline
2. **Content Production Demo**: AI healthcare blog post creation workflow
3. **Software Development Demo**: Task management API development process
4. **Interactive Mode**: Custom tasks with your chosen workflow type

### Example Output

```
⚙️ Demo 1: Data Analysis Workflow
────────────────────────────────────
📋 Task: Analyze customer satisfaction survey data
🏗️ Pipeline: Data Extraction → Cleaning → Analysis → Visualization → Report
🔄 Starting workflow execution...

✅ Status: COMPLETED
📈 Execution Order: data_extraction → data_cleaning → data_analysis → data_visualization → report_generation
📊 Tasks Completed: 5/5
⏱️ Execution Time: 67,450ms

🎯 Final Result:
Comprehensive Customer Satisfaction Analysis Report

Executive Summary:
Based on the complete analysis pipeline, we have identified three key improvement areas...
```

## 💡 Key Learning Outcomes

### 1. Structured Coordination
- **Clear Dependencies**: Explicit task relationships prevent execution conflicts
- **Sequential Processing**: Ensures proper information flow between stages
- **Context Preservation**: Maintains knowledge continuity throughout pipeline

### 2. Task Management
- **Status Tracking**: Real-time monitoring of workflow progress
- **Priority Handling**: Execute higher-priority tasks first when possible
- **Error Recovery**: Graceful handling of task failures with retry logic

### 3. Scalable Architecture
- **Template System**: Reusable workflow patterns for different domains
- **Flexible Configuration**: Easy modification of task dependencies and priorities
- **Agent Specialization**: Each task uses domain-specific expertise

### 4. Production Readiness
- **Comprehensive Logging**: Detailed execution tracking and debugging
- **Performance Metrics**: Execution time and throughput monitoring
- **Failure Analysis**: Clear error reporting and recovery mechanisms

## 🔄 Extension Ideas

### Parallel Task Execution

```python
# Tasks without dependencies can run in parallel
def execute_parallel_tasks(self, ready_tasks: List[str]):
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(self.execute_task, task_id): task_id 
                  for task_id in ready_tasks}
        
        for future in as_completed(futures):
            task_id = futures[future]
            try:
                future.result()
            except Exception as e:
                logger.error(f"Parallel task {task_id} failed: {e}")
```

### Dynamic Workflow Modification

```python
# Add tasks dynamically based on results
def add_conditional_task(self, condition_result: str):
    if "technical" in condition_result.lower():
        technical_task = WorkflowTask(
            task_id="technical_analysis",
            description="Perform technical deep dive",
            dependencies=["analysis"]
        )
        self.add_task(technical_task)
```

### Workflow Persistence

```python
# Save and restore workflow state
def save_workflow_state(self) -> Dict:
    return {
        "workflow_id": self.workflow_id,
        "tasks": {task_id: asdict(task) for task_id, task in self.tasks.items()},
        "execution_order": self.execution_order,
        "task_results": self.task_results
    }

def restore_workflow_state(self, state: Dict):
    # Restore workflow from saved state for resumption
    pass
```

## 🎓 Educational Value

This example teaches:

1. **Sequential Coordination**: How to structure multi-step processes with dependencies
2. **Context Management**: Preserving and passing information between processing stages
3. **Task Orchestration**: Managing complex workflows with multiple specialized agents
4. **Error Handling**: Building resilient systems with retry and recovery mechanisms
5. **Performance Monitoring**: Tracking and optimizing workflow execution

## 📚 Comparison with Other Patterns

| Pattern | Coordination | Structure | Best For |
|---------|-------------|-----------|----------|
| **Workflow** | Sequential dependencies | Linear/parallel pipeline | Multi-step processes with clear stages |
| **Graph** | DAG dependencies | Network structure | Complex dependency relationships |
| **Swarm** | Autonomous handoffs | Self-organizing team | Collaborative problem-solving |
| **Agents as Tools** | Hierarchical routing | Orchestrator + specialists | Domain-specific expertise routing |
| **A2A** | Peer-to-peer | Direct communication | Negotiation and consensus building |

## 🚀 Advanced Features

### Workflow as a Tool

```python
from strands_tools import workflow

# Use workflow tool within an agent
orchestrator = Agent(
    tools=[workflow],
    system_prompt="Create and manage workflows to solve complex tasks"
)

# Agent can dynamically create workflows
result = orchestrator("Analyze market data and create investment strategy")
```

### State Management and Recovery

```python
# Pause and resume workflows
orchestrator.pause_workflow(workflow_id)
orchestrator.resume_workflow(workflow_id)

# Inspect intermediate results
status = orchestrator.get_workflow_status(workflow_id)
print(status["completed_tasks"])
```

### Resource Optimization

```python
# Intelligent resource allocation
class ResourceManager:
    def allocate_agent(self, task: WorkflowTask) -> Agent:
        # Select optimal agent based on task requirements
        if task.task_id.startswith("data_"):
            return self.data_specialist_agent
        elif task.task_id.startswith("content_"):
            return self.content_specialist_agent
        else:
            return self.general_purpose_agent
```

## 🏭 Production Considerations

### Monitoring and Observability

```python
# Comprehensive workflow monitoring
def track_workflow_metrics(self, result: WorkflowResult):
    metrics = {
        "total_execution_time": result.execution_time_ms,
        "task_success_rate": result.completed_tasks / result.total_tasks,
        "average_task_time": result.execution_time_ms / result.total_tasks,
        "failure_points": [task_id for task_id, task in self.tasks.items() 
                          if task.status == TaskStatus.FAILED]
    }
    # Send to monitoring system
    self.metrics_collector.record(metrics)
```

### Scalability Patterns

```python
# Distributed workflow execution
class DistributedWorkflowEngine(WorkflowEngine):
    def execute_task_distributed(self, task_id: str):
        # Execute task on distributed compute resources
        task_payload = self.build_task_payload(task_id)
        result = self.task_queue.submit(task_payload)
        return result
```

This Workflow pattern demonstrates the power of structured, sequential agent coordination, enabling complex multi-step processes with clear dependencies, comprehensive task management, and robust error handling for production-ready multi-agent systems.

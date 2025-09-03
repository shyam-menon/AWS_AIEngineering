#!/usr/bin/env python3
"""
Swarm Multi-Agent Pattern Example

This example demonstrates the "Swarm" pattern where multiple specialized agents
collab    return Swarm(
        nodes=[researcher, architect, coder, reviewer],
        max_handoffs=15,
        max_iterations=20,
        execution_timeout=600.0,  # 10 minutes
        node_timeout=180.0,  # 3 minutes per agent
        repetitive_handoff_detection_window=6,
        repetitive_handoff_min_unique_agents=2
    )onomously as a team with shared context and working memory.

Unlike hierarchical patterns, Swarm agents:
- Share working memory and context
- Coordinate autonomously through handoff tools
- Self-organize based on task requirements
- Contribute to collective intelligence

The system includes:
- Software Development Swarm (Researcher, Architect, Coder, Reviewer)
- Content Creation Swarm (Researcher, Writer, Editor, Designer)
- Business Analysis Swarm (Analyst, Strategist, Financial Advisor, Presenter)

This demonstrates emergent intelligence through collaborative agent teamwork.
"""

import logging
import asyncio
from typing import Dict, Any, List, Optional
from strands import Agent
from strands.multiagent import Swarm
from strands_tools import calculator, current_time, file_read

# Configure detailed logging for swarm operations
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Enable debug logs for swarm coordination
swarm_logger = logging.getLogger("strands.multiagent")
swarm_logger.setLevel(logging.DEBUG)


# ===============================
# SOFTWARE DEVELOPMENT SWARM
# ===============================

def create_software_development_swarm() -> Swarm:
    """
    Create a swarm for software development tasks.
    
    This swarm includes specialists for research, architecture, coding, and review.
    Each agent can hand off to others when their expertise is needed.
    """
    
    # Research Specialist Agent
    researcher = Agent(
        name="researcher",
        model="us.amazon.nova-lite-v1:0",
        system_prompt="""You are a Research Specialist in a software development team.
        
        Your expertise:
        - Technology research and evaluation
        - Requirements analysis and clarification
        - Best practices investigation
        - Competitive analysis
        - Feasibility studies
        
        When you receive a task:
        1. Analyze requirements thoroughly
        2. Research relevant technologies and approaches
        3. Document findings for the team
        4. Hand off to the Architect when design is needed
        5. Hand off to the Coder for direct implementation requests
        
        Share your research findings with the team through detailed analysis.
        Use handoff_to_agent when other specialists are needed.""",
        tools=[current_time, calculator]
    )
    
    # Architecture Specialist Agent
    architect = Agent(
        name="architect", 
        model="us.amazon.nova-lite-v1:0",
        system_prompt="""You are an Architecture Specialist in a software development team.
        
        Your expertise:
        - System architecture design
        - Technology stack selection
        - Design patterns and principles
        - Scalability and performance planning
        - Integration strategies
        
        When you receive a task:
        1. Design system architecture based on requirements
        2. Select appropriate technologies and patterns
        3. Create detailed technical specifications
        4. Hand off to the Coder for implementation
        5. Hand off to the Researcher if more analysis is needed
        
        Provide clear architectural decisions and rationale.
        Use handoff_to_agent when implementation or further research is needed.""",
        tools=[current_time, calculator]
    )
    
    # Coding Specialist Agent
    coder = Agent(
        name="coder",
        model="us.amazon.nova-lite-v1:0", 
        system_prompt="""You are a Coding Specialist in a software development team.
        
        Your expertise:
        - Implementation of software solutions
        - Writing clean, efficient code
        - Following coding standards and best practices
        - Debugging and troubleshooting
        - Code optimization
        
        When you receive a task:
        1. Implement solutions based on requirements/architecture
        2. Write well-documented, testable code
        3. Follow established patterns and standards
        4. Hand off to the Reviewer for code review
        5. Hand off to the Architect for design clarification
        
        Provide complete, working code implementations.
        Use handoff_to_agent when review or design input is needed.""",
        tools=[current_time, calculator, file_read]
    )
    
    # Code Review Specialist Agent
    reviewer = Agent(
        name="reviewer",
        model="us.amazon.nova-lite-v1:0",
        system_prompt="""You are a Code Review Specialist in a software development team.
        
        Your expertise:
        - Code quality assessment
        - Security review and best practices
        - Performance optimization suggestions
        - Testing strategy and coverage
        - Documentation review
        
        When you receive a task:
        1. Review code for quality, security, and performance
        2. Suggest improvements and optimizations
        3. Validate against requirements and architecture
        4. Provide final assessment and recommendations
        5. Hand off back to Coder if significant changes needed
        
        Provide thorough, constructive code reviews.
        Use handoff_to_agent if major revisions are required.""",
        tools=[current_time, calculator]
    )
    
    # Create the software development swarm
    return Swarm(
        nodes=[researcher, architect, coder, reviewer],
        max_handoffs=15,
        max_iterations=20,
        execution_timeout=600.0,  # 10 minutes
        node_timeout=180.0,      # 3 minutes per agent
        repetitive_handoff_detection_window=6,
        repetitive_handoff_min_unique_agents=2
    )


# ===============================
# CONTENT CREATION SWARM
# ===============================

def create_content_creation_swarm() -> Swarm:
    """
    Create a swarm for content creation tasks.
    
    This swarm specializes in research, writing, editing, and design for content projects.
    """
    
    # Content Researcher Agent
    content_researcher = Agent(
        name="content_researcher",
        model="us.amazon.nova-lite-v1:0",
        system_prompt="""You are a Content Research Specialist in a content creation team.
        
        Your expertise:
        - Topic research and fact-checking
        - Audience analysis and targeting
        - Trend identification and analysis
        - Source verification and citation
        - Content strategy research
        
        When you receive a task:
        1. Research the topic thoroughly
        2. Identify target audience and their needs
        3. Gather credible sources and data
        4. Provide research brief for content creation
        5. Hand off to Writer for content creation
        
        Deliver comprehensive research with actionable insights.
        Use handoff_to_agent when writing or design is needed.""",
        tools=[current_time, calculator]
    )
    
    # Content Writer Agent
    content_writer = Agent(
        name="content_writer",
        model="us.amazon.nova-lite-v1:0",
        system_prompt="""You are a Content Writer Specialist in a content creation team.
        
        Your expertise:
        - Creating engaging, well-structured content
        - Adapting tone and style for different audiences
        - SEO-optimized writing techniques
        - Storytelling and narrative development
        - Technical and creative writing
        
        When you receive a task:
        1. Create compelling content based on research
        2. Structure information clearly and engagingly
        3. Adapt style to target audience
        4. Include relevant examples and analogies
        5. Hand off to Editor for review and refinement
        
        Produce high-quality, engaging content.
        Use handoff_to_agent when editing or design input is needed.""",
        tools=[current_time, calculator]
    )
    
    # Content Editor Agent
    content_editor = Agent(
        name="content_editor",
        model="us.amazon.nova-lite-v1:0",
        system_prompt="""You are a Content Editor Specialist in a content creation team.
        
        Your expertise:
        - Content editing and proofreading
        - Style and consistency optimization
        - Clarity and readability improvement
        - Fact-checking and accuracy verification
        - Brand voice and tone alignment
        
        When you receive a task:
        1. Review content for clarity and accuracy
        2. Edit for style, tone, and consistency
        3. Optimize for readability and engagement
        4. Verify facts and sources
        5. Hand off to Designer for visual enhancement
        
        Deliver polished, publication-ready content.
        Use handoff_to_agent when design or further research is needed.""",
        tools=[current_time, calculator]
    )
    
    # Content Designer Agent
    content_designer = Agent(
        name="content_designer",
        model="us.amazon.nova-lite-v1:0",
        system_prompt="""You are a Content Designer Specialist in a content creation team.
        
        Your expertise:
        - Visual content design and layout
        - Information architecture and flow
        - User experience for content consumption
        - Visual hierarchy and accessibility
        - Multi-media content integration
        
        When you receive a task:
        1. Design visual layout and structure
        2. Create engaging visual elements
        3. Optimize for user experience and accessibility
        4. Ensure brand consistency
        5. Provide final content presentation recommendations
        
        Deliver comprehensive visual content design.
        Use handoff_to_agent if content revisions are needed.""",
        tools=[current_time, calculator]
    )
    
    # Create the content creation swarm
    return Swarm(
        nodes=[content_researcher, content_writer, content_editor, content_designer],
        max_handoffs=12,
        max_iterations=15,
        execution_timeout=450.0,  # 7.5 minutes
        node_timeout=120.0,      # 2 minutes per agent
        repetitive_handoff_detection_window=5,
        repetitive_handoff_min_unique_agents=2
    )


# ===============================
# BUSINESS ANALYSIS SWARM
# ===============================

def create_business_analysis_swarm() -> Swarm:
    """
    Create a swarm for business analysis tasks.
    
    This swarm focuses on business strategy, analysis, financial modeling, and presentation.
    """
    
    # Business Analyst Agent
    business_analyst = Agent(
        name="business_analyst",
        model="us.amazon.nova-lite-v1:0",
        system_prompt="""You are a Business Analyst Specialist in a business analysis team.
        
        Your expertise:
        - Business process analysis and optimization
        - Requirements gathering and documentation
        - Market analysis and competitive intelligence
        - Risk assessment and mitigation strategies
        - Performance metrics and KPI development
        
        When you receive a task:
        1. Analyze business requirements and processes
        2. Identify opportunities and challenges
        3. Document findings and recommendations
        4. Hand off to Strategist for strategic planning
        5. Hand off to Financial Advisor for financial analysis
        
        Provide thorough business analysis with actionable insights.
        Use handoff_to_agent when strategic or financial expertise is needed.""",
        tools=[current_time, calculator]
    )
    
    # Strategic Planner Agent
    strategist = Agent(
        name="strategist",
        model="us.amazon.nova-lite-v1:0",
        system_prompt="""You are a Strategic Planning Specialist in a business analysis team.
        
        Your expertise:
        - Strategic planning and roadmap development
        - Competitive strategy formulation
        - Business model innovation
        - Growth strategy and expansion planning
        - Change management and implementation
        
        When you receive a task:
        1. Develop strategic recommendations
        2. Create implementation roadmaps
        3. Assess strategic risks and opportunities
        4. Align strategy with business objectives
        5. Hand off to Financial Advisor for financial validation
        
        Deliver comprehensive strategic plans and recommendations.
        Use handoff_to_agent when financial modeling or presentation is needed.""",
        tools=[current_time, calculator]
    )
    
    # Financial Advisor Agent
    financial_advisor = Agent(
        name="financial_advisor",
        model="us.amazon.nova-lite-v1:0",
        system_prompt="""You are a Financial Advisor Specialist in a business analysis team.
        
        Your expertise:
        - Financial modeling and forecasting
        - ROI analysis and business case development
        - Budget planning and cost optimization
        - Investment analysis and valuation
        - Financial risk assessment
        
        When you receive a task:
        1. Develop financial models and projections
        2. Analyze costs, benefits, and ROI
        3. Create business cases with financial justification
        4. Assess financial risks and opportunities
        5. Hand off to Presenter for executive presentation
        
        Provide detailed financial analysis and recommendations.
        Use handoff_to_agent when presentation or further analysis is needed.""",
        tools=[current_time, calculator]
    )
    
    # Business Presenter Agent
    business_presenter = Agent(
        name="business_presenter",
        model="us.amazon.nova-lite-v1:0",
        system_prompt="""You are a Business Presentation Specialist in a business analysis team.
        
        Your expertise:
        - Executive presentation development
        - Data visualization and storytelling
        - Stakeholder communication strategies
        - Decision-support documentation
        - Persuasive presentation techniques
        
        When you receive a task:
        1. Create compelling executive presentations
        2. Synthesize complex analysis into clear insights
        3. Develop persuasive narratives and recommendations
        4. Structure information for decision-makers
        5. Provide final presentation recommendations
        
        Deliver executive-ready presentations and communications.
        Use handoff_to_agent if additional analysis or financial modeling is needed.""",
        tools=[current_time, calculator]
    )
    
    # Create the business analysis swarm
    return Swarm(
        nodes=[business_analyst, strategist, financial_advisor, business_presenter],
        max_handoffs=10,
        max_iterations=12,
        execution_timeout=400.0,  # 6.7 minutes
        node_timeout=100.0,      # 1.7 minutes per agent
        repetitive_handoff_detection_window=4,
        repetitive_handoff_min_unique_agents=2
    )


# ===============================
# SWARM ORCHESTRATOR
# ===============================

class SwarmOrchestrator:
    """
    Orchestrator for managing different swarm types and demonstrating their capabilities.
    
    This class provides a unified interface for working with different swarm configurations
    and shows how autonomous agent collaboration works in practice.
    """
    
    def __init__(self):
        """Initialize the swarm orchestrator with different swarm types."""
        logger.info("🐝 Initializing Swarm Orchestrator...")
        
        # Create different swarm types
        self.swarms = {
            "software_development": create_software_development_swarm(),
            "content_creation": create_content_creation_swarm(), 
            "business_analysis": create_business_analysis_swarm()
        }
        
        logger.info(f"✅ Swarm Orchestrator initialized with {len(self.swarms)} swarm types")
    
    def execute_swarm(self, swarm_type: str, task: str) -> Dict[str, Any]:
        """
        Execute a specific swarm type on a given task.
        
        Args:
            swarm_type: Type of swarm to execute
            task: Task description for the swarm
            
        Returns:
            Dictionary containing swarm execution results and metrics
        """
        if swarm_type not in self.swarms:
            raise ValueError(f"Unknown swarm type: {swarm_type}")
        
        logger.info(f"🐝 Executing {swarm_type} swarm on task: {task}")
        
        try:
            # Execute the swarm
            swarm = self.swarms[swarm_type]
            result = swarm(task)
            
            # Extract key information
            execution_info = {
                "status": result.status,
                "task": task,
                "swarm_type": swarm_type,
                "agents_involved": [node.node_id for node in result.node_history],
                "total_iterations": result.execution_count,
                "execution_time_ms": getattr(result, 'execution_time', 0),
                "final_result": str(result.result) if hasattr(result, 'result') else "No final result",
                "agent_results": {}
            }
            
            # Get individual agent results
            if hasattr(result, 'results'):
                for agent_name, agent_result in result.results.items():
                    if hasattr(agent_result, 'result'):
                        execution_info["agent_results"][agent_name] = str(agent_result.result)
            
            logger.info(f"✅ Swarm execution completed: {result.status}")
            return execution_info
            
        except Exception as e:
            logger.error(f"❌ Error executing swarm: {e}")
            return {
                "status": "FAILED",
                "error": str(e),
                "task": task,
                "swarm_type": swarm_type
            }
    
    async def execute_swarm_async(self, swarm_type: str, task: str) -> Dict[str, Any]:
        """
        Execute a swarm asynchronously.
        
        Args:
            swarm_type: Type of swarm to execute
            task: Task description for the swarm
            
        Returns:
            Dictionary containing swarm execution results and metrics
        """
        if swarm_type not in self.swarms:
            raise ValueError(f"Unknown swarm type: {swarm_type}")
        
        logger.info(f"🐝 Executing {swarm_type} swarm asynchronously on task: {task}")
        
        try:
            swarm = self.swarms[swarm_type]
            result = await swarm.invoke_async(task)
            
            execution_info = {
                "status": result.status,
                "task": task,
                "swarm_type": swarm_type,
                "agents_involved": [node.node_id for node in result.node_history],
                "total_iterations": result.execution_count,
                "execution_time_ms": getattr(result, 'execution_time', 0),
                "final_result": str(result.result) if hasattr(result, 'result') else "No final result"
            }
            
            logger.info(f"✅ Async swarm execution completed: {result.status}")
            return execution_info
            
        except Exception as e:
            logger.error(f"❌ Error executing async swarm: {e}")
            return {
                "status": "FAILED", 
                "error": str(e),
                "task": task,
                "swarm_type": swarm_type
            }
    
    def demonstrate_swarms(self):
        """Demonstrate different swarm types with example tasks."""
        
        demo_tasks = [
            {
                "swarm_type": "software_development",
                "task": "Design and implement a REST API for a task management application with user authentication",
                "description": "Software Development Swarm",
                "emoji": "💻"
            },
            {
                "swarm_type": "content_creation", 
                "task": "Create a comprehensive blog post about the benefits of AI in healthcare, targeting healthcare professionals",
                "description": "Content Creation Swarm",
                "emoji": "📝"
            },
            {
                "swarm_type": "business_analysis",
                "task": "Analyze the market opportunity for a new AI-powered customer service platform and develop a go-to-market strategy",
                "description": "Business Analysis Swarm", 
                "emoji": "📊"
            }
        ]
        
        print("\n" + "="*80)
        print("🐝 SWARM MULTI-AGENT PATTERN DEMONSTRATION")
        print("="*80)
        print("\nSwarms demonstrate autonomous agent collaboration with shared context.")
        print("Watch agents coordinate, hand off tasks, and build on each other's work!\n")
        
        for i, demo in enumerate(demo_tasks, 1):
            print(f"\n{demo['emoji']} Demo {i}: {demo['description']}")
            print("-" * 70)
            print(f"📋 Task: {demo['task']}")
            print(f"\n🐝 Swarm Type: {demo['swarm_type']}")
            print("🔄 Starting autonomous agent collaboration...")
            
            try:
                result = self.execute_swarm(demo['swarm_type'], demo['task'])
                
                print(f"\n✅ Status: {result['status']}")
                print(f"👥 Agents Involved: {' → '.join(result['agents_involved'])}")
                print(f"🔢 Total Iterations: {result['total_iterations']}")
                print(f"⏱️ Execution Time: {result.get('execution_time_ms', 0)}ms")
                
                if 'final_result' in result and result['final_result']:
                    print(f"\n🎯 Final Result:")
                    print(result['final_result'][:500] + "..." if len(result['final_result']) > 500 else result['final_result'])
                    
            except Exception as e:
                print(f"❌ Error: {e}")
            
            print("\n" + "."*70)
    
    def interactive_mode(self):
        """Run swarms in interactive mode for custom tasks."""
        print("\n" + "="*80)
        print("🐝 INTERACTIVE SWARM MODE - Autonomous Agent Collaboration")
        print("="*80)
        print("💡 Available swarm types:")
        print("   💻 software_development - Research, Architecture, Coding, Review")
        print("   📝 content_creation - Research, Writing, Editing, Design") 
        print("   📊 business_analysis - Analysis, Strategy, Finance, Presentation")
        print("   • Type 'quit' to exit")
        print("-" * 80)
        
        while True:
            try:
                print("\n🐝 Choose a swarm type (software_development/content_creation/business_analysis):")
                swarm_choice = input("🗣️  Swarm Type: ").strip().lower()
                
                if swarm_choice in ['quit', 'exit', 'bye']:
                    print("👋 Thank you for exploring Swarm multi-agent collaboration!")
                    break
                
                if swarm_choice not in self.swarms:
                    print(f"❌ Unknown swarm type. Choose from: {', '.join(self.swarms.keys())}")
                    continue
                
                task_input = input("🗣️  Task Description: ").strip()
                
                if not task_input:
                    print("📝 Please provide a task description.")
                    continue
                
                print(f"\n🐝 Executing {swarm_choice} swarm...")
                print("🔄 Agents will collaborate autonomously with shared context...")
                
                result = self.execute_swarm(swarm_choice, task_input)
                
                print(f"\n✅ Swarm Status: {result['status']}")
                print(f"👥 Agent Collaboration: {' → '.join(result['agents_involved'])}")
                print(f"🔢 Iterations: {result['total_iterations']}")
                
                if 'final_result' in result:
                    print(f"\n🎯 Swarm Result:\n{result['final_result']}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Thanks for exploring swarm intelligence!")
                break
            except Exception as e:
                logger.error(f"Error in interactive mode: {e}")
                print(f"❌ Sorry, I encountered an error: {e}")


def main():
    """Main function to run the Swarm multi-agent pattern demonstration."""
    
    print("🐝 Swarm Multi-Agent Pattern Example")
    print("=" * 45)
    print("\nThis example demonstrates autonomous agent collaboration where:")
    print("• Agents share working memory and context")
    print("• Teams self-organize based on expertise")
    print("• Coordination happens through handoff tools")
    print("• Collective intelligence emerges from collaboration")
    
    try:
        # Initialize the swarm orchestrator
        orchestrator = SwarmOrchestrator()
        
        # Run swarm demonstrations
        orchestrator.demonstrate_swarms()
        
        # Ask user if they want to try interactive mode
        print("\n" + "="*80)
        try_interactive = input("🎮 Would you like to try interactive swarm mode? (y/n): ").strip().lower()
        
        if try_interactive in ['y', 'yes']:
            orchestrator.interactive_mode()
        else:
            print("👍 Demo completed! You can run this script again to explore swarm collaboration.")
            
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"❌ Fatal error: {e}")
        print("🔧 Please check your Strands installation and try again.")


if __name__ == "__main__":
    main()

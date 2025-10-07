"""
Mock Knowledge Base Data

This module provides mock data for testing the priority-based routing system
without requiring an actual AWS Knowledge Base connection.
"""

import random
from typing import List, Dict, Any


# Mock documents organized by source type
MOCK_DOCUMENTS = {
    "SDM Playbook": [
        {
            "text": "Project initiation process: 1) Define project scope and objectives, 2) Identify key stakeholders and sponsors, 3) Create initial project charter, 4) Establish communication protocols, 5) Set up project governance structure. Follow these steps for successful project launch.",
            "metadata": {"source_type": "SDM Playbook", "document_id": "playbook_001", "category": "project_management"}
        },
        {
            "text": "Risk management procedure: Identify potential risks early in the project lifecycle. Create risk register with probability and impact assessments. Develop mitigation strategies for high-priority risks. Review risk status weekly in team meetings.",
            "metadata": {"source_type": "SDM Playbook", "document_id": "playbook_002", "category": "risk_management"}
        },
        {
            "text": "Change management protocol: All scope changes must be documented using the standard change request form. Changes require approval from project sponsor and technical lead. Impact assessment must include timeline and resource implications.",
            "metadata": {"source_type": "SDM Playbook", "document_id": "playbook_003", "category": "change_management"}
        },
        {
            "text": "Quality assurance guidelines: Implement peer review process for all deliverables. Conduct testing at multiple stages. Document all issues and resolutions. Maintain quality metrics dashboard for tracking purposes.",
            "metadata": {"source_type": "SDM Playbook", "document_id": "playbook_004", "category": "quality_assurance"}
        }
    ],
    
    "Templates": [
        {
            "text": "Project Charter Template: Include project title, business case, objectives, scope, success criteria, timeline, budget, and key stakeholders. Use this standardized format for all new projects to ensure consistency and completeness.",
            "metadata": {"source_type": "Templates", "document_id": "template_001", "category": "project_documents"}
        },
        {
            "text": "Status Report Template: Weekly status reports should include: completed tasks, upcoming milestones, risks and issues, budget status, resource utilization, and next week's priorities. Send every Friday by 5 PM.",
            "metadata": {"source_type": "Templates", "document_id": "template_002", "category": "reporting"}
        },
        {
            "text": "Meeting Minutes Template: Record attendees, agenda items discussed, decisions made, action items with owners and due dates, and next meeting schedule. Distribute within 24 hours of meeting completion.",
            "metadata": {"source_type": "Templates", "document_id": "template_003", "category": "communication"}
        },
        {
            "text": "One-pager template for executive briefings: Include problem statement, proposed solution, benefits, costs, timeline, and recommendation. Keep to single page with clear headings and bullet points for executive review.",
            "metadata": {"source_type": "Templates", "document_id": "template_004", "category": "executive_communication"}
        }
    ],
    
    "Process Master Document": [
        {
            "text": "Software Development Lifecycle (SDLC) process: Requirements gathering → Design → Development → Testing → Deployment → Maintenance. Each phase has specific deliverables and approval gates. Use agile methodology with 2-week sprints.",
            "metadata": {"source_type": "Process Master Document", "document_id": "process_001", "category": "development"}
        },
        {
            "text": "Procurement process workflow: 1) Identify need and create requisition, 2) Obtain necessary approvals based on dollar threshold, 3) Vendor selection and negotiation, 4) Contract execution, 5) Goods/services delivery and payment processing.",
            "metadata": {"source_type": "Process Master Document", "document_id": "process_002", "category": "procurement"}
        },
        {
            "text": "Employee onboarding process: HR orientation → IT setup → Department introduction → Role-specific training → 30-day check-in → 90-day performance review. Ensure all steps completed within first month of employment.",
            "metadata": {"source_type": "Process Master Document", "document_id": "process_003", "category": "human_resources"}
        },
        {
            "text": "Incident response procedure: Immediate assessment → Containment → Investigation → Resolution → Post-incident review. Critical incidents require notification to management within 1 hour of discovery.",
            "metadata": {"source_type": "Process Master Document", "document_id": "process_004", "category": "incident_management"}
        }
    ],
    
    "Trainings": [
        {
            "text": "Leadership Development Program: 12-week course covering communication skills, team management, strategic thinking, and decision-making. Includes mentorship component and 360-degree feedback assessment. Available quarterly.",
            "metadata": {"source_type": "Trainings", "document_id": "training_001", "category": "leadership"}
        },
        {
            "text": "Technical Skills Training: Programming languages, cloud platforms, data analysis tools. Self-paced online modules with hands-on labs. Certification tracks available for AWS, Microsoft, and Google platforms.",
            "metadata": {"source_type": "Trainings", "document_id": "training_002", "category": "technical"}
        },
        {
            "text": "Project Management Certification Prep: PMP and Agile certification preparation courses. Includes exam fees and study materials. 95% pass rate for participants who complete all modules and practice exams.",
            "metadata": {"source_type": "Trainings", "document_id": "training_003", "category": "project_management"}
        },
        {
            "text": "Compliance and Ethics Training: Annual mandatory training covering company policies, data protection, anti-harassment, and professional conduct. Must be completed by all employees before year-end.",
            "metadata": {"source_type": "Trainings", "document_id": "training_004", "category": "compliance"}
        }
    ],
    
    "Reports": [
        {
            "text": "Q3 Performance Metrics: Project delivery rate improved 15% compared to Q2. Customer satisfaction scores averaged 4.2/5. Budget variance reduced to 3% from previous 8%. On-time delivery reached 92% milestone.",
            "metadata": {"source_type": "Reports", "document_id": "report_001", "category": "performance"}
        },
        {
            "text": "Annual Security Assessment: Conducted penetration testing and vulnerability scans. Identified 12 medium-risk and 3 high-risk vulnerabilities. All critical issues resolved within 30 days. Compliance rating: 94%.",
            "metadata": {"source_type": "Reports", "document_id": "report_002", "category": "security"}
        },
        {
            "text": "Employee Engagement Survey Results: Overall satisfaction increased 8% year-over-year. Work-life balance and career development scored highest. Communication and recognition areas identified for improvement.",
            "metadata": {"source_type": "Reports", "document_id": "report_003", "category": "human_resources"}
        },
        {
            "text": "Technology Stack Analysis: Current infrastructure can support 40% growth. Recommend cloud migration for cost optimization. Legacy systems need modernization within 18 months to maintain security standards.",
            "metadata": {"source_type": "Reports", "document_id": "report_004", "category": "technology"}
        }
    ],
    
    "Tools": [
        {
            "text": "Project Management Software: Jira for task tracking, Confluence for documentation, Slack for team communication. All tools integrated with SSO authentication. Training available through IT helpdesk.",
            "metadata": {"source_type": "Tools", "document_id": "tool_001", "category": "project_management"}
        },
        {
            "text": "Development Tools: Visual Studio Code, Git for version control, Docker for containerization, Jenkins for CI/CD pipeline. Standard configuration templates available in IT portal.",
            "metadata": {"source_type": "Tools", "document_id": "tool_002", "category": "development"}
        },
        {
            "text": "Analytics Platform: Tableau for data visualization, SQL Server for data warehousing, Power BI for reporting. Access permissions managed through Active Directory groups. Training sessions held monthly.",
            "metadata": {"source_type": "Tools", "document_id": "tool_003", "category": "analytics"}
        },
        {
            "text": "Communication Tools: Microsoft Teams for video conferencing, SharePoint for document collaboration, Outlook for email and calendar management. Mobile apps available for remote access.",
            "metadata": {"source_type": "Tools", "document_id": "tool_004", "category": "communication"}
        }
    ]
}


def get_mock_results(query: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """
    Generate mock knowledge base results based on query analysis.
    
    Args:
        query: User query string
        max_results: Maximum number of results to return
        
    Returns:
        List of mock knowledge base results
    """
    query_lower = query.lower()
    relevant_results = []
    
    # Determine which sources are most relevant to the query
    source_relevance = _analyze_query_relevance(query_lower)
    
    # Collect results from all sources, weighted by relevance
    for source_type, documents in MOCK_DOCUMENTS.items():
        relevance_score = source_relevance.get(source_type, 0.1)
        
        for doc in documents:
            # Calculate similarity score based on keyword matching
            similarity_score = _calculate_similarity(query_lower, doc["text"].lower())
            
            # Combine relevance and similarity for final score
            final_score = (relevance_score * 0.6) + (similarity_score * 0.4)
            
            # Add some randomness to simulate real-world variation
            final_score += random.uniform(-0.1, 0.1)
            final_score = max(0.0, min(1.0, final_score))  # Clamp between 0 and 1
            
            relevant_results.append({
                "content": {"text": doc["text"]},
                "metadata": {
                    **doc["metadata"],
                    "source": source_type,
                    "relevance_score": relevance_score,
                    "similarity_score": similarity_score
                },
                "score": final_score
            })
    
    # Sort by score and return top results
    relevant_results.sort(key=lambda x: x["score"], reverse=True)
    return relevant_results[:max_results]


def _analyze_query_relevance(query_lower: str) -> Dict[str, float]:
    """
    Analyze query to determine relevance to different source types.
    
    Args:
        query_lower: Lowercase query string
        
    Returns:
        Dictionary mapping source types to relevance scores
    """
    relevance_keywords = {
        "SDM Playbook": ["playbook", "procedure", "process", "how to", "steps", "guide", "protocol", "guideline"],
        "Templates": ["template", "format", "example", "one-pager", "form", "document", "structure"],
        "Process Master Document": ["process", "workflow", "procedure", "lifecycle", "methodology"],
        "Trainings": ["training", "course", "learn", "education", "certification", "skill", "development"],
        "Reports": ["report", "analysis", "metrics", "data", "statistics", "performance", "results"],
        "Tools": ["tool", "software", "application", "platform", "system", "technology"]
    }
    
    source_relevance = {}
    
    for source_type, keywords in relevance_keywords.items():
        relevance_score = 0.0
        for keyword in keywords:
            if keyword in query_lower:
                relevance_score += 0.8 / len(keywords)  # Normalize by number of keywords
        
        # Add base relevance for all sources
        relevance_score += 0.2
        source_relevance[source_type] = min(1.0, relevance_score)
    
    return source_relevance


def _calculate_similarity(query_lower: str, doc_text_lower: str) -> float:
    """
    Calculate similarity between query and document text using simple keyword matching.
    
    Args:
        query_lower: Lowercase query string
        doc_text_lower: Lowercase document text
        
    Returns:
        Similarity score between 0 and 1
    """
    # Simple keyword-based similarity
    query_words = set(query_lower.split())
    doc_words = set(doc_text_lower.split())
    
    # Remove common stop words
    stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "is", "are", "was", "were", "be", "been", "have", "has", "had", "do", "does", "did", "will", "would", "could", "should"}
    
    query_words -= stop_words
    doc_words -= stop_words
    
    if not query_words:
        return 0.0
    
    # Calculate Jaccard similarity
    intersection = len(query_words.intersection(doc_words))
    union = len(query_words.union(doc_words))
    
    if union == 0:
        return 0.0
    
    return intersection / union


def get_sample_queries() -> List[Dict[str, Any]]:
    """
    Get sample queries for testing the priority routing system.
    
    Returns:
        List of sample queries with expected source preferences
    """
    return [
        {
            "query": "How do I create a project charter?",
            "expected_sources": ["Templates", "SDM Playbook"],
            "category": "project_setup"
        },
        {
            "query": "What's the process for software development?",
            "expected_sources": ["Process Master Document", "SDM Playbook"],
            "category": "development_process"
        },
        {
            "query": "Show me available training programs",
            "expected_sources": ["Trainings"],
            "category": "training_inquiry"
        },
        {
            "query": "What tools are available for project management?",
            "expected_sources": ["Tools"],
            "category": "tool_inquiry"
        },
        {
            "query": "Give me the latest performance metrics",
            "expected_sources": ["Reports"],
            "category": "metrics_request"
        },
        {
            "query": "How to handle project risks?",
            "expected_sources": ["SDM Playbook", "Process Master Document"],
            "category": "risk_management"
        },
        {
            "query": "Need a template for status reporting",
            "expected_sources": ["Templates"],
            "category": "template_request"
        },
        {
            "query": "What's the employee onboarding process?",
            "expected_sources": ["Process Master Document", "SDM Playbook"],
            "category": "hr_process"
        },
        {
            "query": "Show me security assessment results",
            "expected_sources": ["Reports"],
            "category": "security_inquiry"
        },
        {
            "query": "Available leadership training options?",
            "expected_sources": ["Trainings"],
            "category": "leadership_development"
        }
    ]


def get_source_statistics() -> Dict[str, Any]:
    """
    Get statistics about the mock knowledge base content.
    
    Returns:
        Statistics dictionary
    """
    total_documents = sum(len(docs) for docs in MOCK_DOCUMENTS.values())
    
    source_stats = {}
    for source_type, documents in MOCK_DOCUMENTS.items():
        categories = set(doc["metadata"]["category"] for doc in documents)
        avg_length = sum(len(doc["text"]) for doc in documents) / len(documents)
        
        source_stats[source_type] = {
            "document_count": len(documents),
            "categories": list(categories),
            "avg_content_length": avg_length
        }
    
    return {
        "total_documents": total_documents,
        "source_count": len(MOCK_DOCUMENTS),
        "source_statistics": source_stats
    }
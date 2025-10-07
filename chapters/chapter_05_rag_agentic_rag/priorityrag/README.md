# Priority-Based RAG System

An intelligent query routing system for AWS Knowledge Base that prioritizes sources based on document types and query analysis. This system ensures that high-priority sources like playbooks and templates receive preferential treatment in search results and response generation.

## 🚀 Features

- **Intelligent Source Prioritization**: Configurable priority mapping for different document types
- **Query Analysis**: Automatic detection of query intent and optimal source routing
- **Multi-Modal Routing**: Support for different query types (templates, processes, training, etc.)
- **Performance Tracking**: Comprehensive metrics and analytics
- **Mock Data Support**: Full demonstration capabilities without AWS dependencies
- **Flexible Configuration**: Easy customization of routing behavior
- **Interactive Demo**: Multiple demonstration modes

## 🏗️ Architecture

```
User Query → Query Analysis → Priority Routing → Source Selection → Response Generation
     ↓              ↓              ↓                ↓                    ↓
  Intent        Source         Priority          Retrieval          Synthesized
 Analysis      Matching        Scoring          Execution           Response
```

## 📋 Priority Mapping

The system uses a configurable priority map to ensure important sources are favored:

```python
priority_map = {
    "SDM Playbook": 1.0,           # Highest priority (playbooks)
    "Templates": 0.8,              # High priority (one-pagers)
    "Process Master Document": 0.7, # Medium-high priority
    "Trainings": 0.6,              # Medium priority
    "Reports": 0.5,                # Medium-low priority
    "Tools": 0.4                   # Lowest priority
}
```

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- AWS CLI configured (for production use)
- Access to AWS Bedrock (for production use)

### Setup

1. **Clone or create the directory structure**:
   ```bash
   mkdir priorityrag
   cd priorityrag
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure AWS (for production use)**:
   ```bash
   aws configure
   # Ensure you have access to AWS Bedrock and Knowledge Base
   ```

## 🚀 Quick Start

### 1. Quick Test (Fastest Way to See It Work)

Run the quick test script to see the system in action immediately:

```bash
python quick_test.py
```

**What you'll see**:
- 5 sample queries processed automatically
- Real-time priority routing decisions
- Source selection and prioritization
- Performance metrics summary

### 2. Interactive Demo (Recommended for Deep Exploration)

Run the interactive demonstration to experience the priority routing system:

```bash
python demo.py --mode interactive
```

**What you'll see**:
- Welcome message with system configuration
- Interactive chat interface
- Real-time query processing and routing decisions
- Source prioritization in action
- Performance metrics

### 2. Batch Testing

Test the system with predefined sample queries:

```bash
python demo.py --mode batch
```

**What this demonstrates**:
- Query classification accuracy
- Source routing effectiveness
- Performance metrics across different query types
- Expected vs actual source usage

### 3. Routing Analysis

See detailed routing decisions for different query types:

```bash
python demo.py --mode analysis
```

**What you'll learn**:
- How queries are analyzed for intent
- Source preference determination
- Priority score calculations
- Routing decision rationale

### 4. Configuration Testing

Compare different configuration presets:

```bash
python demo.py --mode config
```

**Available presets**:
- `balanced`: Equal weighting of factors
- `priority_focused`: Emphasizes source priority
- `confidence_focused`: Emphasizes retrieval confidence

## 💻 Usage Examples

### Basic Usage

```python
from priorityrag import PriorityBasedRouter, PriorityAwareChatBot

# Initialize with mock data (for testing)
router = PriorityBasedRouter(
    knowledge_base_id="demo",
    use_mock=True
)

# Get prioritized results
results = router.retrieve_with_priority("How to create a project template?")

# Use the chatbot
chatbot = PriorityAwareChatBot(
    knowledge_base_id="demo",
    use_mock=True
)

response = chatbot.generate_response("What's the onboarding process?")
print(response["response"])
```

### Production Usage

```python
from priorityrag import PriorityBasedRouter, PriorityAwareChatBot
from priorityrag.utils.config import RouterConfig

# Production configuration
config = RouterConfig()
config.knowledge_base_id = "your-actual-kb-id"
config.aws_region = "us-east-1"
config.use_mock_data = False

# Initialize with real AWS Knowledge Base
chatbot = PriorityAwareChatBot(
    knowledge_base_id=config.knowledge_base_id,
    region=config.aws_region,
    use_mock=False
)

# Process user query
response = chatbot.generate_response("Show me the latest security playbook")
```

### Custom Priority Configuration

```python
from priorityrag.utils.config import RouterConfig

# Create custom configuration
config = RouterConfig()

# Update priority mapping for your specific sources
config.update_priorities({
    "Critical Procedures": 1.0,
    "Standard Templates": 0.9,
    "Training Materials": 0.7,
    "Reference Documents": 0.5
})

# Adjust scoring weights
config.priority_weight = 0.8      # Emphasize priority
config.confidence_weight = 0.15   # Less emphasis on confidence
config.query_match_weight = 0.05  # Minimal query matching weight
```

## 📊 Sample Queries and Expected Routing

| Query | Expected Primary Source | Reasoning |
|-------|------------------------|-----------|
| "How do I create a project charter?" | Templates → SDM Playbook | Template request with procedural elements |
| "What's the software development process?" | Process Master Document | Clear process inquiry |
| "Show me available training programs" | Trainings | Direct training inquiry |
| "What tools are recommended for analytics?" | Tools | Tool-specific request |
| "Give me the latest performance metrics" | Reports | Data/metrics request |

## 🎯 Query Types and Routing Logic

### 1. Template Requests
- **Keywords**: template, format, example, one-pager
- **Primary Sources**: Templates → SDM Playbook
- **Example**: "Need a status report template"

### 2. Process Inquiries
- **Keywords**: process, workflow, procedure, steps
- **Primary Sources**: Process Master Document → SDM Playbook
- **Example**: "What's the employee onboarding workflow?"

### 3. Training Requests
- **Keywords**: training, course, learn, skill
- **Primary Sources**: Trainings
- **Example**: "Available leadership development programs?"

### 4. Tool Information
- **Keywords**: tool, software, application, system
- **Primary Sources**: Tools
- **Example**: "What project management tools do we use?"

### 5. Reports and Analytics
- **Keywords**: report, metrics, data, analysis
- **Primary Sources**: Reports
- **Example**: "Show me quarterly performance data"

## ⚙️ Configuration Options

### Router Configuration

```python
from priorityrag.utils.config import RouterConfig

config = RouterConfig()

# Priority mapping (0.0 to 1.0)
config.priority_map = {
    "SDM Playbook": 1.0,
    "Templates": 0.8,
    # ... other sources
}

# Scoring weights (should sum to ~1.0)
config.priority_weight = 0.6      # Source priority importance
config.confidence_weight = 0.3    # Retrieval confidence importance
config.query_match_weight = 0.1   # Query-source matching importance

# Retrieval limits
config.max_retrieval_results = 20  # Max from Knowledge Base
config.max_final_results = 10      # Max returned to user
```

### Environment Variables

You can configure the system using environment variables:

```bash
export KNOWLEDGE_BASE_ID="your-kb-id"
export AWS_REGION="us-east-1"
export PRIORITY_WEIGHT="0.7"
export CONFIDENCE_WEIGHT="0.2"
export QUERY_MATCH_WEIGHT="0.1"
export VERBOSE_LOGGING="true"
```

## 📈 Performance Metrics

The system tracks comprehensive metrics:

### Router Metrics
- Total queries processed
- Success rate
- Average confidence scores
- Source usage distribution

### Performance Metrics
- Response times
- Query type distribution
- Source effectiveness
- Priority score distributions

### View Metrics

```bash
# Show comprehensive metrics dashboard
python demo.py --mode metrics

# Export metrics to file
python demo.py --export results.json
```

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=priorityrag

# Run specific test category
pytest tests/test_router.py
```

### Test Query Categories

The system includes comprehensive test coverage for:
- Query classification accuracy
- Source routing effectiveness
- Priority calculation correctness
- Performance benchmarks
- Configuration validation

## 🔧 Customization

### Adding New Source Types

```python
# Update priority mapping
config.priority_map["New Source Type"] = 0.75

# Add query patterns
config.query_patterns[r'new|custom|pattern'] = ["New Source Type"]

# Add source hints
config.query_source_hints["keyword"] = ["New Source Type"]
```

### Custom Query Analysis

```python
from priorityrag.utils.helpers import QueryAnalyzer

# Extend query analysis
class CustomQueryAnalyzer(QueryAnalyzer):
    @staticmethod
    def classify_domain_specific_intent(query: str):
        # Your custom logic here
        pass
```

### Custom Response Generation

```python
class CustomChatBot(PriorityAwareChatBot):
    def _generate_custom_response(self, query: str, results: List[SourceResult]) -> str:
        # Your custom response logic
        pass
```

## 🚨 Troubleshooting

### Common Issues

1. **Import Errors**:
   ```bash
   # Ensure you're in the correct directory
   cd priorityrag
   python demo.py
   ```

2. **AWS Authentication Issues**:
   ```bash
   # Check AWS configuration
   aws sts get-caller-identity
   
   # Use mock data for testing
   python demo.py --mode interactive  # Uses mock by default
   ```

3. **Missing Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Low Routing Confidence**:
   - Check query clarity and specificity
   - Review priority mapping alignment
   - Adjust configuration weights

### Debug Mode

Enable verbose logging for detailed debugging:

```bash
python demo.py --verbose --mode interactive
```

## 📚 File Structure

```
priorityrag/
├── __init__.py                 # Package initialization
├── priority_router.py          # Core routing logic
├── chatbot.py                  # Chatbot implementation
├── demo.py                     # Main demonstration script
├── requirements.txt            # Dependencies
├── README.md                   # This file
├── data/
│   ├── __init__.py
│   └── mock_knowledge_base.py  # Mock data for testing
└── utils/
    ├── __init__.py
    ├── config.py               # Configuration management
    └── helpers.py              # Utility functions
```

## 🔗 Integration with AWS

### Production Setup

1. **Create Knowledge Base**:
   - Set up AWS Bedrock Knowledge Base
   - Configure data sources (S3, etc.)
   - Note the Knowledge Base ID

2. **Update Configuration**:
   ```python
   config = RouterConfig()
   config.knowledge_base_id = "your-actual-kb-id"
   config.use_mock_data = False
   ```

3. **IAM Permissions**:
   Ensure your AWS credentials have:
   - `bedrock:Retrieve` permission
   - `bedrock:InvokeModel` permission
   - Access to your specific Knowledge Base

### Metadata Requirements

For optimal routing, ensure your Knowledge Base documents include metadata:

```json
{
  "source_type": "SDM Playbook",
  "category": "project_management",
  "document_type": "procedure",
  "priority_level": "high"
}
```

## 🎉 Success Metrics

You'll know the system is working effectively when:

- [ ] High-priority sources appear first in results
- [ ] Query-to-source matching works accurately
- [ ] Response times are consistently fast
- [ ] User satisfaction with response relevance is high
- [ ] Priority sources are utilized more frequently
- [ ] Fallback mechanisms activate gracefully

## 🤝 Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   pip install pytest black flake8
   ```
4. Make changes and add tests
5. Run tests and formatting:
   ```bash
   pytest
   black .
   flake8 .
   ```

### Adding Features

- New routing strategies
- Additional query analysis methods
- Enhanced performance tracking
- Custom response generators
- Integration with other AWS services

## 📄 License

This project is part of the AWS AI Engineering course materials and is intended for educational purposes.

## 🆘 Support

For issues and questions:

1. Check the troubleshooting section above
2. Review the demo modes for examples
3. Ensure proper AWS configuration
4. Enable verbose logging for debugging

## 🎯 Next Steps

After mastering this priority-based routing system:

1. **Scale to Production**: Deploy with real AWS Knowledge Base
2. **Add Analytics**: Implement advanced performance monitoring
3. **Extend Sources**: Add more document types and sources
4. **Multi-Modal**: Add support for images and documents
5. **ML Enhancement**: Use machine learning for routing optimization
6. **A/B Testing**: Test different routing strategies

---

**Happy Routing! 🚀**

This priority-based RAG system demonstrates the power of intelligent query routing in enterprise knowledge management scenarios. The system ensures that your most important documents (like SDM Playbooks and Templates) receive the attention they deserve while maintaining high performance and user satisfaction.
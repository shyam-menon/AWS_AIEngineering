# Makefile for RAG Demo - AWS AI Engineering Course
# Chapter 4: Storage for Retrieval
#
# This Makefile provides convenient targets for managing the RAG demo
# environment and running different components.

.PHONY: help setup up down demo-local demo-kb agent test clean install-deps validate

# Load environment variables if .env exists
ifneq (,$(wildcard .env))
    include .env
    export
endif

# Default target
help:
	@echo "🤖 RAG Demo - AWS AI Engineering Course"
	@echo "========================================"
	@echo ""
	@echo "📋 Available targets:"
	@echo ""
	@echo "🔧 Setup and Environment:"
	@echo "  install-deps    Install Python dependencies"
	@echo "  setup          Install dependencies and validate environment"
	@echo "  validate       Validate AWS configuration and connectivity"
	@echo ""
	@echo "☁️  AWS Infrastructure:"
	@echo "  up             Create AWS Knowledge Base infrastructure"
	@echo "  down           Destroy AWS infrastructure (stops charges)"
	@echo "  status         Check Knowledge Base status"
	@echo ""
	@echo "🎯 Demo Modes:"
	@echo "  demo-local     Run local FAISS RAG demo"
	@echo "  demo-kb        Run Bedrock Knowledge Base demo"
	@echo "  agent          Run Strands agent wrapper demo"
	@echo "  compare        Compare both approaches side-by-side"
	@echo ""
	@echo "🚀 Quick Workflows:"
	@echo "  run-kb-ephemeral   Create KB, run demo, then destroy (full cycle)"
	@echo "  local-only         Build and run local FAISS demo only"
	@echo ""
	@echo "🧪 Testing and Maintenance:"
	@echo "  test           Run test suite"
	@echo "  clean          Clean up local files and indexes"
	@echo "  rebuild-local  Force rebuild of local FAISS index"
	@echo ""
	@echo "📖 Documentation:"
	@echo "  docs           Open README.md for detailed instructions"
	@echo ""
	@echo "💡 Examples:"
	@echo "  make setup && make demo-local    # Quick start with local RAG"
	@echo "  make up && make demo-kb          # Test managed RAG (requires AWS)"
	@echo "  make run-kb-ephemeral           # Full demo with automatic cleanup"

# Install Python dependencies
install-deps:
	@echo "📦 Installing Python dependencies..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed"

# Complete setup
setup: install-deps
	@echo "🔧 Setting up RAG demo environment..."
	@if [ ! -f .env ]; then \
		echo "📝 Creating .env from template..."; \
		cp .env.example .env; \
		echo "⚠️  Please edit .env with your AWS credentials"; \
	fi
	@$(MAKE) validate

# Validate environment
validate:
	@echo "🧪 Validating environment..."
	python -c "from common import test_bedrock_connection; test_bedrock_connection()"

# Create AWS infrastructure
up:
	@echo "🚀 Creating AWS Knowledge Base infrastructure..."
	@if [ ! -x scripts/setup-kb.sh ]; then chmod +x scripts/setup-kb.sh; fi
	./scripts/setup-kb.sh

# Destroy AWS infrastructure
down:
	@echo "🧹 Destroying AWS infrastructure..."
	@if [ ! -x scripts/teardown-kb.sh ]; then chmod +x scripts/teardown-kb.sh; fi
	./scripts/teardown-kb.sh

# Check Knowledge Base status
status:
	@echo "📊 Checking Knowledge Base status..."
	@if [ -f .kb.env ]; then \
		source .kb.env && python rag_bedrock_kb.py --status; \
	else \
		echo "❌ No .kb.env found. Run 'make up' first."; \
	fi

# Run local FAISS demo
demo-local:
	@echo "🔍 Running local FAISS RAG demo..."
	python rag_vector_local.py

# Run Bedrock Knowledge Base demo
demo-kb:
	@echo "🏛️ Running Bedrock Knowledge Base demo..."
	@if [ ! -f .kb.env ]; then \
		echo "❌ Knowledge Base not set up. Run 'make up' first."; \
		exit 1; \
	fi
	python rag_bedrock_kb.py

# Run Strands agent demo
agent:
	@echo "🤖 Running Strands agent demo..."
	python strands_agent.py --demo

# Compare both approaches
compare:
	@echo "🔄 Comparing RAG approaches..."
	@echo "Testing local FAISS approach:"
	@echo "--------------------------------"
	python rag_vector_local.py --question "What is AI Engineering?"
	@echo ""
	@echo "Testing Bedrock Knowledge Base approach:"
	@echo "---------------------------------------"
	@if [ -f .kb.env ]; then \
		python rag_bedrock_kb.py --question "What is AI Engineering?"; \
	else \
		echo "❌ Knowledge Base not available. Run 'make up' first."; \
	fi

# Full ephemeral workflow
run-kb-ephemeral:
	@echo "🎢 Running ephemeral Knowledge Base demo..."
	@echo "This will create AWS resources, run demo, then clean up automatically."
	@echo ""
	$(MAKE) up
	@echo ""
	@echo "🎯 Running demo with Knowledge Base..."
	$(MAKE) demo-kb
	@echo ""
	@echo "🧹 Cleaning up AWS resources..."
	$(MAKE) down
	@echo ""
	@echo "✅ Ephemeral demo complete!"

# Local-only workflow
local-only:
	@echo "🏠 Running local-only RAG demo..."
	$(MAKE) setup
	$(MAKE) demo-local

# Force rebuild local index
rebuild-local:
	@echo "🔄 Rebuilding local FAISS index..."
	python rag_vector_local.py --rebuild

# Run tests
test:
	@echo "🧪 Running test suite..."
	@if [ -d tests ]; then \
		python -m pytest tests/ -v; \
	else \
		echo "⚠️  No tests directory found"; \
	fi

# Clean up local files
clean:
	@echo "🧹 Cleaning up local files..."
	@rm -f faiss_index.faiss faiss_index_data.npz
	@rm -rf __pycache__ .pytest_cache
	@find . -name "*.pyc" -delete
	@echo "✅ Local cleanup complete"

# Interactive demos
demo-local-interactive:
	@echo "💬 Starting interactive local FAISS demo..."
	python rag_vector_local.py --interactive

demo-kb-interactive:
	@echo "💬 Starting interactive Knowledge Base demo..."
	@if [ ! -f .kb.env ]; then \
		echo "❌ Knowledge Base not set up. Run 'make up' first."; \
		exit 1; \
	fi
	python rag_bedrock_kb.py --interactive

agent-interactive:
	@echo "💬 Starting interactive agent demo..."
	python strands_agent.py --interactive

# Development targets
dev-setup: setup
	@echo "🛠️  Setting up development environment..."
	pip install pytest pytest-mock black flake8
	@echo "✅ Development environment ready"

format:
	@echo "🎨 Formatting code..."
	black *.py
	@echo "✅ Code formatted"

lint:
	@echo "🔍 Linting code..."
	flake8 *.py --max-line-length=88 --ignore=E203,W503
	@echo "✅ Linting complete"

# Documentation
docs:
	@echo "📖 Opening documentation..."
	@if command -v code >/dev/null 2>&1; then \
		code README.md; \
	elif command -v open >/dev/null 2>&1; then \
		open README.md; \
	elif command -v xdg-open >/dev/null 2>&1; then \
		xdg-open README.md; \
	else \
		echo "📄 Please open README.md in your editor"; \
	fi

# Debug targets
debug-env:
	@echo "🔍 Environment Debug Information:"
	@echo "================================="
	@echo "AWS Region: $(AWS_REGION)"
	@echo "Embed Model: $(BEDROCK_EMBED_MODEL_ID)"
	@echo "Chat Model: $(BEDROCK_CHAT_MODEL_ID)"
	@echo "KB ID: $(KB_ID)"
	@echo ""
	@echo "📁 Files:"
	@echo "  .env exists: $$(test -f .env && echo 'Yes' || echo 'No')"
	@echo "  .kb.env exists: $$(test -f .kb.env && echo 'Yes' || echo 'No')"
	@echo "  FAISS index exists: $$(test -f faiss_index.faiss && echo 'Yes' || echo 'No')"
	@echo ""
	@echo "🔗 AWS Connectivity:"
	@aws sts get-caller-identity 2>/dev/null | head -3 || echo "❌ AWS credentials not configured"

# Cost estimation
cost-estimate:
	@echo "💰 AWS Cost Estimates for RAG Demo:"
	@echo "===================================="
	@echo ""
	@echo "📊 OpenSearch Serverless:"
	@echo "  • Base cost: ~$$0.24/OCU/hour"
	@echo "  • Minimum: 0.5 OCU = ~$$2.88/day"
	@echo "  • Demo usage: ~$$0.12-0.50/hour"
	@echo ""
	@echo "📦 S3 Storage:"
	@echo "  • Small docs: ~$$0.01/month"
	@echo "  • Negligible for demo"
	@echo ""
	@echo "🤖 Bedrock Usage:"
	@echo "  • Embeddings: ~$$0.0001/1K tokens"
	@echo "  • Chat (Nova Lite): ~$$0.0008/1K input tokens"
	@echo "  • Demo cost: ~$$0.10-0.50 total"
	@echo ""
	@echo "💡 Total estimated cost:"
	@echo "  • 1 hour demo: ~$$0.25-0.75"
	@echo "  • Full day: ~$$3-4 (if left running)"
	@echo ""
	@echo "⚠️  Remember to run 'make down' when finished!"

# Troubleshooting
troubleshoot:
	@echo "🔧 RAG Demo Troubleshooting:"
	@echo "============================"
	@echo ""
	@echo "🔍 Common Issues:"
	@echo ""
	@echo "1. AWS Credentials:"
	@echo "   • Run: aws sts get-caller-identity"
	@echo "   • Check: ~/.aws/credentials or environment variables"
	@echo ""
	@echo "2. Model Access:"
	@echo "   • Visit: https://console.aws.amazon.com/bedrock/home#/modelaccess"
	@echo "   • Enable: Amazon Titan Embed Text v2 and Nova Lite"
	@echo ""
	@echo "3. Dependencies:"
	@echo "   • Run: make install-deps"
	@echo "   • Check: pip list | grep -E 'boto3|faiss|numpy'"
	@echo ""
	@echo "4. Region Issues:"
	@echo "   • Bedrock available regions: us-east-1, us-west-2, eu-west-1"
	@echo "   • Set AWS_REGION in .env"
	@echo ""
	@echo "5. Knowledge Base Setup:"
	@echo "   • Check: make status"
	@echo "   • Rebuild: make down && make up"
	@echo ""
	@echo "🆘 Still having issues? Check README.md for detailed troubleshooting."

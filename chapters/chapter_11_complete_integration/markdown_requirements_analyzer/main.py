#!/usr/bin/env python3
"""
Markdown Requirements Analyzer - Main Entry Point

This is the main entry point for the markdown requirements analyzer.
It provides a unified interface for converting markdown business requirements
to JSON and analyzing them with AWS Bedrock LLM.
"""

import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from cli_interface import main as cli_main

if __name__ == "__main__":
    cli_main()
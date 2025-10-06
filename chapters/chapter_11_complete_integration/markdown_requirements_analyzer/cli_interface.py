#!/usr/bin/env python3
"""
Command Line Interface

This module provides a comprehensive CLI for the markdown requirements analyzer.
Supports conversion, analysis, batch processing, and configuration management.
"""

import argparse
import json
import sys
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

from markdown_converter import MarkdownConverter, convert_single_file, convert_directory_to_json
from bedrock_analyzer import BedrockRequirementsAnalyzer, analyze_requirements_json
from config_manager import ConfigManager, get_config
import utils

logger = logging.getLogger(__name__)


class CLIInterface:
    """
    Command-line interface for the markdown requirements analyzer.
    
    Provides commands for conversion, analysis, batch processing,
    and configuration management.
    """
    
    def __init__(self):
        """Initialize the CLI interface."""
        self.parser = self._create_parser()
        self.config = None
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """
        Create the main argument parser with subcommands.
        
        Returns:
            Configured ArgumentParser
        """
        parser = argparse.ArgumentParser(
            description="Markdown Requirements Analyzer - Convert markdown business requirements to JSON and analyze with AWS Bedrock",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Convert single markdown file
  python cli_interface.py convert requirements.md

  # Convert and analyze
  python cli_interface.py convert requirements.md --analyze

  # Batch convert directory
  python cli_interface.py batch ./requirements_dir --output ./json_output

  # Analyze existing JSON
  python cli_interface.py analyze requirements.json

  # Create sample configuration
  python cli_interface.py config --create-sample

  # Validate configuration
  python cli_interface.py config --validate
            """
        )
        
        # Global options
        parser.add_argument('--config', '-c', 
                          help='Configuration file path')
        parser.add_argument('--verbose', '-v', 
                          action='store_true',
                          help='Enable verbose logging')
        parser.add_argument('--quiet', '-q', 
                          action='store_true',
                          help='Suppress non-error output')
        
        # Create subparsers
        subparsers = parser.add_subparsers(dest='command', 
                                         help='Available commands')
        
        # Convert command
        self._add_convert_parser(subparsers)
        
        # Analyze command
        self._add_analyze_parser(subparsers)
        
        # Batch command
        self._add_batch_parser(subparsers)
        
        # Config command
        self._add_config_parser(subparsers)
        
        # List command
        self._add_list_parser(subparsers)
        
        return parser
    
    def _add_convert_parser(self, subparsers):
        """Add convert subcommand parser."""
        convert_parser = subparsers.add_parser('convert', 
                                             help='Convert markdown file to JSON')
        convert_parser.add_argument('input_file', 
                                  help='Path to markdown file')
        convert_parser.add_argument('--output', '-o', 
                                  help='Output JSON file path')
        convert_parser.add_argument('--analyze', '-a', 
                                  action='store_true',
                                  help='Also analyze requirements with Bedrock')
        convert_parser.add_argument('--analysis-type', 
                                  choices=['comprehensive', 'completeness', 'improvements', 'structure'],
                                  default='comprehensive',
                                  help='Type of analysis to perform')
        convert_parser.add_argument('--no-validate', 
                                  action='store_true',
                                  help='Skip markdown structure validation')
        convert_parser.add_argument('--pretty', 
                                  action='store_true', 
                                  default=True,
                                  help='Format JSON output with indentation')
    
    def _add_analyze_parser(self, subparsers):
        """Add analyze subcommand parser."""
        analyze_parser = subparsers.add_parser('analyze', 
                                             help='Analyze JSON requirements with Bedrock')
        analyze_parser.add_argument('input_file', 
                                  help='Path to JSON requirements file')
        analyze_parser.add_argument('--output', '-o', 
                                  help='Output analysis file path')
        analyze_parser.add_argument('--type', '-t', 
                                  choices=['comprehensive', 'completeness', 'improvements', 'structure'],
                                  default='comprehensive',
                                  help='Type of analysis to perform')
        analyze_parser.add_argument('--model', '-m', 
                                  help='Bedrock model ID to use')
        analyze_parser.add_argument('--region', '-r', 
                                  help='AWS region')
    
    def _add_batch_parser(self, subparsers):
        """Add batch subcommand parser."""
        batch_parser = subparsers.add_parser('batch', 
                                           help='Batch process multiple markdown files')
        batch_parser.add_argument('input_directory', 
                                help='Directory containing markdown files')
        batch_parser.add_argument('--output', '-o', 
                                help='Output directory for JSON files')
        batch_parser.add_argument('--recursive', '-r', 
                                action='store_true', 
                                default=True,
                                help='Process subdirectories recursively')
        batch_parser.add_argument('--analyze', '-a', 
                                action='store_true',
                                help='Also analyze each file with Bedrock')
        batch_parser.add_argument('--analysis-type', 
                                choices=['comprehensive', 'completeness', 'improvements', 'structure'],
                                default='comprehensive',
                                help='Type of analysis to perform')
        batch_parser.add_argument('--parallel', '-p', 
                                type=int, 
                                default=1,
                                help='Number of parallel processes (1=sequential)')
        batch_parser.add_argument('--report', 
                                action='store_true',
                                help='Generate summary report')
    
    def _add_config_parser(self, subparsers):
        """Add config subcommand parser."""
        config_parser = subparsers.add_parser('config', 
                                            help='Configuration management')
        config_parser.add_argument('--create-sample', 
                                 action='store_true',
                                 help='Create sample configuration file')
        config_parser.add_argument('--validate', 
                                 action='store_true',
                                 help='Validate current configuration')
        config_parser.add_argument('--show', 
                                 action='store_true',
                                 help='Show current configuration')
        config_parser.add_argument('--output', '-o', 
                                 help='Output path for sample configuration')
    
    def _add_list_parser(self, subparsers):
        """Add list subcommand parser."""
        list_parser = subparsers.add_parser('list', 
                                          help='List available models and resources')
        list_parser.add_argument('--models', 
                               action='store_true',
                               help='List available Bedrock models')
        list_parser.add_argument('--region', '-r', 
                               help='AWS region')
    
    def run(self, args: Optional[List[str]] = None) -> int:
        """
        Run the CLI with given arguments.
        
        Args:
            args: Command line arguments (None for sys.argv)
            
        Returns:
            Exit code (0 for success, non-zero for error)
        """
        try:
            parsed_args = self.parser.parse_args(args)
            
            # Setup logging based on verbosity
            self._setup_logging(parsed_args)
            
            # Load configuration
            self.config = get_config(parsed_args.config)
            
            # Handle no command case
            if not parsed_args.command:
                self.parser.print_help()
                return 1
            
            # Route to appropriate handler
            if parsed_args.command == 'convert':
                return self._handle_convert(parsed_args)
            elif parsed_args.command == 'analyze':
                return self._handle_analyze(parsed_args)
            elif parsed_args.command == 'batch':
                return self._handle_batch(parsed_args)
            elif parsed_args.command == 'config':
                return self._handle_config(parsed_args)
            elif parsed_args.command == 'list':
                return self._handle_list(parsed_args)
            else:
                self.parser.print_help()
                return 1
                
        except KeyboardInterrupt:
            utils.print_info("Operation cancelled by user")
            return 130
        except Exception as e:
            utils.print_error(f"Unexpected error: {str(e)}")
            logger.exception("Unexpected error in CLI")
            return 1
    
    def _setup_logging(self, args):
        """Setup logging based on command line arguments."""
        if args.quiet:
            logging.getLogger().setLevel(logging.ERROR)
        elif args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            logging.getLogger().setLevel(logging.INFO)
    
    def _handle_convert(self, args) -> int:
        """Handle convert command."""
        try:
            utils.print_info(f"Converting markdown file: {args.input_file}")
            
            # Setup converter
            converter = MarkdownConverter(validate_structure=not args.no_validate)
            
            # Convert file
            result = converter.convert_file(args.input_file)
            
            if not result['success']:
                utils.print_error(f"Conversion failed: {result['error']}")
                return 1
            
            utils.print_success("Conversion completed successfully!")
            utils.print_info(f"Sections found: {result['metadata']['sections_count']}")
            
            # Save JSON output
            output_path = args.output
            if not output_path:
                input_path = Path(args.input_file)
                output_path = input_path.with_suffix('.json')
            
            if not converter.save_json(result['data'], output_path, pretty=args.pretty):
                utils.print_error("Failed to save JSON output")
                return 1
            
            utils.print_success(f"JSON saved to: {output_path}")
            
            # Analyze if requested
            if args.analyze:
                utils.print_info("Starting Bedrock analysis...")
                
                analysis_result = self._analyze_json_data(result['data'], args.analysis_type)
                
                if analysis_result['success']:
                    utils.print_success("Analysis completed!")
                    
                    # Save analysis
                    analysis_path = Path(output_path).with_suffix('.analysis.json')
                    with open(analysis_path, 'w') as f:
                        json.dump(analysis_result, f, indent=2)
                    
                    utils.print_info(f"Analysis saved to: {analysis_path}")
                    
                    # Print summary
                    self._print_analysis_summary(analysis_result['analysis'])
                else:
                    utils.print_error(f"Analysis failed: {analysis_result['error']}")
                    return 1
            
            return 0
            
        except Exception as e:
            utils.print_error(f"Convert command failed: {str(e)}")
            logger.exception("Convert command error")
            return 1
    
    def _handle_analyze(self, args) -> int:
        """Handle analyze command."""
        try:
            utils.print_info(f"Analyzing requirements: {args.input_file}")
            
            # Load JSON file
            with open(args.input_file, 'r') as f:
                requirements_json = json.load(f)
            
            # Setup analyzer configuration
            region = args.region or self.config.get('aws.region')
            model_id = args.model or self.config.get('aws.bedrock.model_id')
            
            # Analyze
            analyzer = BedrockRequirementsAnalyzer(region=region, model_id=model_id)
            result = analyzer.analyze_requirements(requirements_json, args.type)
            
            if not result['success']:
                utils.print_error(f"Analysis failed: {result['error']}")
                return 1
            
            utils.print_success("Analysis completed successfully!")
            
            # Save analysis output
            output_path = args.output
            if not output_path:
                input_path = Path(args.input_file)
                output_path = input_path.with_suffix('.analysis.json')
            
            with open(output_path, 'w') as f:
                json.dump(result, f, indent=2)
            
            utils.print_success(f"Analysis saved to: {output_path}")
            
            # Print summary
            self._print_analysis_summary(result['analysis'])
            
            return 0
            
        except Exception as e:
            utils.print_error(f"Analyze command failed: {str(e)}")
            logger.exception("Analyze command error")
            return 1
    
    def _handle_batch(self, args) -> int:
        """Handle batch command."""
        try:
            utils.print_info(f"Batch processing directory: {args.input_directory}")
            
            # Setup converter
            converter = MarkdownConverter()
            
            # Convert files
            results = converter.convert_directory(args.input_directory, args.recursive)
            
            if not results:
                utils.print_warning("No markdown files found to process")
                return 0
            
            successful = sum(1 for r in results if r['success'])
            utils.print_info(f"Conversion results: {successful}/{len(results)} successful")
            
            # Save JSON outputs
            if args.output:
                output_dir = Path(args.output)
                output_dir.mkdir(parents=True, exist_ok=True)
                
                for result in results:
                    if result['success']:
                        output_file = output_dir / f"{Path(result['file_path']).stem}.json"
                        converter.save_json(result['data'], output_file)
            
            # Analyze if requested
            if args.analyze:
                utils.print_info("Starting batch analysis...")
                
                analysis_results = []
                for result in results:
                    if result['success']:
                        analysis = self._analyze_json_data(result['data'], args.analysis_type)
                        analysis['source_file'] = result['file_path']
                        analysis_results.append(analysis)
                
                # Save analysis results
                if args.output:
                    analysis_file = Path(args.output) / 'batch_analysis.json'
                    with open(analysis_file, 'w') as f:
                        json.dump(analysis_results, f, indent=2)
                    utils.print_info(f"Batch analysis saved to: {analysis_file}")
            
            # Generate report if requested
            if args.report:
                self._generate_batch_report(results, args.output)
            
            return 0 if successful > 0 else 1
            
        except Exception as e:
            utils.print_error(f"Batch command failed: {str(e)}")
            logger.exception("Batch command error")
            return 1
    
    def _handle_config(self, args) -> int:
        """Handle config command."""
        try:
            if args.create_sample:
                output_path = args.output or 'config.json'
                if self.config.create_sample_config(output_path):
                    utils.print_success(f"Sample configuration created: {output_path}")
                    return 0
                else:
                    utils.print_error("Failed to create sample configuration")
                    return 1
            
            elif args.validate:
                validation = self.config.validate_config()
                
                if validation['valid']:
                    utils.print_success("Configuration is valid!")
                else:
                    utils.print_error("Configuration validation failed:")
                    for issue in validation['issues']:
                        utils.print_error(f"  - {issue}")
                
                if validation['warnings']:
                    utils.print_warning("Configuration warnings:")
                    for warning in validation['warnings']:
                        utils.print_warning(f"  - {warning}")
                
                return 0 if validation['valid'] else 1
            
            elif args.show:
                print(json.dumps(self.config.config, indent=2))
                return 0
            
            else:
                utils.print_info("Use --create-sample, --validate, or --show")
                return 1
                
        except Exception as e:
            utils.print_error(f"Config command failed: {str(e)}")
            logger.exception("Config command error")
            return 1
    
    def _handle_list(self, args) -> int:
        """Handle list command."""
        try:
            if args.models:
                region = args.region or self.config.get('aws.region')
                
                utils.print_info(f"Listing Bedrock models in region: {region}")
                
                from bedrock_analyzer import BedrockRequirementsAnalyzer
                analyzer = BedrockRequirementsAnalyzer(region=region)
                
                # This would require adding a list_models method to BedrockRequirementsAnalyzer
                utils.print_info("Model listing functionality would be implemented here")
                return 0
            
            else:
                utils.print_info("Use --models to list available Bedrock models")
                return 1
                
        except Exception as e:
            utils.print_error(f"List command failed: {str(e)}")
            logger.exception("List command error")
            return 1
    
    def _analyze_json_data(self, json_data: Dict[str, Any], analysis_type: str) -> Dict[str, Any]:
        """
        Analyze JSON data using Bedrock.
        
        Args:
            json_data: JSON data to analyze
            analysis_type: Type of analysis
            
        Returns:
            Analysis results
        """
        bedrock_config = self.config.get_bedrock_config()
        aws_config = self.config.get_aws_config()
        
        analyzer = BedrockRequirementsAnalyzer(
            region=aws_config.get('region', 'us-east-1'),
            model_id=bedrock_config.get('model_id', 'amazon.nova-lite-v1:0')
        )
        
        return analyzer.analyze_requirements(json_data, analysis_type)
    
    def _print_analysis_summary(self, analysis: Dict[str, Any]):
        """Print a summary of analysis results."""
        if 'completeness_score' in analysis:
            utils.print_info(f"Completeness Score: {analysis['completeness_score']}/100")
        
        if 'quality_score' in analysis:
            utils.print_info(f"Quality Score: {analysis['quality_score']}/100")
        
        if 'missing_elements' in analysis and analysis['missing_elements']:
            utils.print_warning("Missing Elements:")
            for element in analysis['missing_elements'][:3]:  # Show first 3
                utils.print_warning(f"  - {element}")
        
        if 'recommendations' in analysis and analysis['recommendations']:
            utils.print_info("Top Recommendations:")
            for rec in analysis['recommendations'][:3]:  # Show first 3
                utils.print_info(f"  - {rec}")
    
    def _generate_batch_report(self, results: List[Dict[str, Any]], output_dir: Optional[str]):
        """Generate a summary report for batch processing."""
        report = {
            'summary': {
                'total_files': len(results),
                'successful': sum(1 for r in results if r['success']),
                'failed': sum(1 for r in results if not r['success'])
            },
            'files': results
        }
        
        if output_dir:
            report_file = Path(output_dir) / 'batch_report.json'
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2)
            utils.print_info(f"Batch report saved to: {report_file}")
        else:
            print(json.dumps(report, indent=2))


def main():
    """Main entry point for the CLI."""
    cli = CLIInterface()
    exit_code = cli.run()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
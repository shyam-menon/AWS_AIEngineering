#!/usr/bin/env python3
"""
Markdown to JSON Converter

This module handles conversion of markdown files containing business requirements
to structured JSON format using the markdown-to-json library.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
import markdown_to_json

logger = logging.getLogger(__name__)


class MarkdownConverter:
    """
    Converts markdown files to structured JSON format.
    
    Supports both single file and batch processing with validation
    and error handling.
    """
    
    def __init__(self, validate_structure: bool = True):
        """
        Initialize the markdown converter.
        
        Args:
            validate_structure: Whether to validate markdown structure before conversion
        """
        self.validate_structure = validate_structure
        
    def convert_file(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Convert a single markdown file to JSON.
        
        Args:
            file_path: Path to the markdown file
            
        Returns:
            Dictionary containing the converted JSON data and metadata
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Markdown file not found: {file_path}")
            
        if not file_path.suffix.lower() in ['.md', '.markdown']:
            raise ValueError(f"File must be a markdown file (.md or .markdown): {file_path}")
        
        try:
            logger.info(f"Converting markdown file: {file_path}")
            
            # Read the markdown content
            with open(file_path, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
            
            # Validate structure if requested
            if self.validate_structure:
                validation_result = self._validate_markdown_structure(markdown_content)
                if not validation_result['valid']:
                    logger.warning(f"Markdown structure validation failed: {validation_result['issues']}")
            
            # Convert to JSON using markdown-to-json
            json_data = markdown_to_json.dictify(markdown_content)
            
            # Create response with metadata
            result = {
                'success': True,
                'file_path': str(file_path),
                'file_name': file_path.name,
                'data': json_data,
                'metadata': {
                    'file_size': file_path.stat().st_size,
                    'sections_count': len(json_data) if isinstance(json_data, dict) else 0,
                    'validation': validation_result if self.validate_structure else None
                }
            }
            
            logger.info(f"Successfully converted {file_path} - {result['metadata']['sections_count']} sections found")
            return result
            
        except Exception as e:
            logger.error(f"Error converting {file_path}: {str(e)}")
            return {
                'success': False,
                'file_path': str(file_path),
                'file_name': file_path.name,
                'error': str(e),
                'data': None
            }
    
    def convert_batch(self, file_paths: List[Union[str, Path]]) -> List[Dict[str, Any]]:
        """
        Convert multiple markdown files to JSON.
        
        Args:
            file_paths: List of paths to markdown files
            
        Returns:
            List of conversion results
        """
        results = []
        
        logger.info(f"Starting batch conversion of {len(file_paths)} files")
        
        for file_path in file_paths:
            try:
                result = self.convert_file(file_path)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to convert {file_path}: {str(e)}")
                results.append({
                    'success': False,
                    'file_path': str(file_path),
                    'file_name': Path(file_path).name,
                    'error': str(e),
                    'data': None
                })
        
        successful = sum(1 for r in results if r['success'])
        logger.info(f"Batch conversion completed: {successful}/{len(file_paths)} files successful")
        
        return results
    
    def convert_directory(self, directory_path: Union[str, Path], recursive: bool = True) -> List[Dict[str, Any]]:
        """
        Convert all markdown files in a directory.
        
        Args:
            directory_path: Path to the directory
            recursive: Whether to search subdirectories
            
        Returns:
            List of conversion results
        """
        directory_path = Path(directory_path)
        
        if not directory_path.exists():
            raise FileNotFoundError(f"Directory not found: {directory_path}")
            
        if not directory_path.is_dir():
            raise ValueError(f"Path is not a directory: {directory_path}")
        
        # Find all markdown files
        pattern = '**/*.md' if recursive else '*.md'
        markdown_files = list(directory_path.glob(pattern))
        markdown_files.extend(list(directory_path.glob(pattern.replace('.md', '.markdown'))))
        
        if not markdown_files:
            logger.warning(f"No markdown files found in {directory_path}")
            return []
        
        logger.info(f"Found {len(markdown_files)} markdown files in {directory_path}")
        
        return self.convert_batch(markdown_files)
    
    def _validate_markdown_structure(self, content: str) -> Dict[str, Any]:
        """
        Validate the structure of markdown content.
        
        Args:
            content: Markdown content to validate
            
        Returns:
            Validation result with issues identified
        """
        issues = []
        valid = True
        
        lines = content.split('\n')
        has_headers = False
        header_levels = []
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            
            # Check for headers
            if line.startswith('#'):
                has_headers = True
                level = len(line) - len(line.lstrip('#'))
                header_levels.append(level)
            
            # Check for empty content
            if not line and line_num < len(lines) - 1:
                continue
        
        # Validate header structure
        if not has_headers:
            issues.append("No headers found - markdown should have section headers")
            valid = False
        
        if header_levels:
            # Check for proper header hierarchy
            for i in range(1, len(header_levels)):
                if header_levels[i] > header_levels[i-1] + 1:
                    issues.append(f"Header level jump detected - missing intermediate level")
                    valid = False
                    break
        
        # Check content length
        if len(content.strip()) < 50:
            issues.append("Content appears too short for meaningful requirements")
            valid = False
        
        return {
            'valid': valid,
            'issues': issues,
            'stats': {
                'total_lines': len(lines),
                'header_count': len(header_levels),
                'content_length': len(content)
            }
        }
    
    def save_json(self, json_data: Dict[str, Any], output_path: Union[str, Path], 
                  pretty: bool = True) -> bool:
        """
        Save JSON data to a file.
        
        Args:
            json_data: JSON data to save
            output_path: Path for the output file
            pretty: Whether to format JSON with indentation
            
        Returns:
            True if successful, False otherwise
        """
        try:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                if pretty:
                    json.dump(json_data, f, indent=2, ensure_ascii=False)
                else:
                    json.dump(json_data, f, ensure_ascii=False)
            
            logger.info(f"JSON data saved to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving JSON to {output_path}: {str(e)}")
            return False


# Utility functions for common operations
def convert_single_file(file_path: Union[str, Path], output_path: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
    """
    Convenience function to convert a single file.
    
    Args:
        file_path: Path to the markdown file
        output_path: Optional path for JSON output
        
    Returns:
        Conversion result
    """
    converter = MarkdownConverter()
    result = converter.convert_file(file_path)
    
    if output_path and result['success']:
        converter.save_json(result['data'], output_path)
    
    return result


def convert_directory_to_json(directory_path: Union[str, Path], 
                             output_dir: Optional[Union[str, Path]] = None,
                             recursive: bool = True) -> List[Dict[str, Any]]:
    """
    Convenience function to convert all markdown files in a directory.
    
    Args:
        directory_path: Path to the directory
        output_dir: Optional directory for JSON outputs
        recursive: Whether to search subdirectories
        
    Returns:
        List of conversion results
    """
    converter = MarkdownConverter()
    results = converter.convert_directory(directory_path, recursive)
    
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for result in results:
            if result['success']:
                output_file = output_dir / f"{Path(result['file_path']).stem}.json"
                converter.save_json(result['data'], output_file)
    
    return results


if __name__ == "__main__":
    # Simple test when run directly
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python markdown_converter.py <markdown_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    result = convert_single_file(file_path)
    
    if result['success']:
        print(f"✅ Conversion successful!")
        print(f"📊 Sections found: {result['metadata']['sections_count']}")
        print(json.dumps(result['data'], indent=2))
    else:
        print(f"❌ Conversion failed: {result['error']}")
        sys.exit(1)
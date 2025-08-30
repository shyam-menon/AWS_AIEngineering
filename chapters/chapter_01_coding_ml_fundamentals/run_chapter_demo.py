"""
Chapter 1 Demo: Python Fundamentals for AI Development
======================================================

This script demonstrates all the Python fundamentals covered in Chapter 1.
Run this to see a comprehensive overview of all concepts.

Author: AWS AI Engineering Course
Date: August 2025
"""

import sys
import time

def print_section_header(title):
    """Print a formatted section header."""
    print("\n" + "="*60)
    print(f"🐍 {title}")
    print("="*60)

def print_demo_header(title):
    """Print a formatted demo header."""
    print(f"\n📚 {title}")
    print("-" * (len(title) + 4))

def wait_for_user():
    """Wait for user input to continue."""
    input("\n▶️  Press Enter to continue to the next section...")

def main():
    """Run all Python fundamentals demonstrations."""
    
    print("🚀 Welcome to Chapter 1: Python Fundamentals for AI Development!")
    print("This demo will walk you through all the core Python concepts.")
    print("Each section builds the foundation for AI engineering.")
    
    wait_for_user()
    
    # 1. Data Types and Structures
    print_section_header("1. DATA TYPES AND STRUCTURES")
    print("Understanding Python's built-in data types and collections...")
    
    try:
        import python_data_types
        python_data_types.demonstrate_basic_data_types()
        python_data_types.demonstrate_data_structures()
        python_data_types.demonstrate_type_conversion()
        python_data_types.ai_development_examples()
    except ImportError as e:
        print(f"⚠️  Could not import python_data_types: {e}")
        print("Make sure python_data_types.py is in the same directory.")
    
    wait_for_user()
    
    # 2. Control Flow
    print_section_header("2. CONTROL FLOW")
    print("Mastering conditional statements and loops...")
    
    try:
        import python_control_flow
        python_control_flow.demonstrate_conditional_statements()
        python_control_flow.demonstrate_loops()
        python_control_flow.ai_development_control_flow()
    except ImportError as e:
        print(f"⚠️  Could not import python_control_flow: {e}")
    
    wait_for_user()
    
    # 3. Functions
    print_section_header("3. FUNCTIONS")
    print("Learning to organize code into reusable blocks...")
    
    try:
        import python_functions
        python_functions.demonstrate_basic_functions()
        python_functions.demonstrate_advanced_parameters()
        python_functions.ai_development_functions()
    except ImportError as e:
        print(f"⚠️  Could not import python_functions: {e}")
    
    wait_for_user()
    
    # 4. Object-Oriented Programming
    print_section_header("4. OBJECT-ORIENTED PROGRAMMING")
    print("Building modular and scalable applications with OOP...")
    
    try:
        import python_oop
        python_oop.demonstrate_classes_and_objects()
        python_oop.demonstrate_inheritance()
        python_oop.ai_development_oop()
    except ImportError as e:
        print(f"⚠️  Could not import python_oop: {e}")
    
    wait_for_user()
    
    # 5. File I/O
    print_section_header("5. FILE INPUT/OUTPUT")
    print("Handling data and logs through file operations...")
    
    try:
        import python_file_io
        python_file_io.demonstrate_basic_file_operations()
        python_file_io.demonstrate_json_handling()
        python_file_io.ai_development_file_patterns()
    except ImportError as e:
        print(f"⚠️  Could not import python_file_io: {e}")
    
    wait_for_user()
    
    # 6. AWS Infrastructure (if available)
    print_section_header("6. AWS INFRASTRUCTURE BASICS")
    print("Connecting Python to AWS services...")
    
    try:
        print("🔧 Testing AWS connectivity with EC2...")
        import subprocess
        result = subprocess.run([sys.executable, "ec2_list.py"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ AWS EC2 example ran successfully!")
            print("Output preview:")
            print(result.stdout[:300] + "..." if len(result.stdout) > 300 else result.stdout)
        else:
            print("⚠️  AWS credentials may not be configured.")
            print("Error:", result.stderr[:200])
    except Exception as e:
        print(f"⚠️  Could not run EC2 example: {e}")
    
    # Final Summary
    print_section_header("CHAPTER 1 COMPLETION SUMMARY")
    
    skills_learned = [
        "✅ Data Types: int, float, str, bool, list, dict, tuple, set",
        "✅ Control Flow: if/elif/else, for/while loops, comprehensions",
        "✅ Functions: definition, parameters, scope, lambda functions",
        "✅ OOP: classes, objects, inheritance, polymorphism, encapsulation",
        "✅ File I/O: reading/writing files, JSON, CSV, error handling",
        "✅ AWS Basics: Boto3, EC2 interaction, infrastructure concepts"
    ]
    
    print("🎉 Congratulations! You've completed Chapter 1.")
    print("You've learned the following Python fundamentals for AI development:")
    print()
    for skill in skills_learned:
        print(f"  {skill}")
    
    print("\n🔥 Key AI Development Patterns You've Learned:")
    ai_patterns = [
        "📊 Data structures for model configurations",
        "🔄 Control flow for training loops and preprocessing",
        "🧩 Functions for modular AI pipeline components",
        "🏗️  Object-oriented design for model hierarchies",
        "💾 File I/O for datasets, checkpoints, and logging",
        "☁️  AWS integration for cloud-based AI workflows"
    ]
    
    for pattern in ai_patterns:
        print(f"  {pattern}")
    
    print("\n🚀 Ready for Chapter 2: LLM APIs and AWS Bedrock!")
    print("You now have the Python foundation to build sophisticated AI applications.")
    
    print("\n📚 Quick Reference Commands:")
    print("  python python_data_types.py    # Data types and structures")
    print("  python python_control_flow.py  # Conditional statements and loops")
    print("  python python_functions.py     # Function definition and usage")
    print("  python python_oop.py           # Object-oriented programming")
    print("  python python_file_io.py       # File input/output operations")
    print("  python ec2_list.py             # AWS EC2 interaction")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user. Thanks for exploring Chapter 1!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An error occurred during the demo: {e}")
        print("Please ensure all Python fundamental files are in the same directory.")
        sys.exit(1)

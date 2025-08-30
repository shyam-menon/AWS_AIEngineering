"""
Python Data Types and Structures Examples
=========================================

This module demonstrates the fundamental data types and structures in Python
that are essential for AI development.

Author: AWS AI Engineering Course
Date: August 2025
"""

def demonstrate_basic_data_types():
    """Demonstrate Python's built-in data types."""
    print("=== BASIC DATA TYPES ===\n")
    
    # Integers
    age = 25
    year = 2025
    negative_num = -10
    print(f"Integers: age = {age}, year = {year}, negative = {negative_num}")
    print(f"Type of age: {type(age)}")
    
    # Floats
    height = 5.8
    pi = 3.14159
    scientific = 1.5e-4  # Scientific notation
    print(f"\nFloats: height = {height}, pi = {pi}, scientific = {scientific}")
    print(f"Type of height: {type(height)}")
    
    # Strings
    name = "Alice"
    message = 'Hello, World!'
    multiline = """This is a
    multiline string
    for documentation"""
    print(f"\nStrings: name = '{name}', message = '{message}'")
    print(f"Multiline:\n{multiline}")
    print(f"Type of name: {type(name)}")
    
    # Booleans
    is_active = True
    is_completed = False
    print(f"\nBooleans: is_active = {is_active}, is_completed = {is_completed}")
    print(f"Type of is_active: {type(is_active)}")
    
    # None type
    result = None
    print(f"\nNone type: result = {result}")
    print(f"Type of None: {type(result)}")

def demonstrate_data_structures():
    """Demonstrate Python's built-in data structures."""
    print("\n=== DATA STRUCTURES ===\n")
    
    # Lists - Ordered, mutable collections
    print("1. LISTS (ordered, mutable)")
    fruits = ["apple", "banana", "cherry"]
    numbers = [1, 2, 3, 4, 5]
    mixed = ["Alice", 25, True, 3.14]
    
    print(f"Fruits: {fruits}")
    print(f"Numbers: {numbers}")
    print(f"Mixed types: {mixed}")
    
    # List operations
    fruits.append("orange")
    print(f"After append: {fruits}")
    fruits.remove("banana")
    print(f"After remove: {fruits}")
    print(f"First fruit: {fruits[0]}")
    print(f"Last fruit: {fruits[-1]}")
    print(f"List length: {len(fruits)}")
    
    # Tuples - Ordered, immutable collections
    print("\n2. TUPLES (ordered, immutable)")
    coordinates = (10.5, 20.3)
    rgb_color = (255, 128, 0)
    person = ("Bob", 30, "Engineer")
    
    print(f"Coordinates: {coordinates}")
    print(f"RGB Color: {rgb_color}")
    print(f"Person: {person}")
    
    # Tuple operations
    x, y = coordinates  # Unpacking
    print(f"Unpacked coordinates: x = {x}, y = {y}")
    print(f"First element: {person[0]}")
    print(f"Tuple length: {len(person)}")
    
    # Dictionaries - Key-value pairs, unordered, mutable
    print("\n3. DICTIONARIES (key-value pairs, mutable)")
    student = {
        "name": "Charlie",
        "age": 22,
        "major": "Computer Science",
        "gpa": 3.8
    }
    
    print(f"Student: {student}")
    print(f"Student name: {student['name']}")
    print(f"Student GPA: {student.get('gpa', 'N/A')}")
    
    # Dictionary operations
    student["graduation_year"] = 2024
    print(f"After adding graduation year: {student}")
    
    print(f"Keys: {list(student.keys())}")
    print(f"Values: {list(student.values())}")
    print(f"Items: {list(student.items())}")
    
    # Sets - Unordered collections of unique elements
    print("\n4. SETS (unordered, unique elements)")
    colors = {"red", "green", "blue"}
    numbers_set = {1, 2, 3, 4, 5, 5, 5}  # Duplicates will be removed
    
    print(f"Colors: {colors}")
    print(f"Numbers set (duplicates removed): {numbers_set}")
    
    # Set operations
    colors.add("yellow")
    print(f"After adding yellow: {colors}")
    
    colors2 = {"blue", "purple", "orange"}
    print(f"Colors2: {colors2}")
    print(f"Union: {colors | colors2}")
    print(f"Intersection: {colors & colors2}")
    print(f"Difference: {colors - colors2}")

def demonstrate_type_conversion():
    """Demonstrate type conversion between data types."""
    print("\n=== TYPE CONVERSION ===\n")
    
    # String to number conversion
    age_str = "25"
    age_int = int(age_str)
    height_str = "5.8"
    height_float = float(height_str)
    
    print(f"String to int: '{age_str}' -> {age_int}")
    print(f"String to float: '{height_str}' -> {height_float}")
    
    # Number to string conversion
    number = 42
    number_str = str(number)
    print(f"Int to string: {number} -> '{number_str}'")
    
    # List/tuple/set conversions
    list_data = [1, 2, 3, 4, 4]
    tuple_data = tuple(list_data)
    set_data = set(list_data)
    
    print(f"List to tuple: {list_data} -> {tuple_data}")
    print(f"List to set: {list_data} -> {set_data}")
    print(f"Set to list: {set_data} -> {list(set_data)}")

def ai_development_examples():
    """Examples of how these data types are used in AI development."""
    print("\n=== AI DEVELOPMENT EXAMPLES ===\n")
    
    # Model configuration using dictionary
    model_config = {
        "model_name": "claude-3-sonnet",
        "max_tokens": 1000,
        "temperature": 0.7,
        "top_p": 0.95,
        "features": ["text_generation", "conversation", "analysis"]
    }
    print("Model Configuration:")
    for key, value in model_config.items():
        print(f"  {key}: {value}")
    
    # Training data as list of tuples
    training_data = [
        ("What is AI?", "Artificial Intelligence is..."),
        ("Explain ML", "Machine Learning is..."),
        ("Define NLP", "Natural Language Processing is...")
    ]
    print(f"\nTraining Data (first example): {training_data[0]}")
    
    # Feature vectors as lists
    feature_vector = [0.2, 0.8, 0.1, 0.9, 0.3]
    labels = ["positive", "negative", "neutral"]
    
    print(f"Feature Vector: {feature_vector}")
    print(f"Classification Labels: {labels}")
    
    # Model performance metrics as dictionary
    metrics = {
        "accuracy": 0.95,
        "precision": 0.92,
        "recall": 0.89,
        "f1_score": 0.90
    }
    print(f"\nModel Metrics: {metrics}")

if __name__ == "__main__":
    demonstrate_basic_data_types()
    demonstrate_data_structures()
    demonstrate_type_conversion()
    ai_development_examples()
    
    print("\n" + "="*50)
    print("SUMMARY: Python Data Types & Structures")
    print("="*50)
    print("✓ Basic Types: int, float, str, bool, None")
    print("✓ Lists: Ordered, mutable collections")
    print("✓ Tuples: Ordered, immutable collections")
    print("✓ Dictionaries: Key-value pairs, mutable")
    print("✓ Sets: Unordered, unique elements")
    print("✓ Type conversion between different types")
    print("✓ AI development use cases and examples")

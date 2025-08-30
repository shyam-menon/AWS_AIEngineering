"""
Python Functions Examples
=========================

This module demonstrates how to define and use functions in Python,
including parameters, return values, and best practices for AI development.

Author: AWS AI Engineering Course
Date: August 2025
"""

def demonstrate_basic_functions():
    """Demonstrate basic function definition and calling."""
    print("=== BASIC FUNCTIONS ===\n")
    
    # Simple function with no parameters
    def greet():
        return "Hello, World!"
    
    # Function with parameters
    def greet_person(name):
        return f"Hello, {name}!"
    
    # Function with multiple parameters
    def add_numbers(a, b):
        return a + b
    
    # Function with default parameters
    def greet_with_title(name, title="Mr./Ms."):
        return f"Hello, {title} {name}!"
    
    print("1. BASIC FUNCTION CALLS")
    print(f"greet(): {greet()}")
    print(f"greet_person('Alice'): {greet_person('Alice')}")
    print(f"add_numbers(5, 3): {add_numbers(5, 3)}")
    print(f"greet_with_title('Smith'): {greet_with_title('Smith')}")
    print(f"greet_with_title('Johnson', 'Dr.'): {greet_with_title('Johnson', 'Dr.')}")

def demonstrate_advanced_parameters():
    """Demonstrate advanced parameter features."""
    print("\n=== ADVANCED PARAMETERS ===\n")
    
    # Function with *args (variable positional arguments)
    def sum_all(*numbers):
        total = 0
        for num in numbers:
            total += num
        return total
    
    # Function with **kwargs (variable keyword arguments)
    def create_profile(**kwargs):
        profile = {}
        for key, value in kwargs.items():
            profile[key] = value
        return profile
    
    # Function with mixed parameters
    def process_data(required_param, default_param="default", *args, **kwargs):
        result = {
            "required": required_param,
            "default": default_param,
            "extra_args": args,
            "extra_kwargs": kwargs
        }
        return result
    
    print("1. VARIABLE ARGUMENTS")
    print(f"sum_all(1, 2, 3): {sum_all(1, 2, 3)}")
    print(f"sum_all(1, 2, 3, 4, 5): {sum_all(1, 2, 3, 4, 5)}")
    
    print("\n2. KEYWORD ARGUMENTS")
    profile = create_profile(name="Alice", age=25, city="New York", job="Engineer")
    print(f"Profile: {profile}")
    
    print("\n3. MIXED PARAMETERS")
    result = process_data("mandatory", "custom", 1, 2, 3, extra="value", flag=True)
    print(f"Result: {result}")

def demonstrate_return_values():
    """Demonstrate different types of return values."""
    print("\n=== RETURN VALUES ===\n")
    
    # Function returning multiple values
    def get_statistics(numbers):
        if not numbers:
            return None, None, None
        
        total = sum(numbers)
        average = total / len(numbers)
        maximum = max(numbers)
        return total, average, maximum
    
    # Function returning different types based on conditions
    def process_input(value):
        if isinstance(value, str):
            return value.upper()
        elif isinstance(value, (int, float)):
            return value * 2
        elif isinstance(value, list):
            return len(value)
        else:
            return None
    
    # Function with early return
    def validate_age(age):
        if age < 0:
            return False, "Age cannot be negative"
        if age > 150:
            return False, "Age seems unrealistic"
        return True, "Valid age"
    
    print("1. MULTIPLE RETURN VALUES")
    numbers = [10, 20, 30, 40, 50]
    total, avg, max_val = get_statistics(numbers)
    print(f"Numbers: {numbers}")
    print(f"Total: {total}, Average: {avg:.1f}, Maximum: {max_val}")
    
    print("\n2. CONDITIONAL RETURNS")
    test_values = ["hello", 42, [1, 2, 3, 4], True]
    for value in test_values:
        result = process_input(value)
        print(f"process_input({value}): {result}")
    
    print("\n3. VALIDATION WITH EARLY RETURN")
    test_ages = [-5, 25, 200]
    for age in test_ages:
        is_valid, message = validate_age(age)
        print(f"Age {age}: {message} (Valid: {is_valid})")

def demonstrate_scope():
    """Demonstrate variable scope in functions."""
    print("\n=== VARIABLE SCOPE ===\n")
    
    global_var = "I'm global"
    
    def demonstrate_local_scope():
        local_var = "I'm local"
        print(f"Inside function - Local: {local_var}")
        print(f"Inside function - Global: {global_var}")
    
    def modify_global():
        global global_var
        global_var = "Modified global"
        print(f"Modified global variable: {global_var}")
    
    def demonstrate_nonlocal():
        outer_var = "I'm in outer function"
        
        def inner_function():
            nonlocal outer_var
            outer_var = "Modified by inner function"
            print(f"Inner function modified: {outer_var}")
        
        print(f"Before inner function: {outer_var}")
        inner_function()
        print(f"After inner function: {outer_var}")
        
        return outer_var
    
    print("1. LOCAL AND GLOBAL SCOPE")
    print(f"Global variable: {global_var}")
    demonstrate_local_scope()
    
    print("\n2. MODIFYING GLOBAL VARIABLES")
    modify_global()
    print(f"Global after modification: {global_var}")
    
    print("\n3. NONLOCAL VARIABLES")
    result = demonstrate_nonlocal()
    print(f"Returned value: {result}")

def ai_development_functions():
    """Functions commonly used in AI development."""
    print("\n=== AI DEVELOPMENT FUNCTIONS ===\n")
    
    def preprocess_text(text, lowercase=True, remove_punctuation=True):
        """Preprocess text for AI model input."""
        if not isinstance(text, str):
            return ""
        
        processed = text.strip()
        
        if lowercase:
            processed = processed.lower()
        
        if remove_punctuation:
            import string
            processed = processed.translate(str.maketrans("", "", string.punctuation))
        
        return processed
    
    def calculate_accuracy(predictions, actual):
        """Calculate model accuracy."""
        if len(predictions) != len(actual):
            raise ValueError("Predictions and actual values must have same length")
        
        if not predictions:
            return 0.0
        
        correct = sum(1 for p, a in zip(predictions, actual) if p == a)
        accuracy = correct / len(predictions)
        return accuracy
    
    def create_model_config(model_name, **parameters):
        """Create a standardized model configuration."""
        default_config = {
            "max_tokens": 1000,
            "temperature": 0.7,
            "top_p": 0.95,
            "model": model_name
        }
        
        # Update with provided parameters
        default_config.update(parameters)
        return default_config
    
    def batch_process(data, batch_size=32, processor_func=None):
        """Process data in batches."""
        if processor_func is None:
            processor_func = lambda x: x  # Identity function
        
        results = []
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            batch_results = [processor_func(item) for item in batch]
            results.extend(batch_results)
            print(f"Processed batch {i//batch_size + 1}: {len(batch)} items")
        
        return results
    
    print("1. TEXT PREPROCESSING")
    sample_texts = [
        "Hello, World!",
        "This is a SAMPLE text with Punctuation!!!",
        "  Another Example.  "
    ]
    
    for text in sample_texts:
        processed = preprocess_text(text)
        print(f"'{text}' -> '{processed}'")
    
    print("\n2. MODEL ACCURACY CALCULATION")
    predictions = ["positive", "negative", "positive", "negative", "positive"]
    actual = ["positive", "positive", "positive", "negative", "positive"]
    
    accuracy = calculate_accuracy(predictions, actual)
    print(f"Predictions: {predictions}")
    print(f"Actual:      {actual}")
    print(f"Accuracy: {accuracy:.2%}")
    
    print("\n3. MODEL CONFIGURATION")
    config1 = create_model_config("claude-3-sonnet")
    config2 = create_model_config("claude-3-opus", temperature=0.3, max_tokens=2000)
    
    print(f"Default config: {config1}")
    print(f"Custom config: {config2}")
    
    print("\n4. BATCH PROCESSING")
    data = list(range(1, 11))  # [1, 2, 3, ..., 10]
    
    def square_number(x):
        return x ** 2
    
    results = batch_process(data, batch_size=3, processor_func=square_number)
    print(f"Original data: {data}")
    print(f"Squared results: {results}")

def demonstrate_lambda_functions():
    """Demonstrate lambda (anonymous) functions."""
    print("\n=== LAMBDA FUNCTIONS ===\n")
    
    # Basic lambda function
    square = lambda x: x ** 2
    add = lambda a, b: a + b
    
    print("1. BASIC LAMBDA FUNCTIONS")
    print(f"square(5): {square(5)}")
    print(f"add(3, 7): {add(3, 7)}")
    
    # Lambda with map, filter, sorted
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    print("\n2. LAMBDA WITH BUILT-IN FUNCTIONS")
    squares = list(map(lambda x: x**2, numbers))
    print(f"Squares: {squares}")
    
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    print(f"Even numbers: {evens}")
    
    # Lambda for sorting
    students = [("Alice", 85), ("Bob", 90), ("Charlie", 78)]
    sorted_by_grade = sorted(students, key=lambda student: student[1])
    print(f"Students sorted by grade: {sorted_by_grade}")

if __name__ == "__main__":
    demonstrate_basic_functions()
    demonstrate_advanced_parameters()
    demonstrate_return_values()
    demonstrate_scope()
    ai_development_functions()
    demonstrate_lambda_functions()
    
    print("\n" + "="*50)
    print("SUMMARY: Python Functions")
    print("="*50)
    print("✓ Basic function definition and calling")
    print("✓ Parameters: positional, default, *args, **kwargs")
    print("✓ Return values: single, multiple, conditional")
    print("✓ Variable scope: local, global, nonlocal")
    print("✓ Lambda functions: anonymous functions")
    print("✓ AI development function patterns")
    print("✓ Error handling and validation")
    print("✓ Code reusability and modularity")

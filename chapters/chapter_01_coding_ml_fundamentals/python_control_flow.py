"""
Python Control Flow Examples
============================

This module demonstrates control flow statements in Python including
conditional statements and loops, essential for AI development logic.

Author: AWS AI Engineering Course
Date: August 2025
"""

def demonstrate_conditional_statements():
    """Demonstrate if, elif, else statements."""
    print("=== CONDITIONAL STATEMENTS ===\n")
    
    # Basic if statement
    print("1. BASIC IF STATEMENT")
    temperature = 75
    if temperature > 70:
        print(f"Temperature {temperature}°F - It's warm outside!")
    
    # If-else statement
    print("\n2. IF-ELSE STATEMENT")
    age = 20
    if age >= 18:
        print(f"Age {age} - You are an adult.")
    else:
        print(f"Age {age} - You are a minor.")
    
    # If-elif-else statement
    print("\n3. IF-ELIF-ELSE STATEMENT")
    score = 85
    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    elif score >= 60:
        grade = "D"
    else:
        grade = "F"
    print(f"Score: {score}, Grade: {grade}")
    
    # Nested conditions
    print("\n4. NESTED CONDITIONS")
    weather = "sunny"
    temperature = 75
    
    if weather == "sunny":
        if temperature > 70:
            activity = "Go to the beach"
        else:
            activity = "Go for a walk"
    elif weather == "rainy":
        activity = "Stay inside and read"
    else:
        activity = "Check weather again"
    
    print(f"Weather: {weather}, Temp: {temperature}°F")
    print(f"Suggested activity: {activity}")

def demonstrate_comparison_operators():
    """Demonstrate comparison and logical operators."""
    print("\n=== COMPARISON & LOGICAL OPERATORS ===\n")
    
    a, b = 10, 5
    
    print("1. COMPARISON OPERATORS")
    print(f"a = {a}, b = {b}")
    print(f"a == b: {a == b}")  # Equal
    print(f"a != b: {a != b}")  # Not equal
    print(f"a > b: {a > b}")    # Greater than
    print(f"a < b: {a < b}")    # Less than
    print(f"a >= b: {a >= b}")  # Greater than or equal
    print(f"a <= b: {a <= b}")  # Less than or equal
    
    print("\n2. LOGICAL OPERATORS")
    x, y, z = True, False, True
    print(f"x = {x}, y = {y}, z = {z}")
    print(f"x and y: {x and y}")  # AND
    print(f"x or y: {x or y}")    # OR
    print(f"not x: {not x}")      # NOT
    print(f"x and (y or z): {x and (y or z)}")  # Complex

def demonstrate_loops():
    """Demonstrate for and while loops."""
    print("\n=== LOOPS ===\n")
    
    # For loop with range
    print("1. FOR LOOP WITH RANGE")
    print("Counting from 1 to 5:")
    for i in range(1, 6):
        print(f"  Count: {i}")
    
    # For loop with list
    print("\n2. FOR LOOP WITH LIST")
    fruits = ["apple", "banana", "cherry", "date"]
    print("Iterating through fruits:")
    for fruit in fruits:
        print(f"  Fruit: {fruit}")
    
    # For loop with enumerate
    print("\n3. FOR LOOP WITH ENUMERATE")
    colors = ["red", "green", "blue"]
    print("Colors with indices:")
    for index, color in enumerate(colors):
        print(f"  {index}: {color}")
    
    # For loop with dictionary
    print("\n4. FOR LOOP WITH DICTIONARY")
    student = {"name": "Alice", "age": 20, "major": "CS"}
    print("Student information:")
    for key, value in student.items():
        print(f"  {key}: {value}")
    
    # While loop
    print("\n5. WHILE LOOP")
    count = 0
    print("While loop counting to 3:")
    while count < 3:
        print(f"  Count: {count}")
        count += 1
    
    # While loop with condition
    print("\n6. WHILE LOOP WITH CONDITION")
    numbers = [1, 3, 5, 8, 9, 10]
    i = 0
    print("Finding first even number:")
    while i < len(numbers):
        if numbers[i] % 2 == 0:
            print(f"  First even number: {numbers[i]} at index {i}")
            break
        i += 1

def demonstrate_loop_control():
    """Demonstrate break, continue, and else in loops."""
    print("\n=== LOOP CONTROL STATEMENTS ===\n")
    
    # Break statement
    print("1. BREAK STATEMENT")
    print("Searching for number 7:")
    numbers = [1, 3, 5, 7, 9, 11]
    for num in numbers:
        if num == 7:
            print(f"  Found {num}! Breaking the loop.")
            break
        print(f"  Checking {num}")
    
    # Continue statement
    print("\n2. CONTINUE STATEMENT")
    print("Printing only even numbers:")
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for num in numbers:
        if num % 2 != 0:  # If odd, skip
            continue
        print(f"  Even number: {num}")
    
    # Else with for loop
    print("\n3. ELSE WITH FOR LOOP")
    print("Searching for number 15:")
    search_list = [1, 3, 5, 7, 9, 11]
    for num in search_list:
        if num == 15:
            print(f"  Found {num}!")
            break
        print(f"  Checking {num}")
    else:
        print("  Number 15 not found in the list.")

def ai_development_control_flow():
    """Examples of control flow in AI development contexts."""
    print("\n=== AI DEVELOPMENT CONTROL FLOW ===\n")
    
    # Model selection based on task
    print("1. MODEL SELECTION LOGIC")
    task_type = "text_generation"
    dataset_size = "large"
    
    if task_type == "text_generation":
        if dataset_size == "large":
            model = "claude-3-opus"
        else:
            model = "claude-3-haiku"
    elif task_type == "analysis":
        model = "claude-3-sonnet"
    else:
        model = "claude-3-haiku"  # Default
    
    print(f"Task: {task_type}, Dataset: {dataset_size}")
    print(f"Selected model: {model}")
    
    # Data preprocessing loop
    print("\n2. DATA PREPROCESSING")
    raw_data = ["Hello World!", "  Clean this text  ", "", "Another example!"]
    processed_data = []
    
    print("Processing text data:")
    for i, text in enumerate(raw_data):
        if not text.strip():  # Skip empty strings
            print(f"  {i}: Skipped empty text")
            continue
        
        # Clean and process
        cleaned = text.strip().lower()
        processed_data.append(cleaned)
        print(f"  {i}: '{text}' -> '{cleaned}'")
    
    print(f"Processed {len(processed_data)} out of {len(raw_data)} items")
    
    # Training loop simulation
    print("\n3. TRAINING LOOP SIMULATION")
    epochs = 3
    learning_rate = 0.01
    loss_threshold = 0.1
    
    for epoch in range(1, epochs + 1):
        # Simulate training
        epoch_loss = 1.0 / epoch  # Decreasing loss
        
        print(f"Epoch {epoch}/{epochs}")
        print(f"  Loss: {epoch_loss:.3f}")
        
        if epoch_loss < loss_threshold:
            print(f"  Early stopping! Loss below threshold ({loss_threshold})")
            break
        
        if epoch == epochs:
            print("  Training completed!")
    
    # Batch processing
    print("\n4. BATCH PROCESSING")
    data_points = list(range(1, 21))  # 20 data points
    batch_size = 5
    
    print(f"Processing {len(data_points)} items in batches of {batch_size}:")
    for i in range(0, len(data_points), batch_size):
        batch = data_points[i:i + batch_size]
        print(f"  Batch {i//batch_size + 1}: {batch}")

def demonstrate_list_comprehensions():
    """Demonstrate list comprehensions as advanced control flow."""
    print("\n=== LIST COMPREHENSIONS ===\n")
    
    # Basic list comprehension
    squares = [x**2 for x in range(1, 6)]
    print(f"Squares: {squares}")
    
    # List comprehension with condition
    even_squares = [x**2 for x in range(1, 11) if x % 2 == 0]
    print(f"Even squares: {even_squares}")
    
    # Processing text data
    texts = ["Hello", "WORLD", "Python", "AI"]
    processed = [text.lower() for text in texts if len(text) > 2]
    print(f"Processed texts: {processed}")
    
    # Dictionary comprehension
    word_lengths = {word: len(word) for word in texts}
    print(f"Word lengths: {word_lengths}")

if __name__ == "__main__":
    demonstrate_conditional_statements()
    demonstrate_comparison_operators()
    demonstrate_loops()
    demonstrate_loop_control()
    ai_development_control_flow()
    demonstrate_list_comprehensions()
    
    print("\n" + "="*50)
    print("SUMMARY: Python Control Flow")
    print("="*50)
    print("✓ Conditional statements: if, elif, else")
    print("✓ Comparison operators: ==, !=, <, >, <=, >=")
    print("✓ Logical operators: and, or, not")
    print("✓ For loops: range, lists, dictionaries")
    print("✓ While loops: condition-based iteration")
    print("✓ Loop control: break, continue, else")
    print("✓ List comprehensions: concise iteration")
    print("✓ AI development applications")

"""
Python File I/O Examples
========================

This module demonstrates how to read from and write to files in Python,
which is essential for handling data and logs in AI development.

Author: AWS AI Engineering Course
Date: August 2025
"""

import os
import json
import csv
from pathlib import Path

def demonstrate_basic_file_operations():
    """Demonstrate basic file reading and writing operations."""
    print("=== BASIC FILE OPERATIONS ===\n")
    
    # Create a sample directory for our examples
    sample_dir = Path("sample_files")
    sample_dir.mkdir(exist_ok=True)
    
    print("1. WRITING TO FILES")
    
    # Write to a text file
    file_path = sample_dir / "sample.txt"
    
    # Method 1: Using open() and close()
    file = open(file_path, 'w')
    file.write("Hello, World!\n")
    file.write("This is a sample file.\n")
    file.close()
    print(f"Written to {file_path}")
    
    # Method 2: Using context manager (recommended)
    with open(file_path, 'a') as f:  # 'a' for append mode
        f.write("This line was appended.\n")
        f.write("Another appended line.\n")
    print(f"Appended to {file_path}")
    
    print("\n2. READING FROM FILES")
    
    # Read entire file
    with open(file_path, 'r') as f:
        content = f.read()
        print("Entire file content:")
        print(content)
    
    # Read line by line
    with open(file_path, 'r') as f:
        print("Reading line by line:")
        for line_num, line in enumerate(f, 1):
            print(f"  Line {line_num}: {line.strip()}")
    
    # Read all lines into a list
    with open(file_path, 'r') as f:
        lines = f.readlines()
        print(f"\nRead {len(lines)} lines into a list")
        print(f"First line: '{lines[0].strip()}'")

def demonstrate_file_modes():
    """Demonstrate different file opening modes."""
    print("\n=== FILE MODES ===\n")
    
    sample_dir = Path("sample_files")
    
    # Different file modes
    modes_demo = sample_dir / "modes_demo.txt"
    
    print("1. WRITE MODE ('w') - Overwrites existing file")
    with open(modes_demo, 'w') as f:
        f.write("Original content\n")
    
    # Read to verify
    with open(modes_demo, 'r') as f:
        print(f"After write mode: {f.read().strip()}")
    
    print("\n2. APPEND MODE ('a') - Adds to existing file")
    with open(modes_demo, 'a') as f:
        f.write("Appended content\n")
    
    with open(modes_demo, 'r') as f:
        print(f"After append mode:\n{f.read()}")
    
    print("3. READ MODE ('r') - Default mode")
    try:
        with open(modes_demo, 'r') as f:
            print(f"Reading in read mode: {f.readline().strip()}")
    except FileNotFoundError:
        print("File not found!")
    
    print("\n4. BINARY MODES")
    binary_file = sample_dir / "binary_demo.bin"
    
    # Write binary data
    data = b"Binary data: \x00\x01\x02\x03"
    with open(binary_file, 'wb') as f:
        f.write(data)
    
    # Read binary data
    with open(binary_file, 'rb') as f:
        read_data = f.read()
        print(f"Binary data: {read_data}")

def demonstrate_json_handling():
    """Demonstrate working with JSON files."""
    print("\n=== JSON FILE HANDLING ===\n")
    
    sample_dir = Path("sample_files")
    
    # Sample data structure
    ai_model_config = {
        "model_name": "claude-3-sonnet",
        "parameters": {
            "max_tokens": 1000,
            "temperature": 0.7,
            "top_p": 0.95
        },
        "training_data": [
            {"text": "Sample training text 1", "label": "positive"},
            {"text": "Sample training text 2", "label": "negative"},
            {"text": "Sample training text 3", "label": "neutral"}
        ],
        "metadata": {
            "created_by": "AI Engineer",
            "version": "1.0",
            "timestamp": "2025-08-30"
        }
    }
    
    json_file = sample_dir / "model_config.json"
    
    print("1. WRITING JSON DATA")
    with open(json_file, 'w') as f:
        json.dump(ai_model_config, f, indent=2)
    print(f"JSON data written to {json_file}")
    
    print("\n2. READING JSON DATA")
    with open(json_file, 'r') as f:
        loaded_config = json.load(f)
    
    print(f"Model name: {loaded_config['model_name']}")
    print(f"Temperature: {loaded_config['parameters']['temperature']}")
    print(f"Training samples: {len(loaded_config['training_data'])}")
    
    print("\n3. PRETTY PRINTING JSON")
    print("Configuration structure:")
    print(json.dumps(loaded_config, indent=2))

def demonstrate_csv_handling():
    """Demonstrate working with CSV files."""
    print("\n=== CSV FILE HANDLING ===\n")
    
    sample_dir = Path("sample_files")
    
    # Sample dataset
    ai_performance_data = [
        ["Model", "Accuracy", "Precision", "Recall", "F1_Score"],
        ["BERT", 0.95, 0.93, 0.92, 0.925],
        ["GPT-3", 0.87, 0.85, 0.88, 0.865],
        ["RoBERTa", 0.94, 0.92, 0.91, 0.915],
        ["DistilBERT", 0.89, 0.87, 0.86, 0.865]
    ]
    
    csv_file = sample_dir / "model_performance.csv"
    
    print("1. WRITING CSV DATA")
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        for row in ai_performance_data:
            writer.writerow(row)
    print(f"CSV data written to {csv_file}")
    
    print("\n2. READING CSV DATA")
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        for row_num, row in enumerate(reader):
            if row_num == 0:
                print(f"Headers: {row}")
            else:
                print(f"Row {row_num}: {row}")
    
    print("\n3. READING CSV AS DICTIONARY")
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        print("Models performance:")
        for row in reader:
            print(f"  {row['Model']}: Accuracy={row['Accuracy']}, F1={row['F1_Score']}")

def demonstrate_error_handling():
    """Demonstrate error handling in file operations."""
    print("\n=== ERROR HANDLING ===\n")
    
    print("1. HANDLING FILE NOT FOUND")
    try:
        with open("nonexistent_file.txt", 'r') as f:
            content = f.read()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("File does not exist - creating a default one")
        with open("default_file.txt", 'w') as f:
            f.write("Default content created due to missing file\n")
    
    print("\n2. HANDLING PERMISSION ERRORS")
    try:
        # Try to write to a protected location (this might work on some systems)
        with open("/root/protected_file.txt", 'w') as f:
            f.write("This might fail")
    except PermissionError as e:
        print(f"Permission Error: {e}")
        print("Writing to current directory instead")
        with open("alternative_file.txt", 'w') as f:
            f.write("Written to accessible location\n")
    
    print("\n3. HANDLING JSON DECODE ERRORS")
    # Create an invalid JSON file
    invalid_json_file = "invalid.json"
    with open(invalid_json_file, 'w') as f:
        f.write("{ invalid json content }")
    
    try:
        with open(invalid_json_file, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        print("Using default configuration instead")
        default_config = {"model": "default", "parameters": {}}
        print(f"Default config: {default_config}")
    
    # Clean up
    os.remove(invalid_json_file)

def demonstrate_pathlib():
    """Demonstrate using pathlib for better path handling."""
    print("\n=== PATHLIB - MODERN PATH HANDLING ===\n")
    
    # Create a Path object
    base_path = Path("ai_project")
    base_path.mkdir(exist_ok=True)
    
    # Create subdirectories
    data_path = base_path / "data"
    models_path = base_path / "models"
    logs_path = base_path / "logs"
    
    for path in [data_path, models_path, logs_path]:
        path.mkdir(exist_ok=True)
        print(f"Created directory: {path}")
    
    print("\n1. PATH OPERATIONS")
    sample_file = data_path / "training_data.txt"
    
    print(f"File path: {sample_file}")
    print(f"Parent directory: {sample_file.parent}")
    print(f"File name: {sample_file.name}")
    print(f"File stem: {sample_file.stem}")
    print(f"File suffix: {sample_file.suffix}")
    print(f"Is absolute: {sample_file.is_absolute()}")
    
    print("\n2. CHECKING PATH PROPERTIES")
    # Write sample content
    with open(sample_file, 'w') as f:
        f.write("Sample training data\nLine 2\nLine 3\n")
    
    print(f"File exists: {sample_file.exists()}")
    print(f"Is file: {sample_file.is_file()}")
    print(f"Is directory: {sample_file.is_dir()}")
    print(f"File size: {sample_file.stat().st_size} bytes")
    
    print("\n3. LISTING DIRECTORY CONTENTS")
    print(f"Contents of {base_path}:")
    for item in base_path.iterdir():
        if item.is_dir():
            print(f"  📁 {item.name}/")
        else:
            print(f"  📄 {item.name}")
    
    print("\n4. FINDING FILES BY PATTERN")
    # Create some sample files
    (data_path / "train.csv").touch()
    (data_path / "test.csv").touch()
    (data_path / "validation.json").touch()
    
    print("CSV files in data directory:")
    for csv_file in data_path.glob("*.csv"):
        print(f"  {csv_file.name}")
    
    print("All files recursively:")
    for file in base_path.rglob("*"):
        if file.is_file():
            print(f"  {file.relative_to(base_path)}")

def ai_development_file_patterns():
    """Common file I/O patterns in AI development."""
    print("\n=== AI DEVELOPMENT FILE PATTERNS ===\n")
    
    sample_dir = Path("ai_files")
    sample_dir.mkdir(exist_ok=True)
    
    print("1. CONFIGURATION FILE MANAGEMENT")
    
    def save_model_config(config, filepath):
        """Save model configuration to file."""
        with open(filepath, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"Configuration saved to {filepath}")
    
    def load_model_config(filepath, default_config=None):
        """Load model configuration with fallback."""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading config: {e}")
            return default_config or {}
    
    # Example usage
    config = {
        "model_type": "transformer",
        "hidden_size": 768,
        "num_layers": 12,
        "learning_rate": 0.001
    }
    
    config_file = sample_dir / "model_config.json"
    save_model_config(config, config_file)
    loaded_config = load_model_config(config_file)
    print(f"Loaded config: {loaded_config['model_type']}")
    
    print("\n2. DATASET LOADING")
    
    def load_text_dataset(filepath):
        """Load text dataset from file."""
        texts = []
        labels = []
        
        try:
            with open(filepath, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    texts.append(row['text'])
                    labels.append(row['label'])
        except FileNotFoundError:
            print(f"Dataset file {filepath} not found")
            return [], []
        
        return texts, labels
    
    # Create sample dataset
    dataset_file = sample_dir / "sample_dataset.csv"
    sample_data = [
        {"text": "I love this product", "label": "positive"},
        {"text": "This is terrible", "label": "negative"},
        {"text": "It's okay", "label": "neutral"}
    ]
    
    with open(dataset_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['text', 'label'])
        writer.writeheader()
        writer.writerows(sample_data)
    
    texts, labels = load_text_dataset(dataset_file)
    print(f"Loaded dataset: {len(texts)} samples")
    for i, (text, label) in enumerate(zip(texts, labels)):
        print(f"  Sample {i+1}: '{text}' -> {label}")
    
    print("\n3. LOGGING TRAINING PROGRESS")
    
    def log_training_progress(epoch, loss, accuracy, log_file):
        """Log training progress to file."""
        timestamp = "2025-08-30 10:30:00"  # Simulated timestamp
        log_entry = f"{timestamp} - Epoch {epoch}: Loss={loss:.4f}, Accuracy={accuracy:.4f}\n"
        
        with open(log_file, 'a') as f:
            f.write(log_entry)
    
    # Simulate training logging
    log_file = sample_dir / "training.log"
    
    print("Simulating training log:")
    for epoch in range(1, 4):
        loss = 1.0 / epoch  # Decreasing loss
        accuracy = 0.5 + (epoch * 0.2)  # Increasing accuracy
        log_training_progress(epoch, loss, accuracy, log_file)
        print(f"  Epoch {epoch}: Loss={loss:.4f}, Accuracy={accuracy:.4f}")
    
    print(f"\nTraining log written to {log_file}")
    
    print("\n4. MODEL CHECKPOINT MANAGEMENT")
    
    def save_model_checkpoint(model_state, filepath):
        """Save model checkpoint (simulated)."""
        checkpoint_data = {
            "model_state": model_state,
            "timestamp": "2025-08-30",
            "epoch": model_state.get("epoch", 0),
            "best_accuracy": model_state.get("accuracy", 0.0)
        }
        
        with open(filepath, 'w') as f:
            json.dump(checkpoint_data, f, indent=2)
        print(f"Checkpoint saved to {filepath}")
    
    def load_latest_checkpoint(checkpoint_dir):
        """Load the latest checkpoint from directory."""
        checkpoint_path = Path(checkpoint_dir)
        if not checkpoint_path.exists():
            return None
        
        # Find latest checkpoint (simplified)
        checkpoints = list(checkpoint_path.glob("checkpoint_*.json"))
        if not checkpoints:
            return None
        
        latest = max(checkpoints, key=lambda p: p.stat().st_mtime)
        
        with open(latest, 'r') as f:
            return json.load(f)
    
    # Create checkpoint directory
    checkpoint_dir = sample_dir / "checkpoints"
    checkpoint_dir.mkdir(exist_ok=True)
    
    # Save some checkpoints
    for epoch in [1, 2, 3]:
        model_state = {
            "epoch": epoch,
            "accuracy": 0.7 + (epoch * 0.1),
            "weights": f"weights_epoch_{epoch}"
        }
        checkpoint_file = checkpoint_dir / f"checkpoint_epoch_{epoch}.json"
        save_model_checkpoint(model_state, checkpoint_file)
    
    # Load latest checkpoint
    latest_checkpoint = load_latest_checkpoint(checkpoint_dir)
    if latest_checkpoint:
        print(f"Latest checkpoint: Epoch {latest_checkpoint['epoch']}, "
              f"Accuracy: {latest_checkpoint['best_accuracy']}")

def cleanup_demo_files():
    """Clean up demonstration files."""
    print("\n=== CLEANUP ===\n")
    
    import shutil
    
    directories_to_remove = ["sample_files", "ai_project", "ai_files"]
    files_to_remove = ["default_file.txt", "alternative_file.txt"]
    
    for directory in directories_to_remove:
        if Path(directory).exists():
            shutil.rmtree(directory)
            print(f"Removed directory: {directory}")
    
    for file in files_to_remove:
        if Path(file).exists():
            Path(file).unlink()
            print(f"Removed file: {file}")

if __name__ == "__main__":
    demonstrate_basic_file_operations()
    demonstrate_file_modes()
    demonstrate_json_handling()
    demonstrate_csv_handling()
    demonstrate_error_handling()
    demonstrate_pathlib()
    ai_development_file_patterns()
    
    print("\n" + "="*50)
    print("SUMMARY: Python File I/O")
    print("="*50)
    print("✓ Basic file operations: read, write, append")
    print("✓ File modes: 'r', 'w', 'a', binary modes")
    print("✓ Context managers: 'with' statement")
    print("✓ JSON handling: structured data storage")
    print("✓ CSV handling: tabular data processing")
    print("✓ Error handling: FileNotFoundError, PermissionError")
    print("✓ Pathlib: modern path manipulation")
    print("✓ AI patterns: configs, datasets, logs, checkpoints")
    
    # Uncomment the next line if you want to clean up demo files
    # cleanup_demo_files()

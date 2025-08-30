"""
Python Object-Oriented Programming (OOP) Examples
=================================================

This module demonstrates the concepts of classes, objects, inheritance, and polymorphism
to build modular and scalable applications for AI development.

Author: AWS AI Engineering Course
Date: August 2025
"""

def demonstrate_classes_and_objects():
    """Demonstrate basic class definition and object creation."""
    print("=== CLASSES AND OBJECTS ===\n")
    
    # Basic class definition
    class Person:
        """A simple Person class."""
        
        # Class variable (shared by all instances)
        species = "Homo sapiens"
        
        # Constructor method
        def __init__(self, name, age):
            # Instance variables (unique to each instance)
            self.name = name
            self.age = age
        
        # Instance method
        def introduce(self):
            return f"Hi, I'm {self.name} and I'm {self.age} years old."
        
        # Instance method with parameters
        def have_birthday(self):
            self.age += 1
            return f"Happy birthday! {self.name} is now {self.age} years old."
        
        # String representation method
        def __str__(self):
            return f"Person(name='{self.name}', age={self.age})"
    
    print("1. CREATING OBJECTS")
    # Create objects (instances)
    person1 = Person("Alice", 25)
    person2 = Person("Bob", 30)
    
    print(f"Person 1: {person1}")
    print(f"Person 2: {person2}")
    
    print("\n2. ACCESSING ATTRIBUTES AND METHODS")
    print(f"person1.name: {person1.name}")
    print(f"person1.age: {person1.age}")
    print(f"person1.species: {person1.species}")
    print(f"person1.introduce(): {person1.introduce()}")
    
    print("\n3. MODIFYING OBJECT STATE")
    print(f"Before birthday: {person1}")
    print(person1.have_birthday())
    print(f"After birthday: {person1}")

def demonstrate_encapsulation():
    """Demonstrate encapsulation with private and protected attributes."""
    print("\n=== ENCAPSULATION ===\n")
    
    class BankAccount:
        """Demonstrates encapsulation with private attributes."""
        
        def __init__(self, account_number, initial_balance=0):
            self.account_number = account_number  # Public
            self._balance = initial_balance       # Protected (convention)
            self.__pin = "1234"                  # Private (name mangling)
        
        # Public method to access private data
        def get_balance(self):
            return self._balance
        
        # Public method to modify private data with validation
        def deposit(self, amount):
            if amount > 0:
                self._balance += amount
                return f"Deposited ${amount}. New balance: ${self._balance}"
            return "Invalid deposit amount"
        
        def withdraw(self, amount, pin):
            if pin != self.__pin:
                return "Invalid PIN"
            if amount > self._balance:
                return "Insufficient funds"
            if amount > 0:
                self._balance -= amount
                return f"Withdrew ${amount}. New balance: ${self._balance}"
            return "Invalid withdrawal amount"
        
        # Private method
        def __validate_pin(self, pin):
            return pin == self.__pin
        
        def __str__(self):
            return f"BankAccount({self.account_number}, Balance: ${self._balance})"
    
    print("1. ENCAPSULATION EXAMPLE")
    account = BankAccount("12345", 1000)
    print(f"Account: {account}")
    print(f"Balance: ${account.get_balance()}")
    
    print("\n2. DEPOSIT AND WITHDRAWAL")
    print(account.deposit(500))
    print(account.withdraw(200, "1234"))
    print(account.withdraw(200, "wrong"))  # Invalid PIN
    
    print("\n3. ACCESSING PRIVATE ATTRIBUTES")
    print(f"Public attribute: {account.account_number}")
    print(f"Protected attribute: {account._balance}")
    # print(f"Private attribute: {account.__pin}")  # This would cause an error
    print(f"Private attribute via name mangling: {account._BankAccount__pin}")

def demonstrate_inheritance():
    """Demonstrate inheritance and method overriding."""
    print("\n=== INHERITANCE ===\n")
    
    # Base class (Parent)
    class Animal:
        """Base Animal class."""
        
        def __init__(self, name, species):
            self.name = name
            self.species = species
        
        def make_sound(self):
            return f"{self.name} makes a sound"
        
        def move(self):
            return f"{self.name} moves around"
        
        def __str__(self):
            return f"{self.species} named {self.name}"
    
    # Derived class (Child)
    class Dog(Animal):
        """Dog class inheriting from Animal."""
        
        def __init__(self, name, breed):
            super().__init__(name, "Dog")  # Call parent constructor
            self.breed = breed
        
        # Override parent method
        def make_sound(self):
            return f"{self.name} barks: Woof!"
        
        # Additional method specific to Dog
        def fetch(self):
            return f"{self.name} fetches the ball"
        
        def __str__(self):
            return f"{self.breed} dog named {self.name}"
    
    class Cat(Animal):
        """Cat class inheriting from Animal."""
        
        def __init__(self, name, indoor=True):
            super().__init__(name, "Cat")
            self.indoor = indoor
        
        # Override parent method
        def make_sound(self):
            return f"{self.name} meows: Meow!"
        
        # Additional method specific to Cat
        def climb(self):
            return f"{self.name} climbs the tree"
    
    print("1. INHERITANCE EXAMPLE")
    # Create instances
    generic_animal = Animal("Unknown", "Generic")
    dog = Dog("Buddy", "Golden Retriever")
    cat = Cat("Whiskers", indoor=True)
    
    animals = [generic_animal, dog, cat]
    
    for animal in animals:
        print(f"Animal: {animal}")
        print(f"  Sound: {animal.make_sound()}")
        print(f"  Movement: {animal.move()}")
        
        # Use specific methods if available
        if isinstance(animal, Dog):
            print(f"  Special: {animal.fetch()}")
        elif isinstance(animal, Cat):
            print(f"  Special: {animal.climb()}")
        print()

def demonstrate_polymorphism():
    """Demonstrate polymorphism - same interface, different implementations."""
    print("\n=== POLYMORPHISM ===\n")
    
    # Base class defining common interface
    class Shape:
        """Base Shape class defining common interface."""
        
        def area(self):
            raise NotImplementedError("Subclass must implement area method")
        
        def perimeter(self):
            raise NotImplementedError("Subclass must implement perimeter method")
        
        def describe(self):
            return f"This is a {self.__class__.__name__}"
    
    class Rectangle(Shape):
        """Rectangle implementation of Shape."""
        
        def __init__(self, width, height):
            self.width = width
            self.height = height
        
        def area(self):
            return self.width * self.height
        
        def perimeter(self):
            return 2 * (self.width + self.height)
        
        def __str__(self):
            return f"Rectangle({self.width}x{self.height})"
    
    class Circle(Shape):
        """Circle implementation of Shape."""
        
        def __init__(self, radius):
            self.radius = radius
        
        def area(self):
            import math
            return math.pi * self.radius ** 2
        
        def perimeter(self):
            import math
            return 2 * math.pi * self.radius
        
        def __str__(self):
            return f"Circle(radius={self.radius})"
    
    class Triangle(Shape):
        """Triangle implementation of Shape."""
        
        def __init__(self, side1, side2, side3):
            self.side1 = side1
            self.side2 = side2
            self.side3 = side3
        
        def area(self):
            # Using Heron's formula
            s = (self.side1 + self.side2 + self.side3) / 2
            import math
            return math.sqrt(s * (s - self.side1) * (s - self.side2) * (s - self.side3))
        
        def perimeter(self):
            return self.side1 + self.side2 + self.side3
        
        def __str__(self):
            return f"Triangle({self.side1}, {self.side2}, {self.side3})"
    
    print("1. POLYMORPHISM IN ACTION")
    # Create different shapes
    shapes = [
        Rectangle(5, 3),
        Circle(4),
        Triangle(3, 4, 5)
    ]
    
    # Same interface, different implementations
    for shape in shapes:
        print(f"Shape: {shape}")
        print(f"  Description: {shape.describe()}")
        print(f"  Area: {shape.area():.2f}")
        print(f"  Perimeter: {shape.perimeter():.2f}")
        print()

def ai_development_oop():
    """Demonstrate OOP concepts in AI development context."""
    print("\n=== AI DEVELOPMENT OOP EXAMPLES ===\n")
    
    # Base class for AI models
    class BaseModel:
        """Base class for AI models."""
        
        def __init__(self, model_name):
            self.model_name = model_name
            self.is_trained = False
            self.training_history = []
        
        def train(self, data):
            raise NotImplementedError("Subclass must implement train method")
        
        def predict(self, input_data):
            if not self.is_trained:
                raise ValueError("Model must be trained before prediction")
            raise NotImplementedError("Subclass must implement predict method")
        
        def evaluate(self, test_data, test_labels):
            raise NotImplementedError("Subclass must implement evaluate method")
        
        def save_model(self, filepath):
            return f"Model {self.model_name} saved to {filepath}"
        
        def __str__(self):
            status = "Trained" if self.is_trained else "Not trained"
            return f"{self.model_name} ({status})"
    
    # Specific model implementations
    class TextClassifier(BaseModel):
        """Text classification model."""
        
        def __init__(self, model_name="TextClassifier"):
            super().__init__(model_name)
            self.vocabulary = set()
            self.classes = []
        
        def train(self, data):
            # Simulate training
            texts, labels = data
            self.vocabulary.update(' '.join(texts).split())
            self.classes = list(set(labels))
            self.is_trained = True
            self.training_history.append(f"Trained on {len(texts)} samples")
            return f"Training completed. Vocab size: {len(self.vocabulary)}"
        
        def predict(self, input_data):
            super().predict(input_data)  # Check if trained
            # Simulate prediction
            return self.classes[0] if self.classes else "unknown"
        
        def evaluate(self, test_data, test_labels):
            accuracy = 0.85  # Simulated accuracy
            return {"accuracy": accuracy, "samples": len(test_data)}
    
    class ImageClassifier(BaseModel):
        """Image classification model."""
        
        def __init__(self, model_name="ImageClassifier", input_size=(224, 224)):
            super().__init__(model_name)
            self.input_size = input_size
            self.num_classes = 0
        
        def train(self, data):
            images, labels = data
            self.num_classes = len(set(labels))
            self.is_trained = True
            self.training_history.append(f"Trained on {len(images)} images")
            return f"Training completed. Classes: {self.num_classes}"
        
        def predict(self, input_data):
            super().predict(input_data)
            # Simulate prediction
            return f"class_{hash(str(input_data)) % self.num_classes}"
        
        def evaluate(self, test_data, test_labels):
            accuracy = 0.92  # Simulated accuracy
            return {"accuracy": accuracy, "samples": len(test_data)}
    
    # Data processor class
    class DataProcessor:
        """Data preprocessing utilities."""
        
        def __init__(self):
            self.transformations = []
        
        def add_transformation(self, transform_func, name):
            self.transformations.append((transform_func, name))
        
        def process(self, data):
            processed_data = data
            for transform_func, name in self.transformations:
                processed_data = transform_func(processed_data)
                print(f"Applied transformation: {name}")
            return processed_data
    
    print("1. AI MODEL HIERARCHY")
    # Create different model types
    text_model = TextClassifier("BERT-Classifier")
    image_model = ImageClassifier("ResNet-50", input_size=(256, 256))
    
    models = [text_model, image_model]
    
    for model in models:
        print(f"Model: {model}")
    
    print("\n2. TRAINING MODELS")
    # Train text model
    text_data = (["hello world", "goodbye world"], ["positive", "negative"])
    result = text_model.train(text_data)
    print(f"Text model: {result}")
    
    # Train image model
    image_data = (["image1.jpg", "image2.jpg"], ["cat", "dog"])
    result = image_model.train(image_data)
    print(f"Image model: {result}")
    
    print("\n3. POLYMORPHIC BEHAVIOR")
    test_inputs = ["test input", "test_image.jpg"]
    
    for model, test_input in zip(models, test_inputs):
        try:
            prediction = model.predict(test_input)
            evaluation = model.evaluate([test_input], ["test_label"])
            print(f"{model.model_name}:")
            print(f"  Prediction: {prediction}")
            print(f"  Evaluation: {evaluation}")
        except Exception as e:
            print(f"{model.model_name}: Error - {e}")
    
    print("\n4. DATA PROCESSING PIPELINE")
    processor = DataProcessor()
    
    # Add transformations
    processor.add_transformation(lambda x: x.lower(), "lowercase")
    processor.add_transformation(lambda x: x.strip(), "strip_whitespace")
    processor.add_transformation(lambda x: x.replace(" ", "_"), "replace_spaces")
    
    sample_text = "  Hello World  "
    processed = processor.process(sample_text)
    print(f"Original: '{sample_text}'")
    print(f"Processed: '{processed}'")

def demonstrate_class_methods_and_static_methods():
    """Demonstrate class methods and static methods."""
    print("\n=== CLASS METHODS AND STATIC METHODS ===\n")
    
    class MLModel:
        """Demonstrates class methods and static methods."""
        
        model_count = 0  # Class variable
        
        def __init__(self, name):
            self.name = name
            MLModel.model_count += 1
        
        @classmethod
        def get_model_count(cls):
            """Class method - operates on the class, not instance."""
            return cls.model_count
        
        @classmethod
        def create_default_model(cls):
            """Class method - alternative constructor."""
            return cls("DefaultModel")
        
        @staticmethod
        def validate_model_name(name):
            """Static method - doesn't access class or instance."""
            if not isinstance(name, str):
                return False
            if len(name) < 3:
                return False
            return True
        
        def __str__(self):
            return f"MLModel('{self.name}')"
    
    print("1. STATIC METHOD")
    print(f"Valid name 'BERT': {MLModel.validate_model_name('BERT')}")
    print(f"Valid name 'AI': {MLModel.validate_model_name('AI')}")
    print(f"Valid name 123: {MLModel.validate_model_name(123)}")
    
    print("\n2. CLASS METHOD - MODEL COUNT")
    print(f"Initial model count: {MLModel.get_model_count()}")
    
    model1 = MLModel("GPT-3")
    model2 = MLModel("BERT")
    print(f"After creating 2 models: {MLModel.get_model_count()}")
    
    print("\n3. CLASS METHOD - ALTERNATIVE CONSTRUCTOR")
    default_model = MLModel.create_default_model()
    print(f"Default model: {default_model}")
    print(f"Final model count: {MLModel.get_model_count()}")

if __name__ == "__main__":
    demonstrate_classes_and_objects()
    demonstrate_encapsulation()
    demonstrate_inheritance()
    demonstrate_polymorphism()
    ai_development_oop()
    demonstrate_class_methods_and_static_methods()
    
    print("\n" + "="*60)
    print("SUMMARY: Python Object-Oriented Programming")
    print("="*60)
    print("✓ Classes and Objects: Blueprint and instances")
    print("✓ Encapsulation: Private/protected attributes and methods")
    print("✓ Inheritance: Code reuse and specialization")
    print("✓ Polymorphism: Same interface, different implementations")
    print("✓ Class methods: Operate on class level")
    print("✓ Static methods: Utility functions within class")
    print("✓ AI development patterns: Model hierarchies")
    print("✓ Code organization: Modular and scalable design")

# AWS Bedrock JSON Output Examples

This module demonstrates how to extract structured JSON data from AWS Bedrock models using various approaches.

## Overview

The `bedrock_json_output.py` script provides comprehensive examples of:
- Extracting structured data from unstructured text
- Robust JSON parsing with error handling  
- Multiple model support (Nova Lite, Claude variants)
- Interactive and automated extraction modes

## Features

### ✅ **Working Examples (Nova Lite)**
- **User Data Extraction**: Extract names, emails, contact information
- **Product Information**: Parse product descriptions into structured data
- **Event Details**: Extract event information (dates, times, locations)
- **Interactive Mode**: Custom extraction with user-defined JSON structures

### 📚 **Reference Examples**
- **Modern Claude API**: Updated API format for Claude 3.x models
- **Legacy Claude API**: Your original code pattern (deprecated)
- **Error Handling**: Robust JSON parsing with fallbacks

## Usage

### Basic Examples
```bash
# Run all examples
python bedrock_json_output.py --mode examples

# User data extraction only
python bedrock_json_output.py --mode user

# Product information extraction
python bedrock_json_output.py --mode product

# Event information extraction  
python bedrock_json_output.py --mode event

# Interactive mode
python bedrock_json_output.py --mode interactive
```

### Custom Region
```bash
python bedrock_json_output.py --region us-west-2 --mode examples
```

## Code Examples

### Nova Lite JSON Extraction
```python
from bedrock_json_output import BedrockJSONExtractor

extractor = BedrockJSONExtractor()
result = extractor.extract_with_nova_lite(
    "Extract name and email from: 'Hi, I'm Jane Smith at jane@company.com'"
)

if result["success"]:
    print(result["data"])  # {"name": "Jane Smith", "email": "jane@company.com"}
```

### Modern Claude API (Reference)
```python
# Updated from your original code
request_body = {
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 300,
    "temperature": 0.1,
    "messages": [
        {
            "role": "user", 
            "content": "Extract JSON from text..."
        }
    ]
}
```

### Legacy Claude API (Your Original Pattern)
```python
# Your original code pattern (deprecated)
body = json.dumps({
    "prompt": f"\\n\\nHuman: {prompt}\\n\\nAssistant:",
    "max_tokens_to_sample": 300,
    "temperature": 0.1,
    "top_p": 0.9,
})
```

## JSON Parsing Features

### Robust Parsing
- Handles markdown code blocks (```json)
- Extracts JSON from mixed text responses
- Graceful error handling with fallbacks
- Validates JSON structure

### Error Recovery
```python
# Handles various response formats:
# - Plain JSON: {"key": "value"}
# - Markdown: ```json\n{"key": "value"}\n```
# - Mixed text: "Here's the JSON: {"key": "value"} as requested"
```

## Interactive Mode

Run interactive mode for custom extractions:
```bash
python bedrock_json_output.py --mode interactive
```

Example session:
```
📝 Enter text to analyze: "Contact Sarah Johnson at sarah.j@techcorp.com, phone: (555) 123-4567"
🗂️ Describe desired JSON structure: name, email, phone
✅ Extracted JSON:
{
  "name": "Sarah Johnson",
  "email": "sarah.j@techcorp.com", 
  "phone": "(555) 123-4567"
}
```

## Model Comparison

| Model | Status | API Format | Performance |
|-------|--------|------------|-------------|
| Nova Lite | ✅ Available | Messages v1 | Excellent JSON |
| Claude 3 Sonnet | 🔒 Requires Access | Anthropic v2023 | High Accuracy |
| Claude v2 Legacy | ⚠️ Deprecated | Completion | Basic Support |

## Tips for Better JSON Extraction

1. **Be Specific**: Clearly define the JSON structure you want
2. **Use Low Temperature**: Set temperature to 0.1 for consistent output
3. **Provide Examples**: Include sample JSON in complex prompts
4. **Handle Errors**: Always check the success flag and handle parsing errors
5. **Clean Responses**: Use the built-in JSON cleaning functions

## Error Handling

The extractor provides comprehensive error handling:
```python
result = extractor.extract_with_nova_lite(prompt)

if result["success"]:
    data = result["data"]      # Parsed JSON
    raw = result["raw_response"]  # Original response
else:
    error = result["error"]    # Error message
    model = result["model"]    # Which model failed
```

## Integration with Other Examples

This JSON extractor can be easily integrated with:
- **Nova Lite Chat**: Add structured data extraction to conversations
- **Nova Lite CLI**: Batch process documents for data extraction  
- **Strands Integration**: Use as a data processing component

Perfect for building data extraction pipelines and structured AI workflows!

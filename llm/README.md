# LLM Module

This module provides comprehensive Large Language Model (LLM) integration for the shop assistant chatbot.

## Structure

```
llm/
├── __init__.py          # Module exports
├── config.py            # LLM configuration management
├── model.py             # Base model initialization
├── client.py            # Enhanced LLM client with retry logic
├── utils.py             # Utility functions for token management
└── README.md            # This file
```

## Features

### 1. Configuration Management (`config.py`)
- Centralized LLM configuration
- Environment-based settings
- Configuration validation
- Runtime configuration updates

### 2. Model Initialization (`model.py`)
- Simple LangChain model setup
- Configuration-driven parameters
- Backward compatibility

### 3. Enhanced Client (`client.py`)
- Retry logic with exponential backoff
- Health check functionality
- Comprehensive error handling
- Message format conversion

### 4. Utility Functions (`utils.py`)
- Token counting using tiktoken
- Text truncation for token limits
- Message formatting and validation
- Cost estimation
- Length validation

## Usage Examples

### Basic Usage
```python
from llm import chat_base_model, llm_client, llm_config

# Check if LLM is configured
if llm_config.is_configured:
    print("LLM is ready to use")
    
    # Use the base model directly
    response = await chat_base_model.ainvoke("Hello!")
    
    # Or use the enhanced client
    messages = [{"role": "user", "content": "Hello!"}]
    response = await llm_client.generate_response(messages)
```

### Token Management
```python
from llm import count_tokens, truncate_text, validate_message_length

# Count tokens
text = "Hello, how are you?"
token_count = count_tokens(text)
print(f"Tokens: {token_count}")

# Truncate text
max_tokens = 100
truncated = truncate_text(long_text, max_tokens)

# Validate message length
messages = [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi there!"}
]
validation = validate_message_length(messages, max_tokens=1000)
if not validation["within_limit"]:
    print("Messages exceed token limit")
```

### Cost Estimation
```python
from llm import estimate_cost

tokens = 500
cost_info = estimate_cost(tokens, model="gpt-3.5-turbo")
print(f"Estimated cost: ${cost_info['total_cost']}")
```

### Health Checking
```python
from llm import llm_client

# Check LLM service health
is_healthy = await llm_client.health_check()
if is_healthy:
    print("LLM service is healthy")
else:
    print("LLM service is unavailable")
```

## Configuration

The LLM module uses the following configuration from your environment:

- `BASE_URL`: LLM API base URL
- `API_KEY`: LLM API key
- `MODEL_ID`: Model identifier
- `MODEL_TEMPERATURE`: Sampling temperature (0.0-2.0)
- `MODEL_MAX_TOKENS`: Maximum tokens per response
- `MODEL_TIMEOUT`: Request timeout in seconds

## Error Handling

The module provides comprehensive error handling:

- `AIModelError`: For LLM-specific errors
- `ExternalServiceError`: For service connectivity issues
- Automatic retry with exponential backoff
- Detailed logging for debugging

## Best Practices

1. **Always check configuration**: Use `llm_config.is_configured` before making requests
2. **Handle tokens wisely**: Use token counting to avoid limits
3. **Implement health checks**: Use `llm_client.health_check()` in production
4. **Monitor costs**: Use `estimate_cost()` for budget management
5. **Validate inputs**: Use `format_messages()` and `validate_message_length()`

## Migration from core.model

If you're migrating from the old `core.model`:

```python
# Old way
from core.model import chat_base_model

# New way (recommended)
from llm import chat_base_model, llm_client, llm_config

# Or use enhanced client
from llm import llm_client
response = await llm_client.generate_response(messages)
```

The old import path still works for backward compatibility, but the new `llm` module provides better functionality.

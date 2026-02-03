---
description: Repository Information Overview
alwaysApply: true
---

# TikTok AI Ad Campaign Creator Information

## Summary
An AI-powered conversational agent for creating TikTok advertising campaigns through natural language interaction. Built for the SoluLab AI Internship Technical Assignment, it focuses on advanced AI agent engineering, structured LLM outputs using Google Gemini, complex business logic enforcement (particularly music requirements), and intelligent API error handling.

## Structure
- [./src/](./src/): Core source code containing the agent logic, API mocks, and CLI interface.
  - [./src/main.py](./src/main.py): CLI Entry Point and user interface.
  - [./src/agent.py](./src/agent.py): Core AI agent and conversation orchestration.
  - [./src/prompts.py](./src/prompts.py): Gemini-optimized LLM prompt templates.
  - [./src/state.py](./src/state.py): Conversation state management.
  - [./src/validators.py](./src/validators.py): Business rules and Pydantic validation logic.
  - [./src/tiktok_auth.py](./src/tiktok_auth.py): Simulated OAuth authorization flow.
  - [./src/tiktok_api.py](./src/tiktok_api.py): Mocked TikTok API client with realistic error scenarios.
  - [./src/config.py](./src/config.py): Configuration management using `pydantic-settings`.
- [./tests/](./tests/): Test suite for validating business logic and agent behavior.
- [./examples/](./examples/): Sample conversation logs and usage examples.
- [./requirements.txt](./requirements.txt): Python dependency definitions.
- [./.env.example](./.env.example): Template for required environment variables.

## Language & Runtime
**Language**: Python  
**Version**: 3.10+  
**Build System**: Pip  
**Package Manager**: pip

## Dependencies
**Main Dependencies**:
- **google-genai**: Google Gemini API integration.
- **pydantic**: Data validation and settings management.
- **pydantic-settings**: Environment variable management.
- **python-dotenv**: Environment configuration.
- **rich**: Enhanced CLI formatting and output.

**Development Dependencies**:
- **pytest**: Testing framework.

## Build & Installation
```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env and add GOOGLE_API_KEY
```

## Application Entry Point
The application is run as a module:
```bash
python -m src.main
```

## Testing
**Framework**: pytest  
**Test Location**: [./tests/](./tests/)  
**Naming Convention**: Files prefixed with `test_` (e.g., `test_validators.py`).  
**Configuration**: Standard pytest configuration.

**Run Command**:
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src
```

## Key Business Logic
The agent enforces specific TikTok advertising rules, most notably the **Music Logic**:
- **Traffic Objective**: Music is optional.
- **Conversions Objective**: Music is REQUIRED.
- **Validation**: Handles existing Music IDs, custom uploads, and interprets API errors (copyright, duration, etc.) into user-friendly guidance.

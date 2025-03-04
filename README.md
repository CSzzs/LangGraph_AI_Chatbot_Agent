# LangGraph AI Chatbot Agent

This project is a chatbot agent built using FastAPI, Streamlit, and LangGraph. It allows users to interact with the LangGraph-based agent through a web interface.

## Features

- FastAPI backend for handling chat requests
- Streamlit frontend for user interaction
- Integration with LangGraph and LangChain for AI model interactions
- Support for multiple AI models

## Requirements

- Python 3.11 or higher
- The following Python packages:
  - fastapi
  - pydantic
  - typing
  - langchain_community
  - langgraph
  - langchain_groq
  - uvicorn
  - streamlit
  - requests

## Installation

1. Clone the repository:

```bash
git clone https://github.com/CSzzs/langgraph_ai_chatbot_agent.git
cd langgraph-ai-chatbot-agent
```
2. Install the required packages:
pip install -r requirements.txt

```python
pip install -r requirements.txt
```
3.Add the following directory to your PATH environment variable:
C:\Users\yourname\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\Scripts

## Configuration
Create a config.json file in the root directory of the project with the following structure:

```json
{
    "GROQ_API_KEY": "your_groq_api_key_here",
    "TAVILY_API_KEY": "your_tavily_api_key_here"
}
```

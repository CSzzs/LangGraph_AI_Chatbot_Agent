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
1.Start the FastAPI backend:
```bash
python app.py
```

2.Start the Streamlit frontend:
```bash
streamlit run ui.py
```
3. Open your web browser and go to http://localhost:8000 to interact with the chatbot agent.

## Project Structure
langgraph-ai-chatbot-agent/
│
├── app.py                  # FastAPI backend
├── ui.py                   # Streamlit frontend
├── config.json             # Configuration file for API keys
├── requirements.txt        # List of required Python packages
└── README.md               # Project documentation

## Usage
- Define your AI agent by providing a system prompt in the input box.
- Select the model you want to use from the dropdown menu.
- Type your messages in the input box and click "Send Query" to interact with the chatbot.

## Code Overview
[app.py]([URL](https://github.com/CSzzs/LangGraph_AI_Chatbot_Agent/blob/main/app.py))

### This file contains the FastAPI backend for handling chat requests.
```python
"""Import necessary libraries modlues and setup for FastAPI, LangGraph, and LangChain"""
from fastapi import FastAPI                                                     #framework to create web applications
from pydantic import BaseModel                                                  #for structrured data data model
from typing import List                                                         #type hint fore type annotations
from langchain_community.tools.tavily_search import TavilySearchResults          #for searching the Tavily
import os                                                                       #for enviornment varible handling
import json                                                                     #for JSON data handling
from langgraph.prebuilt import create_react_agent                               #for create a React Agent
from langchain_groq import ChatGroq                                             #for interating with LLMs

"""Retrive and set API keys for external services"""
working_dir = os.path.dirname(os.path.abspath(__file__))                       #get the current working directory
config_data = json.load(open(f"{working_dir}/config.json"))                    #load the config file

os.environ["GROQ_API_KEY"] = config_data["GROQ_API_KEY"]                                     #get the GROQ API key
os.environ["TAVILY_API_KEY"] = config_data["TAVILY_API_KEY"]                                 #get the Tavily API key

"""Predefined list of supported  models"""
MODEL_NAMES =[
    "llama3-70b-8192",
    "mixtral-8x7b-32768"
]

"""Initialize the TavilSearchResult tool with a specified maximum number of results"""
tool_tavily = TavilySearchResults(max_results=5)

"""Combine the TavilySearchResult and ExecPython tools into a list"""
tools = [tool_tavily]

"""FastAPI application setup with title"""
app = FastAPI(title="LangGraph AI Agent")

"""Define  the request schema using Pydantic's BaseModel"""
class RequestState(BaseModel):                                               
    model_name: str                                                             #Name of the model to use for processing the requset
    system_prompt: str                                                          #system prompt for initialising the model
    messages: List[str]                                                         #list of message in the chat

"""Define and end point for handaling the chat request"""
@app.post("/chat")
def chatr_endpoint(request: RequestState):
    """
    API endpoint to interact with the chatbot using LangGraph and tools.
    Dynamically select the model specified in the request.
    """
    if request.model_name not in MODEL_NAMES:
        return {"error": "Invalid model name. Please select a valid model."}    #return error message if model name is invalid
    

    """Initialize the  LLM with the selected model"""
    llm = ChatGroq(groq_api_key=os.environ["GROQ_API_KEY"], model_name=request.model_name)

    """Create a React agent with the selected model"""
    agent = create_react_agent(llm, tools=tools, state_modifier=request.system_prompt)

    """Create the initial state for processing"""
    state = {"messages": request.messages}

    """process the state using the agent"""
    result = agent.invoke(state)                                                #invoke the agent with the state

    """Return the results as the response"""
    return result

"""run the application if executed as the main script"""
if __name__ == '__main__':
    import uvicorn                                                              #Import uvicorn for running the FastAPI app
    uvicorn.run(app, host='127.0.0.1', port=8000)                               #start the app on localhost with port 8000
```
[ui.py]([URL](https://github.com/CSzzs/LangGraph_AI_Chatbot_Agent/blob/main/ui.py))

### This file contains the Streamlit frontend for user interaction.
```python
import streamlit as st
import requests

st.set_page_config(page_title="LangGraph AI Agent", page_icon="🤖", layout="centered")

#Define API endpoint
API_URL = "http://127.0.0.1:8000/chat"

#Predifine models
MODEL_NAMES =[
    "llama3-70b-8192",
    "mixtral-8x7b-32768"
]

#Streamlit UI Elements
st.title("LangGraph AI Chatbot Agent 🤖")
st.write("Interact with the LangGraph based agent using this interface.")

#Input box for system prompt
given_system_prompt = st.text_area("Define your AI Agent 🤖", height=70, placeholder="Type your system prompt here...")

#Dropdown for selecting the model
selected_model = st.selectbox("Select the model to use", MODEL_NAMES)

#input box for user messages
user_inputs = st.text_area("Type your messages here", height=150, placeholder="Type your messages here...")

#Button for sending the request
if st.button("Send Query"):
    if user_inputs.strip():
        try:
            #send the input to the fastapi backend
            payload = {'messages':[user_inputs], "model_name":selected_model, "system_prompt":given_system_prompt}
            response = requests.post(API_URL, json=payload)

            #Display the response
            if response.status_code == 200:
                response_data = response.json()
                if 'error' in response_data:
                    st.error(response_data['error'])
                else:
                    ai_response = [
                        message.get("content", "")
                        for message in response_data.get("messages",[])
                        if message.get("type") == "ai"
                    ]

                    if ai_response:
                        st.subheader("Agent Response:")
                        st.markdown(f"**Final Response:** {ai_response[-1]}")
                    else:
                        st.warning('No AI response found in the agent output.')
            else:
                st.error(f"Request Failed with status code {response.status_code}.")
        except Exception as e:
            st.error(f"an error occured: {e}")
    else:
        st.warning("please enter a message before clicking  'send query' button.")
```
[config.json]([URL](https://github.com/CSzzs/LangGraph_AI_Chatbot_Agent/blob/main/config.json))
### This file contains the API keys required for the project.
```json
{
    "GROQ_API_KEY": "your_groq_api_key_here",
    "TAVILY_API_KEY": "your_tavily_api_key_here"
}
```
[requiremnet.txt]([URL](https://github.com/CSzzs/LangGraph_AI_Chatbot_Agent/blob/main/requirements.txt))
### This file lists all the required Python packages for the project.
```txt
fastapi
pydantic
typing
langchain_community
langgraph
langchain_groq
uvicorn
streamlit
requests
```
## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Acknowledgements
- FastAPI
- Streamlit
- LangGraph
- LangChain




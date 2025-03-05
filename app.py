"""Import necessary libraries modlues and setup for FastAPI, LangGraph, and LangChain"""
from fastapi import FastAPI                                                     #framework to create web applications
from pydantic import BaseModel                                                  #for structrured data data model
from typing import List                                                         #type hint fore type annotations
from langchain_community.tools.tavily_search import TavilySearchResults         #for searching the Tavily
import os                                                                       #for enviornment varible handling
import json                                                                     #for JSON data handling
from langgraph.prebuilt import create_react_agent                               #for create a React Agent
from langchain_groq import ChatGroq                                             #for interating with LLMs

"""Retrive and set API keys for external services"""
working_dir = os.path.dirname(os.path.abspath(__file__))                       #get the current working directory
config_data = json.load(open(f"{working_dir}/config.json"))                    #load the config file

os.environ["GROQ_API_KEY"] = config_data["GROQ_API_KEY"]                       #get the GROQ API key
os.environ["TAVILY_API_KEY"] = config_data["TAVILY_API_KEY"]                   #get the Tavily API key

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

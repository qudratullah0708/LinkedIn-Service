import os
from typing import Optional, List, Dict, Any
import json

from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

tavily_api_key = os.getenv("TAVILY_API_KEY")
if tavily_api_key:
    tavily_client = TavilyClient(api_key=tavily_api_key)

def Retrieve_news(topic: str):
    """Fetch latest news on a topic using Tavily API"""
    if not tavily_client:
        raise ValueError("Tavily API key is missing. Set TAVILY_API_KEY in your .env file.")
    
    print(f"Fetching Latest News for: {topic}...")
    response = tavily_client.search(topic, search_depth="advanced")
    
    if not response or "results" not in response:
        raise ValueError("Invalid response from Tavily API.")
    
    
    print(f"Raw Content : {response}")
    return response

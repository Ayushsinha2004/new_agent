from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import json
import requests
import os
from dotenv import load_dotenv
load_dotenv()

class CustomSerperTool(BaseTool):
    name: str = "Custom Serper Dev tool"
    description: str = (
        "Search the internet for the given topic for latest news in detail"
    )
    

    def _run(self, query: str) -> str:
        """
        Search the internet
        """
        url = "https://google.serper.dev/news"

        payload = json.dumps({
            "q": query,
            "gl": "in"
        })
        headers = {
            'X-API-KEY': os.getenv('SERPER_API_KEY'),
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        # Parse the JSON response
        response_data = response.json()
        news_items = response_data.get("news", [])

        # Process or return the news items
        news_titles = [item["title"] for item in news_items]
        return news_titles

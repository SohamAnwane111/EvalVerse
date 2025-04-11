from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
import requests
from dotenv import load_dotenv
import os
from Engine.driver import load_config

load_dotenv('application.env')

config=load_config('llm_config.yaml')

API_KEY=config['serper']['api']['key']

class WebSearcherSchema(BaseModel):
    search_query: str = Field(..., description="The query to search on the web")

class WebSearcher(BaseTool):
    name: str = "WebSearcher"
    description: str = "A tool to search the web for information using a search_query."
    args_schema: Type[BaseModel] = WebSearcherSchema

    def _run(self, search_query: str) -> list:
        url = config['serper']['url']['search']
        headers = {
            "X-API-KEY": API_KEY,
            "Content-Type": "application/json"
        }
        payload = {"q": search_query, "num": 1}

        try:
            res = requests.post(url, json=payload, headers=headers)
            res.raise_for_status()
            data = res.json()

            return [
                {
                    "title": item["title"],
                    "link": item["link"],
                    "snippet": item.get("snippet", "")
                }
                for item in data.get("organic", [])[:5]
            ]
        except Exception as e:
            return [{"error": str(e)}]

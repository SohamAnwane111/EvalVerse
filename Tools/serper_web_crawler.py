# import os
# import requests

# class TavilySearchTool:
#     name = "tavily_search"
#     description = "Search the web using Tavily."

#     def run(self, query: str) -> str:
#         api_key = os.getenv("TAVILY_API_KEY")
#         url = "https://api.tavily.com/search"
#         payload = {
#             "api_key": api_key,
#             "query": query,
#             "search_depth": "basic",
#             "include_answer": True,
#             "include_images": False,
#             "include_raw_content": False,
#         }
#         res = requests.post(url, json=payload)
#         data = res.json()
#         return data.get("answer", "No answer found.")

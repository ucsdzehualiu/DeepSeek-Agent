from typing import List, Dict
import os, json
import requests

"""
工具函数

- 首先要在 tools 中添加工具的描述信息
- 然后在 tools 中添加工具的具体实现

- https://tavily.com/
"""

os.environ['TAVILY_API_KEY'] = ''
class Tools:
    def __init__(self) -> None:
        # 工具的配置信息
        self.toolConfig = self._tools()

    def _tools(self) -> List[Dict]:
        tools = [
            {
                'name_for_human': 'Tavily 搜索',
                'name_for_model': 'tavily_search',
                'description_for_model': 'Tavily 搜索是一个强大的搜索引擎，可用于访问互联网、查询百科知识、获取最新的信息，了解时事新闻等。不确定的，有时效性的问题要先查一下',
                'parameters': [
                    {
                        'name': 'search_query',
                        'description': '搜索关键词或短语',
                        'required': True,
                        'schema': {'type': 'string'},
                    }
                ],
            }
        ]
        return tools

    def tavily_search(self, search_query: str) -> str:
        # 工具的实现
        url = "https://api.tavily.com/search"

        payload = json.dumps({"query": search_query})
        headers = {
            'Authorization': f'Bearer {os.getenv("TAVILY_API_KEY", "")}',
            'Content-Type': 'application/json'
        }

        response = requests.post(url, headers=headers, data=payload).json()
        print("HERE IS ONE SEARCH")
        print(response)
        return response.get('results', [{}])[0].get('content', 'No results found.')

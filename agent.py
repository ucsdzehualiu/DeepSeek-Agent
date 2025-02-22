from typing import Dict, List, Optional, Tuple, Union
import json5
import ollama
from tool import Tools

# 工具描述
TOOL_DESC = """{name_for_model}: Call this tool to interact with the {name_for_human} API. What is the {name_for_human} API useful for? {description_for_model} Parameters: {parameters} Format the arguments as a JSON object."""

# 提示词
REACT_PROMPT = """Answer the following questions as best you can. analysis and decide which tool you can use to help you answer. You have access to the following tools:

{tool_descs}

Have to use the following format:
Question: the input question you must answer
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can be repeated zero or more times)
Final Answer: the final answer to the original input question

Begin!
"""


class Agent:
    def __init__(self) -> None:
        self.tool = Tools()
        self.system_prompt = self.build_system_input()
        self.messages = [{"role": "system", "content": self.system_prompt}]

    def build_system_input(self):
        tool_descs, tool_names = [], []
        for tool in self.tool.toolConfig:
            tool_descs.append(TOOL_DESC.format(**tool))
            tool_names.append(tool['name_for_model'])
        tool_descs = '\n\n'.join(tool_descs)
        tool_names = ','.join(tool_names)
        return REACT_PROMPT.format(tool_descs=tool_descs, tool_names=tool_names)

    def parse_latest_plugin_call(self, text):
        plugin_name, plugin_args = '', ''
        i = text.rfind('\nAction:')
        j = text.rfind('\nAction Input:')
        k = text.rfind('\nObservation:')
        if 0 <= i < j:
            if k < j:
                text = text.rstrip() + '\nObservation:'
            k = text.rfind('\nObservation:')
            plugin_name = text[i + len('\nAction:'):j].strip()
            plugin_args = text[j + len('\nAction Input:'):k].strip()
            text = text[:k]
        return plugin_name, plugin_args, text

    def call_plugin(self, plugin_name, plugin_args):
        plugin_args = json5.loads(plugin_args)
        if plugin_name == 'tavily_search':
            res = self.tool.tavily_search(**plugin_args)
            return '\nObservation:' + res

    def text_completion(self, text):
        self.messages.append({"role": "user", "content": f"\nQuestion:{text}"})

        response = ollama.chat(
            model="deepseek-r1:70b",
            messages=self.messages,
            stream=False,  # 改为非流式获取完整响应
            options={
                'temperature': 0.4,
                'max_tokens': 121000,
                'stop': ['<|endoftext|>', '</response>']
            }
        )
        response_text = response["message"]["content"]

        plugin_name, plugin_args, updated_response = self.parse_latest_plugin_call(response_text)
        print("response_text"+response_text)
        print('1')
        print(plugin_name)
        print(plugin_args)
        print(updated_response)
        if plugin_name:
            observation = self.call_plugin(plugin_name, plugin_args)
            self.messages.append({"role": "assistant", "content": updated_response + observation})
            final_response = ollama.chat(model="deepseek-r1:70b",
                                         messages=self.messages,
                                         stream=False,
                                         options={
                                             'temperature': 0.5,
                                             'max_tokens': 121000,
                                             'stop': ['<|endoftext|>', '</response>']
                                         })
            return final_response["message"]["content"]
        else:
            return response_text


if __name__ == '__main__':
    agent = Agent()
    prompt = "最新的美国大选结果是什么"
    res = agent.text_completion(prompt)
    print(res)

from crewai import Agent, Task, Crew, Process, LLM
import os

from langchain_community.tools import DuckDuckGoSearchRun, BaseTool
from langchain_ollama import OllamaLLM
from typing import Optional, Type
from pydantic import BaseModel

from crewai.tools import tool


#  https://docs.crewai.com/concepts/crews

@tool
def multiplication_tool(first_number: int, second_number: int) -> str:
    """Useful for when you need to multiply two numbers together."""
    return first_number * second_number

def cache_func(args, result):
    # In this case, we only cache the result if it's a multiple of 2
    cache = result % 2 == 0
    return cache

multiplication_tool.cache_function = cache_func

# writer1 = Agent(
#         role="Writer",
#         goal="You write lessons of math for kids.",
#         backstory="You're an expert in writing and you love to teach kids but you know nothing of math.",
#         tools=[multiplication_tool],
#         allow_delegation=False,
#     )


# # 自定义 DuckDuckGoSearchRun 工具
# class CustomDuckDuckGoSearchRun(BaseTool):
#     name: str = "duckduckgo_search"  # 添加类型注解
#     description: str = "Search the web using DuckDuckGo"
#     args_schema: Optional[Type[BaseModel]] = None

#     def _run(self, query: str) -> str:
#         search = DuckDuckGoSearchRun()
#         return search.run(query)

#     async def _arun(self, query: str) -> str:
#         raise NotImplementedError("This tool does not support async")

# search_tool = CustomDuckDuckGoSearchRun()


# 使用 OllamaLLM 替代 Ollama
# ollama_qwen = OllamaLLM(model="qwen2.5")
# ollama_deepseek = OllamaLLM(model="deepseek-r1")



researcher = Agent(
        role='Local AI Expert',
        goal='Process information using a local model',
        backstory="An AI assistant running on local hardware.",
        llm=LLM(model="ollama/qwen2.5:latest", base_url="http://localhost:11434"),
        tools=[multiplication_tool],
        allow_delegation=False
    )

# # 创建一个研究员Agent
# researcher = Agent(
#     role='Researcher',
#     goal='Research methods to grow this channel Gao Dalie (高達烈) on youtube and get more subscribers',
#     backstory='You are an AI research assistant',
#     # tools=[search_tool],
#     verbose=True,
#     llm=ollama_qwen,
#     allow_delegation=False
# )

# 创建一个作家Agent
writer = Agent(
    role='Writer',
    goal='Write compelling and engaging reasons as to why someone should join Gao Dalie (高達烈) youtube channel',
    backstory='You are an AI master mind capable of growing any youtube channel',
    verbose=True,
    llm=LLM(model="ollama/qwen2.5:latest", base_url="http://localhost:11434"),
    allow_delegation=False,
)

# 为Agent设置任务
task1 = Task(
    description='1*1', 
    expected_output="A list of recent AI developments",
    agent=researcher
    )
task2 = Task(
    description='2*2', 
    expected_output="A list of recent AI developments",
    agent=researcher
    )
task3 = Task(
    description='Write a list of tasks',
    expected_output="A list of recent AI developments",         
    agent=writer
    )

# 工作人员和流程
crew = Crew(
    agents=[researcher, writer],
    tasks=[task1, task2, task3],
    verbose=True,
    process=Process.sequential
)

result = crew.kickoff()
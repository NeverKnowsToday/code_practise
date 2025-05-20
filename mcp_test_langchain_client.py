import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI


from langchain_ollama import ChatOllama

from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import HumanMessage




async def main():
    #生产模型
    # model = ChatOpenAI(model="qwq-32b",
    #                    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1",
    #                    api_key = "sk-dae4e059c40a46f986667eac732a7668"
    #                    )
    
    chatLLM = ChatTongyi(
        api_key = "sk-dae4e059c40a46f986667eac732a7668",

        streaming=True,
    )

    #本地模型
    #llm = ChatOllama(model="qwen2.5",temperature=0,verbose=True)


    server_params = StdioServerParameters(
        command="python",
        # 确保将这里的路径更新为你的 math_server.py 文件的绝对路径
        args=["/Users/gaoshipeng1/python/openai_test_demo/mcp_test_langchain_server.py"],
        #args=["/path/to/math_server.py"],
        # /Users/gaoshipeng1/python/openai_test_demo
    )

    # 在 async 函数内使用 async with
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 初始化连接
            await session.initialize()

            # 获取工具
            tools = await load_mcp_tools(session)
            print("tools-----:",tools)

            # 创建并运行代理
            agent = create_react_agent(chatLLM, tools)
            agent_response = await agent.ainvoke({"messages": "what's (3 + 5) x 12?"})
            print("agent_response-----:",agent_response)

# 通过 asyncio 事件循环运行 main 函数
if __name__ == "__main__":
    asyncio.run(main())

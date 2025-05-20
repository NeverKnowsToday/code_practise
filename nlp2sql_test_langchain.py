# from sqlalchemy import create_engine
# from langchain_community.utilities.sql_database import SQLDatabase

# from sqlalchemy.exc import SQLAlchemyError

# def get_engine_for_chinook_db():
#     """Create a MySQL engine using PyMySQL."""
#     # MySQL 数据库连接信息
#     db_config = {
#         'user': 'your_username',        # 替换为你的用户名
#         'password': 'your_password',    # 替换为你的密码
#         'host': 'localhost',            # 数据库主机
#         'database': 'chinook',          # 数据库名称
#     }

# def test_connection(engine):
#     """测试数据库连接是否成功."""
#     try:
#         # 尝试连接数据库
#         with engine.connect() as connection:
#             print("连接成功！")
#     except SQLAlchemyError as e:
#         print(f"连接失败：{e}")

# # 创建 MySQL 引擎
# engine = get_engine_for_chinook_db()

# # 测试连接
# test_connection(engine)

# # 创建 SQLDatabase 实例
# db = SQLDatabase(engine)


from sqlalchemy import create_engine
from langchain_community.utilities.sql_database import SQLDatabase
from sqlalchemy.exc import SQLAlchemyError

def get_engine_for_chinook_db():
    """Create a MySQL engine using PyMySQL."""
    # MySQL 数据库连接信息
    db_config = {
        'user': 'your_username',        # 替换为你的用户名
        'password': 'your_password',    # 替换为你的密码
        'host': 'localhost',            # 数据库主机
        'database': 'chinook',          # 数据库名称
    }

    # 创建 SQLAlchemy 引擎，使用 PyMySQL
    engine = create_engine(
        f"mysql+pymysql://root:1234@192.168.2.217:3306/bisheng"
    )
    return engine

def test_connection(engine):
    """测试数据库连接是否成功."""
    try:
        # 尝试连接数据库
        with engine.connect() as connection:
            print("连接成功！")
    except SQLAlchemyError as e:
        print(f"连接失败：{e}")

# 创建 MySQL 引擎
engine = get_engine_for_chinook_db()

# 测试连接
test_connection(engine)

# 创建 SQLDatabase 实例
db = SQLDatabase(engine)


from langchain_community.chat_models.tongyi import ChatTongyi


chatLLM = ChatTongyi(
    api_key = "sk-dae4e059c40a46f986667eac732a7668",
    #streaming=True,
)


# from langchain_ollama import ChatOllama

#     #本地模型
# chatLLM = ChatOllama(model="qwen2.5",temperature=0,verbose=True)

from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit

toolkit = SQLDatabaseToolkit(db=db, llm=chatLLM)


from langchain_community.tools.sql_database.tool import (
    InfoSQLDatabaseTool,
    ListSQLDatabaseTool,
    QuerySQLCheckerTool,
    QuerySQLDatabaseTool,
)

toolkit.get_tools()

from langchain import hub

prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")

assert len(prompt_template.messages) == 1
print(prompt_template.input_variables)

system_message = prompt_template.format(dialect="MySQL", top_k=100)

print("system_message:",system_message)

from langgraph.prebuilt import create_react_agent

agent_executor = create_react_agent(chatLLM, toolkit.get_tools(), prompt=system_message)



# example_query = "bisheng库里哪些表?"
#example_query = "bisheng数据库中assistant表里有哪些记录?"
example_query = "帮我生成一个插入 bisheng数据库中assistant表的 sql的例子"
#


events = agent_executor.stream(
    {"messages": [("user", example_query)]},
    stream_mode="values",
)
for event in events:
    event["messages"][-1].pretty_print()
# math_server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")

import requests


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b


@mcp.tool()
def get_datasource_list(
    page: int,  # 当前页码
    size: int   # 每页显示的数据条数
) -> dict:
    """获取数据源列表。

    Args:
        page: 当前页码。
        size: 每页显示的数据条数。
    
    Returns:
        返回数据源列表或错误信息。
    """
    
    # 定义接口 URL
    url = f"http://192.168.2.245:8081/api/v1/datasource?page={page}&size={size}"
    
    # 定义 token
    # token = get_atoken  # 请替换为有效的token
    
    # 定义请求头
    headers = {
        # "token": get_atoken()
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VyTmFtZSI6ImFkbWluIiwiZXhwIjoyMTAzNDE1ODU5LCJpc3MiOiJkYnBhc3MifQ.aQ1U0i8JWDf91AUKGAThwcg8LqpdIRdmQYkqN7iHVSs"

    }
    
    # 发送 GET 请求
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"请求失败，状态码: {response.status_code}, 原因: {response.text}"}



@mcp.tool()
def create_datasource(
    name: str,         # 数据源名称
    url: str,          # 数据源 URL
    docker_host: str   # Docker 主机地址
) -> dict:
    """创建数据源。

    Args:
        name: 数据源名称。
        url: 数据源 URL。
        docker_host: Docker 主机地址。
    
    Returns:
        返回创建的数据源信息或错误信息。
    """

    
    # 检查参数是否传递
    if not name or not url or not docker_host:
        return {"error": "缺少输入参数: name, url 和 docker_host 都是必需的。"}

    
    
    # 定义接口 URL
    url_endpoint = "http://192.168.2.245:8081/api/v1/datasource"
    
    # 定义 token
    token= "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VyTmFtZSI6ImFkbWluIiwiZXhwIjoyMTAzNDE1ODU5LCJpc3MiOiJkYnBhc3MifQ.aQ1U0i8JWDf91AUKGAThwcg8LqpdIRdmQYkqN7iHVSs"

    
    # 定义请求头
    headers = {
        "token": token,
        "Content-Type": "application/json"
    }
    
    # 定义请求数据
    data = {
        "name": name,
        "url": url,
        "docker_host": docker_host
    }
    
    # 发送 POST 请求
    response = requests.post(url_endpoint, headers=headers, json=data)
    
    if response.status_code == 201:  # 201 Created
        return response.json()
    else:
        return {"error": f"请求失败，状态码: {response.status_code}, 原因: {response.text}"}




if __name__ == "__main__":
    mcp.run(transport="sse")

    
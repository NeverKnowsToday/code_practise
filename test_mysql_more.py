import pymysql
from pymysql import MySQLError
import re

def main(host: str, port: str, user: str, password: str, database: str, sql_query: str) -> dict:
    mysql_connection = None
    results = []  # 用于存储每个查询的结果

    def remove_sql_comments(sql: str) -> str:
        # 使用正则表达式去除单行和多行注释
        sql = re.sub(r'--.*?(\r?\n|$)', '', sql)  # 去掉单行注释
        sql = re.sub(r'/\*.*?\*/', '', sql, flags=re.DOTALL)  # 去掉多行注释
        return sql.strip()

    try:
        mysql_connection = pymysql.connect(
            host=host,
            port=int(port),
            database=database,
            user=user,
            password=password,
            cursorclass=pymysql.cursors.DictCursor
        )

        if mysql_connection.open:
            cursor = mysql_connection.cursor()

            # 将 SQL 查询按分号分割，并过滤掉空的查询
            queries = [remove_sql_comments(q.strip()) for q in sql_query.split(';') if q.strip()]

            for query in queries:
                # 如果是 SELECT 查询，获取结果
                if query.lower().startswith("select"):
                    cursor.execute(query)
                    query_result = cursor.fetchall()
                    results.append({'query': query, 'result': query_result})
                    print(f"Query: {query}\nResult: {query_result}\n")
                else:
                    # 对于其他查询（INSERT, UPDATE, DELETE）
                    cursor.execute(query)
                    mysql_connection.commit()
                    results.append({'query': query, 'affected_rows': cursor.rowcount})

            # 将 results 转换为字符串
            results_str = str(results)

            return {'result1': results_str, 'result2': sql_query}

    except MySQLError as e:
        print(f"Error: {e}")
        return {'result1': str(e), 'result2': sql_query}
    except ValueError as e:
        print(f"Value Error: {e}")
        return {'result1': str(e), 'result2': sql_query}
    finally:
        if mysql_connection:
            cursor.close()
            mysql_connection.close()

# 示例用法：
# sql_query = '''-- 查看集装箱数据
# SELECT * FROM container_data;
# -- 查看散货数据
# SELECT * FROM bulk_data;
# -- 查看液体货物数据
# SELECT * FROM liquid_data;
# -- 查看特殊货物数据
# SELECT * FROM special_cargo_data;'''

# response = main('192.168.2.232', '6306', 'root', '123456', 'PortInfodb', sql_query)

# print(response)

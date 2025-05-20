import pymysql
from pymysql import MySQLError

def main(database: str, sql_query: str) -> dict:
    mysql_connection = None  # Initialize mysql_connection outside the try block
    try:
        # Connect to MySQL database using PyMySQL
        mysql_connection = pymysql.connect(
            host='192.168.2.217',        # MySQL host address
            database=database,           # Database name
            user='root',                 # Database username
            password='1234',             # Database password
            cursorclass=pymysql.cursors.DictCursor  # To get results as dictionaries
        )

        # Check if the connection is successful
        if mysql_connection.open:
            cursor = mysql_connection.cursor()

            # If the query is a SELECT, fetch the results
            if sql_query.strip().lower().startswith("select"):
                cursor.execute(sql_query)
                results = cursor.fetchall()
                return {'result1': results, 'result2': sql_query}

            else:
                # For other queries (INSERT, UPDATE, DELETE)
                cursor.execute(sql_query)
                mysql_connection.commit()
                results = f"Query executed successfully, {cursor.rowcount} row(s) affected."
                return {'result1': results, 'result2': sql_query}

    except MySQLError as e:
        print(f"Error: {e}")
        return {'error': str(e)}
    except ValueError as e:
        print(f"Value Error: {e}")
        return {'error': "Invalid input data"}
    finally:
        # Ensure mysql_connection and cursor are closed properly
        if mysql_connection:
            cursor.close()
            mysql_connection.close()

# Example usage:
# SELECT query:
# response = execute_sql('test', 'SELECT * FROM users WHERE id = 1')
# print(response)

# INSERT query:
# response = execute_sql('test', 'INSERT INTO users (name, age, city) VALUES (%s, %s, %s)', ('John', 28, 'New York'))
# print(response)

# UPDATE query:
# response = execute_sql('test', 'UPDATE users SET age = %s WHERE name = %s', (29, 'John'))
# print(response)

# DELETE query:
# response = execute_sql('test', 'DELETE FROM users WHERE id = %s', (1,))
# print(response)

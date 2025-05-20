import pymysql
from pymysql import MySQLError

def main(database: str, table: str, limit: str, offset: str) -> dict:
    mysql_connection = None  # Initialize mysql_connection outside the try block
    try:
        # Convert limit and offset to integers (with error handling)
        limit = int(limit) if limit.isdigit() else 10  # 默认 10
        offset = int(offset) if offset.isdigit() else 0  # 默认 0
        
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

            # Construct query with LIMIT and OFFSET
            query = f"SELECT * FROM {table} LIMIT %s OFFSET %s"
            cursor.execute(query, (limit, offset))

            # Fetch results
            results = cursor.fetchall()

            # Return results
            return {'result1': results, 'result2': query}

    except MySQLError as e:
        print(f"Error: {e}")
        return {'error': str(e)}
    except ValueError as e:
        print(f"Value Error: {e}")
        return {'error': "Invalid limit or offset value"}
    finally:
        # Ensure mysql_connection and cursor are closed properly
        if mysql_connection:
            cursor.close()
            mysql_connection.close()

# Example usage
response = main('test', 'users', '3', '0')  # Fetch 10 rows, starting from the 20th row
print(response)

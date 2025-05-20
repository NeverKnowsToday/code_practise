import pymysql
from pymysql import MySQLError

def main(database: str, table: str, condition: str) -> dict:
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

            # Construct the query for deletion
            query = f"DELETE FROM {table} WHERE {condition}"

            # Execute the delete query
            cursor.execute(query)

            # Commit the transaction
            mysql_connection.commit()

            # Return success message
            results = {'message': f"Deleted {cursor.rowcount} row(s) from {table} successfully."}
            return {'result1': results, 'result2': query}

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

# Example usage
# response = delete_data('test', 'users', "id = 1")
# print(response)

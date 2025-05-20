import pymysql
from pymysql import MySQLError

def main(database: str, table: str, columns: str, values: str, condition: str) -> dict:
    mysql_connection = None  # Initialize mysql_connection outside the try block
    try:
        # Convert the string of values into a tuple
        values = tuple(values.split(', '))  # Split the string by ', ' and convert to a tuple

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

            # Construct the SET part of the query for updating
            set_clause = ', '.join([f"{col} = %s" for col in columns.split(', ')])
            
            # Construct the query for updating the data
            query = f"UPDATE {table} SET {set_clause} WHERE {condition}"

            # Execute the update query with the values
            cursor.execute(query, values)

            # Commit the transaction
            mysql_connection.commit()

            # Return success message
            results = {'message': f"Updated {cursor.rowcount} row(s) in {table} successfully."}
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
# response = update_data('test', 'users', 'name, age', 'John Doe, 29', "id = 1")
# print(response)

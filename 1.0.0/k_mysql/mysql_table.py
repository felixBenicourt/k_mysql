

import mysql_utilities
import mysql_querry
import table_definitions


class MySQLDatabaseTable():
    """
    A class for managing MySQL database tables.

    This class provides methods for dynamically creating database tables
    using a single, reusable method.
    """
    def __init__(self, connection):
        """
        Initializes the MySQLDatabaseTable instance.

        Args:
            connection (mysql.connector.MySQLConnection): The active database connection.
        """
        self.logger = mysql_utilities.get_logger(__name__)
        self.querry = mysql_querry.MySQLDatabaseQuerry(connection)
        self.connection = connection


    def create_table(self, table_name, columns):
        """
        Creates a database table with the specified name and columns.

        Args:
            table_name (str): The name of the table to create.
            columns (dict): A dictionary where keys are column names and values are
                            SQL data types and constraints.

        Logs:
            - Logs the creation query for debugging.
            - Logs errors in case of execution failure.

        Example:
            columns = {
                "id": "INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY",
                "name": "VARCHAR(255) NOT NULL",
            }
            self.create_table("example_table", columns)
        """
        columns_sql = ", ".join([f"{col} {definition}" for col, definition in columns.items()])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql});"
        mysql_utilities.execute_query(self.connection, query)


    def setup_all_tables(self):
        """
        Sets up all necessary tables by defining their structures
        and using the `create_table` method to create them.
        """
        for table_name, columns in table_definitions.TABLES.items():
            self.create_table(table_name, columns)


    def setup_table(self, table_arg):
        """
        Sets up a specific table by defining its structure
        and using the `create_table` method filtered by the name.

        Args:
            table_arg (str): The name of the table to set up.
        """
        if table_arg not in table_definitions.TABLES:
            raise ValueError(f"Table '{table_arg}' is not defined in TABLES.")
        columns = table_definitions.TABLES[table_arg]
        self.create_table(table_arg, columns)

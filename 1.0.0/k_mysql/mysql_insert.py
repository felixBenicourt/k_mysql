

import mysql_utilities
import mysql.connector
import mysql_querry
import element_config


class MySQLDatabaseInsert():
    """
    A class for inserting data into the MySQL database.

    This class provides methods for inserting new records into the database 
    across different tables. It relies on the provided database connection 
    to execute `INSERT` SQL queries and commit them to the database.
    """
    def __init__(self, connection):
        """
        Initializes the MySQLDatabaseInsert instance.

        This constructor initializes a logger and a `MySQLDatabaseQuerry`
        instance for performing queries. The database connection is also 
        stored for use in query execution.

        Args:
            connection (mysql.connector.MySQLConnection): The active database connection.
        """
        self.logger = mysql_utilities.get_logger(__name__)
        self.querry = mysql_querry.MySQLDatabaseQuerry(connection)
        self.connection = connection


    def insert_row(self, table_name, data):
        """
        Inserts a row into the specified database table.

        This method generates and executes an SQL `INSERT` query using the provided data.
        If the `data` dictionary includes an `id` key, it is ignored as the database generates
        the primary key.

        Args:
            table_name (str): The name of the table to insert data into.
            data (dict): A dictionary of column-value pairs representing the row to insert.

        Returns:
            int: The ID of the newly inserted row.

        Logs:
            - Logs the generated SQL query for debugging.
            - Logs errors in case of query execution failure.

        Raises:
            mysql.connector.Error: If there is an issue with the query execution.

        Example:
            data = {"name": "My Project"}
            row_id = self.insert_row("project", data)
        """
        if 'id' in data:
            del data['id']
        
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders});"
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, tuple(data.values()))
            self.connection.commit()
            return cursor.lastrowid
        except mysql.connector.Error as e:
            self.logger.error("Error inserting into table: %s", e)
            raise
        finally:
            cursor.close()

    def sanitize_data(self, dict_element, required_keys):
        """
        Ensures that the input dictionary contains all required keys.

        This method takes the input dictionary and checks for missing keys based 
        on the `required_keys` list. If any key is missing, it adds the key with 
        a default empty string as the value.

        Args:
            dict_element (dict): The input dictionary containing the data for an element.
            required_keys (list): A list of required keys that must be present in the dictionary.

        Returns:
            dict: A sanitized dictionary with all required keys present.

        Logs:
            - Logs debug messages for any missing keys that are added.

        Example:
            dict_element = {"name": "My Element"}
            required_keys = ["name", "type", "version"]
            sanitized_dict = self.sanitize_data(dict_element, required_keys)
            # Output: {"name": "My Element", "type": "", "version": ""}
        """
        sanitized_dict = dict_element.copy()
        for key in required_keys:
            if key not in sanitized_dict:
                self.logger.debug(f"Adding missing key '{key}' with default value.")
                sanitized_dict[key] = ""
        return sanitized_dict


    def element_exists(self, query_method, sanitized_dict, keys_to_ignore):
        """
        Checks if an element already exists in the database.

        This method uses a query method to retrieve existing records from the database 
        and compares them against the sanitized dictionary. If the element matches 
        any existing record (ignoring specified keys), it is considered as existing.

        Args:
            query_method (str): The name of the method in `MySQLDatabaseQuerry` to fetch existing data.
            sanitized_dict (dict): The sanitized dictionary representing the element data.
            keys_to_ignore (list): A list of keys to ignore during comparison (e.g., auto-generated IDs).

        Returns:
            bool: `True` if the element exists in the database; `False` otherwise.

        Logs:
            - Logs the comparison process to track duplicates and ignored keys.

        Example:
            query_method = "fetch_existing_elements"
            sanitized_dict = {"name": "My Element", "type": "asset"}
            keys_to_ignore = ["id", "created_at"]
            exists = self.element_exists(query_method, sanitized_dict, keys_to_ignore)
            # Output: True or False
        """
        existing_data = getattr(self.querry, query_method)()
        return mysql_utilities.compare_rows(existing_data, sanitized_dict, keys_to_ignore)


    def insert_element(self, element_arg, dict_element):
        """
        Inserts an element into the database based on the specified element type and data.

        This method validates the required fields for the given `element_arg`, sanitizes the input 
        dictionary `dictElement` by ensuring all required keys are present, and checks if the element 
        already exists in the database. If the element doesn't exist, it inserts the data into the 
        appropriate table.

        Args:
            element_arg (str): The type of element to insert. Valid values are:
                            "project", "sequence", "asset", "shot".
            dictElement (dict): A dictionary containing the data for the element. 
                                Must include the required keys for the specified `element_arg`.

        Returns:
            dict: The sanitized and inserted dictionary if the insertion is successful or the element 
                already exists.
            None: If the `element_arg` is not valid.

        Logs:
            - Logs the status of the insertion process:
                - Success: "Project data inserted in the DB."
                - Failure: "Project data already exists; can't be inserted twice in the DB."

        Raises:
            KeyError: If any required key is missing from the `dictElement`.
            ValueError: If `element_arg` is invalid or not supported.

        Example:
            element_arg = "shot"
            dictElement = {
                projectId=1,
                name="00114", 
                type="shot",
                task="cfx",
                variation="main",
                sequenceId=0,
                version=1
            }
        """
        if element_arg not in element_config.ELEMENT_TYPES:
            self.logger.warning(f"Invalid element type: {element_arg}.")
            return None

        config = element_config.ELEMENT_TYPES[element_arg]
        required_keys = config["required_keys"]
        keys_to_ignore = config["keys_to_ignore"]
        query_method = config["query_method"]

        sanitized_dict = self.sanitize_data(dict_element, required_keys)

        if not self.element_exists(query_method, sanitized_dict, keys_to_ignore):
            self.logger.info(f"Inserting {element_arg} into the database.")
            self.insert_row(element_arg, sanitized_dict)
            self.logger.info(f"{element_arg.capitalize()} inserted successfully: {sanitized_dict}.")
        else:
            self.logger.info(f"{element_arg.capitalize()} already exists; insertion skipped.")

        return sanitized_dict




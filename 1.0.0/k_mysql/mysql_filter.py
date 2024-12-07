

import mysql_utilities
import mysql_querry


class MySQLDataFilter():
    def __init__(self, connection):
        """
        Initializes the MySQLDataFilter instance with a database connection.

        Args:
            connection (mysql.connector.MySQLConnection): The active database connection.
        """
        self.logger = mysql_utilities.get_logger(__name__)
        self.querry = mysql_querry.MySQLDatabaseQuerry(connection)
        self.connection = connection

    def filter_dicts(self, data_list, key, value):
        """
        Filters a list of dictionaries based on a specific key-value pair.

        Args:
            data_list (list[dict]): The list of dictionaries to filter.
            key (str): The key to filter by.
            value (Any): The value to filter the key by.

        Returns:
            list[dict]: A list of dictionaries that match the key-value pair.

        Raises:
            ValueError: If data_list is not a list of dictionaries.
        """
        if not isinstance(data_list, list) or not all(isinstance(item, dict) for item in data_list):
            self.logger.error("Expected a list of dictionaries, but received something else.")
            raise ValueError("data_list must be a list of dictionaries.")
        
        return [item for item in data_list if item.get(key) == value]

    def get_highest_value(self, data_list, version_key):
        """
        Returns the dictionary with the latest version value based on the specified version key.

        Args:
            data_list (list[dict]): The list of dictionaries to search.
            version_key (str): The key that holds the version number.

        Returns:
            dict: The dictionary with the highest version value. 
                  Returns None if the list is empty or no valid version is found.

        Raises:
            ValueError: If data_list is not a list of dictionaries.
        """
        if not isinstance(data_list, list) or not all(isinstance(item, dict) for item in data_list):
            self.logger.error("Expected a list of dictionaries, but received something else.")
            raise ValueError("data_list must be a list of dictionaries.")

        if not data_list:
            self.logger.warning("Data list is empty. Returning None.")
            return None

        # Filter out items that don't have a valid version_key or a valid integer value
        valid_items = [
            item for item in data_list if version_key in item and isinstance(item[version_key], int)
        ]
        
        if not valid_items:
            self.logger.warning(f"No valid version found for key '{version_key}'. Returning None.")
            return None

        max_version_dict = max(valid_items, key=lambda x: x[version_key])
        return max_version_dict



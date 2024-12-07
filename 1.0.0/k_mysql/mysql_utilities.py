

import mysql.connector
import logging


def get_logger(name):
    """
    Configures and returns a logger instance.

    This function sets up a logger with a specified logging level and format.
    The logger can be used to log messages across the application.

    Args:
        name (str): The name of the logger, typically the module's `__name__`.

    Returns:
        logging.Logger: A configured logger instance.
    """
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    return logging.getLogger(name)


def execute_query(connection, query, params=None):
    """
    Executes a database query using the provided connection.

    This function executes a given SQL query with optional parameters and
    handles both `SELECT` and data-modification queries (`INSERT`, `UPDATE`, `DELETE`).
    In case of a `SELECT` query, it returns the fetched rows. For other queries,
    it commits the changes to the database.

    Args:
        connection (mysql.connector.MySQLConnection): The active database connection.
        query (str): The SQL query to be executed.
        params (tuple, optional): The parameters to be passed into the query. Defaults to None.

    Returns:
        list: Fetched rows for `SELECT` queries. None for others.

    Raises:
        mysql.connector.Error: If an error occurs during query execution.
    """
    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute(query, params)
        if query.strip().lower().startswith("select"):
            return cursor.fetchall()
        connection.commit()
    except mysql.connector.Error as e:
        get_logger(__name__).error("Error executing query: %s", e)
        raise
    finally:
        if cursor:
            cursor.close()


def compare_rows(rows, target_dict, keys_to_ignore):
    """
    Compares a target dictionary with rows, ignoring specified keys.

    This function filters out certain keys from both the rows and the target
    dictionary before performing the comparison. It checks if the filtered
    target dictionary matches any of the filtered rows.

    Args:
        rows (dict): A dictionary of rows, where the keys are unique identifiers
                     and the values are dictionaries of row data.
        target_dict (dict): The dictionary to compare against the rows.
        keys_to_ignore (list): A list of keys to be ignored during the comparison.

    Returns:
        bool: True if the target dictionary matches any row (ignoring specified keys),
              False otherwise.
    """
    filtered_rows = {
        tuple((k, v) for k, v in row.items() if k not in keys_to_ignore)
        for row in rows.values()
    }
    filtered_target = tuple((k, v) for k, v in target_dict.items() if k not in keys_to_ignore)
    return filtered_target in filtered_rows


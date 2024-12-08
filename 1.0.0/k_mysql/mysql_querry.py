

import mysql_utilities


class MySQLDatabaseQuerry():
    """
    A utility class for performing database queries in a MySQL database.

    This class includes methods for fetching, updating, and deleting data from the database,
    as well as specialized queries for handling projects, sequences, shots, and assets.

    Attributes:
        logger: A logger instance for logging messages.
        connection: A MySQL connection object for interacting with the database.
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
        self.connection = connection


    def fetch_all(self, table_name):
        """
        Fetches all rows from a specified table.

        Args:
            table_name (str): The name of the table to fetch data from.

        Returns:
            list: A list of rows fetched from the specified table.
        """
        query = f"SELECT * FROM {table_name};"
        return mysql_utilities.execute_query(self.connection, query)


    def fetch_by_condition(self, table_name, conditions):
        """
        Fetches rows from a specified table based on given conditions.

        Args:
            table_name (str): The name of the table to fetch data from.
            conditions (dict): A dictionary of conditions, where keys are column names
                               and values are their corresponding values to filter by.

        Returns:
            list: A list of rows that match the conditions.
        """
        condition_sql = " AND ".join([f"{key} = %s" for key in conditions.keys()])
        query = f"SELECT * FROM {table_name} WHERE {condition_sql};"
        return mysql_utilities.execute_query(self.connection, query, tuple(conditions.values()))


    def get_elements_by_name(self, table_name, name_column, name_value):
        """
        Fetches a list of dictionaries of information from a specified table based on the name.

        Args:
            table_name (str): The name of the table to fetch data from.
            name_column (str): The column name to filter by (typically the 'name' column).
            name_value (str): The name value to search for.

        Returns:
            list[dict]: A list of dictionaries, each representing a row where the name matches.
                        Returns an empty list if no matches are found.
        """
        query = f"SELECT * FROM {table_name} WHERE {name_column} = %s;"
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, (name_value,))
            rows = cursor.fetchall()
            if not rows:
                return []  
            column_names = [desc[0] for desc in cursor.description]
            result = [dict(zip(column_names, row)) for row in rows]
        finally:
            cursor.close()

        return result


    def get_elements_by_column_value(self, table_name, column_name, column_value):
        """
        Fetches rows from a specified table where a given column matches a specific value.

        Args:
            table_name (str): The name of the table to fetch data from.
            column_name (str): The column name to filter by.
            column_value (Any): The value to filter the column by.

        Returns:
            list[dict]: A list of dictionaries representing the rows that match the condition.
                        Returns an empty list if no matches are found.
        """
        query = f"SELECT * FROM {table_name} WHERE {column_name} = %s;"
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, (column_value,))
            rows = cursor.fetchall()
            if not rows:
                return []  
            column_names = [desc[0] for desc in cursor.description]
            result = [dict(zip(column_names, row)) for row in rows]
        finally:
            cursor.close()

        return result


    def get_shot_by_sequence(self, sequence_id):
        """
        Fetches all shots associated with a specific sequence ID.

        Args:
            sequence_id (int): The ID of the sequence to fetch shots for.

        Returns:
            list: A list of rows representing shots associated with the sequence.
        """
        query = "SELECT * FROM shot WHERE sequence_id = %s;"
        return mysql_utilities.execute_query(self.connection, query, (sequence_id,))
        

    def get_sequence_with_shot(self, sequence_id):
        """
        Fetches sequence information along with its associated shots.

        Args:
            sequence_id (int): The ID of the sequence to fetch.

        Returns:
            list: A list of rows containing sequence and shot information.
        """
        query = """
        SELECT s.id AS sequence_id, s.name AS sequence_name, sh.id AS shot_id, sh.name AS shot_name
        FROM sequence s
        LEFT JOIN shot sh ON s.id = sh.sequence_id
        WHERE s.id = %s;
        """
        return mysql_utilities.execute_query(self.connection, query, (sequence_id,))


    def get_all_sequence_with_shot(self):
        """
        Fetches all sequences and their associated shots.

        Returns:
            dict: A dictionary where keys are sequence IDs, and values are dictionaries containing
                  sequence names and a list of associated shots.
        """
        query = """
        SELECT 
            s.id AS sequence_id, 
            s.name AS sequence_name, 
            sh.id AS shot_id, 
            sh.name AS shot_name
        FROM sequence s
        LEFT JOIN shot sh ON s.id = sh.sequence_id
        ORDER BY s.name, sh.name;
        """
        rows = mysql_utilities.execute_query(self.connection, query)
        data = {}
        for sequence_id, sequence_name, shot_id, shot_name in rows:
            if sequence_id not in data:
                data[sequence_id] = {"sequence_name": sequence_name, "shots": []}
            if shot_id:
                data[sequence_id]["shots"].append({"shot_id": shot_id, "shot_name": shot_name})
        return data


    def delete_element(self, collumnName, objectId):
        """
        Deletes a specified element from the database.

        This method is a generalized utility for removing a row from a database table.
        The specific table is determined by the provided object type, and the row
        is identified using the given object ID.

        Args:
            collumnName (str): The type of the object (corresponding to a database table name).
            objectId (int or str): The unique identifier of the object (row) to be deleted.

        Returns:
            None
        """
        query = f"DELETE FROM {collumnName} WHERE id = %s;"
        mysql_utilities.execute_query(self.connection, query, (objectId,))


    def get_all_project(self):
        """
        Fetches all projects from the database.

        Returns:
            dict: A dictionary of projects where keys are project IDs, and values are project details.
        """
        query = "SELECT * FROM project"
        rows = mysql_utilities.execute_query(self.connection, query)
        column_names = [
            'id',
            "name"
        ]
        projects = {}
        for row in rows:
            project = dict(zip(column_names, row))
            projects[project['id']] = project
        return projects


    def get_all_sequence(self):
        """
        Fetches all sequences from the database.

        Returns:
            dict: A dictionary of sequences where keys are sequence IDs, and values are sequence details.
        """
        query = "SELECT * FROM sequence"
        rows = mysql_utilities.execute_query(self.connection, query)
        column_names = [
            'id',
            "projectId", 
            "name"
        ]
        sequences = {}
        for row in rows:
            sequence = dict(zip(column_names, row))
            sequences[sequence['id']] = sequence
        return sequences


    def get_all_asset(self):
        """
        Fetches all assets from the database.

        Returns:
            dict: A dictionary of assets where keys are asset IDs, and values are asset details.
        """
        query = "SELECT * FROM asset"
        rows = mysql_utilities.execute_query(self.connection, query)
        column_names = [
            'id',
            "projectId", 
            "name",
            "type", 
            "task", 
            "variation", 
            "version",
            "status"
        ]
        assets = {}
        for row in rows:
            asset = dict(zip(column_names, row))
            assets[asset['id']] = asset
        return assets


    def get_all_shot(self):
        """
        Fetches all shots from the database.

        Returns:
            dict: A dictionary of shots where keys are shot IDs, and values are shot details.
        """
        query = "SELECT * FROM shot;"
        rows = mysql_utilities.execute_query(self.connection, query)
        column_names = [
            'id',
            "projectId", 
            "name",
            "type", 
            "task", 
            "variation", 
            "sequenceId", 
            "version",
            "cutIn", 
            "cutOut"
        ]
        shots = {}
        for row in rows:
            shot = dict(zip(column_names, row))
            shots[shot['id']] = shot
        return shots



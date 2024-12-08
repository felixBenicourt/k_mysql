

import mysql.connector
import mysql_insert
import mysql_utilities
import mysql_table
import mysql_querry
import mysql_filter


class MySQLDatabase(mysql_table.MySQLDatabaseTable, 
                    mysql_insert.MySQLDatabaseInsert, 
                    mysql_querry.MySQLDatabaseQuerry,
                    mysql_filter.MySQLDataFilter
                    ):
    """
    A class for managing the connection to a MySQL database.

    This class provides methods to connect to and disconnect from a MySQL database,
    as well as a `MySQLDatabaseInsert` instance for performing insert operations.

    Attributes:
        host (str): The database host.
        user (str): The username for the database connection.
        password (str): The password for the database connection.
        database (str): The name of the database to connect to.
        connection (mysql.connector.MySQLConnection): The database connection object.
        logger (logging.Logger): Logger for database operations.
        coreMysql (MySQLDatabaseInsert): An instance of `MySQLDatabaseInsert` for executing insert queries.
    """

    def __init__(self, host, user, password, database):
        """
        Initializes the MySQLDatabase instance and establishes a connection.

        This constructor initializes the database connection and sets up the
        `MySQLDatabaseInsert` instance for insert operations. The connection
        is established upon initialization.

        Args:
            host (str): The database host.
            user (str): The username for the database connection.
            password (str): The password for the database connection.
            database (str): The name of the database to connect to.
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.logger = mysql_utilities.get_logger(__name__)
        self.connect()
        self.set_connection()


    def set_connection(self):
        """
        Initializes and sets the `mysql_table`, `mysql_insert`, `mysql_querry` and `mysql_filter` modules.
        """
        mysql_table.MySQLDatabaseTable.__init__(self, self.connection)
        mysql_insert.MySQLDatabaseInsert.__init__(self, self.connection)
        mysql_querry.MySQLDatabaseQuerry.__init__(self, self.connection)
        mysql_filter.MySQLDataFilter.__init__(self, self.connection)
        self.logger.info("MySQL submodules initialized successfully.")


    def connect(self):
        """
        Establishes a connection to the MySQL database.

        This method attempts to connect to the MySQL database using the provided
        credentials and logs the success or failure of the connection attempt.

        Raises:
            mysql.connector.Error: If there is an error connecting to the database.
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.logger.info("Connection successful.")
        except mysql.connector.Error as e:
            self.logger.error("Error connecting to database: %s", e)
            raise


    def disconnect(self):
        """
        Closes the database connection.

        This method ensures the database connection is closed when no longer needed
        and logs the action.

        Raises:
            None
        """
        if self.connection:
            self.connection.close()
            self.logger.info("Connection closed.")

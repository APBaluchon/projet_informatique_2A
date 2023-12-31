import os
import dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from business_layer.service.singleton.singleton import Singleton


class DBConnection(metaclass=Singleton):
    """
    Technical class to open only one connection to the DB.
    """

    def __init__(self):
        dotenv.load_dotenv(override=True)
        try:
            # Open the connection.
            self.__connection = psycopg2.connect(
                host=os.environ["HOST"],
                port=os.environ["PORT"],
                database=os.environ["DATABASE"],
                user=os.environ["USER"],
                password=os.environ["PASSWORD"],
                cursor_factory=RealDictCursor,
            )
        except psycopg2.Error as e:
            print(f"Error connecting to the database: {e}")

    @property
    def connection(self):
        """
        Return the opened connection.

        :return: the opened connection.
        """
        return self.__connection

    def close_connection(self):
        """
        Close the database connection.
        """
        if self.__connection is not None:
            self.__connection.close()
            self.__connection = None

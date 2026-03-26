"""
Module containing the DBBroker class: helper for managing database connections and executing queries.
"""

import os
from typing import List, Tuple

import mariadb  # type: ignore
from dotenv import load_dotenv

from src.Utils.logger import setup_logger

load_dotenv()


class DBBroker:
    """
    Singleton class responsible for managing database connections and executing queries.
    Uses a connection pool to efficiently handle multiple concurrent database operations.
    """

    _instance = None
    _logger = setup_logger("DBBroker")

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBBroker, cls).__new__(cls)
            cls._instance._logger = setup_logger("DBBroker")
            try:
                cls._instance._initialize_pool()
            except Exception as e:
                raise RuntimeError("Failed to initialize DBBroker") from e

        return cls._instance

    def _initialize_pool(self):
        try:
            self._logger.info("Attempting to initialize Database Connection Pool...")

            self.pool = mariadb.ConnectionPool(
                pool_name=os.getenv("DB_POOL_NAME", "web_pool"),
                pool_size=int(os.getenv("DB_POOL_SIZE", "5")),
                host=os.getenv("DB_HOST"),
                port=int(os.getenv("DB_PORT", "3306")),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME"),
            )
            self._logger.info("Database connection pool established successfully.")

        except mariadb.Error as e:
            self._logger.critical(f"Failed to create connection pool: {e}")
            raise

    def _get_connection(self):
        try:
            conn = self.pool.get_connection()
            self._logger.debug("Connection used from pool.")
            return conn
        except mariadb.Error as e:
            self._logger.error(f"Error getting connection from pool: {e}")
            raise

    def execute_read_query(self, query: str, params: Tuple = ()) -> List[dict]:
        """
        Executes a read query (SELECT) and returns the results as a list of dictionaries.

        Args:
            query (str): The SQL query to execute, with placeholders for parameters.
            params (Tuple): A tuple of parameters to substitute into the query.

        Returns:
            List[dict]: A list of dictionaries representing the rows returned by the query.
        """
        connection = None
        cursor = None
        try:
            connection = self._get_connection()
            cursor = connection.cursor(dictionary=True)

            self._logger.debug(
                f"Executing READ query: {query} {'' if not params else f' | Params: {params}'}"
            )

            cursor.execute(query, params)
            result = cursor.fetchall()

            self._logger.debug(
                f"Query executed successfully. Rows returned: {len(result)}"
            )
            return result

        except mariadb.Error:
            self._logger.exception(f"Database Read Error executing query: {query}")
            raise

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
                self._logger.debug("Connection returned to pool.")

    def execute_write_query(self, query: str, params: Tuple = ()) -> Tuple[int, int]:
        """
        Executes a write query (INSERT, UPDATE, DELETE) and returns the number of affected rows and last insert ID.

        Args:
            query (str): The SQL query to execute, with placeholders for parameters.
            params (Tuple): A tuple of parameters to substitute into the query.

        Returns:
            affected_rows (int): The number of rows affected by the query.
            last_insert_id (int): The ID of the last inserted row (if applicable).
        """
        connection = None
        cursor = None
        try:
            connection = self._get_connection()
            cursor = connection.cursor()

            self._logger.debug(
                f"Executing WRITE query: {query} {'' if not params else f' | Params: {params}'}"
            )

            cursor.execute(query, params)
            connection.commit()

            affected_rows = cursor.rowcount
            last_insert_id = cursor.lastrowid
            self._logger.debug(
                f"Write operation successful. Rows affected: {affected_rows}"
            )

            return affected_rows, last_insert_id

        except mariadb.Error:
            if connection:
                connection.rollback()
                self._logger.warning("Transaction rolled back due to error.")

            self._logger.exception(f"Database Write Error executing query: {query}")
            raise

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
                self._logger.debug("Connection returned to pool.")

    def execute_many(self, query: str, params_list: List[Tuple]) -> int:
        """
        Executes a batch of write queries using executemany.

        Args:
            query (str): The SQL query to execute, with placeholders for parameters.
            params_list (List[Tuple]): A list of parameter tuples, one for each execution.

        Returns:
                int: The total number of rows affected by the batch operation.
        """
        connection = None
        cursor = None
        try:
            connection = self._get_connection()
            cursor = connection.cursor()

            self._logger.debug(
                f"Executing batch WRITE query: {query} {'' if not params_list else f' | Batch size: {len(params_list)}'}"
            )

            cursor.executemany(query, params_list)
            connection.commit()

            affected_rows = cursor.rowcount
            self._logger.debug(
                f"Batch write operation successful. Total rows affected: {affected_rows}"
            )

            return affected_rows

        except mariadb.Error as e:
            if connection:
                connection.rollback()
                self._logger.warning("Batch transaction rolled back due to error.")

            self._logger.exception(
                f"Error: {e}", f"Database Batch Write Error executing query: {query}"
            )
            raise

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
                self._logger.debug("Connection returned to pool.")

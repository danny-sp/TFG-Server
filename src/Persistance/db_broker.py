import os
import mariadb
import sys
from dotenv import load_dotenv
from typing import List, Tuple

from src.Utils.logger import setup_logger

load_dotenv()

class DBBroker:
    _instance = None
    _logger = None

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
                pool_size=int(os.getenv("DB_POOL_SIZE", 5)),
                host=os.getenv("DB_HOST"),
                port=int(os.getenv("DB_PORT", 3306)),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME")
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
        connection = None
        cursor = None
        try:
            connection = self._get_connection()
            cursor = connection.cursor(dictionary=True)

            self._logger.debug(f"Executing READ query: {query} {'' if not params else f' | Params: {params}'}")

            cursor.execute(query, params)
            result = cursor.fetchall()

            self._logger.debug(f"Query executed successfully. Rows returned: {len(result)}")
            return result

        except mariadb.Error as e:
            self._logger.exception(f"Database Read Error executing query: {query}")
            raise

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
                self._logger.debug("Connection returned to pool.")

    def execute_write_query(self, query: str, params: Tuple = ()) -> Tuple[int, int]:
        connection = None
        cursor = None
        try:
            connection = self._get_connection()
            cursor = connection.cursor()

            self._logger.debug(f"Executing WRITE query: {query} {'' if not params else f' | Params: {params}'}")

            cursor.execute(query, params)
            connection.commit()

            affected_rows = cursor.rowcount
            last_insert_id = cursor.lastrowid
            self._logger.debug(f"Write operation successful. Rows affected: {affected_rows}")

            return affected_rows, last_insert_id

        except mariadb.Error as e:
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

    def execute_many(self, query: str, params_list: List[Tuple]) -> List[int]:
        connection = None
        cursor = None
        try:
            connection = self._get_connection()
            cursor = connection.cursor()

            self._logger.debug(f"Executing batch WRITE query: {query} {'' if not params_list else f' | Batch size: {len(params_list)}'}")

            cursor.executemany(query, params_list)
            connection.commit()

            affected_rows = cursor.rowcount
            self._logger.debug(f"Batch write operation successful. Total rows affected: {affected_rows}")

            return affected_rows

        except mariadb.Error as e:
            if connection:
                connection.rollback()
                self._logger.warning("Batch transaction rolled back due to error.")

            self._logger.exception(f"Database Batch Write Error executing query: {query}")
            raise

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
                self._logger.debug("Connection returned to pool.")

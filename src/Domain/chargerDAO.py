"""
DAO for charger entity.
"""

from datetime import datetime
from typing import Optional

from src.Domain.charger import Charger
from src.Domain.charging_station import ChargingStation
from src.Persistence.db_broker import DBBroker
from src.Utils.logger import setup_logger

_logger = setup_logger("ChargerDAO")


def insert(charging_station: ChargingStation, charger: Charger) -> int:
    """
    Inserts a new charger into the database for a specific charging station.

    Args:
        charging_station (ChargingStation): The charging station to which the charger belongs.
        charger (Charger): The charger object to insert.

    Returns:
        int: The ID of the newly inserted charger, or -1 if the insertion fails.
    """
    query = """
    INSERT INTO chargers (charging_station_id, power_kw)
    VALUES (?, ?)
    """
    params = (
        charging_station.id,
        charger.power_kw,
    )
    db = DBBroker()
    try:
        _, inserted_id = db.execute_write_query(query, params)
    except Exception as e:
        _logger.error(
            f"Failed to insert charger for station {charging_station.id}: {e}"
        )
        return -1
    return inserted_id


def update(charging_station: ChargingStation, charger: Charger) -> bool:
    """
    Updates an existing charger in the database.

    Args:
        charging_station (ChargingStation): The charging station to which the charger belongs.
        charger (Charger): The charger object with updated values.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    query = """
    UPDATE chargers
    SET charging_station_id = ?, power_kw = ?
    WHERE id = ?
    """
    params = (charging_station.id, charger.power_kw, charger.id)
    db = DBBroker()
    try:
        db.execute_write_query(query, params)
    except Exception as e:
        _logger.error(f"Failed to update charger with ID {charger.id}: {e}")
        return False
    return True


def delete(charger: Charger) -> bool:
    """
    Deletes a charger from the database.

    Args:
        charger (Charger): The charger object to delete.

    Returns:
        bool: True if the deletion was successful and affected rows, False otherwise.
    """
    query = "DELETE FROM chargers WHERE id = ?"
    params = (charger.id,)
    db = DBBroker()
    try:
        n, _ = db.execute_write_query(query, params)
    except Exception as e:
        _logger.error(f"Failed to delete charger with ID {charger.id}: {e}")
        return False
    return n > 0


def read_by_id(charger_id: int) -> Optional[Charger]:
    """
    Reads a charger from the database by its ID.

    Args:
        charger_id (int): The ID of the charger to retrieve.

    Returns:
        Optional[Charger]: The retrieved Charger object, or None if not found or an error occurs.
    """
    db = DBBroker()
    try:
        rows = db.execute_read_query(
            "SELECT * FROM chargers WHERE id = ?", (charger_id,)
        )
        return _row_to_charger(rows[0]) if rows else None
    except Exception as e:
        _logger.error(f"Failed to read charger with ID {charger_id}: {e}")
        return None


def read_by_station(charging_station: ChargingStation) -> list[Charger]:
    """
    Reads all chargers for a specific charging station.

    Args:
        charging_station (ChargingStation): The charging station object.

    Returns:
        list[Charger]: A list of chargers belonging to the station.
    """
    db = DBBroker()
    try:
        rows = db.execute_read_query(
            "SELECT * FROM chargers WHERE charging_station_id = ?",
            (charging_station.id,),
        )
        return [_row_to_charger(row) for row in rows] if rows else []
    except Exception as e:
        _logger.error(f"Failed to read chargers for station {charging_station.id}: {e}")
        return []


def read_by_station_id(station_id: int) -> list[Charger]:
    """
    Reads all chargers for a specific charging station by its ID.

    Args:
        station_id (int): The ID of the charging station.

    Returns:
        list[Charger]: A list of chargers belonging to the station.
    """
    db = DBBroker()
    try:
        rows = db.execute_read_query(
            "SELECT * FROM chargers WHERE charging_station_id = ?",
            (station_id,),
        )
        return [_row_to_charger(row) for row in rows] if rows else []
    except Exception as e:
        _logger.error(f"Failed to read chargers for station ID {station_id}: {e}")
        return []


def _row_to_charger(row: dict) -> Charger:
    """
    Converts a database row into a Charger object.

    Args:
        row (dict): A dictionary representing a row from the database.

    Returns:
        Charger: The instantiated Charger object.
    """
    return Charger(
        id=row["id"], power_kw=row["power_kw"]
    )

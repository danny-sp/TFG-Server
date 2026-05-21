"""
DAO for charging_station entity.
"""

from typing import Optional

import src.Domain.chargerDAO as ChargerDAO
from src.Domain.charging_station import ChargingStation
from src.Persistence.db_broker import DBBroker
from src.Utils.logger import setup_logger

_logger = setup_logger("ChargingStationDAO")


def insert(charging_station: ChargingStation) -> int:
    """
    Inserts a new charging station into the database.

    Args:
        charging_station (ChargingStation): The charging station object to insert.

    Returns:
        int: The ID of the newly inserted charging station, or -1 if the insertion fails.
    """
    query = """
    INSERT INTO charging_stations (station_name, operator, location)
    VALUES (?, ?, ST_GeomFromText(?))
    """
    params = (
        charging_station.name,
        charging_station.operator,
        f"POINT({charging_station.location[1]} {charging_station.location[0]})",
    )
    db = DBBroker()
    try:
        _, inserted_id = db.execute_write_query(query, params)
    except Exception as e:
        _logger.error(f"Failed to insert charging_station {charging_station.name}: {e}")
        return -1
    return inserted_id


def update(charging_station: ChargingStation) -> bool:
    """
    Updates an existing charging station in the database.

    Args:
        charging_station (ChargingStation): The charging station object with updated values.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    query = """
    UPDATE charging_stations
    SET station_name = ?, operator = ?, location = ST_GeomFromText(?)
    WHERE id = ?
    """
    params = (
        charging_station.name,
        charging_station.operator,
        f"POINT({charging_station.location[1]} {charging_station.location[0]})",
        charging_station.id,
    )
    db = DBBroker()
    try:
        db.execute_write_query(query, params)
    except Exception as e:
        _logger.error(
            f"Failed to update charging_station with ID {charging_station.id}: {e}"
        )
        return False
    return True


def delete(charging_station: ChargingStation) -> bool:
    """
    Deletes a charging station from the database.

    Args:
        charging_station (ChargingStation): The charging station object to delete.

    Returns:
        bool: True if the deletion was successful and affected rows, False otherwise.
    """
    query = "DELETE FROM charging_stations WHERE id = ?"
    params = (charging_station.id,)
    db = DBBroker()
    try:
        n, _ = db.execute_write_query(query, params)
    except Exception as e:
        _logger.error(
            f"Failed to delete charging_station with ID {charging_station.id}: {e}"
        )
        return False
    return n > 0


def read_stations_in_area(
    min_lat: float, max_lat: float, min_lon: float, max_lon: float
) -> list[ChargingStation]:
    """
    Reads charging stations within a specific geographic bounding box.

    Args:
        min_lat (float): Minimum latitude of the bounding box.
        max_lat (float): Maximum latitude of the bounding box.
        min_lon (float): Minimum longitude of the bounding box.
        max_lon (float): Maximum longitude of the bounding box.

    Returns:
        list[ChargingStation]: A list of charging stations in the specified area.
    """
    polygon_wkt = f"POLYGON(({min_lon} {min_lat}, {max_lon} {min_lat}, {max_lon} {max_lat}, {min_lon} {max_lat}, {min_lon} {min_lat}))"

    query = """
        SELECT cs.id, cs.station_name, o.operator_name as operator, 
                ST_Y(cs.location) as latitude, 
                ST_X(cs.location) as longitude
        FROM charging_stations cs, operators o
        WHERE o.id = cs.operator_id AND MBRContains(
            ST_GeomFromText(?),
            cs.location
        )
        """

    params = (polygon_wkt,)
    db = DBBroker()
    try:
        rows = db.execute_read_query(query, params)
        return [_row_to_charging_station(row) for row in rows]
    except Exception as e:
        _logger.error(f"Failed to read charging_stations in area: {e}")
        return []


def read_by_id(station_id: int) -> Optional[ChargingStation]:
    """
    Reads a charging station by its ID.

    Args:
        station_id (int): The ID of the charging station to read.

    Returns:
        Optional[ChargingStation]: The ChargingStation object if found, otherwise None.
    """

    query = """
    SELECT cs.id, cs.station_name, o.operator_name as operator, 
            ST_Y(cs.location) as latitude, 
            ST_X(cs.location) as longitude
    FROM charging_stations cs, operators o
    WHERE o.id = cs.operator_id AND cs.id = ?
    """
    db = DBBroker()
    try:
        rows = db.execute_read_query(query, (station_id,))
        return _row_to_charging_station(rows[0]) if rows else None
    except Exception as e:
        _logger.error(f"Failed to read charging_station with ID {station_id}: {e}")
        return None


def _row_to_charging_station(row) -> ChargingStation:
    """
    Converts a database row into a ChargingStation object.

    Args:
        row: A row from the database containing charging station info.

    Returns:
        ChargingStation: The instantiated ChargingStation object.
    """
    return ChargingStation(
        id=row["id"],
        name=row["station_name"],
        operator=row["operator"],
        location=(row["latitude"], row["longitude"]),
        chargers=ChargerDAO.read_by_station_id(row["id"]),
    )

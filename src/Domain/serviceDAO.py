"""
DAO for service entity.
"""

from typing import Optional

from src.Domain.service import Service
from src.Persistance.db_broker import DBBroker
from src.Utils.constants import ServiceType
from src.Utils.logger import setup_logger

_logger = setup_logger("ServiceDAO")


def insert(service: Service) -> int:
    """
    Inserts a new service into the database.

    Args:
        service (Service): The service object to insert.

    Returns:
        int: The ID of the newly inserted service, or -1 if the insertion fails.
    """
    query = """
    INSERT INTO services (service_name, service_type, location)
    VALUES (?, ?, ST_GeomFromText(?))
    """
    params = (
        service.name,
        service.type.value,
        service.location,
    )
    db = DBBroker()
    try:
        _, inserted_id = db.execute_write_query(query, params)
    except Exception as e:
        _logger.error(f"Failed to insert service: {e}")
        return -1
    return inserted_id


def update(service: Service) -> bool:
    """
    Updates an existing service in the database.

    Args:
        service (Service): The service object with updated values.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    query = """
    UPDATE services
    SET service_name = ?, service_type = ?, location = ?
    WHERE id = ?
    """
    params = (
        service.name,
        service.type.value,
        service.location,
        service.id,
    )
    db = DBBroker()
    try:
        db.execute_write_query(query, params)
    except Exception as e:
        _logger.error(f"Failed to update service with ID {service.id}: {e}")
        return False
    return True


def delete(service: Service) -> bool:
    """
    Deletes a service from the database.

    Args:
        service (Service): The service object to delete.

    Returns:
        bool: True if the deletion was successful and affected rows, False otherwise.
    """
    query = "DELETE FROM services WHERE id = ?"
    params = (service.id,)
    db = DBBroker()
    try:
        n, _ = db.execute_write_query(query, params)
    except Exception as e:
        _logger.error(f"Failed to delete service with ID {service.id}: {e}")
        return False
    return n > 0


def read_by_id(id: int) -> Optional[Service]:
    """
    Reads a service from the database by its ID.

    Args:
        id (int): The ID of the service to retrieve.

    Returns:
        Optional[Service]: The retrieved Service object, or None if not found or an error occurs.
    """
    db = DBBroker()
    try:
        rows = db.execute_read_query("SELECT * FROM services WHERE id = ?", (id,))
        return _row_to_service(rows[0]) if rows else None
    except Exception as e:
        _logger.error(f"Failed to read service with ID {id}: {e}")
        return None


def read_near_point(
    location: tuple[float, float], max_distance: float = 200
) -> list[Service]:
    """
    Reads services located within a certain distance from a given point.

    Args:
        location (tuple[float, float]): The central point (latitude, longitude).
        max_distance (float): The maximum distance in meters.

    Returns:
        list[Service]: A list of Services near the given point.
    """
    station_location = f"POINT({location[1]} {location[0]})"
    query = """
    SELECT s.id, s.service_name, s.service_type,
            ST_Y(s.location) as latitude,
            ST_X(s.location) as longitude
    FROM services s
    WHERE ST_Distance_Sphere(ST_GeomFromText(?), s.location) < ?
    """

    params = (station_location, max_distance)
    db = DBBroker()
    try:
        rows = db.execute_read_query(query, params)
        return [_row_to_service(row) for row in rows]
    except Exception as e:
        _logger.error(f"Failed to read services near point {location}: {e}")
        return []


def _row_to_service(row: dict) -> Service:
    """
    Converts a database row into a Service object.

    Args:
        row (dict): A dictionary representing a row from the database.

    Returns:
        Service: The instantiated Service object.
    """
    return Service(
        id=row["id"],
        name=row["service_name"],
        type=ServiceType(row["service_type"]),
        location=(row["latitude"], row["longitude"]),
    )

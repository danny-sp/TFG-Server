"""
DAO for vehicle entity.
"""

from typing import Optional

from src.Domain.ev_user import EVUser
from src.Domain.vehicle import Vehicle
from src.Persistence.db_broker import DBBroker
from src.Utils.logger import setup_logger

_logger = setup_logger("VehicleDAO")


def insert(vehicle: Vehicle, user: EVUser) -> int:
    """
    Inserts a new vehicle into the database.

    Args:
        vehicle (Vehicle): The vehicle object to insert.
        user (EVUser): The user to whom the vehicle belongs.

    Returns:
        int: The ID of the newly inserted vehicle, or -1 if the insertion fails.
    """
    query = """
    INSERT INTO vehicles (plate, consumption_wh_km, capacity_kwh, max_kw_speed, user_id, registration_date)
    VALUES (?, ?, ?, ?, ?)
    """
    params = (
        vehicle.plate,
        vehicle.consumption_wh_km,
        vehicle.capacity_kwh,
        vehicle.max_kw_speed,
        user.id,
        vehicle.reg_date,
    )
    db = DBBroker()
    try:
        _, inserted_id = db.execute_write_query(query, params)
    except Exception as e:
        _logger.error(f"Failed to insert vehicle with plate {vehicle.plate}: {e}")
        return -1
    return inserted_id


def update(vehicle: Vehicle, user: EVUser) -> bool:
    """
    Updates an existing vehicle in the database.

    Args:
        vehicle (Vehicle): The vehicle object with updated values.
        user (EVUser): The user to whom the vehicle belongs.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    query = """
    UPDATE vehicles
    SET consumption_wh_km = ?, capacity_kwh = ?, max_kw_speed = ?, user_id = ?, registration_date = ?
    WHERE plate = ?
    """
    params = (
        vehicle.consumption_wh_km,
        vehicle.capacity_kwh,
        vehicle.max_kw_speed,
        user.id,
        vehicle.reg_date,
        vehicle.plate,
    )
    db = DBBroker()
    try:
        db.execute_write_query(query, params)
    except Exception as e:
        _logger.error(f"Failed to update vehicle with plate {vehicle.plate}: {e}")
        return False
    return True


def delete(vehicle: Vehicle) -> bool:
    """
    Deletes a vehicle from the database based on its plate.

    Args:
        vehicle (Vehicle): The vehicle object to delete.

    Returns:
        bool: True if the deletion was successful and affected rows, False otherwise.
    """
    query = "DELETE FROM vehicles WHERE plate = ?"
    params = (vehicle.plate,)
    db = DBBroker()
    try:
        n, _ = db.execute_write_query(query, params)
    except Exception as e:
        _logger.error(f"Failed to delete vehicle with plate {vehicle.plate}: {e}")
        return False
    return n > 0


def read_by_plate(plate: str) -> Optional[Vehicle]:
    """
    Reads a vehicle from the database by its license plate.

    Args:
        plate (str): The license plate of the vehicle.

    Returns:
        Optional[Vehicle]: The retrieved Vehicle object, or None if not found or an error occurs.
    """
    db = DBBroker()
    try:
        rows = db.execute_read_query("SELECT * FROM vehicles WHERE plate = ?", (plate,))
        return _row_to_vehicle(rows[0]) if rows else None
    except Exception as e:
        _logger.error(f"Failed to read vehicle with plate {plate}: {e}")
        return None


def read_by_user_id(user: EVUser) -> list[Vehicle]:
    """
    Reads all vehicles associated with a specific user.

    Args:
        user (EVUser): The user whose vehicles are to be read.

    Returns:
        list[Vehicle]: A list of vehicles belonging to the user.
    """
    db = DBBroker()
    try:
        rows = db.execute_read_query(
            "SELECT * FROM vehicles WHERE user_id = ?", (user.id,)
        )
        return [_row_to_vehicle(row) for row in rows] if rows else []
    except Exception as e:
        _logger.error(f"Failed to read vehicles for user ID {user.id}: {e}")
        return []


def _row_to_vehicle(row: dict) -> Vehicle:
    return Vehicle(
        plate=row["plate"],
        consumption_wh_km=row["consumption_wh_km"],
        capacity_kwh=row["capacity_kwh"],
        max_kw_speed=row["max_kw_speed"],
        reg_date=row["registration_date"],
    )

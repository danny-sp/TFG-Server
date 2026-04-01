"""
DAO for booking entity.
"""

from typing import Optional

from src.Domain.booking import Booking
from src.Persistance.db_broker import DBBroker
from src.Utils.constants import BookingStatus
from src.Utils.logger import setup_logger

_logger = setup_logger("BookingDAO")


def insert(booking: Booking) -> int:
    """
    Inserts a new booking into the database.

    Args:
        booking (Booking): The booking object to insert.

    Returns:
        int: The ID of the newly inserted booking, or -1 if insertion fails.
    """
    query = """
    INSERT INTO bookings (vehicle_plate, booking_date, start_date, end_date, status, price)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    params = (
        booking.vehicle.plate,
        booking.booking_date,
        booking.start_date,
        booking.end_date,
        booking.status.value,
        booking.price,
    )
    db = DBBroker()
    try:
        _, inserted_id = db.execute_write_query(query, params)
    except Exception as e:
        _logger.error(
            f"Failed to insert booking for vehicle {booking.vehicle.plate}: {e}"
        )
        return -1
    return inserted_id


def update(booking: Booking) -> bool:
    """
    Updates an existing booking in the database.

    Args:
        booking (Booking): The booking object with updated values.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    query = """
    UPDATE bookings
    SET vehicle_plate = ?, booking_date = ?, start_date = ?, end_date = ?, status = ?, price = ?
    WHERE id = ?
    """
    params = (
        booking.vehicle.plate,
        booking.booking_date,
        booking.start_date,
        booking.end_date,
        booking.status.value,
        booking.price,
        booking.id,
    )
    db = DBBroker()
    try:
        db.execute_write_query(query, params)
    except Exception as e:
        _logger.error(f"Failed to update booking with ID {booking.id}: {e}")
        return False
    return True


def delete(booking: Booking) -> bool:
    """
    Deletes a booking from the database.

    Args:
        booking (Booking): The booking object to delete.

    Returns:
        bool: True if the deletion was successful and affected rows, False otherwise.
    """
    query = "DELETE FROM bookings WHERE id = ?"
    params = (booking.id,)
    db = DBBroker()
    try:
        n, _ = db.execute_write_query(query, params)
    except Exception as e:
        _logger.error(f"Failed to delete booking with ID {booking.id}: {e}")
        return False
    return n > 0


def read_by_id(booking_id: int) -> Optional[Booking]:
    """
    Reads a booking from the database by its ID.

    Args:
        booking_id (int): The ID of the booking to retrieve.

    Returns:
        Optional[Booking]: The retrieved Booking object, or None if not found or an error occurs.
    """
    db = DBBroker()
    try:
        rows = db.execute_read_query(
            "SELECT * FROM bookings WHERE id = ?", (booking_id,)
        )
        return _row_to_booking(rows[0]) if rows else None
    except Exception as e:
        _logger.error(f"Failed to read booking with ID {booking_id}: {e}")
        return None


def read_active_by_vehicle_plate(plate: str) -> Optional[Booking]:
    """
    Reads the most recent active booking for a given vehicle plate.

    Args:
        plate (str): The license plate of the vehicle.

    Returns:
        Optional[Booking]: The active Booking object, or None if no active booking is found.
    """
    query = """
    SELECT * FROM bookings 
    WHERE vehicle_plate = ? AND status = ?
    ORDER BY booking_date DESC
    LIMIT 1
    """
    params = (plate, BookingStatus.SCHEDULED.value)
    db = DBBroker()
    try:
        rows = db.execute_read_query(query, params)
        return _row_to_booking(rows[0]) if rows else None
    except Exception as e:
        _logger.error(f"Failed to read active booking for vehicle {plate}: {e}")
        return None


def _row_to_booking(row: dict) -> Booking:
    """
    Converts a database row into a Booking object.

    Args:
        row (dict): A dictionary representing a row from the database.

    Returns:
        Booking: The instantiated Booking object.
    """
    return Booking(
        id=row["id"],
        vehicle=vehicle,
        booking_date=row["booking_date"],
        start_date=row["start_date"],
        end_date=row["end_date"],
        status=BookingStatus(row["status"]),
        price=row["price"],
    )

"""
DAO for charging_session entity.
"""

from typing import Optional

from src.Domain.charging_session import ChargingSession
from src.Persistance.db_broker import DBBroker
from src.Utils.logger import setup_logger

_logger = setup_logger("ChargingSessionDAO")


def insert(charging_session: ChargingSession) -> int:
    """
    Inserts a new charging session into the database.

    Args:
        charging_session (ChargingSession): The charging session object to insert.

    Returns:
        int: The ID of the newly inserted charging session, or -1 if the insertion fails.
    """
    query = """
    INSERT INTO charging_sessions (booking_id, charger_id, start_date, end_date, energy_delivered_kwh, total_cost)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    params = (
        charging_session.booking.id,
        charging_session.charger.id,
        charging_session.start_date,
        charging_session.end_date,
        charging_session.energy_delivered_kwh,
        charging_session.total_cost,
    )
    db = DBBroker()
    try:
        _, inserted_id = db.execute_write_query(query, params)
    except Exception as e:
        _logger.error(
            f"Failed to insert charging_session for booking {charging_session.booking.id}: {e}"
        )
        return -1
    return inserted_id


def update(charging_session: ChargingSession) -> bool:
    """
    Updates an existing charging session in the database.

    Args:
        charging_session (ChargingSession): The charging session object with updated values.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    query = """
    UPDATE charging_sessions
    SET booking_id = ?, charger_id = ?, start_date = ?, end_date = ?, energy_delivered_kwh = ?, total_cost = ?
    WHERE id = ?
    """
    params = (
        charging_session.booking.id,
        charging_session.charger.id,
        charging_session.start_date,
        charging_session.end_date,
        charging_session.energy_delivered_kwh,
        charging_session.total_cost,
        charging_session.id,
    )
    db = DBBroker()
    try:
        db.execute_write_query(query, params)
    except Exception as e:
        _logger.error(
            f"Failed to update charging_session with ID {charging_session.id}: {e}"
        )
        return False
    return True


def delete(charging_session: ChargingSession) -> bool:
    """
    Deletes a charging session from the database.

    Args:
        charging_session (ChargingSession): The charging session object to delete.

    Returns:
        bool: True if the deletion was successful and affected rows, False otherwise.
    """
    query = "DELETE FROM charging_sessions WHERE id = ?"
    params = (charging_session.id,)
    db = DBBroker()
    try:
        n, _ = db.execute_write_query(query, params)
    except Exception as e:
        _logger.error(
            f"Failed to delete charging_session with ID {charging_session.id}: {e}"
        )
        return False
    return n > 0


def read_by_id(session_id: int) -> Optional[ChargingSession]:
    """
    Reads a charging session from the database by its ID.

    Args:
        session_id (int): The ID of the charging session to retrieve.

    Returns:
        Optional[ChargingSession]: The retrieved ChargingSession object, or None if not found or an error occurs.
    """
    db = DBBroker()
    try:
        rows = db.execute_read_query(
            "SELECT * FROM charging_sessions WHERE id = ?", (session_id,)
        )
        return _row_to_charging_session(rows[0]) if rows else None
    except Exception as e:
        _logger.error(f"Failed to read charging_session with ID {session_id}: {e}")
        return None


def _row_to_charging_session(row: dict) -> ChargingSession:
    """
    Converts a database row into a ChargingSession object.

    Args:
        row (dict): A dictionary representing a row from the database.

    Returns:
        ChargingSession: The instantiated ChargingSession object.
    """
    pass
    # bookingDAO = BookingDAO()
    # booking = bookingDAO.read_by_id(row['booking_id'])

    # chargerDAO = ChargerDAO()
    # charger = chargerDAO.read_by_id(row['charger_id'])
    # return ChargingSession(
    #     session_id=row["id"],
    #     booking=booking,
    #     charger=charger,
    #     start_date=row["start_date"],
    #     end_date=row["end_date"],
    #     energy_delivered_kwh=row["energy_delivered_kwh"],
    #     total_cost=row["total_cost"],
    # )

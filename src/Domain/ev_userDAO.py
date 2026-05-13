"""
DAO for EVUser entity.
"""

from typing import Optional

from src.Domain.ev_user import EVUser
from src.Persistance.db_broker import DBBroker
from src.Utils.logger import setup_logger

_logger = setup_logger("EVUserDAO")


def insert(ev_user: EVUser) -> int:
    """
    Inserts a new EV user into the database.

    Args:
        ev_user (EVUser): The EV user object to insert.

    Returns:
        int: The ID of the newly inserted user, or -1 if the insertion fails.
    """
    query = """
    INSERT INTO ev_users (username, email, phone, active_user, registration_date)
    VALUES (?, ?, ?, ?, ?)
    """
    params = (
        ev_user.username,
        ev_user.email,
        ev_user.phone,
        ev_user.active,
        ev_user.registration_date,
    )
    db = DBBroker()
    try:
        _, inserted_id = db.execute_write_query(query, params)
    except Exception as e:
        _logger.error(f"Failed to insert ev_user {ev_user.username}: {e}")
        return -1
    return inserted_id


def update(ev_user: EVUser) -> bool:
    """
    Updates an existing EV user in the database.

    Args:
        ev_user (EVUser): The EV user object with updated values.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    query = """
    UPDATE ev_users
    SET username = ?, email = ?, phone = ?, active_user = ?, registration_date = ?
    WHERE id = ?
    """
    params = (
        ev_user.username,
        ev_user.email,
        ev_user.phone,
        ev_user.active,
        ev_user.registration_date,
        ev_user.id,
    )
    db = DBBroker()
    try:
        db.execute_write_query(query, params)
    except Exception as e:
        _logger.error(f"Failed to update ev_user with ID {ev_user.id}: {e}")
        return False
    return True


def delete(ev_user: EVUser) -> bool:
    """
    Deletes an EV user from the database.

    Args:
        ev_user (EVUser): The EV user object to delete.

    Returns:
        bool: True if the deletion was successful and affected rows, False otherwise.
    """
    query = "DELETE FROM ev_users WHERE id = ?"
    params = (ev_user.id,)
    db = DBBroker()
    try:
        n, _ = db.execute_write_query(query, params)
    except Exception as e:
        _logger.error(f"Failed to delete ev_user with ID {ev_user.id}: {e}")
        return False
    return n > 0


def read_by_id(user_id: int) -> Optional[EVUser]:
    """
    Reads an EV user from the database by its ID.

    Args:
        user_id (int): The ID of the EV user to retrieve.

    Returns:
        Optional[EVUser]: The retrieved EVUser object, or None if not found or an error occurs.
    """
    db = DBBroker()
    try:
        rows = db.execute_read_query("SELECT * FROM ev_users WHERE id = ?", (user_id,))
        return _row_to_ev_user(rows[0]) if rows else None
    except Exception as e:
        _logger.error(f"Failed to read ev_user with ID {user_id}: {e}")
        return None

def read_by_plate(plate: str) -> Optional[EVUser]:
    """
    Reads an EV user from the database by the license plate of their vehicle.

    Args:
        plate (str): The license plate of the vehicle associated with the EV user.

    Returns:
        Optional[EVUser]: The retrieved EVUser object, or None if not found or an error occurs.
    """
    db = DBBroker()
    try:
        rows = db.execute_read_query(
            """
            SELECT ev_users.*
            FROM ev_users, vehicles
            WHERE vehicles.plate = ? AND ev_users.id = vehicles.user_id
            """,
            (plate,),
        )
        return _row_to_ev_user(rows[0]) if rows else None
    except Exception as e:
        _logger.error(f"Failed to read ev_user with vehicle plate {plate}: {e}")
        return None

def _row_to_ev_user(row: dict) -> EVUser:
    """
    Converts a database row into an EVUser object.

    Args:
        row (dict): A dictionary representing a row from the database.

    Returns:
        EVUser: The instantiated EVUser object.
    """
    return EVUser(
        id=row["id"],
        username=row["username"],
        email=row["email"],
        phone=row["phone"],
        active=bool(row["active_user"]),
        registration_date=row["registration_date"],
        value_time=row["value_of_time"]
    )

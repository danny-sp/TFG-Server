from typing import Optional

from src.Domain.booking import Booking

from src.Persistance.db_broker import DBBroker

from src.Utils.constants import BookingStatus

def insert(booking: Booking) -> int:
    query = """
    INSERT INTO bookings (vehicle_plate, booking_date, start_date, end_date, price_rate_id, status, price)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    params = (
        booking.vehicle.plate,
        booking.booking_date,
        booking.start_date,
        booking.end_date,
        booking.price_rate.id,
        booking.status.value,
        booking.price,
    )
    db = DBBroker()
    _, inserted_id = db.execute_write_query(query, params)
    return inserted_id

def update(booking: Booking) -> None:
    query = """
    UPDATE bookings
    SET vehicle_plate = ?, booking_date = ?, start_date = ?, end_date = ?, price_rate_id = ?, status = ?, price = ?
    WHERE id = ?
    """
    params = (
        booking.vehicle.plate,
        booking.booking_date,
        booking.start_date,
        booking.end_date,
        booking.price_rate.id,
        booking.status.value,
        booking.price,
        booking.id
    )
    db = DBBroker()
    return db.execute_write_query(query, params)

def delete(booking: Booking) -> None:
    query = "DELETE FROM bookings WHERE id = ?"
    params = (booking.id,)
    db = DBBroker()
    return db.execute_write_query(query, params)

def read_by_id(booking_id: int) -> Optional[Booking]:
    db = DBBroker()
    rows = db.execute_read_query("SELECT * FROM bookings WHERE id = ?", (booking_id,))
    return _row_to_booking(rows[0]) if rows else None

def read_active_by_vehicle_plate(plate: str) -> Optional[Booking]:
    query = """
    SELECT * FROM bookings 
    WHERE vehicle_plate = ? AND status = ?
    ORDER BY booking_date DESC
    LIMIT 1
    """
    params = (plate, BookingStatus.SCHEDULED.value)
    db = DBBroker()
    rows = db.execute_read_query(query, params)
    return _row_to_booking(rows[0]) if rows else None

def _row_to_booking(row: dict) -> Booking:
    return Booking(
        id=row['id'],
        vehicle=vehicle,
        booking_date=row['booking_date'],
        start_date=row['start_date'],
        end_date=row['end_date'],
        price_rate=price_rate,
        status=BookingStatus(row['status']),
        price=row['price']
    )

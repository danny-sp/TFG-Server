# from src.Domain.ev_userDAO import EVUserDAO

from src.Domain.ev_user import EVUser
from src.Domain.vehicle import Vehicle

from src.Persistance.db_broker import DBBroker

def insert(vehicle: Vehicle) -> int:
    query = """
    INSERT INTO vehicles (plate, capacity_kwh, max_kw_speed, user_id, registration_date)
    VALUES (?, ?, ?, ?, ?)
    """
    params = (
        vehicle.plate,
        vehicle.capacity_kwh,
        vehicle.max_kw_speed,
        vehicle.user.id,
        vehicle.reg_date
    )
    db = DBBroker()
    _, inserted_id = db.execute_write_query(query, params)
    return inserted_id

def update(vehicle: Vehicle) -> None:
    query = """
    UPDATE vehicles
    SET capacity_kwh = ?, max_kw_speed = ?, user_id = ?, registration_date = ?
    WHERE plate = ?
    """
    params = (
        vehicle.capacity_kwh,
        vehicle.max_kw_speed,
        vehicle.user.id,
        vehicle.reg_date,
        vehicle.plate
    )
    db = DBBroker()
    return db.execute_write_query(query, params)

def delete(vehicle: Vehicle) -> None:
    query = "DELETE FROM vehicles WHERE plate = ?"
    params = (vehicle.plate,)
    db = DBBroker()
    return db.execute_write_query(query, params)

def read_by_plate(plate: str) -> Vehicle:
    db = DBBroker()
    rows = db.execute_read_query("SELECT * FROM vehicles WHERE plate = ?", (plate,))
    return _row_to_vehicle(rows[0]) if rows else None

def read_by_user_id(user: EVUser) -> list[Vehicle]:
    db = DBBroker()
    rows = db.execute_read_query("SELECT * FROM vehicles WHERE user_id = ?", (user.id,))
    return [_row_to_vehicle(row, user) for row in rows] if rows else []

def _row_to_vehicle(row: dict) -> Vehicle:
    return Vehicle(
        plate=row['plate'],
        consumption_wh_km=row['consumption_wh_km'],
        capacity_kwh=row['capacity_kwh'],
        max_kw_speed=row['max_kw_speed'],
        reg_date=row['registration_date']
    )

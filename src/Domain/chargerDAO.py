from datetime import datetime, timedelta

from src.Domain.charger import Charger
from src.Domain.charging_station import ChargingStation

from src.Persistance.db_broker import DBBroker

def insert(charging_station: ChargingStation, charger: Charger) -> int:
    query = """
    INSERT INTO chargers (charging_station_id, power_kw, charger_active)
    VALUES (?, ?, ?)
    """
    params = (
        charging_station.id,
        charger.power_kw,
        charger.busy,
    )
    db = DBBroker()
    _, inserted_id = db.execute_write_query(query, params)
    return inserted_id

def update(charging_station: ChargingStation, charger: Charger) -> None:
    query = """
    UPDATE chargers
    SET charging_station_id = ?, power_kw = ?, charger_busy = ?
    WHERE id = ?
    """
    params = (
        charging_station.id,
        charger.power_kw,
        charger.busy,
        charger.id
    )
    db = DBBroker()
    return db.execute_write_query(query, params)

def delete(charger: Charger) -> None:
    query = "DELETE FROM chargers WHERE id = ?"
    params = (charger.id,)
    db = DBBroker()
    return db.execute_write_query(query, params)

def read_by_id(charger_id: int) -> Charger:
    db = DBBroker()
    rows = db.execute_read_query("SELECT * FROM chargers WHERE id = ?", (charger_id,))
    return _row_to_charger(rows[0]) if rows else None

def read_by_station(charging_station: ChargingStation) -> list[Charger]:
    db = DBBroker()
    rows = db.execute_read_query("SELECT * FROM chargers WHERE charging_station_id = ?", (charging_station.id,))
    return [_row_to_charger(row) for row in rows] if rows else []

def read_available_by_station(charging_station: ChargingStation, start_time: datetime, end_time: datetime) -> list[Charger]:
    db = DBBroker()

    query = """
        SELECT c.* FROM chargers c
        WHERE c.charging_station_id = ?
          AND c.charger_busy = 0
          AND NOT EXISTS (
              SELECT 1 
              FROM bookings b 
              WHERE b.charger_id = c.id
                AND b.status != 'cancelled'
                AND b.start_date < ?
                AND b.end_date > ?
          )
    """

    params = (charging_station.id, end_time, start_time)

    rows = db.execute_read_query(query, params)

    return [_row_to_charger(row) for row in rows] if rows else []

def _row_to_charger(row: dict) -> Charger:
    return Charger(
        id=row['id'],
        power_kw=row['power_kw'],
        busy=bool(row['charger_busy'])
    )

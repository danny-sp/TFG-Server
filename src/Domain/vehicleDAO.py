# from src.Domain.ev_userDAO import EVUserDAO

from src.Domain.ev_user import EVUser
from src.Domain.vehicle import Vehicle

from src.Persistance.db_broker import DBBroker

class VehicleDAO:
    def __init__(self):
        self._db = DBBroker()

    def insert(self, vehicle: Vehicle) -> int:
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
        _, inserted_id = self._db.execute_write_query(query, params)
        return inserted_id

    def update(self, vehicle: Vehicle) -> None:
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
        return self._db.execute_write_query(query, params)

    def delete(self, vehicle: Vehicle) -> None:
        query = "DELETE FROM vehicles WHERE plate = ?"
        params = (vehicle.plate,)
        return self._db.execute_write_query(query, params)

    def read_by_plate(self, plate: str) -> Vehicle:
        rows = self._db.execute_read_query("SELECT * FROM vehicles WHERE plate = ?", (plate,))
        return self._row_to_vehicle(rows[0]) if rows else None

    def read_by_user_id(self, user: EVUser) -> list[Vehicle]:
        rows = self._db.execute_read_query("SELECT * FROM vehicles WHERE user_id = ?", (user.id,))
        return [self._row_to_vehicle(row, user) for row in rows] if rows else []

    def _row_to_vehicle(self, row: dict) -> Vehicle:
        return Vehicle(
            plate=row['plate'],
            consumption_wh_km=row['consumption_wh_km'],
            capacity_kwh=row['capacity_kwh'],
            max_kw_speed=row['max_kw_speed'],
            reg_date=row['registration_date']
        )

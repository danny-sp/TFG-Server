# from src.Domain.charging_stationDAO import ChargingStationDAO

from src.Domain.charging_station import ChargingStation
from src.Domain.service import Service

from src.Persistance.db_broker import DBBroker

from src.Utils.constants import ServiceType

class ServiceDAO:
    def __init__(self):
        self._db = DBBroker()

    def insert(self, service: Service) -> int:
        query = """
        INSERT INTO services (charging_station_id, service_name, service_type, open_time, close_time)
        VALUES (?, ?, ?, ?, ?)
        """
        params = (
            service.charging_station.id,
            service.name,
            service.type.value,
            service.open_time,
            service.close_time
        )
        _, inserted_id = self._db.execute_write_query(query, params)
        return inserted_id

    def update(self, service: Service) -> None:
        query = """
        UPDATE services
        SET charging_station_id = ?, service_name = ?, service_type = ?, open_time = ?, close_time = ?
        WHERE id = ?
        """
        params = (
            service.charging_station.id,
            service.name,
            service.type.value,
            service.open_time,
            service.close_time,
            service.id
        )
        return self._db.execute_write_query(query, params)

    def delete(self, service: Service) -> None:
        query = "DELETE FROM services WHERE id = ?"
        params = (service.id,)
        return self._db.execute_write_query(query, params)

    def read_by_id(self, id: int) -> Service:
        rows = self._db.execute_read_query("SELECT * FROM services WHERE id = ?", (id,))
        return self._row_to_service(rows[0]) if rows else None

    def read_near_point(self, location: tuple[float, float], max_distance: float = 200) -> list[Service]:
        station_location = f"POINT({location[1]} {location[0]})"
        query = """
        SELECT s.id, s.service_name, s.service_type,
                ST_Y(s.location) as latitude,
                ST_X(s.location) as longitude
        FROM services s
        WHERE ST_Distance(ST_GeomFromText(?), s.location) < ?
        """

        params = (station_location, max_distance)
        rows = self._db.execute_read_query(query, params)
        return [self._row_to_service(row) for row in rows]

    def _row_to_service(self, row: dict) -> Service:
        return Service(
            id=row['id'],
            name=row['service_name'],
            type=ServiceType(row['service_type']),
            location=(row['latitude'], row['longitude'])
        )

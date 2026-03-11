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

    def _row_to_service(self, row: dict, charging_station: ChargingStation = None) -> Service:
        # if charging_station is None:
        #     charging_stationDAO = ChargingStationDAO()
        #     charging_station = charging_stationDAO.read_by_id(row['charging_station_id'])

        return Service(
            id=row['id'],
            name=row['service_name'],
            type=ServiceType(row['service_type']),
            open_time=row['open_time'],
            close_time=row['close_time'],
            charging_station=charging_station
        )

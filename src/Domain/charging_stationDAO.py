
from src.Domain.charging_station import ChargingStation

from src.Persistance.db_broker import DBBroker

class ChargingStationDAO:
    def __init__(self):
        self._db = DBBroker()

    def insert(self, charging_station: ChargingStation) -> int:
        query = """
        INSERT INTO charging_stations (station_name, latitude, longitude, open_time, close_time)
        VALUES (?, ?, ?, ?, ?)
        """
        params = (
            charging_station.name,
            charging_station.latitude,
            charging_station.longitude,
            charging_station.open_time,
            charging_station.close_time
        )
        _, inserted_id = self._db.execute_write_query(query, params)
        return inserted_id

    def update(self, charging_station: ChargingStation) -> None:
        query = """
        UPDATE charging_stations
        SET station_name = ?, latitude = ?, longitude = ?, open_time = ?, close_time = ?
        WHERE id = ?
        """
        params = (
            charging_station.name,
            charging_station.latitude,
            charging_station.longitude,
            charging_station.open_time,
            charging_station.close_time,
            charging_station.id
        )
        return self._db.execute_write_query(query, params)

    def delete(self, charging_station: ChargingStation) -> None:
        query = "DELETE FROM charging_stations WHERE id = ?"
        params = (charging_station.id,)
        return self._db.execute_write_query(query, params)

    def read_by_id(self, station_id: int) -> ChargingStation:
        rows = self._db.execute_read_query("SELECT * FROM charging_stations WHERE id = ?", (station_id,))
        return self._row_to_charging_station(rows[0]) if rows else None

    def _row_to_charging_station(self, row) -> ChargingStation:
        return ChargingStation(
            id=row["id"],
            name=row["station_name"],
            latitude=row["latitude"],
            longitude=row["longitude"],
            open_time=row["open_time"],
            close_time=row["close_time"]
        )


from src.Domain.charger_typeDAO import ChargerTypeDAO
from src.Domain.charging_stationDAO import ChargingStationDAO

from src.Domain.charger import Charger
from src.Domain.charger_type import ChargerType
from src.Domain.charging_station import ChargingStation

from src.Persistance.db_broker import DBBroker

class ChargerDAO:
    def __init__(self):
        self._db = DBBroker()

    def insert(self, charger: Charger) -> int:
        query = """
        INSERT INTO chargers (charging_station_id, charger_type_id, charger_busy, charger_active)
        VALUES (?, ?, ?, ?)
        """
        params = (
            charger.charging_station.id,
            charger.type.id,
            charger.busy,
            charger.active
        )
        _, inserted_id = self._db.execute_write_query(query, params)
        return inserted_id

    def update(self, charger: Charger) -> None:
        query = """
        UPDATE chargers
        SET charging_station_id = ?, charger_type_id = ?, charger_busy = ?, charger_active = ?
        WHERE id = ?
        """
        params = (
            charger.charging_station.id,
            charger.type.id,
            charger.busy,
            charger.active,
            charger.id
        )
        return self._db.execute_write_query(query, params)

    def delete(self, charger: Charger) -> None:
        query = "DELETE FROM chargers WHERE id = ?"
        params = (charger.id,)
        return self._db.execute_write_query(query, params)

    def read_by_id(self, charger_id: int) -> Charger:
        rows = self._db.execute_read_query("SELECT * FROM chargers WHERE id = ?", (charger_id,))
        return self._row_to_charger(rows[0]) if rows else None

    def _row_to_charger(self, row: dict, charging_station: ChargingStation = None, charger_type: ChargerType = None) -> Charger:
        if charging_station is None:
            charging_stationDAO = ChargingStationDAO()
            charging_station = charging_stationDAO.read_by_id(row['charging_station_id'])
        if charger_type is None:
            charger_typeDAO = ChargerTypeDAO()
            charger_type = charger_typeDAO.read_by_id(row['charger_type_id'])

        return Charger(
            id=row['id'],
            type=charger_type,
            charging_station=charging_station,
            busy=bool(row['charger_busy']),
            active=bool(row['charger_active'])
        )

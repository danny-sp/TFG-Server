# from src.Domain.charger_typeDAO import ChargerTypeDAO
# from src.Domain.charging_stationDAO import ChargingStationDAO

from src.Domain.charger_type import ChargerType
from src.Domain.charging_station import ChargingStation
from src.Domain.price_rate import PriceRate

from src.Persistance.db_broker import DBBroker

class PriceRateDAO:
    def __init__(self):
        self._db = DBBroker()

    def insert(self, price_rate: PriceRate) -> int:
        query = """
        INSERT INTO price_rates (charging_station_id, charger_type_id, price_per_kwh, begin_date, end_date)
        VALUES (?, ?, ?, ?, ?)
        """
        params = (
            price_rate.charging_station.id,
            price_rate.charger_type.id,
            price_rate.price_per_kwh,
            price_rate.start_date,
            price_rate.end_date
        )
        _, inserted_id = self._db.execute_write_query(query, params)
        return inserted_id

    def update(self, price_rate: PriceRate) -> None:
        query = """
        UPDATE price_rates
        SET charging_station_id = ?, charger_type_id = ?, price_per_kwh = ?, begin_date = ?, end_date = ?
        WHERE id = ?
        """
        params = (
            price_rate.charging_station.id,
            price_rate.charger_type.id,
            price_rate.price_per_kwh,
            price_rate.start_date,
            price_rate.end_date,
            price_rate.id
        )
        return self._db.execute_write_query(query, params)

    def delete(self, price_rate: PriceRate) -> None:
        query = "DELETE FROM price_rates WHERE id = ?"
        params = (price_rate.id,)
        return self._db.execute_write_query(query, params)

    def read_by_id(self, id: int) -> PriceRate:
        rows = self._db.execute_read_query("SELECT * FROM price_rates WHERE id = ?", (id,))
        return self._row_to_price_rate(rows[0]) if rows else None

    def _row_to_price_rate(self, row: dict, charging_station: ChargingStation = None, charger_type: ChargerType = None) -> PriceRate:
        # if charging_station is None:
        #     charging_stationDAO = ChargingStationDAO()
        #     charging_station = charging_stationDAO.read_by_id(row['charging_station_id'])
        # if charger_type is None:
        #     charger_typeDAO = ChargerTypeDAO()
        #     charger_type = charger_typeDAO.read_by_id(row['charger_type_id'])

        return PriceRate(
            id=row['id'],
            charging_station=charging_station,
            charger_type=charger_type,
            start_date=row['begin_date'],
            end_date=row['end_date'],
            price_per_kwh=row['price_per_kwh']
        )

from datetime import datetime

from src.Domain.price_rateDAO import PriceRateDAO

from src.Domain.charger_type import ChargerType
from src.Domain.charging_station import ChargingStation

class PriceRate:
    def __init__(self, id: int, charging_station: ChargingStation, charger_type: ChargerType, start_date: datetime, end_date: datetime, price_per_kwh: float):
        self._id = id
        self._charging_station = charging_station
        self._charger_type = charger_type
        self._start_date = start_date
        self._end_date = end_date
        self._price_per_kwh = price_per_kwh

        self._price_rateDAO = PriceRateDAO()

    def insert(self):
        self._price_rateDAO.insert(self)

    def update(self):
        self._price_rateDAO.update(self)

    def delete(self):
        self._price_rateDAO.delete(self)

    ##############
    # PROPERTIES #
    ##############
    @property
    def id(self) -> int:
        return self._id

    @property
    def charging_station(self) -> ChargingStation:
        return self._charging_station

    @property
    def charger_type(self) -> ChargerType:
        return self._charger_type

    @property
    def start_date(self) -> datetime:
        return self._start_date

    @property
    def end_date(self) -> datetime:
        return self._end_date

    @property
    def price_per_kwh(self) -> float:
        return self._price_per_kwh

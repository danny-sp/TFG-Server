from datetime import time

from src.Domain.charger_type import ChargerType
from src.Domain.charging_station import ChargingStation

class PriceRate:
    def __init__(self, id: int, charging_station: ChargingStation, charger_type: ChargerType, start_hour: time, end_hour: time, price_per_kwh: float):
        self._id = id
        self._charging_station = charging_station
        self._charger_type = charger_type
        self._start_hour = start_hour
        self._end_hour = end_hour
        self._price_per_kwh = price_per_kwh

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
    def start_hour(self) -> time:
        return self._start_hour

    @property
    def end_hour(self) -> time:
        return self._end_hour

    @property
    def price_per_kwh(self) -> float:
        return self._price_per_kwh

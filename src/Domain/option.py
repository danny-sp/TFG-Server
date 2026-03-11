from datetime import datetime

from src.Domain.charging_station import ChargingStation
from src.Domain.price_rate import PriceRate
from src.Domain.charger_type import ChargerType

class Option:
    def __init__(self, request_id: int, charging_station: ChargingStation, price_rate: PriceRate, charger_type: ChargerType, start_time: datetime, end_time: datetime):
        self._request_id = request_id
        self._charging_station = charging_station
        self._price_rate = price_rate
        self._charger_type = charger_type
        self._start_time = start_time
        self._end_time = end_time
        self._duration_hours = (end_time - start_time).total_seconds() / 3600
        # self._price = self._duration_hours * self._price_rate.price_per_kwh
        self._price = 40.7


    def to_dict(self):
        return {
            "request_id": self._request_id,
            "charging_station": {
                "id": self._charging_station.id,
                "name": self._charging_station.name,
                "location": self._charging_station.location,
                "operator": self._charging_station.operator
            },
            "price_rate": {
                # "id": self._price_rate.id,
                # "price_per_kwh": self._price_rate.price_per_kwh
                "id": 1,
                "price_per_kwh": 0.20
            },
            "charger_type": {
                # "id": self._charger_type.id,
                # "name": self._charger_type.name
                "id": 1,
                "name": "Type 2"
            },
            "start_time": self._start_time.isoformat(),
            "end_time": self._end_time.isoformat(),
            "duration_hours": self._duration_hours,
            "price": self._price
        }

    ##############
    # PROPERTIES #
    ##############
    @property
    def request_id(self) -> int:
        return self._request_id

    @property
    def charging_station(self) -> ChargingStation:
        return self._charging_station

    @property
    def price_rate(self) -> PriceRate:
        return self._price_rate

    @property
    def charger_type(self) -> ChargerType:
        return self._charger_type

    @property
    def start_time(self) -> datetime:
        return self._start_time

    @property
    def end_time(self) -> datetime:
        return self._end_time

    @property
    def duration_hours(self) -> float:
        return self._duration_hours

    @property
    def price(self) -> float:
        return self._price

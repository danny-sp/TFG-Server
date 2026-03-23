from datetime import datetime, timedelta

from src.Domain.charging_station import ChargingStation
from src.Domain.price_rate import PriceRate
from src.Domain.service import Service

class Option:
    def __init__(self, request_id: int, charging_station: ChargingStation, price_rate: PriceRate, start_time: datetime, duration_hours: float, kw_speed: float, delay_hours: float=0.0, services_nearby: list[Service] = []):
        self._request_id = request_id
        self._charging_station = charging_station
        self._start_time = start_time
        self._end_time = start_time + timedelta(hours=duration_hours)
        self._duration_hours = duration_hours
        self._delay_hours = delay_hours
        # self._price = self._duration_hours * self._price_rate.price_per_kwh
        self._price = 40.7
        self._kw_speed = kw_speed
        self._services_nearby = services_nearby

    def to_dict(self):
        return {
            "request_id": self._request_id,
            "charging_station": {
                "id": self._charging_station.id,
                "name": self._charging_station.name,
                "location": self._charging_station.location,
                "operator": self._charging_station.operator
            },
            "price": float(self._price),
            "kw_speed": float(self._kw_speed),
            "start_time": self._start_time.isoformat(),
            "end_time": self._end_time.isoformat(),
            "duration_hours": float(self._duration_hours),
            "delay_hours": float(self._delay_hours),
            "services_nearby": list(set(service.type for service in self._services_nearby))
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
    def price(self) -> float:
        return self._price

    @property
    def kw_speed(self) -> float:
        return self._kw_speed

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
    def delay_hours(self) -> float:
        return self._delay_hours
    @delay_hours.setter
    def delay_hours(self, delay: float):
        self._delay_hours = delay

    @property
    def price(self) -> float:
        return self._price

    @property
    def services_nearby(self) -> list[Service]:
        return self._services_nearby
    @services_nearby.setter
    def services_nearby(self, services: list[Service]):
        self._services_nearby = services

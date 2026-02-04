from datetime import time

from src.Domain.service import Service
from src.Domain.charger import Charger

class ChargingStation:
    def __init__(self, id: int, name: str, latitude: float, longitude: float, open_time: time, close_time: time, services: list[Service], chargers: list[Charger]):
        self._id = id
        self._name = name
        self._latitude = latitude
        self._longitude = longitude
        self._open_time = open_time
        self._close_time = close_time
        self._services = services
        self._chargers = chargers

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def location(self) -> tuple[float, float]:
        return (self._latitude, self._longitude)

    @property
    def open_time(self) -> time:
        return self._open_time

    @property
    def close_time(self) -> time:
        return self._close_time

    @property
    def services(self) -> list[Service]:
        return self._services

    @property
    def chargers(self) -> list[Charger]:
        return self._chargers

from src.Domain.service import Service
from src.Domain.charger import Charger

class ChargingStation:
    def __init__(self, id: int, name: str, location: tuple[float, float], operator: str, chargers: list[Charger]=[]):
        self._id = id
        self._name = name
        self._location = location
        self._operator = operator
        self._chargers = chargers

    ##############
    # PROPERTIES #
    ##############
    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def location(self) -> tuple[float, float]:
        return self._location

    @property
    def operator(self) -> str:
        return self._operator

    @property
    def services(self) -> list[Service]:
        return self._services

    @property
    def chargers(self) -> list[Charger]:
        return self._chargers
    @chargers.setter
    def chargers(self, chargers: list[Charger]):
        self._chargers = chargers

from datetime import time

from src.Domain.serviceDAO import ServiceDAO

from src.Domain.charging_station import ChargingStation

from src.Utils.constants import ServiceType

class Service:
    def __init__(self, id: int, name: str, type: ServiceType, open_time: time, close_time: time, charging_station: ChargingStation):
        self._id = id
        self._name = name
        self._type = type
        self._open_time = open_time
        self._close_time = close_time
        self._charging_station = charging_station

        self._serviceDAO = ServiceDAO()

    def insert(self):
        self._serviceDAO.insert(self)

    def update(self):
        self._serviceDAO.update(self)

    def delete(self):
        self._serviceDAO.delete(self)

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
    def type(self) -> ServiceType:
        return self._type

    @property
    def open_time(self) -> time:
        return self._open_time

    @property
    def close_time(self) -> time:
        return self._close_time

    @property
    def charging_station(self) -> ChargingStation:
        return self._charging_station

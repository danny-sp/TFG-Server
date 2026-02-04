from datetime import time

from src.Utils.constants import ServiceType

class Service:
    def __init__(self, id: int, name: str, type: ServiceType, open_time: time, close_time: time):
        self._id = id
        self._name = name
        self._type = type
        self._open_time = open_time
        self._close_time = close_time

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

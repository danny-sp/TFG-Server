from typing import Tuple

from src.Utils.constants import ServiceType

class Service:
    def __init__(self, id: int, name: str, type: ServiceType, location: Tuple[int, int]):
        self._id = id
        self._name = name
        self._type = type
        self._location = location

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
    def location(self) -> Tuple[int, int]:
        return self._location

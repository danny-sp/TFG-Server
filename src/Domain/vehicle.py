from datetime import datetime

class Vehicle:
    def __init__(self, plate: str, capacity_kwh: float, max_kw_speed: float, reg_date: datetime):
        self._plate = plate
        self._capacity_kwh = capacity_kwh
        self._max_kw_speed = max_kw_speed
        self._reg_date = reg_date

    @property
    def plate(self) -> str:
        return self._plate

    @property
    def capacity_kwh(self) -> float:
        return self._capacity_kwh

    @property
    def max_kw_speed(self) -> float:
        return self._max_kw_speed

    @property
    def reg_date(self) -> datetime:
        return self._reg_date

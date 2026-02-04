from datetime import datetime

from src.Domain.charger import Charger
from src.Domain.booking import Booking

class ChargingSession:
    def __init__(self, session_id: int, booking: Booking, charger: Charger, start_time: datetime, end_time: datetime = None, energy_delivered_kwh: float = 0.0, total_cost: float = 0.0):
        self._session_id = session_id
        self._booking = booking
        self._charger = charger
        self._start_time = start_time
        self._end_time = end_time
        self._energy_delivered_kwh = energy_delivered_kwh
        self._total_cost = total_cost

    @property
    def id(self) -> int:
        return self._session_id

    @property
    def booking(self) -> Booking:
        return self._booking

    @property
    def charger(self) -> Charger:
        return self._charger

    @property
    def start_time(self) -> datetime:
        return self._start_time

    @property
    def end_time(self) -> datetime:
        return self._end_time

    @end_time.setter
    def end_time(self, end_time: datetime):
        self._end_time = end_time

    @property
    def energy_delivered_kwh(self) -> float:
        return self._energy_delivered_kwh

    @property
    def total_cost(self) -> float:
        return self._total_cost

from datetime import datetime

from src.Domain.charging_sessionDAO import ChargingSessionDAO

from src.Domain.charger import Charger
from src.Domain.booking import Booking

class ChargingSession:
    def __init__(self, id: int, booking: Booking, charger: Charger, start_date: datetime, end_date: datetime = None, energy_delivered_kwh: float = 0.0, total_cost: float = 0.0):
        self._id = id
        self._booking = booking
        self._charger = charger
        self._start_date = start_date
        self._end_date = end_date
        self._energy_delivered_kwh = energy_delivered_kwh
        self._total_cost = total_cost

    ##############
    # PROPERTIES #
    ##############
    @property
    def id(self) -> int:
        return self._id

    @property
    def booking(self) -> Booking:
        return self._booking

    @property
    def charger(self) -> Charger:
        return self._charger

    @property
    def start_date(self) -> datetime:
        return self._start_date

    @property
    def end_date(self) -> datetime:
        return self._end_date

    @end_date.setter
    def end_date(self, end_date: datetime):
        self._end_date = end_date

    @property
    def energy_delivered_kwh(self) -> float:
        return self._energy_delivered_kwh

    @property
    def total_cost(self) -> float:
        return self._total_cost

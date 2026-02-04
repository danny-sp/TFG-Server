from datetime import datetime

from src.Domain.charging_station import ChargingStation
from src.Domain.price_rate import PriceRate
from src.Domain.vehicle import Vehicle

from src.Utils.constants import BookingStatus

class Booking:
    def __init__(self, booking_id: int, vehicle: Vehicle, booking_date: datetime, start_time: datetime, end_time: datetime, price_rate: PriceRate, booking_status: BookingStatus, price: float = 0.0):
        self._booking_id = booking_id
        self._vehicle = vehicle
        self._booking_date = booking_date
        self._start_time = start_time
        self._end_time = end_time
        self._price = price
        self._price_rate = price_rate
        self._booking_status = booking_status

    @property
    def id(self) -> int:
        return self._booking_id

    @property
    def vehicle(self) -> Vehicle:
        return self._vehicle

    @property
    def booking_date(self) -> datetime:
        return self._booking_date

    @property
    def start_time(self) -> datetime:
        return self._start_time

    @property
    def end_time(self) -> datetime:
        return self._end_time

    @property
    def price_rate(self) -> PriceRate:
        return self._price_rate

    @property
    def charging_station(self) -> ChargingStation:
        return self._price_rate.charging_station

    @property
    def price(self) -> float:
        return self._price

    @property
    def booking_status(self) -> BookingStatus:
        return self._booking_status

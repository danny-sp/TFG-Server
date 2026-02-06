from datetime import datetime

from src.Domain.bookingDAO import BookingDAO

from src.Domain.charging_station import ChargingStation
from src.Domain.price_rate import PriceRate
from src.Domain.vehicle import Vehicle

from src.Utils.constants import BookingStatus

class Booking:
    def __init__(self, id: int, vehicle: Vehicle, booking_date: datetime, start_date: datetime, end_date: datetime, price_rate: PriceRate, status: BookingStatus, price: float = 0.0):
        self._id = id
        self._vehicle = vehicle
        self._booking_date = booking_date
        self._start_date = start_date
        self._end_date = end_date
        self._price = price
        self._price_rate = price_rate
        self._status = status

        self._bookingDAO = BookingDAO()

    def insert(self):
        self._bookingDAO.insert(self)

    def update(self):
        self._bookingDAO.update(self)

    def delete(self):
        self._bookingDAO.delete(self)

    ##############
    # PROPERTIES #
    ##############
    # Error Code: 1005. Can't create table `ev_charging_system`.`charging_sessions` 
    # (errno: 150 "Foreign key constraint is incorrectly formed")

    @property
    def id(self) -> int:
        return self._id

    @property
    def vehicle(self) -> Vehicle:
        return self._vehicle

    @property
    def booking_date(self) -> datetime:
        return self._booking_date

    @property
    def start_date(self) -> datetime:
        return self._start_date

    @property
    def end_date(self) -> datetime:
        return self._end_date

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
    def status(self) -> BookingStatus:
        return self._status

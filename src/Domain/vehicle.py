from datetime import datetime

from src.Domain.vehicleDAO import VehicleDAO

from src.Domain.ev_user import EVUser

class Vehicle:
    def __init__(self, plate: str, capacity_kwh: float, max_kw_speed: float, user: EVUser, reg_date: datetime = None):
        self._plate = plate
        self._capacity_kwh = capacity_kwh
        self._max_kw_speed = max_kw_speed
        self._user = user
        self._reg_date = reg_date if reg_date else datetime.now()

        self._vehicleDAO = VehicleDAO()

    def insert(self):
        self._vehicleDAO.insert(self)

    def update(self):
        self._vehicleDAO.update(self)

    def delete(self):
        self._vehicleDAO.delete(self)

    ##############
    # PROPERTIES #
    ##############
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
    def user(self) -> EVUser:
        return self._user

    @property
    def reg_date(self) -> datetime:
        return self._reg_date

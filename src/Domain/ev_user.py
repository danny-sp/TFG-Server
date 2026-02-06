from datetime import datetime

from src.Domain.ev_userDAO import EVUserDAO
from src.Domain.vehicleDAO import VehicleDAO

from src.Domain.vehicle import Vehicle

class EVUser:
    def __init__(self, id: int, username: str, email: str, phone: str = None, active: bool = True, registration_date: datetime = None, vehicles: list[Vehicle] = []):
        self._id = id
        self._username = username
        self._email = email
        self._phone = phone
        self._active = active
        self._registration_date = registration_date if registration_date else datetime.now()
        self._vehicles = vehicles

        if len(vehicles) == 0:
            self._vehicles = self._load_vehicles()

        self._ev_userDAO = EVUserDAO()

    def insert(self):
        self._ev_userDAO.insert(self)

    def update(self):
        self._ev_userDAO.update(self)

    def delete(self):
        self._ev_userDAO.delete(self)

    def _load_vehicles(self) -> list[Vehicle]:
        vehicleDAO = VehicleDAO()
        return vehicleDAO.read_by_user_id(self)

    ##############
    # PROPERTIES #
    ##############
    @property
    def id(self) -> int:
        return self._user_id

    @property
    def username(self) -> str:
        return self._username

    @property
    def email(self) -> str:
        return self._email

    @property
    def phone(self) -> str:
        return self._phone

    @property
    def active(self) -> bool:
        return self._active

    @property
    def registration_date(self) -> datetime:
        return self._registration_date

    @property
    def vehicles(self) -> list[Vehicle]:
        return self._vehicles

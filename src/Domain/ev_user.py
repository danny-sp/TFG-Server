from datetime import datetime

from src.Domain.vehicle import Vehicle

class EVUser:
    def __init__(self, user_id: int, username: str, email: str, phone: str = None, active: bool = True, registration_date: datetime = None, vehicles: list[Vehicle] = None):
        self._user_id = user_id
        self._username = username
        self._email = email
        self._phone = phone
        self._active = active
        self._registration_date = registration_date if registration_date else datetime.now()
        self._vehicles = vehicles

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

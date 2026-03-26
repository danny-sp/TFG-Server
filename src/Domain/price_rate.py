from datetime import datetime

from src.Domain.charging_station import ChargingStation


class PriceRate:
    def __init__(
        self,
        id: int,
        charging_station: ChargingStation,
        start_date: datetime,
        end_date: datetime,
        price_per_kwh: float,
    ):
        self._id = id
        self._charging_station = charging_station
        self._start_date = start_date
        self._end_date = end_date
        self._price_per_kwh = price_per_kwh

    ##############
    # PROPERTIES #
    ##############
    @property
    def id(self) -> int:
        return self._id

    @property
    def charging_station(self) -> ChargingStation:
        return self._charging_station

    @property
    def start_date(self) -> datetime:
        return self._start_date

    @property
    def end_date(self) -> datetime:
        return self._end_date

    @property
    def price_per_kwh(self) -> float:
        return self._price_per_kwh

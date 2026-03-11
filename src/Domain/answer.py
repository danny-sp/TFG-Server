from src.Domain.charging_station import ChargingStation
from src.Domain.price_rate import PriceRate

class Answer:
    def __init__(self, request_id: int, charging_station: ChargingStation, price_rate: PriceRate, price: float):
        self._request_id = request_id
        self._charging_station = charging_station
        self._price_rate = price_rate
        self._price = price

    ##############
    # PROPERTIES #
    ##############
    @property
    def request_id(self) -> int:
        return self._request_id

    @property
    def charging_station(self) -> ChargingStation:
        return self._charging_station

    @property
    def price_rate(self) -> PriceRate:
        return self._price_rate

    @property
    def price(self) -> float:
        return self._price

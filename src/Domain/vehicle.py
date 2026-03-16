from datetime import datetime

class Vehicle:
    def __init__(self, plate: str, consumption_wh_km: float, capacity_kwh: float, max_kw_speed: float, reg_date: datetime = None):
        self._plate = plate
        self._consumption_wh_km = float(consumption_wh_km)
        self._capacity_kwh = float(capacity_kwh)
        self._max_kw_speed = float(max_kw_speed)
        self._reg_date = reg_date if reg_date else datetime.now()

    def distance_percent(self, current_percent: float, minimum_percent: float) -> float:
        if current_percent <= 0 or current_percent > 100:
            raise ValueError("Current percent must be between 0 and 100.")

        if minimum_percent <= 0 or minimum_percent > 100:
            raise ValueError("Minimum percent must be between 0 and 100.")

        if current_percent < minimum_percent:
            raise ValueError("Current percent must be greater than or equal to minimum percent.")

        usable_kwh = self.capacity_kwh * (current_percent - minimum_percent) / 100
        distance = (usable_kwh * 1000) / self.consumption_wh_km

        return distance

    ##############
    # PROPERTIES #
    ##############
    @property
    def plate(self) -> str:
        return self._plate

    @property
    def consumption_wh_km(self) -> float:
        return self._consumption_wh_km

    @property
    def capacity_kwh(self) -> float:
        return self._capacity_kwh

    @property
    def max_kw_speed(self) -> float:
        return self._max_kw_speed

    @property
    def reg_date(self) -> datetime:
        return self._reg_date

from datetime import datetime

class Vehicle:
    def __init__(self, plate: str, consumption_wh_km: float, capacity_kwh: float, max_kw_speed: float, reg_date: datetime = None, current_percent: float = None):
        self._plate = plate
        self._consumption_wh_km = float(consumption_wh_km)
        self._capacity_kwh = float(capacity_kwh)
        self._max_kw_speed = float(max_kw_speed)
        self._reg_date = reg_date if reg_date else datetime.now()
        if current_percent is not None:
            if current_percent < 0 or current_percent > 100:
                raise ValueError("Current percent must be between 0 and 100.")
            self._current_percent = float(current_percent)
        else:
            self._current_percent = 0.0

    def distance_percent(self, minimum_percent: float) -> float:
        if minimum_percent <= 0 or minimum_percent > 100:
            raise ValueError("Minimum percent must be between 0 and 100.")

        if minimum_percent >self._current_percent:
            raise ValueError("Minimum percent must be less than or equal to current percent.")

        usable_kwh = self.capacity_kwh * (self._current_percent - minimum_percent) / 100
        distance = (usable_kwh * 1000) / self.consumption_wh_km

        return distance

    def percent_after_distance(self, distance_km: float) -> float:
        if distance_km < 0:
            raise ValueError("Distance must be a non-negative number.")

        energy_needed_kwh = (distance_km * self.consumption_wh_km) / 1000
        percent_needed = (energy_needed_kwh / self.capacity_kwh) * 100

        remaining_percent = self._current_percent - percent_needed
        return remaining_percent if remaining_percent >= 0 else -1.0

    def charging_time(self, target_percent: float, kw_chg: float) -> float:
        if target_percent < 0 or target_percent > 100:
            raise ValueError("Target percent must be between 0 and 100.")

        if target_percent <= self._current_percent:
            raise ValueError("Target percent must be greater than current percent.")

        if kw_chg <= 0:
            raise ValueError("KW charging speed must be a positive number.")

        kw_speed = float(min(kw_chg, self.max_kw_speed))

        charge_kwh = self.capacity_kwh * (target_percent - self._current_percent) / 100
        time_hours = charge_kwh / kw_speed

        return time_hours

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

    @property
    def current_percent(self) -> float:
        return self._current_percent
    @current_percent.setter
    def current_percent(self, value: float):
        if value < 0 or value > 100:
            raise ValueError("Current percent must be between 0 and 100.")
        self._current_percent = value

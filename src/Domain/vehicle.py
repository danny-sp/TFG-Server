"""
Domain model representing an Electric Vehicle (EV).
Following Pydantic's BaseModel for data validation and immutability.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class Vehicle(BaseModel):
    """
    Domain model representing an Electric Vehicle (EV).

    Attributes:
        plate (str): The license plate of the vehicle.
        consumption_wh_km (float): The average energy consumption in watt-hours per kilometer.
        capacity_kwh (float): The total battery capacity in kilowatt-hours.
        max_kw_speed (float): The maximum charging speed accepted by the vehicle in kilowatts.
        reg_date (datetime): The registration date of the vehicle.
    """

    # model_config enforces immutability and prevents adding non-declared attributes
    model_config = ConfigDict(extra="forbid", frozen=True)

    plate: str = Field(..., min_length=1, description="Vehicle license plate")
    consumption_wh_km: float = Field(
        ..., gt=0.0, description="Average consumption in Wh per km"
    )
    capacity_kwh: float = Field(
        ..., gt=0.0, description="Total battery capacity in kWh"
    )
    max_kw_speed: float = Field(
        ..., gt=0.0, description="Maximum charging speed accepted in kW"
    )
    reg_date: datetime = Field(
        default_factory=datetime.now, description="Registration date"
    )

    def distance_percent(self, current_percent: float, minimum_percent: float) -> float:
        """
        Calculates the maximum distance the vehicle can travel from its current percentage
        until it reaches the specified minimum percentage.

        Args:
            current_percent (float): The current battery percentage (0-100).
            minimum_percent (float): The minimum battery percentage to consider (0-100).

        Returns:
            float: The maximum distance in kilometers the vehicle can travel until reaching the minimum percentage.
        """

        self._validate_percent(current_percent, "Current percent")
        self._validate_percent(minimum_percent, "Minimum percent")

        if minimum_percent > current_percent:
            raise ValueError(
                "Minimum percent must be less than or equal to current percent."
            )

        usable_kwh = self.capacity_kwh * (current_percent - minimum_percent) / 100.0
        distance = (usable_kwh * 1000.0) / self.consumption_wh_km

        return distance

    def percent_after_distance(
        self, current_percent: float, distance_km: float
    ) -> float:
        """
        Calculates the remaining battery percentage after traveling a specific distance.
        Returns -1.0 if the vehicle cannot cover the distance with the current charge.

        Args:
            current_percent (float): The current battery percentage (0-100).
            distance_km (float): The distance to be traveled in kilometers.

        Returns:
            float: The remaining battery percentage after traveling the distance, or -1.0 if not feasible.
        """

        self._validate_percent(current_percent, "Current percent")

        if distance_km < 0:
            raise ValueError("Distance must be a non-negative number.")

        energy_needed_kwh = (distance_km * self.consumption_wh_km) / 1000.0
        percent_needed = (energy_needed_kwh / self.capacity_kwh) * 100.0

        remaining_percent = current_percent - percent_needed

        return remaining_percent if remaining_percent >= 0 else -1.0

    def charging_time(
        self, current_percent: float, target_percent: float, kw_chg: float
    ) -> float:
        """
        Calculates the time (in hours) required to charge the vehicle from the
        current percentage to a target percentage at a given charging speed.

        Args:
            current_percent (float): The current battery percentage (0-100).
            target_percent (float): The desired battery percentage after charging (0-100).
            kw_chg (float): The charging speed in kW.

        Returns:
            float: The time in hours required to charge to the target percentage.
        """

        self._validate_percent(current_percent, "Current percent")
        self._validate_percent(target_percent, "Target percent")

        if target_percent <= current_percent:
            raise ValueError("Target percent must be greater than current percent.")

        if kw_chg <= 0:
            raise ValueError("KW charging speed must be a positive number.")

        actual_kw_speed = float(min(kw_chg, self.max_kw_speed))

        charge_kwh = self.capacity_kwh * (target_percent - current_percent) / 100.0
        time_hours = charge_kwh / actual_kw_speed

        return time_hours

    # --------------------------------------------------------
    # PRIVATE HELPERS
    # --------------------------------------------------------

    @staticmethod
    def _validate_percent(percent: float, field_name: str) -> None:
        """
        Helper method to validate that a percentage is within the 0-100 range.

        Args:
            percent (float): The percentage value to validate.
            field_name (str): The name of the field being validated (for error messages).

        Raises:
                ValueError: If the percentage is not within the 0-100 range.
        """

        if not 0.0 <= percent <= 100.0:
            raise ValueError(f"{field_name} must be between 0 and 100.")

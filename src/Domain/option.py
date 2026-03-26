"""
Domain model representing a potential charging route option.
Following Pydantic's BaseModel.
Not frozen for updating some fields, which are not set at creation time.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, computed_field

from src.Domain.charging_station import ChargingStation
from src.Domain.price_rate import PriceRate
from src.Domain.service import Service


class Option(BaseModel):
    """
    Domain model representing a potential charging route option.

    Attributes:
        request_id (str): The UUID of the routing request that generated this option.
        charging_station (ChargingStation): The proposed station for charging.
        price_rate (PriceRate | None): The applied price rate for this option, if available.
        start_time (datetime): The estimated time of arrival at the station.
        charging_hours (float): The required charging time in hours.
        kw_speed (float): The charging speed in kilowatts.
        route_hours (float): The estimated driving duration in hours to reach the station.
        delay_hours (float): The estimated time lost compared to the direct route.
        price (float): The estimated total price for this charging option.
        services_nearby (list[Service]): A list of available services near the station.
    """

    model_config = ConfigDict(
        extra="forbid",
        arbitrary_types_allowed=True,
        frozen=False,
        validate_assignment=True,
    )

    request_id: str = Field(..., description="The UUID of the routing request")
    charging_station: ChargingStation = Field(..., description="The proposed station")
    price_rate: PriceRate | None = Field(
        default=None, description="The applied price rate"
    )
    start_time: datetime = Field(
        ..., description="Estimated time of arrival at the station"
    )
    charging_hours: float = Field(
        ..., gt=0.0, description="Required charging time in hours"
    )
    kw_speed: float = Field(..., gt=0.0, description="Charging speed in kW")

    route_hours: float = Field(
        default=0.0, ge=0.0, description="Driving duration in hours"
    )
    delay_hours: float = Field(
        default=0.0, ge=0.0, description="Time lost compared to the direct route"
    )
    price: float = Field(default=0.0, ge=0.0, description="Estimated total price")
    services_nearby: list[Service] = Field(
        default_factory=list, description="List of available services near the station"
    )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def end_time(self) -> datetime:
        """
        Dynamically calculates the end time based on the start time and charging duration.
        """
        return self.start_time + timedelta(hours=self.charging_hours)

    def to_dict(self) -> dict[str, Any]:
        """
        Serializes the Option into a specific dictionary format required by the
        frontend or API response.
        """
        return {
            "request_id": self.request_id,
            "charging_station": {
                "id": self.charging_station.id,  # pylint: disable=no-member
                "name": self.charging_station.name,  # pylint: disable=no-member
                "location": self.charging_station.location,  # pylint: disable=no-member
                "operator": self.charging_station.operator,  # pylint: disable=no-member
            },
            "price": float(self.price),
            "kw_speed": float(self.kw_speed),
            "start_time": self.start_time.isoformat(),  # pylint: disable=no-member
            "end_time": self.end_time.isoformat(),
            "charging_hours": float(self.charging_hours),
            "route_hours": float(self.route_hours),
            "delay_hours": float(self.delay_hours),
            "services_nearby": list({service.type for service in self.services_nearby}),
        }

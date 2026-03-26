"""
Domain model representing a physical Charging Station location.
Following Pydantic's BaseModel for data validation and immutability.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from src.Domain.charger import Charger


class ChargingStation(BaseModel):
    """
    Domain model representing a physical Charging Station location.
    """

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True, frozen=True)

    id: int = Field(..., gt=0, description="Unique database identifier for the station")
    name: str = Field(..., min_length=1, description="Commercial name of the station")
    location: tuple[float, float] = Field(
        ..., description="GPS coordinates of the station"
    )
    operator: str = Field(
        ..., description="Company responsible for operating the station"
    )
    chargers: list[Charger] = Field(
        default_factory=list,
        description="Collection of physical chargers available at this location",
    )

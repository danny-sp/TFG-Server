"""
Domain model representing an amenity or service near a charging station.
Following Pydantic's BaseModel for data validation and immutability.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from src.Utils.constants import ServiceType


class Service(BaseModel):
    """
    Domain model representing an amenity or service near a charging station.

     Attributes:
        id (int): Unique database identifier for the service.
        name (str): Commercial or descriptive name of the service.
        type (ServiceType): The category/type of the service provided.
        location (tuple[float, float]): GPS coordinates (latitude, longitude) of the service location.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    id: int = Field(..., gt=0, description="Unique database identifier for the service")
    name: str = Field(
        ..., min_length=1, description="Commercial or descriptive name of the service"
    )
    type: ServiceType = Field(
        ..., description="The category/type of the service provided"
    )
    location: tuple[float, float] = Field(
        ..., description="GPS coordinates (latitude, longitude)"
    )

"""
Domain model representing a routing request from an EV user.
Following Pydantic's BaseModel.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Request(BaseModel):
    """
    Domain model representing a routing request from an EV user.

    Attributes:
        uuid (str): Unique identifier for the request, typically a UUID string.
        plate (str): The license plate of the vehicle making the request.
        timestamp (datetime): The exact time when the request was generated.
        current_percent (float): The current battery percentage of the vehicle (0 to 100).
        position (tuple[float, float]): The current GPS coordinates of the vehicle (latitude, longitude).
        destination (tuple[float, float]): The GPS coordinates of the desired destination (latitude, longitude).
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    uuid: str = Field(..., description="Unique identifier for the request")
    plate: str = Field(..., min_length=1, description="Vehicle license plate")
    timestamp: datetime = Field(
        default_factory=datetime.now, description="Exact time the request was generated"
    )
    current_percent: float = Field(
        ..., ge=0.0, le=100.0, description="Current battery percentage (0 to 100)"
    )
    position: tuple[float, float] = Field(
        ..., description="Current GPS coordinates (lat, lon)"
    )
    destination: tuple[float, float] = Field(
        ..., description="Destination GPS coordinates (lat, lon)"
    )
    price_hour: float = Field(
        default=15.0, gt=0.0, description="Price per hour for the driver"
    )

    def to_dict(self) -> dict[str, Any]:
        """
        Serializes the Request into a flattened dictionary format.

        This explicitly unwraps the coordinate tuples into flat keys
        (latitude, longitude) for specific API or messaging queue requirements.

        Returns:
            dict[str, Any]: A dictionary representation of the Request with flattened coordinates.
        """
        return {
            "uuid": self.uuid,
            "plate": self.plate,
            "timestamp": self.timestamp.isoformat(),  # pylint: disable=no-member
            "current_percent": self.current_percent,
            "latitude": self.position[0],
            "longitude": self.position[1],
            "destination_lat": self.destination[0],
            "destination_lon": self.destination[1],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Request:
        """
        Factory method to instantiate a Request from a flattened dictionary.

        Args:
            data (dict[str, Any]): A dictionary containing the request data with flat coordinate keys.

        Returns:
            Request: An instance of the Request class populated with the provided data.
        """
        return cls(
            uuid=data["uuid"],
            plate=data["plate"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            current_percent=data["current_percent"],
            position=(data["latitude"], data["longitude"]),
            destination=(data["destination_lat"], data["destination_lon"]),
            price_hour=data.get("price_hour", 15), # Default price per hour if not provided
        )

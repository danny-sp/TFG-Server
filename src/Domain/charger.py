"""
Domain model representing a EV Charger.
Following Pydantic's BaseModel for data validation and immutability.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class Charger(BaseModel):
    """
    Domain model representing a EV Charger.

    Attributes:
        id (int): Unique database identifier for the charger.
        power_kw (float): The maximum charging power of the charger in kilowatts.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    id: int = Field(..., gt=0, description="Unique database identifier")
    power_kw: float = Field(..., gt=0.0, description="Maximum charging power (kW)")

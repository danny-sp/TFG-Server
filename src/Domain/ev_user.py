"""
Domain model representing an Electric Vehicle (EV) system user.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from src.Domain.vehicle import Vehicle


class EVUser(BaseModel):
    """
    Domain model representing an Electric Vehicle (EV) system user.

    This class is immutable (frozen) as the user data is pre-populated in the
    database. It acts as a container for user metadata and their associated
    collection of vehicles.
    """

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True, frozen=True)

    id: int = Field(..., gt=0, description="Unique database identifier for the user")
    username: str = Field(..., min_length=1, description="Unique login name")
    email: str = Field(..., description="Primary contact email address")
    phone: str | None = Field(default=None, description="Optional contact phone number")
    value_time: float = Field(
        default=15.0,
        gt=0,
        description="User's subjective value of time in €/hour, used for route optimization",
    )
    active: bool = Field(
        default=True, description="Indicates if the account is currently active"
    )
    registration_date: datetime = Field(
        default_factory=datetime.now,
        description="Date and time when the user registered",
    )
    vehicles: list[Vehicle] = Field(
        default_factory=list,
        description="List of vehicles owned or managed by this user",
    )

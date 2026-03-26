"""
Domain model representing an EV Charging Session.
Following Pydantic's BaseModel.
Not frozen for updating some fields, which are not set at creation time.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from src.Domain.booking import Booking
from src.Domain.charger import Charger


class ChargingSession(BaseModel):
    """
    Domain model representing an EV Charging Session.

    Attributes:
        id (int | None): Unique identifier for the charging session, assigned by the database.
        booking (Booking): The associated booking for this charging session.
        charger (Charger): The physical charger used for this session.
        start_date (datetime): The timestamp when the charging session started.
        end_date (datetime | None): The timestamp when the charging session ended. Can be None if the session is still active.
        energy_delivered_kwh (float): The total energy delivered during the session in kilowatt-hours.
        total_cost (Decimal): The total cost of the charging session, calculated based on the energy delivered and the price rate.
    """

    model_config = ConfigDict(
        extra="forbid",
        arbitrary_types_allowed=True,
        frozen=False,
        validate_assignment=True,
    )

    id: int | None = Field(default=None, gt=0, description="Unique identifier")
    booking: Booking = Field(..., description="The associated booking")
    charger: Charger = Field(..., description="The physical charger used")
    start_date: datetime = Field(..., description="Session start timestamp")
    end_date: datetime | None = Field(default=None, description="Session end timestamp")
    energy_delivered_kwh: float = Field(
        default=0.0, ge=0.0, description="Energy in kWh"
    )
    total_cost: Decimal = Field(
        default=Decimal("0.0"), ge=Decimal("0.0"), description="Total cost"
    )

    @model_validator(mode="after")
    def validate_business_rules(self) -> ChargingSession:
        """Validates that the end date is not before the start date."""
        if self.end_date is not None and self.end_date < self.start_date:
            raise ValueError("End date cannot be strictly before the start date.")
        return self

"""
Domain model representing a Charging Station Booking.
Following Pydantic's BaseModel for data validation and immutability.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import (BaseModel, ConfigDict, Field, computed_field,
                      model_validator)

from src.Domain.price_rate import PriceRate
from src.Domain.vehicle import Vehicle
from src.Utils.constants import BookingStatus


class Booking(BaseModel):
    """
    Domain model representing a Charging Station Booking.
    """

    # Enforces immutability and permits custom classes like Vehicle and PriceRate
    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True, frozen=True)

    id: int | None = Field(
        default=None, description="Unique identifier for the booking"
    )
    vehicle: Vehicle = Field(
        ..., description="The vehicle associated with this booking"
    )
    booking_date: datetime = Field(
        ..., description="The exact date and time the booking was made"
    )
    start_date: datetime = Field(
        ..., description="The scheduled start date and time for charging"
    )
    end_date: datetime = Field(
        ..., description="The scheduled end date and time for charging"
    )
    price_rate: PriceRate = Field(
        ..., description="The applied price rate for this booking"
    )
    price: Decimal = Field(
        ..., description="The total calculated price for the booking"
    )
    status: BookingStatus = Field(..., description="The current status of the booking")

    @computed_field  # type: ignore[prop-decorator]
    @property
    def charging_hours(self) -> float:
        """
        Computes the total charging duration in hours based on the start and end dates.

        Returns:
            float: The total charging duration in hours.
        """
        return (self.end_date - self.start_date).total_seconds() / 3600.0

    @model_validator(mode="after")
    def validate_business_rules(self) -> Booking:
        """
        Validates the core business invariants of a booking after instantiation.
        These rules apply whether the booking is brand new or loaded from the database.

        Returns:
            Booking: The validated model instance.

        Raises:
            ValueError: If any rule is violated.
        """
        now = datetime.now()

        # Temporal validations
        if self.booking_date > now:
            raise ValueError("Booking date cannot be in the future.")

        if self.start_date < self.booking_date:
            raise ValueError("Start date cannot be before the booking date.")

        if self.end_date <= self.start_date:
            raise ValueError("End date must be strictly after the start date.")

        # Duration validations using the computed field property
        if self.charging_hours <= 0:
            raise ValueError("Charging hours must be strictly greater than zero.")
        if self.charging_hours > 24:
            raise ValueError("Bookings cannot exceed 24 hours of duration.")

        # Financial validation
        if self.price < 0:
            raise ValueError("Price cannot be a negative value.")

        return self

    @classmethod
    def create_new(
        cls,
        vehicle: Vehicle,
        start_date: datetime,
        end_date: datetime,
        price_rate: PriceRate,
        price: Decimal | float | str,
    ) -> Booking:
        """
        Factory method to create a new booking.

        This method enforces that new bookings are created with the current
        timestamp as the booking date and 'SCHEDULED' as the initial status.

        Args:
            vehicle (Vehicle): The vehicle making the booking.
            start_date (datetime): The desired start time.
            end_date (datetime): The desired end time.
            price_rate (PriceRate): The rate applied.
            price (Decimal | float | str): The calculated price (will be cast to Decimal).

        Returns:
            Booking: A new, validated Booking instance.

        Raises:
            ValueError: If the start date is in the past.
        """
        now = datetime.now()

        if start_date < now:
            raise ValueError("Start date for a new booking cannot be in the past.")

        return cls(
            id=None,
            vehicle=vehicle,
            booking_date=now,
            start_date=start_date,
            end_date=end_date,
            price_rate=price_rate,
            price=price,
            status=BookingStatus.SCHEDULED,
        )

    def cancel(self) -> Booking:
        """
        Cancels the booking.

        Since the class is immutable, this method does not modify the current
        object. Instead, it returns a new copy of the booking with the status
        updated to CANCELLED.

        Returns:
            Booking: A new instance representing the canceled booking.

        Raises:
            ValueError: If the booking is not in the SCHEDULED state.
        """
        if self.status != BookingStatus.SCHEDULED:
            raise ValueError(
                f"Cannot cancel a booking with status: {self.status.name}"
            )  # pylint: disable=no-member

        return self.model_copy(update={"status": BookingStatus.CANCELLED})

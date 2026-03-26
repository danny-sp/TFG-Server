"""
Constants and enumerations for the application.
"""

from enum import StrEnum


class ServiceType(StrEnum):
    """
    Enumeration of possible service types available near charging stations.
    """

    CAFE = "cafe"
    RESTAURANT = "restaurant"
    MOTEL = "motel"
    MECHANIC = "mechanic"
    SUPERMARKET = "supermarket"
    ATM = "atm"
    PHARMACY = "pharmacy"


class BookingStatus(StrEnum):
    """
    Enumeration of different booking statuses for a charging station reservation.
    """

    SCHEDULED = "scheduled"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

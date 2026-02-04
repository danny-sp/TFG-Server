from enum import StrEnum

class ServiceType(StrEnum):
    CAFE = 'cafe'
    RESTAURANT = 'restaurant'
    MOTEL = 'motel'
    MECHANIC = 'mechanic'
    SUPERMARKET = 'supermarket'
    ATM = 'atm'
    PHARMACY = 'pharmacy'

class BookingStatus(StrEnum):
    SCHEDULED = 'scheduled'
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'
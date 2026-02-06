
from src.Domain.bookingDAO import BookingDAO
from src.Domain.chargerDAO import ChargerDAO

from src.Domain.charging_session import ChargingSession

from src.Persistance.db_broker import DBBroker

class ChargingSessionDAO:
    def __init__(self):
        self._db = DBBroker()

    def insert(self, charging_session: ChargingSession):
        query = """
        INSERT INTO charging_sessions (booking_id, charger_id, start_date, end_date, energy_delivered_kwh, total_cost)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (
            charging_session.booking.id,
            charging_session.charger.id,
            charging_session.start_date,
            charging_session.end_date,
            charging_session.energy_delivered_kwh,
            charging_session.total_cost
        )
        _, inserted_id = self._db.execute_write_query(query, params)
        return inserted_id

    def update(self, charging_session: ChargingSession):
        query = """
        UPDATE charging_sessions
        SET booking_id = ?, charger_id = ?, start_date = ?, end_date = ?, energy_delivered_kwh = ?, total_cost = ?
        WHERE id = ?
        """
        params = (
            charging_session.booking.id,
            charging_session.charger.id,
            charging_session.start_date,
            charging_session.end_date,
            charging_session.energy_delivered_kwh,
            charging_session.total_cost,
            charging_session.id
        )
        return self._db.execute_write_query(query, params)

    def delete(self, charging_session: ChargingSession):
        query = "DELETE FROM charging_sessions WHERE id = ?"
        params = (charging_session.id,)
        return self._db.execute_write_query(query, params)

    def read_by_id(self, session_id: int) -> ChargingSession:
        rows = self._db.execute_read_query("SELECT * FROM charging_sessions WHERE id = ?", (session_id,))
        return self._row_to_charging_session(rows[0]) if rows else None

    def _row_to_charging_session(self, row: dict) -> ChargingSession:
        bookingDAO = BookingDAO()
        booking = bookingDAO.read_by_id(row['booking_id'])

        chargerDAO = ChargerDAO()
        charger = chargerDAO.read_by_id(row['charger_id'])

        return ChargingSession(
            session_id=row['id'],
            booking=booking,
            charger=charger,
            start_date=row['start_date'],
            end_date=row['end_date'],
            energy_delivered_kwh=row['energy_delivered_kwh'],
            total_cost=row['total_cost']
        )

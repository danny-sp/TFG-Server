from src.Domain.vehicleDAO import VehicleDAO

from src.Domain.ev_user import EVUser

from src.Persistance.db_broker import DBBroker

class EVUserDAO:
    def __init__(self):
        self._db = DBBroker()

    def insert(self, ev_user: EVUser) -> int:
        query = """
        INSERT INTO ev_users (username, email, phone, active_user, registration_date)
        VALUES (?, ?, ?, ?, ?)
        """
        params = (
            ev_user.username,
            ev_user.email,
            ev_user.phone,
            ev_user.active,
            ev_user.registration_date
        )
        _, inserted_id = self._db.execute_write_query(query, params)
        return inserted_id

    def update(self, ev_user: EVUser) -> None:
        query = """
        UPDATE ev_users
        SET username = ?, email = ?, phone = ?, active_user = ?, registration_date = ?
        WHERE id = ?
        """
        params = (
            ev_user.username,
            ev_user.email,
            ev_user.phone,
            ev_user.active,
            ev_user.registration_date,
            ev_user.id
        )
        return self._db.execute_write_query(query, params)

    def delete(self, ev_user: EVUser) -> None:
        query = "DELETE FROM ev_users WHERE id = ?"
        params = (ev_user.id,)
        return self._db.execute_write_query(query, params)

    def read_by_id(self, user_id: int) -> EVUser:
        rows = self._db.execute_read_query("SELECT * FROM ev_users WHERE id = ?", (user_id,))
        return self._row_to_ev_user(rows[0]) if rows else None

    def _row_to_ev_user(self, row: dict) -> EVUser:
        return EVUser(
            user_id=row['id'],
            username=row['username'],
            email=row['email'],
            phone=row['phone'],
            active=bool(row['active_user']),
            registration_date=row['registration_date'],
        )

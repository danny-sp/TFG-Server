from src.Domain.charger_type import ChargerType

from src.Persistance.db_broker import DBBroker

class ChargerTypeDAO:
    def __init__(self):
        self._db = DBBroker()

    def insert(self, charger_type: ChargerType) -> int:
        query = """
        INSERT INTO charger_types (charger_name, max_kw_speed, description)
        VALUES (?, ?, ?)
        """
        params = (
            charger_type.name,
            charger_type.kw_speed,
            charger_type.description
        )
        _, inserted_id = self._db.execute_write_query(query, params)
        return inserted_id

    def update(self, charger_type: ChargerType) -> None:
        query = """
        UPDATE charger_types
        SET charger_name = ?, max_kw_speed = ?, description = ?
        WHERE id = ?
        """
        params = (
            charger_type.name,
            charger_type.kw_speed,
            charger_type.description,
            charger_type.id
        )
        return self._db.execute_write_query(query, params)

    def delete(self, charger_type: ChargerType) -> None:
        query = "DELETE FROM charger_types WHERE id = ?"
        params = (charger_type.id,)
        return self._db.execute_write_query(query, params)

    def read_by_id(self, id: int) -> ChargerType:
        rows = self._db.execute_read_query("SELECT * FROM charger_types WHERE id = ?", (id,))
        return self._row_to_charger_type(rows[0]) if rows else None

    def _row_to_charger_type(self, row: dict) -> ChargerType:
        return ChargerType(
            id=row['id'],
            name=row['charger_name'],
            kw_speed=row['max_kw_speed'],
            description=row['description']
        )

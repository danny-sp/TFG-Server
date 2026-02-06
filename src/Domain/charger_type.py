from src.Domain.charger_typeDAO import ChargerTypeDAO

class ChargerType:
    def __init__(self, id: int, name: str, kw_speed: float, description: str):
        self._id = id
        self._name = name
        self._kw_speed = kw_speed
        self._description = description

        self._chargerTypeDAO = ChargerTypeDAO()

    def insert(self):
        self._chargerTypeDAO.insert(self)

    def update(self):
        self._chargerTypeDAO.update(self)

    def delete(self):
        self._chargerTypeDAO.delete(self)

    ##############
    # PROPERTIES #
    ##############
    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def kw_speed(self) -> float:
        return self._kw_speed

    @property
    def description(self) -> str:
        return self._description

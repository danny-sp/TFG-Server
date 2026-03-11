class ChargerType:
    def __init__(self, id: int, name: str, kw_speed: float, description: str):
        self._id = id
        self._name = name
        self._kw_speed = kw_speed
        self._description = description

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

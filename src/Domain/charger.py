class Charger:
    def __init__(self, id: int, power_kw: float, busy: bool):
        self._id = id
        self._power_kw = power_kw
        self._busy = busy

    ##############
    # PROPERTIES #
    ##############
    @property
    def id(self) -> int:
        return self._id

    @property
    def power_kw(self) -> float:
        return self._power_kw

    @property
    def busy(self) -> bool:
        return self._busy

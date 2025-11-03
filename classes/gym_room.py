class InvalidRoomTypeError(ValueError):
    """Недопустимый тип зала."""
    pass

class GymRoom:
    VALID_TYPES = {"кардио", "силовой", "басссейн", "йога"}

    def __init__(self, room_id: int, room_name: str, room_type: str, capacity: int = 20):
        self.room_id = self._validate_id(room_id)
        self.room_name = self._validate_name(room_name)
        self.room_type = self._validate_type(room_type)
        self.capacity = self._validate_capacity(capacity)

    @staticmethod
    def _validate_id(room_id: int) -> int:
        if not isinstance(room_id, int) or room_id <= 0:
            raise ValueError("ID зала должен быть положительным целым числом.")
        return room_id

    @staticmethod
    def _validate_name(name: str) -> str:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Название зала не может быть пустым.")
        return name.strip()

    @classmethod
    def _validate_type(cls, room_type: str) -> str:
        room_type = room_type.strip().lower()
        if room_type not in cls.VALID_TYPES:
            raise InvalidRoomTypeError(
                f"Недопустимый тип зала. Допустимые: {', '.join(cls.VALID_TYPES)}"
            )
        return room_type

    @staticmethod
    def _validate_capacity(capacity: int) -> int:
        if not isinstance(capacity, int) or capacity < 1:
            raise ValueError("Вместимость зала должна быть положительным целым числом.")
        return capacity

    def __str__(self) -> str:
        return f"Зал «{self.room_name}» ({self.room_type}, до {self.capacity} чел.)"
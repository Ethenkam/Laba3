class Equipment:
    def __init__(self, equipment_id, room_id, name, type, is_available=True):
        self.equipment_id = equipment_id
        self.name = name
        self.room_id = room_id
        self.type = type
        self.is_available = is_available

    @staticmethod
    def _validate_equipment_id(equipment_id: int) -> int:
        if not isinstance(equipment_id, int) or equipment_id <= 0:
            raise ValueError("ID тренажера должен быть положительным целым числом.")
        return equipment_id
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
    @staticmethod
    def _validate_capacity(is_available: bool) -> bool:
        if not isinstance(is_available, bool):
            raise ValueError("Доступность тренажера должна быть True или False.")
        return is_available
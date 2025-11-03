from datetime import datetime
from classes.people import Coach
from classes.gym_room import GymRoom

class GroupClass:
    def __init__(
        self,
        class_id: int,
        class_name: str,
        coach: Coach,
        room: GymRoom,
        schedule: datetime,
        max_capacity: int = 10,
        current_attendees: int = 0,
        attendees: list = None,
    ):
        self.class_id = self._validate_id(class_id)
        self.class_name = self._validate_name(class_name)
        self.coach = coach
        self.room = room
        self.schedule = schedule
        self.max_capacity = self._validate_capacity(max_capacity)
        self.current_attendees = current_attendees
        self.attendees = attendees if attendees is not None else []

    @staticmethod
    def _validate_id(class_id: int) -> int:
        if not isinstance(class_id, int) or class_id <= 0:
            raise ValueError("ID занятия должен быть положительным целым числом.")
        return class_id

    @staticmethod
    def _validate_name(name: str) -> str:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Название занятия не может быть пустым.")
        return name.strip()

    @staticmethod
    def _validate_capacity(cap: int) -> int:
        if not isinstance(cap, int) or cap < 1:
            raise ValueError("Макс. вместимость должна быть ≥ 8.")
        return cap

    def add_attendee(self, member_id) -> bool:
        if self.current_attendees < self.max_capacity:
            self.current_attendees += 1
            self.attendees.append(member_id)
            return True
        return False

    def get_available_spots(self) -> int:
        return self.max_capacity - self.current_attendees

    def __str__(self) -> str:
        return (
            f"{self.class_name} | "
            f"тренер: {self.coach.get_full_name()} | "
            f"зал: {self.room.room_name} | "
            f"{self.schedule.strftime('%d.%m.%Y %H:%M')} | "
            f"мест: {self.max_capacity-self.current_attendees}/{self.max_capacity}"
            f"участники: {self.attendees}"
        )
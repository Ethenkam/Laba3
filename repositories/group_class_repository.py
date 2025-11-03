# repositories/group_class_repository.py
import json
import os
from datetime import datetime
from typing import List
from classes.group_class import GroupClass
from repositories.coach_repository import CoachRepository
from repositories.gym_room_repository import GymRoomRepository

class GroupClassRepository:
    def __init__(self, filename: str = "data/group_classes.json"):
        self.filename = filename
        os.makedirs(os.path.dirname(filename), exist_ok=True)

    def _load_raw_data(self) -> List[dict]:
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Ошибка чтения group_classes.json: {e}")
            return []

    def _save_raw_data(self, data: List[dict]) -> None:
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Ошибка записи group_classes.json: {e}")

    def save(self, cls: GroupClass) -> None:
        data = self._load_raw_data()

        # Преобразуем объект в словарь
        cls_dict = {
            "class_id": cls.class_id,
            "class_name": cls.class_name,
            "coach_id": cls.coach.id,
            "room_id": cls.room.room_id,
            "schedule": cls.schedule.isoformat(),  # ISO 8601
            "max_capacity": cls.max_capacity,
            "current_attendees": cls.current_attendees,
            "attendees": cls.attendees,
        }

        # Обновляем существующий или добавляем новый
        updated = False
        for i, item in enumerate(data):
            if item["class_id"] == cls.class_id:
                data[i] = cls_dict
                updated = True
                break

        if not updated:
            data.append(cls_dict)

        self._save_raw_data(data)
        print(f"Занятие '{cls.class_name}' сохранено.")

    def find_all(self) -> List[GroupClass]:
        data = self._load_raw_data()
        classes = []

        # Загружаем зависимости
        coach_repo = CoachRepository()
        room_repo = GymRoomRepository()
        coaches = {c.id: c for c in coach_repo.find_all()}  # dict по id
        rooms = {r.room_id: r for r in room_repo.find_all()}  # dict по room_id

        for item in data:
            try:
                # Проверка наличия обязательных полей
                required_fields = [
                    "class_id", "class_name", "coach_id", "room_id",
                    "schedule", "max_capacity", "current_attendees"
                ]
                for field in required_fields:
                    if field not in item:
                        raise KeyError(f"Отсутствует обязательное поле: {field}")

                coach = coaches.get(item["coach_id"])
                room = rooms.get(item["room_id"])

                if coach is None:
                    print(f"Тренер с ID {item['coach_id']} не найден для занятия {item['class_id']}")
                    continue
                if room is None:
                    print(f"Зал с ID {item['room_id']} не найден для занятия {item['class_id']}")
                    continue

                group_class = GroupClass(
                    class_id=item["class_id"],
                    class_name=item["class_name"],
                    coach=coach,
                    room=room,
                    schedule=datetime.fromisoformat(item["schedule"]),
                    max_capacity=item["max_capacity"],
                    current_attendees=item["current_attendees"],
                    attendees=item.get("attendees", [])
                )
                classes.append(group_class)

            except (KeyError, ValueError) as e:
                print(f"Рекорректная запись занятия: {e}")
                continue

        return classes

    def find_by_id(self, class_id: int) -> GroupClass|None:
        for cls in self.find_all():
            if cls.class_id == class_id:
                return cls
        return None

    def delete(self, class_id: int) -> bool:
        data = self._load_raw_data()
        for i, item in enumerate(data):
            if item["class_id"] == class_id:
                del data[i]
                self._save_raw_data(data)
                print(f"Групповое занятие с ID {class_id} удалено.")
                return True
        return False

import json
import os
from decimal import Decimal
from typing import List
from classes.people import Coach

class CoachRepository:
    def __init__(self, filename: str = "data/coaches.json"):
        self.filename = filename
        os.makedirs(os.path.dirname(filename), exist_ok=True)

    def _load_raw_data(self) -> List[dict]:
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Ошибка чтения coaches.json: {e}")
            return []

    def _save_raw_data(self, data: List[dict]) -> None:
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Ошибка записи coaches.json: {e}")

    def save(self, coach: Coach) -> None:
        data = self._load_raw_data()

        coach_dict = {
            "id": coach.id,
            "first_name": coach.first_name,
            "last_name": coach.last_name,
            "email": coach.email,
            "phone": coach.phone,
            "specialization": coach.specialization,
            "hourly_rate": str(coach.hourly_rate),  # Decimal → str
            "is_active": coach.is_active
        }

        updated = False
        for i, item in enumerate(data):
            if item["id"] == coach.id:
                data[i] = coach_dict
                updated = True
                break

        if not updated:
            data.append(coach_dict)

        self._save_raw_data(data)
        print(f"Тренер '{coach.get_full_name()}' сохранён.")

    def find_all(self) -> List[Coach]:
        data = self._load_raw_data()
        coaches = []
        for item in data:
            try:
                coach = Coach(
                    id=item["id"],
                    first_name=item["first_name"],
                    last_name=item["last_name"],
                    email=item["email"],
                    phone=item["phone"],
                    specialization=item["specialization"],
                    hourly_rate=Decimal(item["hourly_rate"])
                )
                coach.is_active = item.get("is_active", True)
                coaches.append(coach)
            except (KeyError, ValueError) as e:
                print(f"некорректный тренер: {e}")
                continue
        return coaches

    def find_by_id(self, coach_id: int) -> Coach | None:
        for coach in self.find_all():
            if coach.id == coach_id:
                return coach
        return None

    def delete(self, coach_id: int) -> bool:
        data = self._load_raw_data()
        for i, item in enumerate(data):
            if item["id"] == coach_id:
                del data[i]
                self._save_raw_data(data)
                print(f"Тренер с ID {coach_id} удалён.")
                return True
        return False

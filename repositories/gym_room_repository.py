# repositories/gym_room_repository.py
import json
import os
from typing import List
from classes.gym_room import GymRoom

class GymRoomRepository:
    def __init__(self, filename: str = "data/gym_rooms.json"):
        self.filename = filename
        os.makedirs(os.path.dirname(filename), exist_ok=True)

    def _load_raw_data(self) -> List[dict]:
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Ошибка чтения gym_rooms.json: {e}")
            return []

    def _save_raw_data(self, data: List[dict]) -> None:
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Ошибка записи gym_rooms.json: {e}")

    def save(self, room: GymRoom) -> None:
        data = self._load_raw_data()

        room_dict = {
            "room_id": room.room_id,
            "room_name": room.room_name,
            "room_type": room.room_type,
            "capacity": room.capacity
        }

        updated = False
        for i, item in enumerate(data):
            if item["room_id"] == room.room_id:
                data[i] = room_dict
                updated = True
                break

        if not updated:
            data.append(room_dict)

        self._save_raw_data(data)
        print(f"Зал «{room.room_name}» сохранён.")

    def find_all(self) -> List[GymRoom]:
        data = self._load_raw_data()
        rooms = []
        for item in data:
            try:
                room = GymRoom(
                    room_id=item["room_id"],
                    room_name=item["room_name"],
                    room_type=item["room_type"],
                    capacity=item["capacity"]
                )
                rooms.append(room)
            except (KeyError, ValueError) as e:
                print(f"Hекорректный зал: {e}")
                continue
        return rooms

    def find_by_id(self, room_id: int) -> GymRoom | None:
        for room in self.find_all():
            if room.room_id == room_id:
                return room
        return None

    def delete(self, room_id: int) -> bool:
        data = self._load_raw_data()
        for i, item in enumerate(data):
            if item["room_id"] == room_id:
                del data[i]
                self._save_raw_data(data)
                print(f"Зал с ID {room_id} удалён.")
                return True
        return False

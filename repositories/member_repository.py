from typing import List, Optional
import json
import os
from datetime import date
from classes.people import Member


class MemberRepository:
    def __init__(self, filename: str = 'data/members.json'):
        self.filename = filename
        os.makedirs(os.path.dirname(filename), exist_ok=True)

    def _load(self) -> List:
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    return []
                return json.loads(content)
        except json.JSONDecodeError:
            return []

    def _save(self, members: List):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(members, f, indent=2, ensure_ascii=False)

    def save(self, member: Member) -> None:
        data = self._load()
        member_dict = {
            "id": member.id,
            "first_name": member.first_name,
            "last_name": member.last_name,
            "email": member.email,
            "phone": member.phone,
            "membership_start": member.membership_start_date.isoformat() if member.membership_start_date else None,
            "membership_end": member.membership_end_date.isoformat() if member.membership_end_date else None,
            "is_active": member.is_active,
        }

        # Проверяем, существует ли член с таким ID
        updated = False
        for i, m in enumerate(data):
            if m["id"] == member.id:
                data[i] = member_dict
                updated = True
                break

        # Если члена нет, добавляем нового
        if not updated:
            data.append(member_dict)

        # Сохраняем обновленные данные
        self._save(data)

    def get_all(self) -> List[Member]:
        data = self._load()
        members = []
        for item in data:
            m = Member(
                id=item["id"],
                first_name=item["first_name"],
                last_name=item["last_name"],
                email=item["email"],
                phone=item["phone"],
                membership_start_date=date.fromisoformat(item["membership_start"]) if item["membership_start"] else None,
                membership_end_date=date.fromisoformat(item["membership_end"]) if item["membership_end"] else None,
                is_active=item["is_active"]
            )
            members.append(m)
        return members

    def get_by_id(self, member_id: int) -> Optional[Member]:
        for m in self.get_all():
            if m.id == member_id:
                return m
        return None

    def delete(self, member_id: int) -> bool:
        data = self._load()
        for i, item in enumerate(data):
            if item["id"] == member_id:
                del data[i]
                self._save(data)
                return True
        return False
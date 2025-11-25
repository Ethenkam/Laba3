import json
import os
from typing import List, Dict, Union
from classes.Membership_plan import MembershipPlan

class MembershipPlanRepository:
    def __init__(self, filename: str = "data/membership_plans.json"):
        self.filename = filename
        os.makedirs(os.path.dirname(filename), exist_ok=True)

    def _load(self) -> List[Dict]:
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return []
                return json.loads(content)
        except json.JSONDecodeError:
            return []

    def _save(self, data: List[Dict]) -> None:
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def save(self, plan: MembershipPlan) -> None:
        data = self._load()
        plan_dict = {
            "plan_id": plan.plan_id,
            "name": plan.name,
            "duration_days": plan.duration_days,
            "price": plan.price
        }
        updated = False
        for i, item in enumerate(data):
            if item["plan_id"] == plan.plan_id:
                data[i] = plan_dict
                updated = True
                break
        if not updated:
            data.append(plan_dict)
        self._save(data)

    def find_all(self) -> List[MembershipPlan]:
        data = self._load()
        plans = []
        for item in data:
            try:
                plan = MembershipPlan(
                    plan_id=item["plan_id"],
                    name=item["name"],
                    duration_days=item["duration_days"],
                    price=item["price"]
                )
                plans.append(plan)
            except (KeyError, ValueError) as e:
                print(f"Hекорректный план: {e}")
                continue
        return plans

    def find_by_id(self, plan_id: int) -> MembershipPlan | None:
        for plan in self.find_all():
            if plan.plan_id == plan_id:
                return plan
        return None

    def delete(self, plan_id: int) -> bool:
        data = self._load()
        for i, item in enumerate(data):
            if item["plan_id"] == plan_id:
                del data[i]
                self._save(data)
                return True
        return False
# repositories/payment_repository.py
import json
import os
from datetime import date
from typing import List
from classes.Payment import Payment

class PaymentRepository:
    def __init__(self, filename: str = "data/payments.json"):
        self.filename = filename
        os.makedirs(os.path.dirname(filename), exist_ok=True)

    def _load(self) -> List[dict]:
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self,  data: List[dict]) -> None:
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def save(self, payment: Payment) -> None:
        data = self._load()
        payment_dict = {
            "payment_id": payment.payment_id,
            "member_id": payment.member_id,
            "plan_id": payment.plan_id,
            "amount": payment.amount,
            "payment_date": payment.payment_date.isoformat(),
        }
        data.append(payment_dict)  # Платежи обычно не обновляют, только добавляют
        self._save(data)

    def find_all(self) -> List[Payment]:
        data = self._load()
        payments = []
        for item in data:
            try:
                payment = Payment(
                    payment_id=item["payment_id"],
                    member_id=item["member_id"],
                    plan_id=item["plan_id"],
                    amount=item["amount"],
                    payment_date=date.fromisoformat(item["payment_date"]),
                )
                payments.append(payment)
            except (KeyError, ValueError) as e:
                print(f"Неправильный платёж {e}")
                continue
        return payments

    def find_by_member_id(self, member_id: int) -> List[Payment]:
        return [p for p in self.find_all() if p.member_id == member_id]

    def delete(self, payment_id: int) -> bool:
        data = self._load()
        for i, item in enumerate(data):
            if item["payment_id"] == payment_id:
                del data[i]
                self._save(data)
                return True
        return False

class MembershipPlan:
    def __init__(self, plan_id: int, name: str, duration_days: int, price: int):
        self.plan_id = self._validate_id(plan_id)
        self.name = self._validate_name(name)
        self.duration_days = self._validate_duration(duration_days)
        self.price = self._validate_price(price)

    @staticmethod
    def _validate_id(plan_id: int) -> int:
        if not isinstance(plan_id, int) or plan_id <= 0:
            raise ValueError("ID плана должен быть положительным целым числом.")
        return plan_id

    @staticmethod
    def _validate_name(name: str) -> str:
        if not isinstance(name, str) or len(name)==0:
            raise ValueError("Название плана не может быть пустым.")
        return name.strip()

    @staticmethod
    def _validate_duration(days: int) -> int:
        if not isinstance(days, int) or days <= 0:
            raise ValueError("Длительность должна быть положительным целым числом (в днях).")
        return days

    @staticmethod
    def _validate_price(price: int) -> int:
        if not isinstance(price, int) or price < 0:
            raise ValueError("Цена не может быть отрицательной.")
        return price

    def __str__(self) -> str:
        return f"Абонемент «{self.name}» ({self.duration_days} дней, {self.price} руб.)"
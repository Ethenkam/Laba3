from datetime import date
class Payment:

    def __init__(
        self,
        payment_id: int,
        member_id: int,
        plan_id: int,
        amount: int,
        payment_date: date,
    ):
        self.payment_id = self._validate_id(payment_id)
        self.member_id = self._validate_member_id(member_id)
        self.plan_id = self._validate_plan_id(plan_id)
        self.amount = self._validate_amount(amount)
        self.payment_date = self._validate_date(payment_date)

    @staticmethod
    def _validate_id(payment_id: int) -> int:
        if not isinstance(payment_id, int) or payment_id <= 0:
            raise ValueError("ID платежа должен быть положительным целым числом.")
        return payment_id

    @staticmethod
    def _validate_member_id(member_id: int) -> int:
        if not isinstance(member_id, int) or member_id <= 0:
            raise ValueError("ID участника должен быть положительным целым числом.")
        return member_id

    @staticmethod
    def _validate_plan_id(plan_id: int) -> int:
        if not isinstance(plan_id, int) or plan_id <= 0:
            raise ValueError("ID плана должен быть положительным целым числом.")
        return plan_id

    @staticmethod
    def _validate_amount(amount: int) -> int:
        if not isinstance(amount, int) or amount <= 0:
            raise ValueError("Сумма платежа должна быть положительной.")
        return amount

    @staticmethod
    def _validate_date(d: date) -> date:
        if not isinstance(d, date):
            raise ValueError("Дата платежа должна быть объектом datetime.date.")
        return d

    def __str__(self) -> str:
        return (
            f"Платёж #{self.payment_id} | "
            f"участник: {self.member_id} | "
            f"сумма: {self.amount} руб. | "
            f"дата: {self.payment_date} | "
        )
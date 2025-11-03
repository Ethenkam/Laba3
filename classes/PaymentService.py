from datetime import date, timedelta
from repositories.member_repository import MemberRepository
from repositories.payment_repository import PaymentRepository
from classes.Payment import Payment


class PaymentService:
    def __init__(self, member_repo: MemberRepository, payment_repo: PaymentRepository):
        self.member_repo = member_repo
        self.payment_repo = payment_repo

    def purchase_membership(self, member_id: int, plan, payment_id: int) -> bool:
        try:
            member = self.member_repo.get_by_id(member_id)
            if not member:
                print(f"Участник с ID {member_id} не найден.")
                return False

            payment = Payment(
                payment_id=payment_id,
                member_id=member_id,
                plan_id=plan.plan_id,
                amount=plan.price,
                payment_date=date.today()
            )
            self.payment_repo.save(payment)
            print(f"Платёж #{payment_id} создан: {plan.price} руб.")
            member.membership_start_date = date.today()
            member.membership_end_date = date.today() + timedelta(days=plan.duration_days)
            member.is_active = True
            self.member_repo.save(member)
            print(f"Абонемент активирован до: {member.membership_end_date}")

            return True

        except Exception as e:
            print(f"Ошибка при покупке абонемента: {e}")
            return False# services/payment_service.py

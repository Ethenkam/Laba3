from datetime import date, datetime, timedelta
from decimal import Decimal
from classes.PaymentService import PaymentService

from classes.people import Member, Coach
from classes.gym_room import GymRoom
from classes.group_class import GroupClass
from classes.Membership_plan import MembershipPlan
from classes.Payment import Payment

from repositories.member_repository import MemberRepository
from repositories.coach_repository import CoachRepository
from repositories.gym_room_repository import GymRoomRepository
from repositories.group_class_repository import GroupClassRepository
from repositories.membership_plan_repository import MembershipPlanRepository
from repositories.payment_repository import PaymentRepository
member_repo = MemberRepository()
new_member = Member(
    id=1,
    first_name="Sagal",
    last_name="Sosovich",
    email="SagalSosovich@gmail.com",
    phone="79553828498",
    membership_start_date=date.today(),
    membership_end_date=date.today() - timedelta(days=1),
    is_active=False
)
member_repo.save(new_member)
for member in member_repo.get_all():
    print(member)
plan_repo = MembershipPlanRepository()
plans = plan_repo.find_all()
chosen_plan = plans[0]
payment_repo = PaymentRepository()
payment_service = PaymentService(member_repo, payment_repo)
success = payment_service.purchase_membership(
    member_id=new_member.id,
    plan=chosen_plan,
    payment_id=1
)
for m in member_repo.get_all():
    status = "активен" if m.is_active else "неактивен"
    print(f"  - {m.get_full_name()} | {status} | абонемент до: {m.membership_end_date}")
print("\nПоследние платежи:")
for p in payment_repo.find_all()[-3:]:
        print(f"  - {p}")
group_repo = GroupClassRepository()
coach_repo = CoachRepository()
room_repo = GymRoomRepository()
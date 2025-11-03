from repositories.member_repository import MemberRepository
from repositories.coach_repository import CoachRepository
from repositories.gym_room_repository import GymRoomRepository
from repositories.group_class_repository import GroupClassRepository
from repositories.membership_plan_repository import MembershipPlanRepository
from repositories.payment_repository import PaymentRepository

from Import import test_import

print("Проверка работоспособности импорта XML:")
success = test_import()

if success:
    print("\nВывод информации о клубе после импорта:")
    
    member_repo = MemberRepository()
    print("\nУчастники:")
    for member in member_repo.get_all():
        print(f"- {member.get_full_name()}, активен: {member.is_active}")

    plan_repo = MembershipPlanRepository()
    plans = plan_repo.find_all()
    print("\nАбонементы:")
    for plan in plans:
        print(f"- {plan.name}: {plan.price} руб.")

    payment_repo = PaymentRepository()
    coach_repo = CoachRepository()
    room_repo = GymRoomRepository()
    group_repo = GroupClassRepository()

    print("\nПоследние платежи:")
    for p in payment_repo.find_all()[-3:]:
        print(f"- {p}")

    print("\nТренеры:")
    for coach in coach_repo.find_all():
        print(f"- {coach.get_full_name()}, специализация: {coach.specialization}")

    print("\nЗалы:")
    for room in room_repo.find_all():
        print(f"- {room.room_name}, тип: {room.room_type}, вместимость: {room.capacity}")

    print("\nГрупповые занятия:")
    for clas in group_repo.find_all():
        print(f"- {clas.class_name} ({clas.schedule.strftime('%d.%m.%Y %H:%M')})")
else:
    print("Импорт не выполнен, проверка данных невозможна")
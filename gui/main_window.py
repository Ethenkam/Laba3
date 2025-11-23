import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QStatusBar, QToolBar, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon

from gui.members_tab import MembersTab
from gui.classes_tab import ClassesTab
from gui.coaches_tab import CoachesTab
from gui.rooms_tab import RoomsTab
from gui.plans_tab import PlansTab
from gui.reports_tab import ReportsTab

from repositories.member_repository import MemberRepository
from repositories.coach_repository import CoachRepository
from repositories.gym_room_repository import GymRoomRepository
from repositories.group_class_repository import GroupClassRepository
from repositories.membership_plan_repository import MembershipPlanRepository
from repositories.payment_repository import PaymentRepository


class GymManagementSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Система управления фитнес-клубом")
        self.setGeometry(100, 100, 1200, 800)

        self.member_repo = MemberRepository()
        self.coach_repo = CoachRepository()
        self.room_repo = GymRoomRepository()
        self.group_class_repo = GroupClassRepository()
        self.plan_repo = MembershipPlanRepository()
        self.payment_repo = PaymentRepository()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self.create_toolbar()
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        self.create_status_bar()
        self.create_tabs()
        self.ensure_data_exists()

    def create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        
        # Refresh action
        refresh_action = QAction("Обновить данные", self)
        refresh_action.setStatusTip("Обновить все таблицы")
        refresh_action.triggered.connect(self.refresh_all_tables)
        toolbar.addAction(refresh_action)
        
        # Export action
        export_action = QAction("Экспорт в CSV", self)
        export_action.setStatusTip("Экспортировать данные в CSV файл")
        export_action.triggered.connect(self.export_to_csv)
        toolbar.addAction(export_action)

    def create_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Готов", 2000)

    def create_tabs(self):
        # Create all tabs
        self.members_tab = MembersTab(self.member_repo, self.plan_repo, self.payment_repo)
        self.classes_tab = ClassesTab(self.group_class_repo, self.coach_repo, self.room_repo, self.member_repo)
        self.coaches_tab = CoachesTab(self.coach_repo)
        self.rooms_tab = RoomsTab(self.room_repo)
        self.plans_tab = PlansTab(self.plan_repo)
        self.reports_tab = ReportsTab(self.payment_repo, self.member_repo, self.plan_repo)

        # Add tabs to the tab widget
        self.tabs.addTab(self.members_tab, "Участники")
        self.tabs.addTab(self.classes_tab, "Занятия")
        self.tabs.addTab(self.coaches_tab, "Тренеры")
        self.tabs.addTab(self.rooms_tab, "Залы")
        self.tabs.addTab(self.plans_tab, "Абонементы")
        self.tabs.addTab(self.reports_tab, "Отчеты")

        # Refresh all tables
        self.refresh_all_tables()

    def ensure_data_exists(self):
        if not self.plan_repo.find_all():
            from classes.Membership_plan import MembershipPlan
            from decimal import Decimal
            self.plan_repo.save(MembershipPlan(1, "Базовый (10 мес)", 300, 34800))
            self.plan_repo.save(MembershipPlan(2, "Премиум (14 мес)", 420, 41200))

        if not self.coach_repo.find_all():
            from classes.people import Coach
            from decimal import Decimal
            coach = Coach(1, "Иван", "Сидоров", "ivan@fit.com", "79998887766", "Кардио", Decimal("2000.00"))
            self.coach_repo.save(coach)

        if not self.room_repo.find_all():
            from classes.gym_room import GymRoom
            room = GymRoom(1, "Зал для кардио", "кардио", 15)
            self.room_repo.save(room)

    def refresh_all_tables(self):
        self.members_tab.refresh_members_table()
        self.classes_tab.refresh_classes_table()
        self.coaches_tab.refresh_coaches_table()
        self.rooms_tab.refresh_rooms_table()
        self.plans_tab.refresh_plans_table()
        self.reports_tab.refresh_payments_table()
        self.status_bar.showMessage("Все таблицы обновлены", 2000)

    def export_to_csv(self):
        """Placeholder for CSV export functionality"""
        QMessageBox.information(self, "Экспорт в CSV", 
                                "Функция экспорта в CSV будет реализована в следующей версии.\n\n"
                                "Будет экспортированы все данные из текущей вкладки в формате CSV.")


def main():
    app = QApplication(sys.argv)
    window = GymManagementSystem()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
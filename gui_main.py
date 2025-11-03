import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QTabWidget, QTableWidget, QTableWidgetItem,
    QLineEdit, QDateEdit, QCheckBox, QMessageBox, QGroupBox, QFormLayout,
    QTextEdit, QDateTimeEdit
)
from PyQt6.QtCore import Qt, QDate, QDateTime
from datetime import date, datetime
from decimal import Decimal

from classes.people import Member, Coach
from classes.gym_room import GymRoom
from classes.group_class import GroupClass
from classes.Membership_plan import MembershipPlan
from classes.PaymentService import PaymentService
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
        self.setGeometry(100, 100, 1000, 700)

        self.member_repo = MemberRepository()
        self.coach_repo = CoachRepository()
        self.room_repo = GymRoomRepository()
        self.group_class_repo = GroupClassRepository()
        self.plan_repo = MembershipPlanRepository()
        self.payment_repo = PaymentRepository()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        self.create_members_tab()
        self.create_classes_tab()
        self.create_coaches_tab()
        self.create_rooms_tab()
        self.create_plans_tab()
        self.create_reports_tab()

        self.ensure_data_exists()

        self.refresh_all_tables()

    def ensure_data_exists(self):
        if not self.plan_repo.find_all():
            self.plan_repo.save(MembershipPlan(1, "Базовый (10 мес)", 300, 34800))
            self.plan_repo.save(MembershipPlan(2, "Премиум (14 мес)", 420, 41200))

        if not self.coach_repo.find_all():
            coach = Coach(1, "Иван", "Сидоров", "ivan@fit.com", "79998887766", "Кардио", Decimal("2000.00"))
            self.coach_repo.save(coach)

        if not self.room_repo.find_all():
            room = GymRoom(1, "Зал для кардио", "кардио", 15)
            self.room_repo.save(room)

    def create_members_tab(self):
        members_tab = QWidget()
        layout = QVBoxLayout(members_tab)
        
        # Members table
        self.members_table = QTableWidget()
        self.members_table.setColumnCount(8)
        self.members_table.setHorizontalHeaderLabels([
            "ID", "Имя", "Фамилия", "Email", "Телефон", 
            "Дата начала", "Дата окончания", "Активен"
        ])
        layout.addWidget(QLabel("Участники:"))
        layout.addWidget(self.members_table)
        
        # Member form
        form_group = QGroupBox("Добавить/Редактировать участника")
        form_layout = QFormLayout()
        
        self.member_id_edit = QLineEdit()
        self.member_first_name_edit = QLineEdit()
        self.member_last_name_edit = QLineEdit()
        self.member_email_edit = QLineEdit()
        self.member_phone_edit = QLineEdit()
        self.member_start_date_edit = QDateEdit()
        self.member_start_date_edit.setDate(QDate.currentDate())
        self.member_end_date_edit = QDateEdit()
        self.member_end_date_edit.setDate(QDate.currentDate())
        self.member_active_checkbox = QCheckBox()
        
        form_layout.addRow("ID:", self.member_id_edit)
        form_layout.addRow("Имя:", self.member_first_name_edit)
        form_layout.addRow("Фамилия:", self.member_last_name_edit)
        form_layout.addRow("Email:", self.member_email_edit)
        form_layout.addRow("Телефон:", self.member_phone_edit)
        form_layout.addRow("Дата начала:", self.member_start_date_edit)
        form_layout.addRow("Дата окончания:", self.member_end_date_edit)
        form_layout.addRow("Активен:", self.member_active_checkbox)
        
        buttons_layout = QHBoxLayout()
        self.add_member_btn = QPushButton("Добавить участника")
        self.add_member_btn.clicked.connect(self.add_member)
        self.update_member_btn = QPushButton("Обновить участника")
        self.update_member_btn.clicked.connect(self.update_member)
        self.delete_member_btn = QPushButton("Удалить участника")
        self.delete_member_btn.clicked.connect(self.delete_member)
        self.clear_member_form_btn = QPushButton("Очистить форму")
        self.clear_member_form_btn.clicked.connect(self.clear_member_form)
        
        buttons_layout.addWidget(self.add_member_btn)
        buttons_layout.addWidget(self.update_member_btn)
        buttons_layout.addWidget(self.delete_member_btn)
        buttons_layout.addWidget(self.clear_member_form_btn)
        
        form_layout.addRow(buttons_layout)
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        self.tabs.addTab(members_tab, "Участники")

    def create_classes_tab(self):
        classes_tab = QWidget()
        layout = QVBoxLayout(classes_tab)
        
        # Classes table
        self.classes_table = QTableWidget()
        self.classes_table.setColumnCount(7)
        self.classes_table.setHorizontalHeaderLabels([
            "ID", "Название", "Тренер", "Зал", "Дата/время", "Вместимость", "Участники"
        ])
        layout.addWidget(QLabel("Групповые занятия:"))
        layout.addWidget(self.classes_table)
        
        # Class form
        form_group = QGroupBox("Добавить/Редактировать занятие")
        form_layout = QFormLayout()
        
        self.class_id_edit = QLineEdit()
        self.class_name_edit = QLineEdit()
        self.class_coach_combo = QLineEdit()  # In a full implementation, this would be a combo box
        self.class_room_combo = QLineEdit()   # In a full implementation, this would be a combo box
        self.class_datetime_edit = QDateTimeEdit()
        self.class_datetime_edit.setDateTime(QDateTime.currentDateTime())
        self.class_capacity_edit = QLineEdit()
        
        form_layout.addRow("ID:", self.class_id_edit)
        form_layout.addRow("Название:", self.class_name_edit)
        form_layout.addRow("Тренер (ID):", self.class_coach_combo)
        form_layout.addRow("Зал (ID):", self.class_room_combo)
        form_layout.addRow("Дата/время:", self.class_datetime_edit)
        form_layout.addRow("Вместимость:", self.class_capacity_edit)
        
        buttons_layout = QHBoxLayout()
        self.add_class_btn = QPushButton("Добавить занятие")
        self.add_class_btn.clicked.connect(self.add_class)
        self.update_class_btn = QPushButton("Обновить занятие")
        self.update_class_btn.clicked.connect(self.update_class)
        self.delete_class_btn = QPushButton("Удалить занятие")
        self.delete_class_btn.clicked.connect(self.delete_class)
        self.clear_class_form_btn = QPushButton("Очистить форму")
        self.clear_class_form_btn.clicked.connect(self.clear_class_form)
        
        buttons_layout.addWidget(self.add_class_btn)
        buttons_layout.addWidget(self.update_class_btn)
        buttons_layout.addWidget(self.delete_class_btn)
        buttons_layout.addWidget(self.clear_class_form_btn)
        
        form_layout.addRow(buttons_layout)
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        self.tabs.addTab(classes_tab, "Занятия")

    def create_coaches_tab(self):
        coaches_tab = QWidget()
        layout = QVBoxLayout(coaches_tab)
        
        # Coaches table
        self.coaches_table = QTableWidget()
        self.coaches_table.setColumnCount(7)
        self.coaches_table.setHorizontalHeaderLabels([
            "ID", "Имя", "Фамилия", "Email", "Телефон", "Специализация", "Ставка"
        ])
        layout.addWidget(QLabel("Тренеры:"))
        layout.addWidget(self.coaches_table)
        
        self.tabs.addTab(coaches_tab, "Тренеры")

    def create_rooms_tab(self):
        rooms_tab = QWidget()
        layout = QVBoxLayout(rooms_tab)
        
        # Rooms table
        self.rooms_table = QTableWidget()
        self.rooms_table.setColumnCount(4)
        self.rooms_table.setHorizontalHeaderLabels([
            "ID", "Название", "Тип", "Вместимость"
        ])
        layout.addWidget(QLabel("Залы:"))
        layout.addWidget(self.rooms_table)
        
        self.tabs.addTab(rooms_tab, "Залы")

    def create_plans_tab(self):
        plans_tab = QWidget()
        layout = QVBoxLayout(plans_tab)
        
        # Plans table
        self.plans_table = QTableWidget()
        self.plans_table.setColumnCount(4)
        self.plans_table.setHorizontalHeaderLabels([
            "ID", "Название", "Длительность (дни)", "Цена"
        ])
        layout.addWidget(QLabel("Абонементы:"))
        layout.addWidget(self.plans_table)
        
        self.tabs.addTab(plans_tab, "Абонементы")

    def create_reports_tab(self):
        reports_tab = QWidget()
        layout = QVBoxLayout(reports_tab)
        
        # Payments table
        self.payments_table = QTableWidget()
        self.payments_table.setColumnCount(4)
        self.payments_table.setHorizontalHeaderLabels([
            "ID", "Участник", "Абонемент", "Сумма"
        ])
        layout.addWidget(QLabel("Платежи:"))
        layout.addWidget(self.payments_table)
        
        self.tabs.addTab(reports_tab, "Отчеты")

    def refresh_all_tables(self):
        self.refresh_members_table()
        self.refresh_classes_table()
        self.refresh_coaches_table()
        self.refresh_rooms_table()
        self.refresh_plans_table()
        self.refresh_payments_table()

    def refresh_members_table(self):
        members = self.member_repo.get_all()
        self.members_table.setRowCount(len(members))
        
        for row, member in enumerate(members):
            self.members_table.setItem(row, 0, QTableWidgetItem(str(member.id)))
            self.members_table.setItem(row, 1, QTableWidgetItem(member.first_name))
            self.members_table.setItem(row, 2, QTableWidgetItem(member.last_name))
            self.members_table.setItem(row, 3, QTableWidgetItem(member.email))
            self.members_table.setItem(row, 4, QTableWidgetItem(member.phone))
            
            start_date = member.membership_start_date.strftime("%d.%m.%Y") if member.membership_start_date else ""
            self.members_table.setItem(row, 5, QTableWidgetItem(start_date))
            
            end_date = member.membership_end_date.strftime("%d.%m.%Y") if member.membership_end_date else ""
            self.members_table.setItem(row, 6, QTableWidgetItem(end_date))
            
            active_status = "Да" if member.is_active else "Нет"
            self.members_table.setItem(row, 7, QTableWidgetItem(active_status))
        
        self.members_table.resizeColumnsToContents()

    def refresh_classes_table(self):
        classes = self.group_class_repo.find_all()
        self.classes_table.setRowCount(len(classes))
        
        for row, group_class in enumerate(classes):
            self.classes_table.setItem(row, 0, QTableWidgetItem(str(group_class.class_id)))
            self.classes_table.setItem(row, 1, QTableWidgetItem(group_class.class_name))
            self.classes_table.setItem(row, 2, QTableWidgetItem(group_class.coach.get_full_name()))
            self.classes_table.setItem(row, 3, QTableWidgetItem(group_class.room.room_name))
            
            schedule = group_class.schedule.strftime("%d.%m.%Y %H:%M") if group_class.schedule else ""
            self.classes_table.setItem(row, 4, QTableWidgetItem(schedule))
            
            self.classes_table.setItem(row, 5, QTableWidgetItem(str(group_class.max_capacity)))
            self.classes_table.setItem(row, 6, QTableWidgetItem(str(len(group_class.attendees))))
        
        self.classes_table.resizeColumnsToContents()

    def refresh_coaches_table(self):
        coaches = self.coach_repo.find_all()
        self.coaches_table.setRowCount(len(coaches))
        
        for row, coach in enumerate(coaches):
            self.coaches_table.setItem(row, 0, QTableWidgetItem(str(coach.id)))
            self.coaches_table.setItem(row, 1, QTableWidgetItem(coach.first_name))
            self.coaches_table.setItem(row, 2, QTableWidgetItem(coach.last_name))
            self.coaches_table.setItem(row, 3, QTableWidgetItem(coach.email))
            self.coaches_table.setItem(row, 4, QTableWidgetItem(coach.phone))
            self.coaches_table.setItem(row, 5, QTableWidgetItem(coach.specialization))
            self.coaches_table.setItem(row, 6, QTableWidgetItem(str(coach.hourly_rate)))
        
        self.coaches_table.resizeColumnsToContents()

    def refresh_rooms_table(self):
        rooms = self.room_repo.find_all()
        self.rooms_table.setRowCount(len(rooms))
        
        for row, room in enumerate(rooms):
            self.rooms_table.setItem(row, 0, QTableWidgetItem(str(room.room_id)))
            self.rooms_table.setItem(row, 1, QTableWidgetItem(room.room_name))
            self.rooms_table.setItem(row, 2, QTableWidgetItem(room.room_type))
            self.rooms_table.setItem(row, 3, QTableWidgetItem(str(room.capacity)))
        
        self.rooms_table.resizeColumnsToContents()

    def refresh_plans_table(self):
        plans = self.plan_repo.find_all()
        self.plans_table.setRowCount(len(plans))
        
        for row, plan in enumerate(plans):
            self.plans_table.setItem(row, 0, QTableWidgetItem(str(plan.plan_id)))
            self.plans_table.setItem(row, 1, QTableWidgetItem(plan.name))
            self.plans_table.setItem(row, 2, QTableWidgetItem(str(plan.duration_days)))
            self.plans_table.setItem(row, 3, QTableWidgetItem(str(plan.price)))
        
        self.plans_table.resizeColumnsToContents()

    def refresh_payments_table(self):
        payments = self.payment_repo.find_all()
        self.payments_table.setRowCount(len(payments))
        
        for row, payment in enumerate(payments):
            self.payments_table.setItem(row, 0, QTableWidgetItem(str(payment.payment_id)))
            
            # Get member name
            member = self.member_repo.get_by_id(payment.member_id)
            member_name = member.get_full_name() if member else "Не найден"
            self.payments_table.setItem(row, 1, QTableWidgetItem(member_name))
            
            # Get plan name
            plan = self.plan_repo.find_by_id(payment.plan_id)
            plan_name = plan.name if plan else "Не найден"
            self.payments_table.setItem(row, 2, QTableWidgetItem(plan_name))
            
            self.payments_table.setItem(row, 3, QTableWidgetItem(str(payment.amount)))
        
        self.payments_table.resizeColumnsToContents()

    def add_member(self):
        try:
            member_id = int(self.member_id_edit.text()) if self.member_id_edit.text() else 0
            first_name = self.member_first_name_edit.text()
            last_name = self.member_last_name_edit.text()
            email = self.member_email_edit.text()
            phone = self.member_phone_edit.text()
            
            start_date = self.member_start_date_edit.date().toPyDate()
            end_date = self.member_end_date_edit.date().toPyDate()
            is_active = self.member_active_checkbox.isChecked()
            
            if not first_name or not last_name or not email or not phone:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все обязательные поля")
                return
            
            member = Member(
                id=member_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                membership_start_date=start_date,
                membership_end_date=end_date,
                is_active=is_active
            )
            
            self.member_repo.save(member)
            QMessageBox.information(self, "Успех", "Участник успешно добавлен")
            self.refresh_members_table()
            self.clear_member_form()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить участника: {str(e)}")

    def update_member(self):
        # For simplicity, we'll just use the same logic as add_member since save() handles both
        self.add_member()

    def delete_member(self):
        try:
            member_id = int(self.member_id_edit.text()) if self.member_id_edit.text() else 0
            if member_id <= 0:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, укажите действительный ID участника")
                return
                
            reply = QMessageBox.question(self, "Подтверждение", 
                                       f"Вы уверены, что хотите удалить участника с ID {member_id}?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            
            if reply == QMessageBox.StandardButton.Yes:
                success = self.member_repo.delete(member_id)
                if success:
                    QMessageBox.information(self, "Успех", "Участник успешно удален")
                    self.refresh_members_table()
                    self.clear_member_form()
                else:
                    QMessageBox.warning(self, "Ошибка", "Участник с указанным ID не найден")
                    
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить участника: {str(e)}")

    def clear_member_form(self):
        self.member_id_edit.clear()
        self.member_first_name_edit.clear()
        self.member_last_name_edit.clear()
        self.member_email_edit.clear()
        self.member_phone_edit.clear()
        self.member_start_date_edit.setDate(QDate.currentDate())
        self.member_end_date_edit.setDate(QDate.currentDate())
        self.member_active_checkbox.setChecked(False)

    def add_class(self):
        # Placeholder for adding class functionality
        QMessageBox.information(self, "Информация", "Функция добавления занятий будет реализована позже")

    def update_class(self):
        QMessageBox.information(self, "Информация", "Функция обновления занятий будет реализована позже")

    def delete_class(self):
        QMessageBox.information(self, "Информация", "Функция удаления занятий будет реализована позже")

    def clear_class_form(self):
        self.class_id_edit.clear()
        self.class_name_edit.clear()
        self.class_coach_combo.clear()
        self.class_room_combo.clear()
        self.class_datetime_edit.setDateTime(QDateTime.currentDateTime())
        self.class_capacity_edit.clear()


def main():
    app = QApplication(sys.argv)
    window = GymManagementSystem()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
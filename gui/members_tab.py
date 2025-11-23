from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QLineEdit, QDateEdit, QCheckBox, QMessageBox, QComboBox, QSplitter, QHeaderView
)
from PyQt6.QtCore import QDate, Qt
from datetime import date, datetime
from decimal import Decimal

from classes.people import Member
from classes.PaymentService import PaymentService


class MembersTab(QWidget):
    def __init__(self, member_repo, plan_repo, payment_repo):
        super().__init__()
        self.member_repo = member_repo
        self.plan_repo = plan_repo
        self.payment_repo = payment_repo
        self.all_members = []

        self.init_ui()
        self.setup_connections()
        self.refresh_members_table()
        self.refresh_plans_combo()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Create splitter for resizable sections
        splitter = QSplitter(Qt.Orientation.Vertical)
        layout.addWidget(splitter)

        # Top section with search and table
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)
        

        search_layout = QHBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Поиск по участникам...")
        self.search_btn = QPushButton("Поиск")
        self.clear_search_btn = QPushButton("Очистить")
        search_layout.addWidget(QLabel("Поиск:"))
        search_layout.addWidget(self.search_box)
        search_layout.addWidget(self.search_btn)
        search_layout.addWidget(self.clear_search_btn)
        top_layout.addLayout(search_layout)

        # Members table
        self.members_table = QTableWidget()
        self.members_table.setColumnCount(8)
        self.members_table.setHorizontalHeaderLabels([
            "ID", "Имя", "Фамилия", "Email", "Телефон",
            "Дата начала", "Дата окончания", "Активен"
        ])
        self.members_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        # Enable sorting
        self.members_table.setSortingEnabled(True)
        header = self.members_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        top_layout.addWidget(QLabel("Участники:"))
        top_layout.addWidget(self.members_table)
        splitter.addWidget(top_widget)

        # Bottom section with forms
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)

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
        self.update_member_btn = QPushButton("Обновить участника")
        self.delete_member_btn = QPushButton("Удалить участника")
        self.clear_member_form_btn = QPushButton("Очистить форму")

        buttons_layout.addWidget(self.add_member_btn)
        buttons_layout.addWidget(self.update_member_btn)
        buttons_layout.addWidget(self.delete_member_btn)
        buttons_layout.addWidget(self.clear_member_form_btn)

        form_layout.addRow(buttons_layout)
        form_group.setLayout(form_layout)
        bottom_layout.addWidget(form_group)

        # Purchase membership form
        purchase_group = QGroupBox("Купить абонемент")
        purchase_layout = QFormLayout()

        self.purchase_member_id_edit = QLineEdit()
        self.purchase_plan_combo = QComboBox()

        purchase_layout.addRow("ID участника:", self.purchase_member_id_edit)
        purchase_layout.addRow("Абонемент:", self.purchase_plan_combo)

        self.purchase_btn = QPushButton("Купить абонемент")
        purchase_layout.addRow(self.purchase_btn)

        purchase_group.setLayout(purchase_layout)
        bottom_layout.addWidget(purchase_group)
        
        splitter.addWidget(bottom_widget)
        splitter.setSizes([400, 400])  # Set initial sizes

    def setup_connections(self):
        self.add_member_btn.clicked.connect(self.add_member)
        self.update_member_btn.clicked.connect(self.update_member)
        self.delete_member_btn.clicked.connect(self.delete_member)
        self.clear_member_form_btn.clicked.connect(self.clear_member_form)
        self.purchase_btn.clicked.connect(self.purchase_membership)
        self.search_btn.clicked.connect(self.search_members)
        self.clear_search_btn.clicked.connect(self.clear_search)
        self.members_table.itemClicked.connect(self.populate_form_from_table)

    def populate_form_from_table(self, item):
        row = item.row()
        self.member_id_edit.setText(self.members_table.item(row, 0).text())
        self.member_first_name_edit.setText(self.members_table.item(row, 1).text())
        self.member_last_name_edit.setText(self.members_table.item(row, 2).text())
        self.member_email_edit.setText(self.members_table.item(row, 3).text())
        self.member_phone_edit.setText(self.members_table.item(row, 4).text())
        
        start_date_str = self.members_table.item(row, 5).text()
        if start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, "%d.%m.%Y").date()
                self.member_start_date_edit.setDate(QDate(start_date.year, start_date.month, start_date.day))
            except ValueError:
                pass
                
        end_date_str = self.members_table.item(row, 6).text()
        if end_date_str:
            try:
                end_date = datetime.strptime(end_date_str, "%d.%m.%Y").date()
                self.member_end_date_edit.setDate(QDate(end_date.year, end_date.month, end_date.day))
            except ValueError:
                pass
        
        is_active = self.members_table.item(row, 7).text() == "Да"
        self.member_active_checkbox.setChecked(is_active)

    def search_members(self):
        search_term = self.search_box.text().lower()
        if not search_term:
            self.refresh_members_table()
            return
            
        filtered_members = []
        for member in self.all_members:
            if (search_term in str(member.id) or 
                search_term in member.first_name.lower() or 
                search_term in member.last_name.lower() or 
                search_term in member.email.lower() or 
                search_term in member.phone.lower()):
                filtered_members.append(member)
                
        self.display_members(filtered_members)

    def clear_search(self):
        self.search_box.clear()
        self.refresh_members_table()

    def display_members(self, members):
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

    def refresh_members_table(self):
        self.all_members = self.member_repo.get_all()
        self.display_members(self.all_members)

    def refresh_plans_combo(self):
        plans = self.plan_repo.find_all()
        self.purchase_plan_combo.clear()
        for plan in plans:
            self.purchase_plan_combo.addItem(f"{plan.name} ({plan.price} руб.)", plan.plan_id)

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

    def purchase_membership(self):
        try:
            member_id = int(self.purchase_member_id_edit.text()) if self.purchase_member_id_edit.text() else 0
            plan_id = self.purchase_plan_combo.currentData()

            if member_id <= 0:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, укажите действительный ID участника")
                return

            if not plan_id:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите абонемент")
                return

            # Get member and plan
            member = self.member_repo.get_by_id(member_id)
            plan = self.plan_repo.find_by_id(plan_id)

            if not member:
                QMessageBox.warning(self, "Ошибка", f"Участник с ID {member_id} не найден")
                return

            if not plan:
                QMessageBox.warning(self, "Ошибка", f"Абонемент с ID {plan_id} не найден")
                return

            # Create payment service and process purchase
            payment_service = PaymentService(self.member_repo, self.payment_repo)

            # Generate new payment ID
            payments = self.payment_repo.find_all()
            payment_id = max([p.payment_id for p in payments], default=0) + 1

            # Process purchase
            success = payment_service.purchase_membership(member_id, plan, payment_id)

            if success:
                QMessageBox.information(self, "Успех", "Абонемент успешно куплен и активирован")
                self.refresh_members_table()
                self.refresh_plans_combo()  # Update UI
                self.purchase_member_id_edit.clear()
            else:
                QMessageBox.critical(self, "Ошибка", "Не удалось купить абонемент")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось купить абонемент: {str(e)}")
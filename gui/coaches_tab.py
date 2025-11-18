from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QLineEdit, QMessageBox
)
from decimal import Decimal

from classes.people import Coach


class CoachesTab(QWidget):
    def __init__(self, coach_repo):
        super().__init__()
        self.coach_repo = coach_repo

        self.init_ui()
        self.setup_connections()
        self.refresh_coaches_table()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Coaches table
        self.coaches_table = QTableWidget()
        self.coaches_table.setColumnCount(7)
        self.coaches_table.setHorizontalHeaderLabels([
            "ID", "Имя", "Фамилия", "Email", "Телефон", "Специализация", "Ставка"
        ])
        layout.addWidget(QLabel("Тренеры:"))
        layout.addWidget(self.coaches_table)

        # Coach form
        form_group = QGroupBox("Добавить/Редактировать тренера")
        form_layout = QFormLayout()

        self.coach_id_edit = QLineEdit()
        self.coach_first_name_edit = QLineEdit()
        self.coach_last_name_edit = QLineEdit()
        self.coach_email_edit = QLineEdit()
        self.coach_phone_edit = QLineEdit()
        self.coach_specialization_edit = QLineEdit()
        self.coach_hourly_rate_edit = QLineEdit()

        form_layout.addRow("ID:", self.coach_id_edit)
        form_layout.addRow("Имя:", self.coach_first_name_edit)
        form_layout.addRow("Фамилия:", self.coach_last_name_edit)
        form_layout.addRow("Email:", self.coach_email_edit)
        form_layout.addRow("Телефон:", self.coach_phone_edit)
        form_layout.addRow("Специализация:", self.coach_specialization_edit)
        form_layout.addRow("Ставка (руб/час):", self.coach_hourly_rate_edit)

        buttons_layout = QHBoxLayout()
        self.add_coach_btn = QPushButton("Добавить тренера")
        self.update_coach_btn = QPushButton("Обновить тренера")
        self.delete_coach_btn = QPushButton("Удалить тренера")
        self.clear_coach_form_btn = QPushButton("Очистить форму")

        buttons_layout.addWidget(self.add_coach_btn)
        buttons_layout.addWidget(self.update_coach_btn)
        buttons_layout.addWidget(self.delete_coach_btn)
        buttons_layout.addWidget(self.clear_coach_form_btn)

        form_layout.addRow(buttons_layout)
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)

    def setup_connections(self):
        self.add_coach_btn.clicked.connect(self.add_coach)
        self.update_coach_btn.clicked.connect(self.update_coach)
        self.delete_coach_btn.clicked.connect(self.delete_coach)
        self.clear_coach_form_btn.clicked.connect(self.clear_coach_form)

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

    def add_coach(self):
        try:
            coach_id = int(self.coach_id_edit.text()) if self.coach_id_edit.text() else 0
            first_name = self.coach_first_name_edit.text()
            last_name = self.coach_last_name_edit.text()
            email = self.coach_email_edit.text()
            phone = self.coach_phone_edit.text()
            specialization = self.coach_specialization_edit.text()
            hourly_rate = Decimal(
                self.coach_hourly_rate_edit.text()) if self.coach_hourly_rate_edit.text() else Decimal("0")

            if not first_name or not last_name or not email or not phone or not specialization:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все обязательные поля")
                return

            coach = Coach(
                id=coach_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                specialization=specialization,
                hourly_rate=hourly_rate
            )

            self.coach_repo.save(coach)
            QMessageBox.information(self, "Успех", "Тренер успешно добавлен")
            self.refresh_coaches_table()
            self.clear_coach_form()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить тренера: {str(e)}")

    def update_coach(self):
        self.add_coach()

    def delete_coach(self):
        try:
            coach_id = int(self.coach_id_edit.text()) if self.coach_id_edit.text() else 0
            if coach_id <= 0:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, укажите действительный ID тренера")
                return
            reply = QMessageBox.question(self, "Подтверждение",
                                         f"Вы уверены, что хотите удалить тренера с ID {coach_id}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                success = self.coach_repo.delete(coach_id)
                if success:
                    QMessageBox.information(self, "Успех", "Тренер успешно удален")
                    self.refresh_coaches_table()
                    self.clear_coach_form()
                else:
                    QMessageBox.warning(self, "Ошибка", "Тренер с указанным ID не найден")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить тренера: {str(e)}")

    def clear_coach_form(self):
        self.coach_id_edit.clear()
        self.coach_first_name_edit.clear()
        self.coach_last_name_edit.clear()
        self.coach_email_edit.clear()
        self.coach_phone_edit.clear()
        self.coach_specialization_edit.clear()
        self.coach_hourly_rate_edit.clear()
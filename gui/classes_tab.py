from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QLineEdit, QDateTimeEdit, QMessageBox
)
from PyQt6.QtCore import QDateTime

from classes.group_class import GroupClass


class ClassesTab(QWidget):
    def __init__(self, group_class_repo, coach_repo, room_repo, member_repo):
        super().__init__()
        self.group_class_repo = group_class_repo
        self.coach_repo = coach_repo
        self.room_repo = room_repo
        self.member_repo = member_repo

        self.init_ui()
        self.setup_connections()
        self.refresh_classes_table()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Classes table
        self.classes_table = QTableWidget()
        self.classes_table.setColumnCount(7)
        self.classes_table.setHorizontalHeaderLabels([
            "ID", "Название", "Тренер", "Зал", "Дата/время", "Вместимость", "Участники"
        ])
        self.classes_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(QLabel("Групповые занятия:"))
        layout.addWidget(self.classes_table)

        # Class form
        form_group = QGroupBox("Добавить/Редактировать занятие")
        form_layout = QFormLayout()

        self.class_id_edit = QLineEdit()
        self.class_name_edit = QLineEdit()
        self.class_coach_combo = QLineEdit()  # In a full implementation, this would be a combo box
        self.class_room_combo = QLineEdit()  # In a full implementation, this would be a combo box
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
        self.update_class_btn = QPushButton("Обновить занятие")
        self.delete_class_btn = QPushButton("Удалить занятие")
        self.clear_class_form_btn = QPushButton("Очистить форму")

        buttons_layout.addWidget(self.add_class_btn)
        buttons_layout.addWidget(self.update_class_btn)
        buttons_layout.addWidget(self.delete_class_btn)
        buttons_layout.addWidget(self.clear_class_form_btn)

        form_layout.addRow(buttons_layout)
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)

        # Enrollment form
        enrollment_group = QGroupBox("Записаться на занятие")
        enrollment_layout = QFormLayout()

        self.enroll_class_id_edit = QLineEdit()
        self.enroll_member_id_edit = QLineEdit()

        enrollment_layout.addRow("ID занятия:", self.enroll_class_id_edit)
        enrollment_layout.addRow("ID участника:", self.enroll_member_id_edit)

        self.enroll_btn = QPushButton("Записаться")
        enrollment_layout.addRow(self.enroll_btn)

        enrollment_group.setLayout(enrollment_layout)
        layout.addWidget(enrollment_group)

    def setup_connections(self):
        self.add_class_btn.clicked.connect(self.add_class)
        self.update_class_btn.clicked.connect(self.update_class)
        self.delete_class_btn.clicked.connect(self.delete_class)
        self.clear_class_form_btn.clicked.connect(self.clear_class_form)
        self.enroll_btn.clicked.connect(self.enroll_member)

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
            # Display enrolled member IDs instead of count
            attendees_str = ", ".join(map(str, group_class.attendees)) if group_class.attendees else ""
            self.classes_table.setItem(row, 6, QTableWidgetItem(attendees_str))

        self.classes_table.resizeColumnsToContents()

    def add_class(self):
        try:
            class_id = int(self.class_id_edit.text()) if self.class_id_edit.text() else 0
            class_name = self.class_name_edit.text()
            coach_id = int(self.class_coach_combo.text()) if self.class_coach_combo.text() else 0
            room_id = int(self.class_room_combo.text()) if self.class_room_combo.text() else 0
            schedule = self.class_datetime_edit.dateTime().toPyDateTime()
            capacity = int(self.class_capacity_edit.text()) if self.class_capacity_edit.text() else 0

            if not class_name:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, укажите название занятия")
                return

            # Get coach and room objects
            coach = self.coach_repo.find_by_id(coach_id)
            if not coach:
                QMessageBox.warning(self, "Ошибка", f"Тренер с ID {coach_id} не найден")
                return

            room = self.room_repo.find_by_id(room_id)
            if not room:
                QMessageBox.warning(self, "Ошибка", f"Зал с ID {room_id} не найден")
                return

            group_class = GroupClass(
                class_id=class_id,
                class_name=class_name,
                coach=coach,
                room=room,
                schedule=schedule,
                max_capacity=capacity
            )
            self.group_class_repo.save(group_class)
            QMessageBox.information(self, "Успех", "Занятие успешно добавлено")
            self.refresh_classes_table()
            self.clear_class_form()

        except ValueError as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка в данных: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить занятие: {str(e)}")

    def update_class(self):
        self.add_class()

    def delete_class(self):
        try:
            class_id = int(self.class_id_edit.text()) if self.class_id_edit.text() else 0
            if class_id <= 0:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, укажите действительный ID занятия")
                return

            reply = QMessageBox.question(self, "Подтверждение",
                                         f"Вы уверены, что хотите удалить занятие с ID {class_id}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                success = self.group_class_repo.delete(class_id)
                if success:
                    QMessageBox.information(self, "Успех", "Занятие успешно удалено")
                    self.refresh_classes_table()
                    self.clear_class_form()
                else:
                    QMessageBox.warning(self, "Ошибка", "Занятие с указанным ID не найдено")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить занятие: {str(e)}")

    def clear_class_form(self):
        self.class_id_edit.clear()
        self.class_name_edit.clear()
        self.class_coach_combo.clear()
        self.class_room_combo.clear()
        self.class_datetime_edit.setDateTime(QDateTime.currentDateTime())
        self.class_capacity_edit.clear()

    def enroll_member(self):
        try:
            class_id = int(self.enroll_class_id_edit.text()) if self.enroll_class_id_edit.text() else 0
            member_id = int(self.enroll_member_id_edit.text()) if self.enroll_member_id_edit.text() else 0

            if class_id <= 0:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, укажите действительный ID занятия")
                return

            if member_id <= 0:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, укажите действительный ID участника")
                return

            # Find the class
            group_class = self.group_class_repo.find_by_id(class_id)
            if not group_class:
                QMessageBox.warning(self, "Ошибка", f"Занятие с ID {class_id} не найдено")
                return

            # Check if member exists
            member = self.member_repo.get_by_id(member_id)
            if not member:
                QMessageBox.warning(self, "Ошибка", f"Участник с ID {member_id} не найден")
                return

            # Check if member is already enrolled
            if member_id in group_class.attendees:
                QMessageBox.warning(self, "Ошибка", "Участник уже записан на это занятие")
                return

            # Check if there are available spots
            if group_class.get_available_spots() <= 0:
                QMessageBox.warning(self, "Ошибка", "Нет свободных мест на занятии")
                return

            # Enroll member
            success = group_class.add_attendee(member_id)
            if success:
                self.group_class_repo.save(group_class)
                QMessageBox.information(self, "Успех", "Участник успешно записан на занятие")
                self.refresh_classes_table()
                self.enroll_class_id_edit.clear()
                self.enroll_member_id_edit.clear()
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось записать участника на занятие")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось записать участника на занятие: {str(e)}")
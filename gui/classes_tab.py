from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QLineEdit, QDateTimeEdit, QMessageBox, QSplitter, QHeaderView, QComboBox
)
from PyQt6.QtCore import QDateTime, Qt

from classes.group_class import GroupClass


class ClassesTab(QWidget):
    def __init__(self, group_class_repo, coach_repo, room_repo, member_repo):
        super().__init__()
        self.group_class_repo = group_class_repo
        self.coach_repo = coach_repo
        self.room_repo = room_repo
        self.member_repo = member_repo
        self.all_classes = []

        self.init_ui()
        self.setup_connections()
        self.refresh_classes_table()
        self.refresh_coaches_combo()
        self.refresh_rooms_combo()
        self.refresh_classes_combo()
        self.refresh_members_combo()
        self.apply_styles()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Создание разделителя
        splitter = QSplitter(Qt.Orientation.Vertical)
        layout.addWidget(splitter)

        # Верхняя часть с поиском и таблицей
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)

        # Поиск
        search_layout = QHBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Поиск по занятиям...")
        self.search_btn = QPushButton("Поиск")
        self.clear_search_btn = QPushButton("Очистить")
        search_layout.addWidget(QLabel("Поиск:"))
        search_layout.addWidget(self.search_box)
        search_layout.addWidget(self.search_btn)
        search_layout.addWidget(self.clear_search_btn)
        top_layout.addLayout(search_layout)

        # Таблица занятий
        self.classes_table = QTableWidget()
        self.classes_table.setColumnCount(7)
        self.classes_table.setHorizontalHeaderLabels([
            "ID", "Название", "Тренер", "Зал", "Дата/время", "Вместимость", "Участники"
        ])
        self.classes_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.classes_table.setSortingEnabled(True)
        header = self.classes_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        top_layout.addWidget(QLabel("Групповые занятия:"))
        top_layout.addWidget(self.classes_table)
        splitter.addWidget(top_widget)

        # Нижняя часть с формами
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)

        # Форма занятия
        form_group = QGroupBox("Добавить/Редактировать занятие")
        form_layout = QFormLayout()

        self.class_id_edit = QLineEdit()
        self.class_name_edit = QLineEdit()
        self.class_coach_combo = QComboBox()
        self.class_room_combo = QComboBox()
        self.class_datetime_edit = QDateTimeEdit()
        self.class_datetime_edit.setDateTime(QDateTime.currentDateTime())
        self.class_capacity_edit = QLineEdit()

        form_layout.addRow("ID:", self.class_id_edit)
        form_layout.addRow("Название:", self.class_name_edit)
        form_layout.addRow("Тренер:", self.class_coach_combo)
        form_layout.addRow("Зал:", self.class_room_combo)
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
        bottom_layout.addWidget(form_group)

        # Форма записи
        enrollment_group = QGroupBox("Записаться на занятие")
        enrollment_layout = QFormLayout()

        self.enroll_class_combo = QComboBox()
        self.enroll_member_combo = QComboBox()

        enrollment_layout.addRow("Занятие:", self.enroll_class_combo)
        enrollment_layout.addRow("Участник:", self.enroll_member_combo)

        self.enroll_btn = QPushButton("Записаться")
        enrollment_layout.addRow(self.enroll_btn)

        enrollment_group.setLayout(enrollment_layout)
        bottom_layout.addWidget(enrollment_group)

        splitter.addWidget(bottom_widget)
        splitter.setSizes([400, 400])

    def apply_styles(self):
        # Применяем стили к элементам
        self.search_box.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #555;
                border-radius: 4px;
                background-color: #2d2d2d;
                color: white;
            }

            QLineEdit:focus {
                border-color: #3a506b;
            }
        """)

        self.classes_table.setStyleSheet("""
            QTableWidget {
                background-color: #2d2d2d;
                alternate-background-color: #3a3a3a;
                selection-background-color: #3a506b;
                gridline-color: #555;
                color: white;
            }

            QTableWidget::item:selected {
                background-color: #3a506b;
            }

            QHeaderView::section {
                background-color: #3a506b;
                color: white;
                padding: 4px;
                border: 1px solid #555;
            }
        """)

    def setup_connections(self):
        self.add_class_btn.clicked.connect(self.add_class)
        self.update_class_btn.clicked.connect(self.update_class)
        self.delete_class_btn.clicked.connect(self.delete_class)
        self.clear_class_form_btn.clicked.connect(self.clear_class_form)
        self.enroll_btn.clicked.connect(self.enroll_member)
        self.search_btn.clicked.connect(self.search_classes)
        self.clear_search_btn.clicked.connect(self.clear_search)
        self.classes_table.itemClicked.connect(self.populate_form_from_table)

    def refresh_coaches_combo(self):
        coaches = self.coach_repo.find_all()
        self.class_coach_combo.clear()
        for coach in coaches:
            self.class_coach_combo.addItem(f"{coach.get_full_name()} (ID: {coach.id})", coach.id)

    def refresh_rooms_combo(self):
        rooms = self.room_repo.find_all()
        self.class_room_combo.clear()
        for room in rooms:
            self.class_room_combo.addItem(f"{room.room_name} (ID: {room.room_id})", room.room_id)

    def refresh_classes_combo(self):
        classes = self.group_class_repo.find_all()
        self.enroll_class_combo.clear()
        for class_item in classes:
            self.enroll_class_combo.addItem(f"{class_item.class_name} (ID: {class_item.class_id})", class_item.class_id)

    def refresh_members_combo(self):
        members = self.member_repo.get_all()
        self.enroll_member_combo.clear()
        for member in members:
            self.enroll_member_combo.addItem(f"{member.get_full_name()} (ID: {member.id})", member.id)

    def populate_form_from_table(self, item):
        row = item.row()
        self.class_id_edit.setText(self.classes_table.item(row, 0).text())
        self.class_name_edit.setText(self.classes_table.item(row, 1).text())

        # Поиск и установка тренера
        coach_text = self.classes_table.item(row, 2).text()
        for i in range(self.class_coach_combo.count()):
            if coach_text in self.class_coach_combo.itemText(i):
                self.class_coach_combo.setCurrentIndex(i)
                break

        # Поиск и установка зала
        room_text = self.classes_table.item(row, 3).text()
        for i in range(self.class_room_combo.count()):
            if room_text in self.class_room_combo.itemText(i):
                self.class_room_combo.setCurrentIndex(i)
                break

        # Установка даты/времени
        datetime_str = self.classes_table.item(row, 4).text()
        try:
            dt = QDateTime.fromString(datetime_str, "dd.MM.yyyy hh:mm")
            if dt.isValid():
                self.class_datetime_edit.setDateTime(dt)
        except Exception:
            self.class_datetime_edit.setDateTime(QDateTime.currentDateTime())

        self.class_capacity_edit.setText(self.classes_table.item(row, 5).text())

    def search_classes(self):
        search_term = self.search_box.text().lower()
        if not search_term:
            self.refresh_classes_table()
            return

        filtered_classes = []
        for class_item in self.all_classes:
            if (search_term in str(class_item.class_id) or
                search_term in class_item.class_name.lower() or
                search_term in class_item.coach.get_full_name().lower() or
                search_term in class_item.room.room_name.lower()):
                filtered_classes.append(class_item)

        self.display_classes(filtered_classes)

    def clear_search(self):
        self.search_box.clear()
        self.refresh_classes_table()

    def display_classes(self, classes):
        self.classes_table.setRowCount(len(classes))

        for row, group_class in enumerate(classes):
            self.classes_table.setItem(row, 0, QTableWidgetItem(str(group_class.class_id)))
            self.classes_table.setItem(row, 1, QTableWidgetItem(group_class.class_name))
            self.classes_table.setItem(row, 2, QTableWidgetItem(group_class.coach.get_full_name()))
            self.classes_table.setItem(row, 3, QTableWidgetItem(group_class.room.room_name))

            schedule = group_class.schedule.strftime("%d.%m.%Y %H:%M") if group_class.schedule else ""
            self.classes_table.setItem(row, 4, QTableWidgetItem(schedule))
            self.classes_table.setItem(row, 5, QTableWidgetItem(str(group_class.max_capacity)))
            # Отображение ID участников
            attendees_str = ", ".join(map(str, group_class.attendees)) if group_class.attendees else ""
            self.classes_table.setItem(row, 6, QTableWidgetItem(attendees_str))

        self.classes_table.resizeColumnsToContents()

    def refresh_classes_table(self):
        self.all_classes = self.group_class_repo.find_all()
        self.display_classes(self.all_classes)

    def add_class(self):
        try:
            class_id = int(self.class_id_edit.text()) if self.class_id_edit.text() else 0
            class_name = self.class_name_edit.text()
            coach_id = self.class_coach_combo.currentData()
            room_id = self.class_room_combo.currentData()
            schedule = self.class_datetime_edit.dateTime().toPyDateTime()
            capacity = int(self.class_capacity_edit.text()) if self.class_capacity_edit.text() else 0

            if not class_name:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, укажите название занятия")
                return

            if coach_id is None:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите тренера")
                return

            if room_id is None:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите зал")
                return

            # Получение объектов тренера и зала
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
            class_id_text = self.class_id_edit.text()
            if not class_id_text:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, укажите ID занятия")
                return
            class_id = int(class_id_text)
            if class_id <= 0:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, укажите действительный ID занятия")
                return

            reply = QMessageBox.question(
                self, "Подтверждение",
                f"Вы уверены, что хотите удалить занятие с ID {class_id}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                success = self.group_class_repo.delete(class_id)
                if success:
                    QMessageBox.information(self, "Успех", "Занятие успешно удалено")
                    self.refresh_classes_table()
                    self.clear_class_form()
                else:
                    QMessageBox.warning(self, "Ошибка", "Занятие с указанным ID не найдено")

        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Некорректный формат ID")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить занятие: {str(e)}")

    def clear_class_form(self):
        self.class_id_edit.clear()
        self.class_name_edit.clear()
        self.class_datetime_edit.setDateTime(QDateTime.currentDateTime())
        self.class_capacity_edit.clear()
        if self.class_coach_combo.count() > 0:
            self.class_coach_combo.setCurrentIndex(0)
        if self.class_room_combo.count() > 0:
            self.class_room_combo.setCurrentIndex(0)

    def enroll_member(self):
        try:
            class_id = self.enroll_class_combo.currentData()
            member_id = self.enroll_member_combo.currentData()

            if class_id is None:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите занятие")
                return

            if member_id is None:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите участника")
                return

            # Поиск занятия
            group_class = self.group_class_repo.find_by_id(class_id)
            if not group_class:
                QMessageBox.warning(self, "Ошибка", f"Занятие с ID {class_id} не найдено")
                return

            # Проверка существования участника
            member = self.member_repo.get_by_id(member_id)
            if not member:
                QMessageBox.warning(self, "Ошибка", f"Участник с ID {member_id} не найден")
                return

            # Проверка, записан ли участник уже
            if member_id in group_class.attendees:
                QMessageBox.warning(self, "Ошибка", "Участник уже записан на это занятие")
                return

            # Проверка наличия мест
            if group_class.get_available_spots() <= 0:
                QMessageBox.warning(self, "Ошибка", "Нет свободных мест на занятии")
                return

            # Запись участника
            success = group_class.add_attendee(member_id)
            if success:
                self.group_class_repo.save(group_class)
                QMessageBox.information(self, "Успех", "Участник успешно записан на занятие")
                self.refresh_classes_table()
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось записать участника на занятие")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось записать участника на занятие: {str(e)}")
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QLineEdit, QMessageBox, QSplitter, QHeaderView
)
from PyQt6.QtCore import Qt
from decimal import Decimal

from classes.people import Coach


class CoachesTab(QWidget):
    def __init__(self, coach_repo):
        super().__init__()
        self.coach_repo = coach_repo
        self.all_coaches = []

        self.init_ui()
        self.setup_connections()
        self.refresh_coaches_table()
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
        self.search_box.setPlaceholderText("Поиск по тренерам...")
        self.search_btn = QPushButton("Поиск")
        self.clear_search_btn = QPushButton("Очистить")
        search_layout.addWidget(QLabel("Поиск:"))
        search_layout.addWidget(self.search_box)
        search_layout.addWidget(self.search_btn)
        search_layout.addWidget(self.clear_search_btn)
        top_layout.addLayout(search_layout)

        # Таблица тренеров
        self.coaches_table = QTableWidget()
        self.coaches_table.setColumnCount(7)
        self.coaches_table.setHorizontalHeaderLabels([
            "ID", "Имя", "Фамилия", "Email", "Телефон", "Специализация", "Ставка"
        ])

        # Включение сортировки
        self.coaches_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.coaches_table.setSortingEnabled(True)
        header = self.coaches_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        top_layout.addWidget(QLabel("Тренеры:"))
        top_layout.addWidget(self.coaches_table)
        splitter.addWidget(top_widget)

        # Нижняя часть с формой
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)

        # Форма тренера
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
        bottom_layout.addWidget(form_group)

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

        self.coaches_table.setStyleSheet("""
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
        self.add_coach_btn.clicked.connect(self.add_coach)
        self.update_coach_btn.clicked.connect(self.update_coach)
        self.delete_coach_btn.clicked.connect(self.delete_coach)
        self.clear_coach_form_btn.clicked.connect(self.clear_coach_form)
        self.search_btn.clicked.connect(self.search_coaches)
        self.clear_search_btn.clicked.connect(self.clear_search)
        self.coaches_table.itemClicked.connect(self.populate_form_from_table)

    def populate_form_from_table(self, item):
        row = item.row()
        self.coach_id_edit.setText(self.coaches_table.item(row, 0).text())
        self.coach_first_name_edit.setText(self.coaches_table.item(row, 1).text())
        self.coach_last_name_edit.setText(self.coaches_table.item(row, 2).text())
        self.coach_email_edit.setText(self.coaches_table.item(row, 3).text())
        self.coach_phone_edit.setText(self.coaches_table.item(row, 4).text())
        self.coach_specialization_edit.setText(self.coaches_table.item(row, 5).text())
        self.coach_hourly_rate_edit.setText(self.coaches_table.item(row, 6).text())

    def search_coaches(self):
        search_term = self.search_box.text().lower()
        if not search_term:
            self.refresh_coaches_table()
            return

        filtered_coaches = []
        for coach in self.all_coaches:
            if (search_term in str(coach.id) or
                search_term in coach.first_name.lower() or
                search_term in coach.last_name.lower() or
                search_term in coach.email.lower() or
                search_term in coach.phone.lower() or
                search_term in coach.specialization.lower()):
                filtered_coaches.append(coach)

        self.display_coaches(filtered_coaches)

    def clear_search(self):
        self.search_box.clear()
        self.refresh_coaches_table()

    def display_coaches(self, coaches):
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

    def refresh_coaches_table(self):
        self.all_coaches = self.coach_repo.find_all()
        self.display_coaches(self.all_coaches)

    def add_coach(self):
        try:
            coach_id = int(self.coach_id_edit.text()) if self.coach_id_edit.text() else 0
            first_name = self.coach_first_name_edit.text()
            last_name = self.coach_last_name_edit.text()
            email = self.coach_email_edit.text()
            phone = self.coach_phone_edit.text()
            specialization = self.coach_specialization_edit.text()
            hourly_rate_text = self.coach_hourly_rate_edit.text()
            hourly_rate = Decimal(hourly_rate_text) if hourly_rate_text else Decimal("0")

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

        except ValueError as e:
            QMessageBox.critical(self, "Ошибка", f"Некорректный формат числа (ставка): {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить тренера: {str(e)}")

    def update_coach(self):
        self.add_coach()

    def delete_coach(self):
        try:
            coach_id_text = self.coach_id_edit.text()
            if not coach_id_text:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, укажите ID тренера")
                return
            coach_id = int(coach_id_text)
            if coach_id <= 0:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, укажите действительный ID тренера")
                return

            reply = QMessageBox.question(
                self, "Подтверждение",
                f"Вы уверены, что хотите удалить тренера с ID {coach_id}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                success = self.coach_repo.delete(coach_id)
                if success:
                    QMessageBox.information(self, "Успех", "Тренер успешно удален")
                    self.refresh_coaches_table()
                    self.clear_coach_form()
                else:
                    QMessageBox.warning(self, "Ошибка", "Тренер с указанным ID не найден")

        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Некорректный формат ID")
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
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QLineEdit, QMessageBox
)

from classes.gym_room import GymRoom


class RoomsTab(QWidget):
    def __init__(self, room_repo):
        super().__init__()
        self.room_repo = room_repo

        self.init_ui()
        self.setup_connections()
        self.refresh_rooms_table()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Rooms table
        self.rooms_table = QTableWidget()
        self.rooms_table.setColumnCount(4)
        self.rooms_table.setHorizontalHeaderLabels([
            "ID", "Название", "Тип", "Вместимость"
        ])
        layout.addWidget(QLabel("Залы:"))
        layout.addWidget(self.rooms_table)

        # Room form
        form_group = QGroupBox("Добавить/Редактировать зал")
        form_layout = QFormLayout()

        self.room_id_edit = QLineEdit()
        self.room_name_edit = QLineEdit()
        self.room_type_edit = QLineEdit()
        self.room_capacity_edit = QLineEdit()

        form_layout.addRow("ID:", self.room_id_edit)
        form_layout.addRow("Название:", self.room_name_edit)
        form_layout.addRow("Тип:", self.room_type_edit)
        form_layout.addRow("Вместимость:", self.room_capacity_edit)

        buttons_layout = QHBoxLayout()
        self.add_room_btn = QPushButton("Добавить зал")
        self.update_room_btn = QPushButton("Обновить зал")
        self.delete_room_btn = QPushButton("Удалить зал")
        self.clear_room_form_btn = QPushButton("Очистить форму")

        buttons_layout.addWidget(self.add_room_btn)
        buttons_layout.addWidget(self.update_room_btn)
        buttons_layout.addWidget(self.delete_room_btn)
        buttons_layout.addWidget(self.clear_room_form_btn)

        form_layout.addRow(buttons_layout)
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)

    def setup_connections(self):
        self.add_room_btn.clicked.connect(self.add_room)
        self.update_room_btn.clicked.connect(self.update_room)
        self.delete_room_btn.clicked.connect(self.delete_room)
        self.clear_room_form_btn.clicked.connect(self.clear_room_form)

    def refresh_rooms_table(self):
        rooms = self.room_repo.find_all()
        self.rooms_table.setRowCount(len(rooms))

        for row, room in enumerate(rooms):
            self.rooms_table.setItem(row, 0, QTableWidgetItem(str(room.room_id)))
            self.rooms_table.setItem(row, 1, QTableWidgetItem(room.room_name))
            self.rooms_table.setItem(row, 2, QTableWidgetItem(room.room_type))
            self.rooms_table.setItem(row, 3, QTableWidgetItem(str(room.capacity)))

        self.rooms_table.resizeColumnsToContents()

    def add_room(self):
        try:
            room_id = int(self.room_id_edit.text()) if self.room_id_edit.text() else 0
            room_name = self.room_name_edit.text()
            room_type = self.room_type_edit.text()
            capacity = int(self.room_capacity_edit.text()) if self.room_capacity_edit.text() else 0

            if not room_name or not room_type:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все обязательные поля")
                return

            room = GymRoom(
                room_id=room_id,
                room_name=room_name,
                room_type=room_type,
                capacity=capacity
            )

            self.room_repo.save(room)
            QMessageBox.information(self, "Успех", "Зал успешно добавлен")
            self.refresh_rooms_table()
            self.clear_room_form()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить зал: {str(e)}")

    def update_room(self):
        self.add_room()

    def delete_room(self):
        try:
            room_id = int(self.room_id_edit.text()) if self.room_id_edit.text() else 0
            if room_id <= 0:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, укажите действительный ID зала")
                return

            reply = QMessageBox.question(self, "Подтверждение",
                                         f"Вы уверены, что хотите удалить зал с ID {room_id}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                success = self.room_repo.delete(room_id)
                if success:
                    QMessageBox.information(self, "Успех", "Зал успешно удален")
                    self.refresh_rooms_table()
                    self.clear_room_form()
                else:
                    QMessageBox.warning(self, "Ошибка", "Зал с указанным ID не найден")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить зал: {str(e)}")

    def clear_room_form(self):
        self.room_id_edit.clear()
        self.room_name_edit.clear()
        self.room_type_edit.clear()
        self.room_capacity_edit.clear()
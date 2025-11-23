from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QLineEdit, QMessageBox, QSplitter, QHeaderView
)
from PyQt6.QtCore import Qt

from classes.gym_room import GymRoom


class RoomsTab(QWidget):
    def __init__(self, room_repo):
        super().__init__()
        self.room_repo = room_repo
        self.all_rooms = []

        self.init_ui()
        self.setup_connections()
        self.refresh_rooms_table()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Create splitter for resizable sections
        splitter = QSplitter(Qt.Orientation.Vertical)
        layout.addWidget(splitter)

        # Top section with search and table
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)
        
        # Search section
        search_layout = QHBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Поиск по залам...")
        self.search_btn = QPushButton("Поиск")
        self.clear_search_btn = QPushButton("Очистить")
        search_layout.addWidget(QLabel("Поиск:"))
        search_layout.addWidget(self.search_box)
        search_layout.addWidget(self.search_btn)
        search_layout.addWidget(self.clear_search_btn)
        top_layout.addLayout(search_layout)

        # Rooms table
        self.rooms_table = QTableWidget()
        self.rooms_table.setColumnCount(4)
        self.rooms_table.setHorizontalHeaderLabels([
            "ID", "Название", "Тип", "Вместимость"
        ])
        
        # Enable sorting
        self.rooms_table.setSortingEnabled(True)
        header = self.rooms_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        top_layout.addWidget(QLabel("Залы:"))
        top_layout.addWidget(self.rooms_table)
        splitter.addWidget(top_widget)

        # Bottom section with form
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)

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
        bottom_layout.addWidget(form_group)
        
        splitter.addWidget(bottom_widget)
        splitter.setSizes([400, 400])  # Set initial sizes

    def setup_connections(self):
        self.add_room_btn.clicked.connect(self.add_room)
        self.update_room_btn.clicked.connect(self.update_room)
        self.delete_room_btn.clicked.connect(self.delete_room)
        self.clear_room_form_btn.clicked.connect(self.clear_room_form)
        self.search_btn.clicked.connect(self.search_rooms)
        self.clear_search_btn.clicked.connect(self.clear_search)
        self.rooms_table.itemClicked.connect(self.populate_form_from_table)

    def populate_form_from_table(self, item):
        row = item.row()
        self.room_id_edit.setText(self.rooms_table.item(row, 0).text())
        self.room_name_edit.setText(self.rooms_table.item(row, 1).text())
        self.room_type_edit.setText(self.rooms_table.item(row, 2).text())
        self.room_capacity_edit.setText(self.rooms_table.item(row, 3).text())

    def search_rooms(self):
        search_term = self.search_box.text().lower()
        if not search_term:
            self.refresh_rooms_table()
            return
            
        filtered_rooms = []
        for room in self.all_rooms:
            if (search_term in str(room.room_id) or 
                search_term in room.room_name.lower() or 
                search_term in room.room_type.lower()):
                filtered_rooms.append(room)
                
        self.display_rooms(filtered_rooms)

    def clear_search(self):
        self.search_box.clear()
        self.refresh_rooms_table()

    def display_rooms(self, rooms):
        self.rooms_table.setRowCount(len(rooms))

        for row, room in enumerate(rooms):
            self.rooms_table.setItem(row, 0, QTableWidgetItem(str(room.room_id)))
            self.rooms_table.setItem(row, 1, QTableWidgetItem(room.room_name))
            self.rooms_table.setItem(row, 2, QTableWidgetItem(room.room_type))
            self.rooms_table.setItem(row, 3, QTableWidgetItem(str(room.capacity)))

        self.rooms_table.resizeColumnsToContents()

    def refresh_rooms_table(self):
        self.all_rooms = self.room_repo.find_all()
        self.display_rooms(self.all_rooms)

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
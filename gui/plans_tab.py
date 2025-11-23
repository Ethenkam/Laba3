from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QLineEdit, QMessageBox, QSplitter, QHeaderView
)
from PyQt6.QtCore import Qt

from classes.Membership_plan import MembershipPlan


class PlansTab(QWidget):
    def __init__(self, plan_repo):
        super().__init__()
        self.plan_repo = plan_repo
        self.all_plans = []

        self.init_ui()
        self.setup_connections()
        self.refresh_plans_table()

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
        self.search_box.setPlaceholderText("Поиск по абонементам...")
        self.search_btn = QPushButton("Поиск")
        self.clear_search_btn = QPushButton("Очистить")
        search_layout.addWidget(QLabel("Поиск:"))
        search_layout.addWidget(self.search_box)
        search_layout.addWidget(self.search_btn)
        search_layout.addWidget(self.clear_search_btn)
        top_layout.addLayout(search_layout)

        # Plans table
        self.plans_table = QTableWidget()
        self.plans_table.setColumnCount(4)
        self.plans_table.setHorizontalHeaderLabels([
            "ID", "Название", "Длительность (дни)", "Цена"
        ])
        
        # Enable sorting
        self.plans_table.setSortingEnabled(True)
        header = self.plans_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        top_layout.addWidget(QLabel("Абонементы:"))
        top_layout.addWidget(self.plans_table)
        splitter.addWidget(top_widget)

        # Bottom section with form
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)

        # Plan form
        form_group = QGroupBox("Добавить/Редактировать абонемент")
        form_layout = QFormLayout()

        self.plan_id_edit = QLineEdit()
        self.plan_name_edit = QLineEdit()
        self.plan_duration_edit = QLineEdit()
        self.plan_price_edit = QLineEdit()

        form_layout.addRow("ID:", self.plan_id_edit)
        form_layout.addRow("Название:", self.plan_name_edit)
        form_layout.addRow("Длительность (дни):", self.plan_duration_edit)
        form_layout.addRow("Цена (руб.):", self.plan_price_edit)

        buttons_layout = QHBoxLayout()
        self.add_plan_btn = QPushButton("Добавить абонемент")
        self.update_plan_btn = QPushButton("Обновить абонемент")
        self.delete_plan_btn = QPushButton("Удалить абонемент")
        self.clear_plan_form_btn = QPushButton("Очистить форму")

        buttons_layout.addWidget(self.add_plan_btn)
        buttons_layout.addWidget(self.update_plan_btn)
        buttons_layout.addWidget(self.delete_plan_btn)
        buttons_layout.addWidget(self.clear_plan_form_btn)

        form_layout.addRow(buttons_layout)
        form_group.setLayout(form_layout)
        bottom_layout.addWidget(form_group)
        
        splitter.addWidget(bottom_widget)
        splitter.setSizes([400, 400])  # Set initial sizes

    def setup_connections(self):
        self.add_plan_btn.clicked.connect(self.add_plan)
        self.update_plan_btn.clicked.connect(self.update_plan)
        self.delete_plan_btn.clicked.connect(self.delete_plan)
        self.clear_plan_form_btn.clicked.connect(self.clear_plan_form)
        self.search_btn.clicked.connect(self.search_plans)
        self.clear_search_btn.clicked.connect(self.clear_search)
        self.plans_table.itemClicked.connect(self.populate_form_from_table)

    def populate_form_from_table(self, item):
        row = item.row()
        self.plan_id_edit.setText(self.plans_table.item(row, 0).text())
        self.plan_name_edit.setText(self.plans_table.item(row, 1).text())
        self.plan_duration_edit.setText(self.plans_table.item(row, 2).text())
        self.plan_price_edit.setText(self.plans_table.item(row, 3).text())

    def search_plans(self):
        search_term = self.search_box.text().lower()
        if not search_term:
            self.refresh_plans_table()
            return
            
        filtered_plans = []
        for plan in self.all_plans:
            if (search_term in str(plan.plan_id) or 
                search_term in plan.name.lower()):
                filtered_plans.append(plan)
                
        self.display_plans(filtered_plans)

    def clear_search(self):
        self.search_box.clear()
        self.refresh_plans_table()

    def display_plans(self, plans):
        self.plans_table.setRowCount(len(plans))

        for row, plan in enumerate(plans):
            self.plans_table.setItem(row, 0, QTableWidgetItem(str(plan.plan_id)))
            self.plans_table.setItem(row, 1, QTableWidgetItem(plan.name))
            self.plans_table.setItem(row, 2, QTableWidgetItem(str(plan.duration_days)))
            self.plans_table.setItem(row, 3, QTableWidgetItem(str(plan.price)))

        self.plans_table.resizeColumnsToContents()

    def refresh_plans_table(self):
        self.all_plans = self.plan_repo.find_all()
        self.display_plans(self.all_plans)

    def add_plan(self):
        try:
            plan_id = int(self.plan_id_edit.text()) if self.plan_id_edit.text() else 0
            name = self.plan_name_edit.text()
            duration_days = int(self.plan_duration_edit.text()) if self.plan_duration_edit.text() else 0
            price = int(self.plan_price_edit.text()) if self.plan_price_edit.text() else 0

            if not name:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, укажите название абонемента")
                return

            plan = MembershipPlan(
                plan_id=plan_id,
                name=name,
                duration_days=duration_days,
                price=price
            )

            self.plan_repo.save(plan)
            QMessageBox.information(self, "Успех", "Абонемент успешно добавлен")
            self.refresh_plans_table()
            self.clear_plan_form()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить абонемент: {str(e)}")

    def update_plan(self):
        self.add_plan()

    def delete_plan(self):
        try:
            plan_id = int(self.plan_id_edit.text()) if self.plan_id_edit.text() else 0
            if plan_id <= 0:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, укажите действительный ID абонемента")
                return

            reply = QMessageBox.question(self, "Подтверждение",
                                         f"Вы уверены, что хотите удалить абонемент с ID {plan_id}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                success = self.plan_repo.delete(plan_id)
                if success:
                    QMessageBox.information(self, "Успех", "Абонемент успешно удален")
                    self.refresh_plans_table()
                    self.clear_plan_form()
                else:
                    QMessageBox.warning(self, "Ошибка", "Абонемент с указанным ID не найден")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить абонемент: {str(e)}")

    def clear_plan_form(self):
        self.plan_id_edit.clear()
        self.plan_name_edit.clear()
        self.plan_duration_edit.clear()
        self.plan_price_edit.clear()
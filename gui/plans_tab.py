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
        self.search_box.setPlaceholderText("Поиск по абонементам...")
        self.search_btn = QPushButton("Поиск")
        self.clear_search_btn = QPushButton("Очистить")
        search_layout.addWidget(QLabel("Поиск:"))
        search_layout.addWidget(self.search_box)
        search_layout.addWidget(self.search_btn)
        search_layout.addWidget(self.clear_search_btn)
        top_layout.addLayout(search_layout)

        # Таблица абонементов
        self.plans_table = QTableWidget()
        self.plans_table.setColumnCount(4)
        self.plans_table.setHorizontalHeaderLabels([
            "ID", "Название", "Длительность (дни)", "Цена"
        ])
        self.plans_table.setSortingEnabled(True)
        header = self.plans_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        top_layout.addWidget(QLabel("Абонементы:"))
        top_layout.addWidget(self.plans_table)
        splitter.addWidget(top_widget)

        # Нижняя часть с формой
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)

        # Форма абонемента
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

        self.plans_table.setStyleSheet("""
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

        except ValueError:
            QMessageBox.critical(self, "Ошибка", "Пожалуйста, введите корректные числовые значения для ID, длительности и цены.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить абонемент: {str(e)}")

    def update_plan(self):
        # Для простоты повторно используем логику добавления
        self.add_plan()

    def delete_plan(self):
        try:
            plan_id_text = self.plan_id_edit.text()
            if not plan_id_text:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, укажите ID абонемента")
                return
            plan_id = int(plan_id_text)
            if plan_id <= 0:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, укажите действительный ID абонемента")
                return

            reply = QMessageBox.question(
                self, "Подтверждение",
                f"Вы уверены, что хотите удалить абонемент с ID {plan_id}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                success = self.plan_repo.delete(plan_id)
                if success:
                    QMessageBox.information(self, "Успех", "Абонемент успешно удален")
                    self.refresh_plans_table()
                    self.clear_plan_form()
                else:
                    QMessageBox.warning(self, "Ошибка", "Абонемент с указанным ID не найден")

        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Некорректный формат ID")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить абонемент: {str(e)}")

    def clear_plan_form(self):
        self.plan_id_edit.clear()
        self.plan_name_edit.clear()
        self.plan_duration_edit.clear()
        self.plan_price_edit.clear()
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QLineEdit, QMessageBox
)

from classes.Membership_plan import MembershipPlan


class PlansTab(QWidget):
    def __init__(self, plan_repo):
        super().__init__()
        self.plan_repo = plan_repo

        self.init_ui()
        self.setup_connections()
        self.refresh_plans_table()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Plans table
        self.plans_table = QTableWidget()
        self.plans_table.setColumnCount(4)
        self.plans_table.setHorizontalHeaderLabels([
            "ID", "Название", "Длительность (дни)", "Цена"
        ])
        layout.addWidget(QLabel("Абонементы:"))
        layout.addWidget(self.plans_table)

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
        layout.addWidget(form_group)

    def setup_connections(self):
        self.add_plan_btn.clicked.connect(self.add_plan)
        self.update_plan_btn.clicked.connect(self.update_plan)
        self.delete_plan_btn.clicked.connect(self.delete_plan)
        self.clear_plan_form_btn.clicked.connect(self.clear_plan_form)

    def refresh_plans_table(self):
        plans = self.plan_repo.find_all()
        self.plans_table.setRowCount(len(plans))

        for row, plan in enumerate(plans):
            self.plans_table.setItem(row, 0, QTableWidgetItem(str(plan.plan_id)))
            self.plans_table.setItem(row, 1, QTableWidgetItem(plan.name))
            self.plans_table.setItem(row, 2, QTableWidgetItem(str(plan.duration_days)))
            self.plans_table.setItem(row, 3, QTableWidgetItem(str(plan.price)))

        self.plans_table.resizeColumnsToContents()

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
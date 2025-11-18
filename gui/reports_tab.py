from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem
)


class ReportsTab(QWidget):
    def __init__(self, payment_repo, member_repo, plan_repo):
        super().__init__()
        self.payment_repo = payment_repo
        self.member_repo = member_repo
        self.plan_repo = plan_repo

        self.init_ui()
        self.refresh_payments_table()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Payments table
        self.payments_table = QTableWidget()
        self.payments_table.setColumnCount(4)
        self.payments_table.setHorizontalHeaderLabels([
            "ID", "Участник", "Абонемент", "Сумма"
        ])
        layout.addWidget(QLabel("Платежи:"))
        layout.addWidget(self.payments_table)

    def refresh_payments_table(self):
        payments = self.payment_repo.find_all()
        self.payments_table.setRowCount(len(payments))

        for row, payment in enumerate(payments):
            self.payments_table.setItem(row, 0, QTableWidgetItem(str(payment.payment_id)))

            # Get member name
            member = self.member_repo.get_by_id(payment.member_id)
            member_name = member.get_full_name() if member else "Не найден"
            self.payments_table.setItem(row, 1, QTableWidgetItem(member_name))

            # Get plan name
            plan = self.plan_repo.find_by_id(payment.plan_id)
            plan_name = plan.name if plan else "Не найден"
            self.payments_table.setItem(row, 2, QTableWidgetItem(plan_name))

            self.payments_table.setItem(row, 3, QTableWidgetItem(str(payment.amount)))

        self.payments_table.resizeColumnsToContents()
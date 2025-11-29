from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QGroupBox, QHeaderView, QPushButton, QHBoxLayout
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from decimal import Decimal


class ReportsTab(QWidget):
    def __init__(self, payment_repo, member_repo, plan_repo):
        super().__init__()
        self.payment_repo = payment_repo
        self.member_repo = member_repo
        self.plan_repo = plan_repo

        self.init_ui()
        self.refresh_payments_table()
        self.plot_revenue_chart()
        self.plot_members_chart()
        self.apply_styles()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        # === Таблица платежей ===
        payments_group = QGroupBox("Платежи")
        payments_layout = QVBoxLayout()

        self.payments_table = QTableWidget()
        self.payments_table.setColumnCount(4)
        self.payments_table.setHorizontalHeaderLabels([
            "ID", "Участник", "Абонемент", "Сумма (руб.)"
        ])
        self.payments_table.setSortingEnabled(True)
        header = self.payments_table.horizontalHeader()
        self.payments_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        payments_layout.addWidget(self.payments_table)
        payments_group.setLayout(payments_layout)
        main_layout.addWidget(payments_group)

        # Статистика
        self.stats_label = QLabel()
        main_layout.addWidget(self.stats_label)

        # Диаграммы
        charts_layout = QHBoxLayout()

        # Диаграмма доходов
        self.revenue_figure = Figure(figsize=(5, 3))
        self.revenue_canvas = FigureCanvas(self.revenue_figure)
        charts_layout.addWidget(self.revenue_canvas)

        # Диаграмма участников
        self.members_figure = Figure(figsize=(5, 3))
        self.members_canvas = FigureCanvas(self.members_figure)
        charts_layout.addWidget(self.members_canvas)

        main_layout.addLayout(charts_layout)

        # Кнопка обновления
        refresh_button = QPushButton("Обновить данные")
        refresh_button.clicked.connect(self.on_refresh)
        main_layout.addWidget(refresh_button)

    def apply_styles(self):
        # Применяем стили к элементам
        self.payments_table.setStyleSheet("""
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

        self.stats_label.setStyleSheet("""
            QLabel {
                background-color: #3a3a3a;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 10px;
                color: white;
                font-weight: bold;
                font-size: 12px;
            }
        """)

    def on_refresh(self):
        self.refresh_payments_table()
        self.plot_revenue_chart()
        self.plot_members_chart()

    def refresh_payments_table(self):
        payments = self.payment_repo.find_all()
        self.payments_table.setRowCount(len(payments))

        total_revenue = Decimal("0.00")
        for row, payment in enumerate(payments):
            self.payments_table.setItem(row, 0, QTableWidgetItem(str(payment.payment_id)))

            member = self.member_repo.get_by_id(payment.member_id)
            member_name = member.get_full_name() if member else "Не найден"
            self.payments_table.setItem(row, 1, QTableWidgetItem(member_name))

            plan = self.plan_repo.find_by_id(payment.plan_id)
            plan_name = plan.name if plan else "Не найден"
            self.payments_table.setItem(row, 2, QTableWidgetItem(plan_name))

            amount = float(payment.amount) if isinstance(payment.amount, Decimal) else payment.amount
            amount_str = f"{amount:.2f}"
            self.payments_table.setItem(row, 3, QTableWidgetItem(amount_str))
            total_revenue += Decimal(str(payment.amount))

        # Обновление статистики
        all_members = self.member_repo.get_all()
        total_members = len(all_members)
        active_members = sum(1 for m in all_members if m.is_active)

        self.stats_label.setText(
            f"Общая выручка: {float(total_revenue):.2f} руб.\n"
            f"Всего участников: {total_members}\n"
            f"Активных участников: {active_members}"
        )

    def plot_revenue_chart(self):
        self.revenue_figure.clear()
        ax = self.revenue_figure.add_subplot(111)

        payments = self.payment_repo.find_all()
        plan_revenue = {}

        for payment in payments:
            plan = self.plan_repo.find_by_id(payment.plan_id)
            plan_name = plan.name if plan else "Неизвестный план"
            plan_revenue[plan_name] = plan_revenue.get(plan_name, Decimal("0")) + payment.amount

        if not plan_revenue:
            ax.text(0.5, 0.5, "Нет данных", ha='center', va='center', transform=ax.transAxes)
        else:
            plans = list(plan_revenue.keys())
            revenues = [float(v) for v in plan_revenue.values()]

            bars = ax.bar(plans, revenues, color='red')
            ax.set_xlabel('Абонементы')
            ax.set_ylabel('Выручка (руб.)')
            ax.set_title('Выручка по типам абонементов', pad=20)
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:,.0f}'.replace(',', ' ')))
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{height:,.0f}'.replace(',', ' '),
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3),
                            textcoords="offset points",
                            ha='center', va='bottom')

            plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

        self.revenue_figure.tight_layout()
        self.revenue_canvas.draw()

    def plot_members_chart(self):
        self.members_figure.clear()
        ax = self.members_figure.add_subplot(111)

        members = self.member_repo.get_all()
        active = sum(1 for m in members if m.is_active)
        inactive = len(members) - active

        if len(members) == 0:
            ax.text(0.5, 0.5, "Нет участников", ha='center', va='center', transform=ax.transAxes)
        else:
            labels = ['Активные', 'Неактивные']
            sizes = [active, inactive]
            colors = ['green', 'red']

            ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            ax.set_title('Распределение участников по статусу')

        self.members_figure.tight_layout()
        self.members_canvas.draw()
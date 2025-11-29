import sys
import csv
import xlsxwriter
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget,
    QStatusBar, QToolBar, QMessageBox, QFileDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QPalette, QColor

from gui.members_tab import MembersTab
from gui.classes_tab import ClassesTab
from gui.coaches_tab import CoachesTab
from gui.rooms_tab import RoomsTab
from gui.plans_tab import PlansTab
from gui.reports_tab import ReportsTab

from repositories.member_repository import MemberRepository
from repositories.coach_repository import CoachRepository
from repositories.gym_room_repository import GymRoomRepository
from repositories.group_class_repository import GroupClassRepository
from repositories.membership_plan_repository import MembershipPlanRepository
from repositories.payment_repository import PaymentRepository


class GymManagementSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Система управления фитнес-клубом")
        self.setGeometry(100, 100, 1200, 800)

        self.apply_stylesheet()

        self.member_repo = MemberRepository()
        self.coach_repo = CoachRepository()
        self.room_repo = GymRoomRepository()
        self.group_class_repo = GroupClassRepository()
        self.plan_repo = MembershipPlanRepository()
        self.payment_repo = PaymentRepository()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        self.create_toolbar()
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        self.create_status_bar()
        self.create_tabs()

    def apply_stylesheet(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.black)
        palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
        self.setPalette(palette)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            QTabWidget::pane {
                border: 1px solid #444;
                border-radius: 4px;
                padding: 2px;
                background-color: #3a3a3a;
            }
            QTabBar::tab {
                background-color: #444;
                border: 1px solid #555;
                border-bottom-color: #444;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                min-width: 8ex;
                padding: 4px;
                color: white;
            }
            QTabBar::tab:selected {
                background-color: #5a5a5a;
                border-bottom-color: #3a3a3a;
            }
            QTabBar::tab:hover:!selected {
                background-color: #505050;
            }
            QToolBar {
                background-color: #3a3a3a;
                border: 1px solid #444;
            }
            QPushButton {
                background-color: #3a506b;
                border: 1px solid #1c2541;
                border-radius: 4px;
                padding: 6px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5bc0be;
                border: 1px solid #1c2541;
            }
            QPushButton:pressed {
                background-color: #0b132b;
            }
            QGroupBox {
                border: 1px solid #555;
                border-radius: 4px;
                margin-top: 1ex;
                color: white;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
            QLineEdit, QComboBox, QDateEdit, QTextEdit, QSpinBox {
                background-color: #2d2d2d;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 4px;
                color: white;
                selection-background-color: #3a506b;
            }
            QHeaderView::section {
                background-color: #3a506b;
                color: white;
                padding: 4px;
                border: 1px solid #555;
            }
            QTableWidget {
                gridline-color: #555;
                background-color: #2d2d2d;
                alternate-background-color: #3a3a3a;
                selection-background-color: #3a506b;
            }
            QStatusBar {
                background-color: #3a3a3a;
                border: 1px solid #444;
            }
            QLabel {
                color: white;
            }
            QCheckBox {
                color: white;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
            QCheckBox::indicator:unchecked {
                border: 1px solid #555;
                background-color: #2d2d2d;
            }
            QCheckBox::indicator:checked {
                border: 1px solid #555;
                background-color: #3a506b;
            }
            QMessageBox {
                background-color: #2b2b2b;
            }
            QMessageBox QLabel {
                color: white;
            }
            QMessageBox QPushButton {
                background-color: #3a506b;
                border: 1px solid #1c2541;
                border-radius: 4px;
                padding: 6px;
                color: white;
                font-weight: bold;
            }
            QMessageBox QPushButton:hover {
                background-color: #5bc0be;
            }
            QMessageBox QPushButton:pressed {
                background-color: #0b132b;
            }
        """)

    def create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        refresh_action = QAction("Обновить данные", self)
        refresh_action.setStatusTip("Обновить все таблицы")
        refresh_action.triggered.connect(self.refresh_all_tables)
        toolbar.addAction(refresh_action)

        export_action = QAction("Экспорт в CSV/XLSX", self)
        export_action.setStatusTip("Экспортировать данные на текущей вкладке")
        export_action.triggered.connect(self.export_to_csv_or_xlsx)
        toolbar.addAction(export_action)

    def create_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Готов", 2000)

    def create_tabs(self):
        self.members_tab = MembersTab(self.member_repo, self.plan_repo, self.payment_repo)
        self.classes_tab = ClassesTab(self.group_class_repo, self.coach_repo, self.room_repo, self.member_repo)
        self.coaches_tab = CoachesTab(self.coach_repo)
        self.rooms_tab = RoomsTab(self.room_repo)
        self.plans_tab = PlansTab(self.plan_repo)
        self.reports_tab = ReportsTab(self.payment_repo, self.member_repo, self.plan_repo)

        self.tabs.addTab(self.members_tab, "Участники")
        self.tabs.addTab(self.classes_tab, "Занятия")
        self.tabs.addTab(self.coaches_tab, "Тренеры")
        self.tabs.addTab(self.rooms_tab, "Залы")
        self.tabs.addTab(self.plans_tab, "Абонементы")
        self.tabs.addTab(self.reports_tab, "Отчеты")

        self.refresh_all_tables()

    def refresh_all_tables(self):
        self.members_tab.refresh_members_table()
        self.classes_tab.refresh_classes_table()
        self.coaches_tab.refresh_coaches_table()
        self.rooms_tab.refresh_rooms_table()
        self.plans_tab.refresh_plans_table()
        self.reports_tab.refresh_payments_table()
        self.members_tab.refresh_plans_combo()
        self.status_bar.showMessage("Все таблицы обновлены", 2000)

    def export_to_csv_or_xlsx(self):
        current_tab_index = self.tabs.currentIndex()
        current_tab = self.tabs.widget(current_tab_index)
        tab_name = self.tabs.tabText(current_tab_index).replace('/', '_')
        default_filename = tab_name

        file_path, selected_filter = QFileDialog.getSaveFileName(
            self,
            "Сохранить как",
            default_filename,
            "Excel Files (*.xlsx);;CSV Files (*.csv);;All Files (*)"
        )

        if not file_path:
            return  # User cancelled

        table = None
        if hasattr(current_tab, 'members_table'):
            table = current_tab.members_table
        elif hasattr(current_tab, 'classes_table'):
            table = current_tab.classes_table
        elif hasattr(current_tab, 'coaches_table'):
            table = current_tab.coaches_table
        elif hasattr(current_tab, 'rooms_table'):
            table = current_tab.rooms_table
        elif hasattr(current_tab, 'plans_table'):
            table = current_tab.plans_table
        elif hasattr(current_tab, 'payments_table'):
            table = current_tab.payments_table

        if table is None:
            QMessageBox.warning(self, "Ошибка экспорта", "Невозможно экспортировать данные с этой вкладки.")
            return

        try:
            if "Excel" in selected_filter or file_path.endswith(".xlsx"):
                if not file_path.endswith(".xlsx"):
                    file_path += ".xlsx"
                self.export_table_to_xlsx(table, file_path)
            else:
                if not file_path.endswith(".csv"):
                    file_path += ".csv"
                self.export_table_to_csv(table, file_path)

            QMessageBox.information(self, "Успех", f"Данные успешно экспортированы в:\n{file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка экспорта", f"Не удалось экспортировать данные:\n{str(e)}")

    def export_table_to_csv(self, table, file_path):
        with open(file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)
            # Header
            header = []
            for col in range(table.columnCount()):
                item = table.horizontalHeaderItem(col)
                header.append(item.text() if item else f"Column {col}")
            writer.writerow(header)
            # Data rows
            for row in range(table.rowCount()):
                row_data = []
                for col in range(table.columnCount()):
                    item = table.item(row, col)
                    row_data.append(item.text() if item else "")
                writer.writerow(row_data)

    def export_table_to_xlsx(self, table, file_path):
        workbook = xlsxwriter.Workbook(file_path)
        worksheet = workbook.add_worksheet()
        header_format = workbook.add_format({'bold': True, 'bg_color': '#D7E4BC'})

        for col in range(table.columnCount()):
            header_item = table.horizontalHeaderItem(col)
            header_text = header_item.text() if header_item else f"Column {col}"
            worksheet.write(0, col, header_text, header_format)

        for row in range(table.rowCount()):
            for col in range(table.columnCount()):
                item = table.item(row, col)
                cell_value = item.text() if item else ""
                worksheet.write(row + 1, col, cell_value)

        workbook.close()


def main():
    app = QApplication(sys.argv)
    window = GymManagementSystem()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
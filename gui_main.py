import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from gui.main_window import GymManagementSystem


def main():
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName("Система управления фитнес-клубом")
    app.setApplicationVersion("1.0")

    window = GymManagementSystem()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
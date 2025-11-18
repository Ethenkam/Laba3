import sys
from PyQt6.QtWidgets import QApplication

from gui.main_window import GymManagementSystem


app = QApplication(sys.argv)
window = GymManagementSystem()
window.show()
sys.exit(app.exec())


import sys

from PyQt6.QtWidgets import QApplication

from gui import MainWindow
from view import View


def main():
    app = QApplication(sys.argv)
    view = View()
    window = MainWindow(view)
    window.show()
    app.exec()


if __name__ == "__main__":
    main()

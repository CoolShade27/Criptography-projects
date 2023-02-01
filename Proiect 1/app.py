import sys
from PyQt5 import QtWidgets
from gui.main_window import MainWindow


def run():
    app = QtWidgets.QApplication(sys.argv)
    GUI = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
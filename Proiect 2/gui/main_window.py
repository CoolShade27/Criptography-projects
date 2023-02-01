from PyQt5 import QtGui, QtWidgets
from config.config import ConfigManager
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QPushButton, QTextEdit, QSpinBox, QLineEdit
from PyQt5.QtGui import QFont

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.config = ConfigManager()
        self.bcolor = self.config.get_default('backgroundcolor')
        self.textcolor = self.config.get_default('textcolor')

        self.setGeometry(100, 100, int(self.config.get_default('defaultwidth')),
                         int(self.config.get_default('defaultheight')))
        self.setWindowTitle('Sistem de dubla criptare')
        self.setWindowIcon(QtGui.QIcon())

        self.frame = QtWidgets.QFrame(self)
        self.frame.setStyleSheet("background-color:" + self.bcolor)
        self.frame.setGeometry(0, 0, 1920, 1080)

        self.p = self.config.get_default('p')
        self.q = self.config.get_default('q')
        self.x0 = self.config.get_default('x0')
        self.filesize = self.config.get_default('filesize')
        self.out = ''

        self.home()

        self.showMaximized()

    def home(self):
        self.save_file_btn = QPushButton('Save file...', self)
        self.save_file_btn.move(1100, 600)
        self.save_file_btn.resize(self.save_file_btn.minimumSizeHint())
        self.save_file_btn.clicked.connect(self.save_file)

        self.pbox = QSpinBox(self)
        self.pbox.move(600, 500)
        self.pbox.setRange(2, 1E5)
        self.pbox.setValue(int(self.p))

        self.qbox = QSpinBox(self)
        self.qbox.move(800, 500)
        self.qbox.setRange(2, 1E5)
        self.qbox.setValue(int(self.q))

        self.xbox = QSpinBox(self)
        self.xbox.move(1000, 500)
        self.xbox.setRange(1, 1E5)
        self.xbox.setValue(int(self.x0))

        self.sizebox = QSpinBox(self)
        self.sizebox.move(1200, 500)
        self.sizebox.setRange(1, 4096)
        self.sizebox.setValue(int(self.filesize))

        self.generate = QPushButton('Generate', self)
        self.generate.resize(self.generate.minimumSizeHint())
        self.generate.move(900, 600)
        self.generate.clicked.connect(self.bbs)

        self.sequence = QTextEdit(self)
        self.sequence.move(600, 650)
        self.sequence.resize(750, 300)
        self.sequence.setStyleSheet('QTextEdit {background-color: ' + self.bcolor + ';}')
        self.sequence.setReadOnly(True)

        self.set_btn = QPushButton('Set values', self)
        self.set_btn.resize(self.set_btn.minimumSizeHint())
        self.set_btn.move(700, 600)
        self.set_btn.clicked.connect(self.set_values)

        self.pline = QLineEdit(self)
        self.pline.resize(30, 20)
        self.pline.move(560, 505)
        self.pline.setStyleSheet('QLineEdit {background-color: ' + self.bcolor + '; border: 0;}')
        self.pline.setText('p = ')
        self.pline.setReadOnly(True)

        self.qline = QLineEdit(self)
        self.qline.resize(30, 20)
        self.qline.move(760, 505)
        self.qline.setStyleSheet('QLineEdit {background-color: ' + self.bcolor + '; border: 0;}')
        self.qline.setText('q = ')
        self.qline.setReadOnly(True)

        self.xline = QLineEdit(self)
        self.xline.resize(35, 20)
        self.xline.move(960, 505)
        self.xline.setStyleSheet('QLineEdit {background-color: ' + self.bcolor + '; border: 0;}')
        self.xline.setText('x0 = ')
        self.xline.setReadOnly(True)

        self.sline = QLineEdit(self)
        self.sline.resize(45, 20)
        self.sline.move(1150, 505)
        self.sline.setStyleSheet('QLineEdit {background-color: ' + self.bcolor + '; border: 0;}')
        self.sline.setText('size = ')
        self.sline.setReadOnly(True)

        self.kb = QLineEdit(self)
        self.kb.resize(30, 20)
        self.kb.move(1310, 505)
        self.kb.setStyleSheet('QLineEdit {background-color: ' + self.bcolor + '; border: 0;}')
        self.kb.setText('KB')
        self.kb.setReadOnly(True)

        self.title = QTextEdit(self)
        self.title.move(550, 100)
        self.title.resize(750, 50)
        self.title.setReadOnly(True)
        self.title.setStyleSheet('QTextEdit {background-color: ' + self.bcolor + ';  border: 0;}')
        self.title.setFont(QFont('Arial', 20))
        self.title.setText('\t\tGeneratorul Blum - Blum - Shub')

        self.description = QTextEdit(self)
        self.description.move(600, 250)
        self.description.resize(750, 200)
        self.description.setReadOnly(True)
        self.description.setStyleSheet('QTextEdit {background-color: ' + self.bcolor + ';}')
        self.description.setFont(QFont('Arial', 10))
        file = open('description.txt', 'r')
        self.description.setText(file.read())
        file.close()

    @pyqtSlot()
    def save_file(self):
        dialog = QtWidgets.QFileDialog.Options()
        dialog |= QtWidgets.QFileDialog.DontUseNativeDialog
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', '.txt',
                                                            'All Files (*.*);;Text Files (*.txt);;Binary Files (*.bin)', options=dialog)

        if filename:
            file = open(filename, 'wb')
            out_bin = self.out.encode('ascii')
            file.write(out_bin)
            file.close()
            self.out = ''
            self.sequence.clear()

    @pyqtSlot()
    def bbs(self):
        p = int(self.p)
        q = int(self.q)
        n = p * q
        x = [int(self.x0) % n]
        self.out = ''
        size = int(self.filesize) * 1024

        self.sequence.clear()
        self.sequence.setText('Generating sequence, please wait...')

        for i in range(0, size):
            x.append((x[i] ** 2) % n)
            self.out += str(x[i + 1] % 2)

        x.clear()
        self.sequence.setText(self.out)

    def is_prime(self, nr):
        prime = True

        for i in range(2, int(nr / 2) + 1):
            if nr % i == 0:
                prime = False

        return prime

    def check_values(self):
        p = self.pbox.value()
        q = self.qbox.value()
        return (p % 4 == 3) and self.is_prime(p) and (q % 4 == 3) and self.is_prime(q)

    def set_values(self):
        if self.check_values():
            self.p = self.pbox.value()
            self.q = self.qbox.value()
            self.x0 = self.xbox.value()
            self.filesize = self.sizebox.value()
            self.sequence.setText('Values updated to p = %d, q = %d, x0 = %d and size = %d KB' %
                                  (self.p, self.q, self.x0, self.filesize))
        else:
            self.sequence.setText('Incorrect numbers!')




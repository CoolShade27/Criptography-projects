import string, random
from PyQt5 import QtGui, QtWidgets
from config.config import ConfigManager
from PyQt5.QtWidgets import QPushButton, QLineEdit, QTextEdit
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QFont


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.config = ConfigManager()
        self.bcolor = self.config.get_default('backgroundcolor')
        self.textcolor = self.config.get_default('textcolor')
        self.current_text = ''
        self.current_filename = 'Current file: '
        self.alphabet = self.config.get_default('alphabet')
        self.square = self.config.get_default('square')
        self.key = ''

        self.setGeometry(100, 100, int(self.config.get_default('defaultwidth')),
                         int(self.config.get_default('defaultheight')))
        self.setWindowTitle('Sistem de dubla criptare')
        self.setWindowIcon(QtGui.QIcon())

        self.frame = QtWidgets.QFrame(self)
        self.frame.setStyleSheet("background-color:" + self.bcolor)
        self.frame.setGeometry(0, 0, 1920, 1080)

        self.home()

        self.showMaximized()

    def bifid(self, text, action='cipher'):
        text = text.upper().strip()
        out = ''
        square_list = list(self.square)
        square_list.remove('J')
        square_dict = {}
        v1 = []
        v2 = []

        text = ''.join(letter for letter in text if letter.isalpha())

        for idx in range(len(square_list)):
            square_dict[square_list[idx]] = (idx // 5, idx % 5)
        square_dict['J'] = square_dict['I']

        if action == 'cipher':
            for letter in text:
                (row, column) = square_dict[letter]
                v1.append(row)
                v2.append(column)

            v1.extend(v2)
            for idx in range(0, len(v1), 2):
                out += square_list[v1[idx] * 5 + v1[idx + 1]]

        if action == 'decipher':
            text_len = len(text)

            if text_len % 2 == 0:
                for idx in range(0, text_len // 2):
                    (row, column) = square_dict[text[idx]]
                    v1.append(row)
                    v1.append(column)
                for idx in range(text_len // 2, text_len):
                    (row, column) = square_dict[text[idx]]
                    v2.append(row)
                    v2.append(column)

            else:
                for idx in range(0, text_len // 2 + 1):
                    (row, column) = square_dict[text[idx]]
                    if idx == text_len // 2:
                        v1.append(row)
                        v2.append(column)
                    else:
                        v1.append(row)
                        v1.append(column)
                for idx in range(text_len // 2 + 1, text_len):
                    (row, column) = square_dict[text[idx]]
                    v2.append(row)
                    v2.append(column)

            for idx in range(len(v1)):
                out += square_list[v1[idx] * 5 + v2[idx]]

        return out

    def monoalfa(self, text, action='cipher'):
        cipher_dict = {}
        decipher_dict = {}
        text = text.upper().strip()
        alphabet = self.alphabet
        l = list(string.ascii_uppercase)
        out = ''

        text = ''.join(letter for letter in text if letter.isalpha())

        for idx in range(len(l)):
            cipher_dict[l[idx]] = alphabet[idx]

        for key, value in cipher_dict.items():
            decipher_dict[value] = key

        if action == 'cipher':
            for letter in text:
                out += cipher_dict[letter]

        if action == 'decipher':
            for letter in text:
                out += decipher_dict[letter]

        return out

    def encrypt(self, plain_text):
        ciphered_text = self.monoalfa(self.bifid(plain_text, 'cipher'), 'cipher')
        return ciphered_text

    def decrypt(self, ciphered_text):
        plain_text = self.bifid(self.monoalfa(ciphered_text, 'decipher'), 'decipher')
        return plain_text

    @pyqtSlot()
    def open_file(self):
        dialog = QtWidgets.QFileDialog.Options()
        dialog |= QtWidgets.QFileDialog.DontUseNativeDialog
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Load file', '',
                                                         'All Files (*.*);;Text Files (*.txt)', options=dialog)

        if filename:
            self.set_current_filename(filename)
            self.current_text_box.clear()
            file = open(filename, 'r')
            self.set_current_text(file.read())
            self.current_text_box.setPlainText(self.current_text)
            self.current_file_box.setText('Current file: ' + self.current_filename)
            file.close()

    @pyqtSlot()
    def save_file(self):
        dialog = QtWidgets.QFileDialog.Options()
        dialog |= QtWidgets.QFileDialog.DontUseNativeDialog
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', '.txt',
                                                            'All Files (*.*);;Text Files (*.txt)', options=dialog)

        if filename:
            file = open(filename, 'w')
            file.write(self.current_text)
            self.set_current_text('')
            self.set_current_filename('Current file: ')
            self.current_text_box.clear()
            self.current_file_box.setText(self.current_filename)
            file.close()

    def set_current_text(self, text):
        self.current_text = text

    def set_current_filename(self, name):
        self.current_filename = name

    def encrypt_current_text(self):
        ciphered_text = self.encrypt(self.current_text)
        self.set_current_text(ciphered_text)
        self.current_text_box.setPlainText(ciphered_text)

    def decrypt_current_text(self):
        plain_text = self.decrypt(self.current_text)
        self.set_current_text(plain_text)
        self.current_text_box.setPlainText(plain_text)

    def display_alphabet(self):
        out = '     Monoalphabetic substitution\n\n'
        left = string.ascii_uppercase
        right = self.alphabet

        for idx in range(len(left)):
            out += '\t' + left[idx] + ' : ' + right[idx] + '\n'

        return out

    def display_square(self):
        out = '      Polybius square\n\n'
        letters = list(self.square)
        letters.remove('J')
        out += '       ' + '1   2   3   4   5\n\n'

        for idx in range(0, len(letters), 5):
            out += str(idx // 5 + 1) + '     '
            l = letters[idx : idx + 5]
            for i in range(0, len(l)):
                if l[i] == 'I':
                    out += 'I/J' + '  '
                else:
                    out += l[i] + '   '
            out += '\n\n'

        return out

    def set_square(self, square):
        self.square = square

    def set_alphabet(self, alphabet):
        self.alphabet = alphabet

    def set_key(self, key):
        self.key = key

    @pyqtSlot()
    def enter_key(self):
        key = str(self.key_box.toPlainText())
        key = key.upper().split()
        key = ''.join(letter for letter in key if letter.isalpha())
        self.set_key(key)
        letters = string.ascii_uppercase

        l = []
        for letter in self.key:
            if letter in l:
                continue
            else:
                l.append(letter)

        for letter in letters:
            if letter in l:
                continue
            else:
                l.append(letter)

        square = ''.join(letter for letter in l)
        self.set_square(square)
        self.square_box.setPlainText(self.display_square())

    @pyqtSlot()
    def shuffle_square(self):
        new = string.ascii_uppercase
        new = ''.join(random.sample(new, len(new)))
        self.set_square(new)
        self.square_box.setPlainText(self.display_square())

    def home(self):
        self.title = QTextEdit(self)
        self.title.move(550, 100)
        self.title.resize(750, 50)
        self.title.setReadOnly(True)
        self.title.setStyleSheet('QTextEdit {background-color: ' + self.bcolor + ';  border: 0;}')
        self.title.setFont(QFont('Arial', 20))
        self.title.setPlainText('\t\t\tSistem de dubla criptare')

        self.description = QTextEdit(self)
        self.description.move(550, 250)
        self.description.resize(750, 200)
        self.description.setReadOnly(True)
        self.description.setStyleSheet('QTextEdit {background-color: ' + self.bcolor + ';}')
        self.description.setFont(QFont('Arial', 10))
        file = open('description.txt', 'r')
        self.description.setPlainText(file.read())
        file.close()

        self.current_text_box = QTextEdit(self)
        self.current_text_box.move(550, 550)
        self.current_text_box.resize(750, 150)
        self.current_text_box.setReadOnly(True)
        self.current_text_box.setStyleSheet('QTextEdit {background-color: ' + self.bcolor + ';}')
        self.current_text_box.setPlaceholderText('Choose a file to open...')

        self.current_file_box = QLineEdit(self)
        self.current_file_box.move(550, 705)
        self.current_file_box.resize(750, 25)
        self.current_file_box.setReadOnly(True)
        self.current_file_box.setFrame(False)
        self.current_file_box.setStyleSheet('QLineEdit {background-color: ' + self.bcolor + ';}')
        self.current_file_box.setText(self.current_filename)

        self.alpha_box = QTextEdit(self)
        self.alpha_box.move(1600, 200)
        self.alpha_box.resize(200, 500)
        self.alpha_box.setReadOnly(True)
        self.alpha_box.setStyleSheet('QTextEdit {background-color: ' + self.bcolor + '; border: 0;}')
        self.alpha_box.setPlainText(self.display_alphabet())

        self.square_box = QTextEdit(self)
        self.square_box.move(100, 200)
        self.square_box.resize(250, 250)
        self.square_box.setReadOnly(True)
        self.square_box.setStyleSheet('QTextEdit {background-color: ' + self.bcolor + '; border: 0;}')
        self.square_box.setPlainText(self.display_square())

        self.key_box = QTextEdit(self)
        self.key_box.move(70, 500)
        self.key_box.resize(200, 30)
        self.key_box.setPlaceholderText('Enter key...')

        self.encrypt_btn = QPushButton('Encrypt text', self)
        self.encrypt_btn.resize(self.encrypt_btn.minimumSizeHint())
        self.encrypt_btn.move(700, 750)
        self.encrypt_btn.clicked.connect(self.encrypt_current_text)

        self.decrypt_btn = QPushButton('Decrypt text', self)
        self.decrypt_btn.resize(self.encrypt_btn.minimumSizeHint())
        self.decrypt_btn.move(1050, 750)
        self.decrypt_btn.clicked.connect(self.decrypt_current_text)

        self.exit_btn = QPushButton('Quit', self)
        self.exit_btn.resize(self.exit_btn.minimumSizeHint())
        self.exit_btn.move(1800, 50)
        self.exit_btn.clicked.connect(self.close)

        self.select_file_btn = QPushButton('Choose file...', self)
        self.select_file_btn.resize(self.select_file_btn.minimumSizeHint())
        self.select_file_btn.move(700, 500)
        self.select_file_btn.clicked.connect(self.open_file)

        self.save_file_btn = QPushButton('Save file...', self)
        self.save_file_btn.resize(self.select_file_btn.minimumSizeHint())
        self.save_file_btn.move(1050, 500)
        self.save_file_btn.clicked.connect(self.save_file)

        self.shuffle_square_btn = QPushButton('Shuffle', self)
        self.shuffle_square_btn.move(120, 600)
        self.shuffle_square_btn.resize(self.shuffle_square_btn.minimumSizeHint())
        self.shuffle_square_btn.clicked.connect(self.shuffle_square)

        self.key_btn = QPushButton('Enter', self)
        self.key_btn.resize(self.key_btn.minimumSizeHint())
        self.key_btn.move(300, 500)
        self.key_btn.clicked.connect(self.enter_key)




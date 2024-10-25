from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
import re


class MainWin(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Текстовый редактор')

        self.line = QLineEdit()
        btn_create_new = QPushButton('Создать файл')
        btn_create_new.clicked.connect(self.create_new)
        btn_save = QPushButton('Сохранить файл')
        btn_save.clicked.connect(self.save)
        btn_open = QPushButton('Открыть файл')
        btn_open.clicked.connect(self.open)
        self.output = QTextEdit()
        self.symbols = QLabel("Всего символов: ")
        self.words = QLabel("Всего слов: ")
        self.the_longest_word = QLabel("Самое длинное слово: ")
        self.the_shortest_word = QLabel("Самое короткое слово: ")
        self.the_most_common_word = QLabel("Самое частое слово: ")

        h_l1 = QHBoxLayout()
        v_l1 = QVBoxLayout()
        v_l2 = QVBoxLayout()
        v_l1.addWidget(self.line)
        v_l1.addWidget(btn_create_new)
        v_l1.addWidget(btn_save)
        v_l1.addWidget(btn_open)
        v_l1.addWidget(self.symbols)
        v_l1.addWidget(self.words)
        v_l1.addWidget(self.the_longest_word)
        v_l1.addWidget(self.the_shortest_word)
        v_l1.addWidget(self.the_most_common_word)
        v_l1.addStretch()
        v_l2.addWidget(self.output)
        h_l1.addLayout(v_l1)
        h_l1.addLayout(v_l2)
        self.setLayout(h_l1)

    def create_new(self):
        self.line.clear()
        self.output.clear()

    def save(self):
        file_name = self.line.text()
        if file_name:
            with open(file_name, 'w') as file:
                file.write(self.output.toPlainText())
        self.file_information()

    def open(self):
        file_name = self.line.text()
        file = QFile(file_name)
        file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text)
        content = file.readAll().data().decode('Windows-1251')
        self.output.setPlainText(content)
        self.file_information()

    def file_information(self):
        text = self.output.toPlainText()
        words = text.split()
        words = [i for i in words if '-' not in i]
        symbols_number = len(text)
        words_number = len(words)
        self.symbols.setText(f'Всего символов: {symbols_number}')
        self.words.setText(f'Всего слов: {words_number}')

        words_without_punctuation = [re.sub(r'[^\w\s]', '', i) for i in words]

        longest_word = max(words_without_punctuation, key=len)
        self.the_longest_word.setText(f'Самое длинное слово:\n{longest_word}')
        shortest_word = min(words_without_punctuation, key=len)
        self.the_shortest_word.setText(f'Самое короткое слово:\n{shortest_word}')

        common_words = []

        for i in range(len(words_without_punctuation)):
            for j in range(i + 1, len(words_without_punctuation)):
                if words_without_punctuation[i] == words_without_punctuation[j] and words_without_punctuation[i] not in\
                        common_words:
                    common_words.append(words_without_punctuation[i])
        if not common_words:
            self.the_most_common_word.setText(f'Самое повторяющееся слово:\n-')
        else:
            self.the_most_common_word.setText(f'Самое повторяющееся слово:\n{common_words[0]}')

def main():
    app = QApplication([])
    win = MainWin()
    win.show()
    app.exec()

if __name__ == '__main__':
    main()

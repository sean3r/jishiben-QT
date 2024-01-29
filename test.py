from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtGui import QTextCursor, QTextCharFormat, QColor

class NotepadWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.textedit1 = QTextEdit()
        self.textedit1.setPlainText("Hello world\ntest\ntest\ntest\ntest\nHello end")

        self.pushbutton1 = QPushButton("find next")
        self.pushbutton1.clicked.connect(self.find_next)

        layout = QVBoxLayout()
        layout.addWidget(self.textedit1)
        layout.addWidget(self.pushbutton1)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.current_position = 0
        self.last_position = -1

    def find_next(self):
        format = QTextCharFormat()
        format.setBackground(QColor('yellow'))
        format.setForeground(QColor('red'))

        cursor = self.textedit1.textCursor()

        if self.last_position != -1:
            cursor.setPosition(self.last_position, QTextCursor.MoveMode.MoveAnchor)
            cursor.select(QTextCursor.SelectionType.WordUnderCursor)
            cursor.setCharFormat(QTextCharFormat())
            self.textedit1.setTextCursor(cursor)

        cursor.setPosition(self.current_position, QTextCursor.MoveMode.MoveAnchor)
        self.textedit1.setTextCursor(cursor)

        if self.textedit1.find("test"):
            cursor = self.textedit1.textCursor()
            cursor.select(QTextCursor.SelectionType.WordUnderCursor)
            cursor.mergeCharFormat(format)
            self.textedit1.setTextCursor(cursor)
            self.last_position = self.current_position
            self.current_position = self.textedit1.textCursor().position()
            cursor.selectionEnd
            print('if')
            
        else:
            self.current_position = 0
            self.last_position = -1
            self.find_next()

app = QApplication([])
window = NotepadWindow()
window.show()
app.exec()

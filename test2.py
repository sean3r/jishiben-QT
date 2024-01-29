from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QVBoxLayout
from PyQt6.QtCore import pyqtSignal

class ChildWindow(QDialog):
    windowClosed = pyqtSignal()

    def closeEvent(self, event):
        self.windowClosed.emit()
        super().closeEvent(event)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Window')
        self.setGeometry(100, 100, 800, 600)

        self.pushButton1 = QPushButton('Open Child Window', self)
        self.pushButton1.setGeometry(200, 200, 200, 50)
        self.pushButton1.clicked.connect(self.openChildWindow)

    def openChildWindow(self):
        self.childWindow = ChildWindow()
        self.childWindow.setWindowTitle('Child Window')
        self.childWindow.windowClosed.connect(self.onChildWindowClosed)
        self.childWindow.exec()

    def onChildWindowClosed(self):
        self.setWindowTitle('Hello World')

app = QApplication([])
mainWindow = MainWindow()
mainWindow.show()
app.exec()

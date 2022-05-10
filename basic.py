# import sys
# import random
# from PySide2.QtWidgets import (QApplication, QLabel, QPushButton,
#                                QVBoxLayout, QWidget)
# from PySide2.QtCore import Slot, Qt

# class MyWidget(QWidget):
#     def __init__(self):
#         QWidget.__init__(self)

#         self.hello = ["Hallo Welt", "你好，世界", "Hei maailma",
#             "Hola Mundo", "Привет мир"]

#         self.button = QPushButton("Click me!")
#         self.text = QLabel("Hello World")
#         self.text.setAlignment(Qt.AlignCenter)

#         self.layout = QVBoxLayout()
#         self.layout.addWidget(self.text)
#         self.layout.addWidget(self.button)
#         self.setLayout(self.layout)

#         # Connecting the signal
#         self.button.clicked.connect(self.magic)

#     @Slot()
#     def magic(self):
#         self.text.setText(random.choice(self.hello))

# if __name__ == "__main__":
#     app = QApplication(sys.argv)

#     widget = MyWidget()
#     widget.resize(800, 600)
#     widget.show()

#     sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 simple window - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

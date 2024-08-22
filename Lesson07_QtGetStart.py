#
# pip install PySide6 --proxy=proxy.citizen.co.jp:8080
#
import sys
from PySide6.QtWidgets import *

class MyWidgetWin(QWidget):
    # コンストラクタ
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MyQtWindow')

MyApp = QApplication(sys.argv)
mainWindow = MyWidgetWin()
mainWindow.show()

MyApp.exec()
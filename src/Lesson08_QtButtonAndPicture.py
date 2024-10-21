#
# pip install PySide6 --proxy=proxy.citizen.co.jp:8080
#
import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
import cv2

class MyMainWindow(QMainWindow):
    # コンストラクタ
    def __init__(self):
        super().__init__()
        #
        self.firstBtn = QPushButton('first')
        self.secondBtn = QPushButton('second')

        self.empire_cv = cv2.imread('./data/empire.jpg')
        self.scene = QGraphicsScene()
        self.view = QGraphicsView()
        empire_qt = cv2qt(self.empire_cv)
        pmap = QPixmap.fromImage(empire_qt)
        self.scene.addPixmap(pmap)
        self.view.setScene(self.scene)

        vbox = QVBoxLayout()
        vbox.addWidget(self.firstBtn)
        vbox.addWidget(self.secondBtn)
        vbox.addStretch()
        
        hbox = QHBoxLayout()
        hbox.addWidget(self.view)
        hbox.addLayout(vbox)

        MainContents = QWidget()
        MainContents.setLayout(hbox)
        self.setCentralWidget(MainContents)

        self.setWindowTitle('MyQtWindow')

def cv2qt(cv_img):
    height, width, depth = cv_img.shape
    imrgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    qt_img = QImage(imrgb.data, width, height, depth*width, QImage.Format_RGB888)
    return qt_img

MyApp = QApplication(sys.argv)
mainWindow = MyMainWindow()
mainWindow.show()

MyApp.exec()
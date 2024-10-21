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
        self.resetBtn = QPushButton('Reset')
        self.resetBtn.clicked.connect(self.resetBtnClicked)
        self.blurBtn = QPushButton('Blur')
        self.blurBtn.clicked.connect(self.blurBtnClicked)

        self.empire_cv = cv2.imread('./data/empire.jpg')
        self.scene = QGraphicsScene()
        self.view = QGraphicsView()
        empire_qt = cv2qt(self.empire_cv)
        pmap = QPixmap.fromImage(empire_qt)
        self.scene.addPixmap(pmap)
        self.view.setScene(self.scene)

        vbox = QVBoxLayout()
        vbox.addWidget(self.resetBtn)
        vbox.addWidget(self.blurBtn)
        vbox.addStretch()
        
        hbox = QHBoxLayout()
        hbox.addWidget(self.view)
        hbox.addLayout(vbox)

        MainContents = QWidget()
        MainContents.setLayout(hbox)
        self.setCentralWidget(MainContents)

        self.setWindowTitle('MyQtWindow')
    
    def blurBtnClicked(self):
        blimg = cv2.blur(self.empire_cv, (20, 20))
        pmap = QPixmap.fromImage(cv2qt(blimg))
        self.scene.clear()
        self.scene.addPixmap(pmap)
        self.view.setScene(self.scene)
    
    def resetBtnClicked(self):
        pmap = QPixmap.fromImage(cv2qt(self.empire_cv))
        self.scene.clear()
        self.scene.addPixmap(pmap)
        self.view.setScene(self.scene)

def cv2qt(cv_img):
    height, width, depth = cv_img.shape
    imrgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    qt_img = QImage(imrgb.data, width, height, depth*width, QImage.Format_RGB888)
    return qt_img

MyApp = QApplication(sys.argv)
mainWindow = MyMainWindow()
mainWindow.show()

MyApp.exec()
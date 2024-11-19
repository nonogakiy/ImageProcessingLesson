#
# pip install PySide6 --proxy=proxy.citizen.co.jp:8080
#
import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
import cv2
import numpy as np

class MyMainWindow(QMainWindow):
    # コンストラクタ
    def __init__(self):
        super().__init__()
        #
        self.resetBtn = QPushButton('Reset')
        self.resetBtn.clicked.connect(self.resetBtnClicked)
        self.FFTBtn = QPushButton('FFT')
        self.FFTBtn.clicked.connect(self.FFTBtnClicked)
        #
        self.empire_cv = cv2.imread('./data/empire.jpg', cv2.IMREAD_GRAYSCALE)
        self.scene = QGraphicsScene()
        self.view = QGraphicsView()
        empire_qt = cv2qt(self.empire_cv)
        pmap = QPixmap.fromImage(empire_qt)
        self.scene.addPixmap(pmap)
        self.view.setScene(self.scene)
        #
        vbox = QVBoxLayout()
        vbox.addWidget(self.resetBtn)
        vbox.addWidget(self.FFTBtn)
        vbox.addStretch()
        #
        hbox = QHBoxLayout()
        hbox.addWidget(self.view)
        hbox.addLayout(vbox)
        #
        MainContents = QWidget()
        MainContents.setLayout(hbox)
        self.setCentralWidget(MainContents)
        #
        self.setWindowTitle('MyQtWindow')
    
    def FFTBtnClicked(self):
        f = np.fft.fft2(self.empire_cv)
        f_mag = 20*np.log(np.abs(f))
        pmap = QPixmap.fromImage(cv2qt(f_mag))
        self.scene.clear()
        self.scene.addPixmap(pmap)
        self.view.setScene(self.scene)
    
    def resetBtnClicked(self):
        pmap = QPixmap.fromImage(cv2qt(self.empire_cv))
        self.scene.clear()
        self.scene.addPixmap(pmap)
        self.view.setScene(self.scene)

def cv2qt(cv_img):
    height, width = cv_img.shape
    qt_img = QImage(cv_img, width, height, width, QImage.Format_Grayscale8)
    return qt_img

MyApp = QApplication(sys.argv)
mainWindow = MyMainWindow()
mainWindow.show()

MyApp.exec()
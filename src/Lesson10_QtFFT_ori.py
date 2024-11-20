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
        width = 512
        height = 512
        self.currmat = np.zeros((width, height), dtype=float)
        x_ind = np.arange(0, width, 1)
        y_ind = np.arange(0, height, 1)
        x_mes, y_mes = np.meshgrid(x_ind, y_ind)
        self.currmat = np.cos(2*np.pi / width * 10 * x_mes + 2*np.pi / height * 20 *y_mes)
        self.currimg_cv = (100 * (self.currmat + 1)).astype(np.uint8)
        self.scene = QGraphicsScene()
        self.view = QGraphicsView()
        currimg_qt = cv2qt(self.currimg_cv)
        pmap = QPixmap.fromImage(currimg_qt)
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
        f = np.fft.fft2(self.currmat)
        f_shift = np.fft.fftshift(f)
        f_mag = np.abs(f_shift)/3
        f_u8 = f_mag.astype(np.uint8)
        pmap = QPixmap.fromImage(cv2qt(f_u8))
        self.scene.clear()
        self.scene.addPixmap(pmap)
        self.view.setScene(self.scene)
    
    def resetBtnClicked(self):
        pmap = QPixmap.fromImage(cv2qt(self.currimg_cv))
        self.scene.clear()
        self.scene.addPixmap(pmap)
        self.view.setScene(self.scene)

def cv2qt(cv_img):
    height, width = cv_img.shape
    qt_img = QImage(cv_img.flatten(), width, height, QImage.Format_Grayscale8)
    return qt_img

MyApp = QApplication(sys.argv)
mainWindow = MyMainWindow()
mainWindow.show()

MyApp.exec()
#
# pip install PySide6 --proxy=proxy.citizen.co.jp:8080
#
import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
import cv2
import numpy as np
import math

class MyMainWindow(QMainWindow):
    # コンストラクタ
    def __init__(self):
        super().__init__()
        #
        self.width = 512
        self.height = 512
        self.kx = self.width /4
        self.ky = 0
        # Slider
        self.sldWaveNumAbs = QSlider()
        self.sldWaveNumAbs.setOrientation(Qt.Orientation.Horizontal)
        self.sldWaveNumAbs.setRange(0, self.width/2)
        self.sldWaveNumAbs.setValue(self.kx)
        self.sldWaveNumAbs.valueChanged.connect(self.sldWaveNumChanged)
        self.sldWaveNumAng = QSlider()
        self.sldWaveNumAng.setOrientation(Qt.Orientation.Horizontal)
        self.sldWaveNumAng.setRange(0, 359)
        self.sldWaveNumAng.setValue(0)
        self.sldWaveNumAng.valueChanged.connect(self.sldWaveNumChanged)
        #
        self.currmat = np.zeros((self.width, self.height), dtype=float)
        x_ind = np.arange(0, self.width, 1)
        y_ind = np.arange(0, self.height, 1)
        self.x_mes, self.y_mes = np.meshgrid(x_ind, y_ind)
        sigma = 50.0
        self.mask = np.exp(-((self.x_mes - self.width/2)**2 + (self.y_mes - self.height/2)**2)/(2*sigma**2)) 
        self.currview = np.cos(2*np.pi / self.width * self.kx * self.x_mes + 2*np.pi / self.height * self.ky * self.y_mes)
        self.currmat = self.currview * self.mask
        self.currimg_cv = (100 * (self.currview + 1)).astype(np.uint8)
        self.scene = QGraphicsScene()
        self.view = QGraphicsView()
        currimg_qt = cv2qt(self.currimg_cv)
        pmap = QPixmap.fromImage(currimg_qt)
        self.scene.addPixmap(pmap)
        self.view.setScene(self.scene)
        #
        f = np.fft.fft2(self.currmat)
        f_shift = np.fft.fftshift(f)
        f_mag = np.abs(f_shift)/50
        f_u8 = f_mag.astype(np.uint8)
        pmap = QPixmap.fromImage(cv2qt(f_u8))
        self.sceneFFT = QGraphicsScene()
        self.viewFFT = QGraphicsView()
        self.sceneFFT.addPixmap(pmap)
        self.viewFFT.setScene(self.sceneFFT)
        #
        vbox = QVBoxLayout()
        vbox.addWidget(self.sldWaveNumAbs)
        vbox.addWidget(self.sldWaveNumAng)
        vbox.addStretch()
        #
        hbox = QHBoxLayout()
        hbox.addWidget(self.view)
        hbox.addWidget(self.viewFFT)
        hbox.addLayout(vbox)
        #
        MainContents = QWidget()
        MainContents.setLayout(hbox)
        self.setCentralWidget(MainContents)
        #
        self.setWindowTitle('MyQtWindow')
    
    def sldWaveNumChanged(self, x):
        kabs = self.sldWaveNumAbs.value()
        kang = self.sldWaveNumAng.value()
        kang = kang / 180.0 *  math.pi

        self.kx = kabs * math.cos(kang)
        self.ky = kabs * math.sin(kang)

        self.currview = np.cos(2*np.pi / self.width * self.kx * self.x_mes + 2*np.pi / self.height * self.ky * self.y_mes)
        self.currmat = self.currview * self.mask
        self.currimg_cv = (100 * (self.currview + 1)).astype(np.uint8)
        currimg_qt = cv2qt(self.currimg_cv)
        pmap = QPixmap.fromImage(currimg_qt)
        self.scene.clear()
        self.scene.addPixmap(pmap)
        self.view.setScene(self.scene)
        #
        f = np.fft.fft2(self.currmat)
        f_shift = np.fft.fftshift(f)
        f_mag = np.abs(f_shift)/50
        f_u8 = f_mag.astype(np.uint8)
        pmap = QPixmap.fromImage(cv2qt(f_u8))
        self.sceneFFT.clear()
        self.sceneFFT.addPixmap(pmap)
        self.viewFFT.setScene(self.sceneFFT)
        
    
def cv2qt(cv_img):
    height, width = cv_img.shape
    qt_img = QImage(cv_img.flatten(), width, height, QImage.Format_Grayscale8)
    return qt_img

MyApp = QApplication(sys.argv)
mainWindow = MyMainWindow()
mainWindow.show()

MyApp.exec()
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt
import cv2
import math

class FilterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Filter')
        self.hbox = QHBoxLayout()
        self.vbox = QVBoxLayout()
        #
        self.rbFilterGroup = QButtonGroup()
        for fn in ['Blur', 'MedianBlur', 'Gaussian', 'Bilateral']:
            rbItem = QRadioButton(fn)
            self.vbox.addWidget(rbItem)
            self.rbFilterGroup.addButton(rbItem)
        self.rbFilterGroup.buttons()[0].setChecked(True)
        #
        self.sldFilterStrength = QSlider()
        self.sldFilterStrength.setOrientation(Qt.Orientation.Horizontal)
        self.sldFilterStrength.setRange(0, 255)
        self.sldFilterStrength.setValue(0)
        self.sldFilterStrength.valueChanged.connect(self.onSldValueChanged)
        self.vbox.addWidget(self.sldFilterStrength)
        self.vbox.addStretch()
        #
        self.scene = QGraphicsScene()
        self.view = QGraphicsView()
        self.empire_cv = cv2.imread('./data/empireMini.jpg')
        empire_qt = cv2qt(self.empire_cv)
        pmap = QPixmap.fromImage(empire_qt)
        self.scene.addPixmap(pmap)
        self.view.setScene(self.scene)
        self.hbox.addWidget(self.view)
        self.hbox.addLayout(self.vbox)
        #
        self.setLayout(self.hbox)

    #Event
    def onSldValueChanged(self, x):
        fn = self.rbFilterGroup.checkedButton().text()
        if fn == 'Blur':
            blur_size = int(math.floor(x / 8))
            if blur_size != 0:
                blimg = cv2.blur(self.empire_cv, (blur_size, blur_size))
                pmap = QPixmap.fromImage(cv2qt(blimg))
                self.scene.addPixmap(pmap)
                self.view.setScene(self.scene)
        elif fn == 'MedianBlur':
            blur_size = int(math.floor(x / 16) * 2 + 1)
            if blur_size != 0:
                blimg = cv2.medianBlur(self.empire_cv, blur_size)
                pmap = QPixmap.fromImage(cv2qt(blimg))
                self.scene.addPixmap(pmap)
                self.view.setScene(self.scene)
        elif fn == 'Gaussian':
            blur_size = x / 255 * 20.0
            if blur_size != 0.0:
                blimg = cv2.GaussianBlur(self.empire_cv, (31,31), blur_size)
                pmap = QPixmap.fromImage(cv2qt(blimg))
                self.scene.addPixmap(pmap)
                self.view.setScene(self.scene)
        else:
            blur_size = x / 255 * 1000.0
            if blur_size != 0.0:
                blimg = cv2.bilateralFilter(self.empire_cv, d=5,sigmaColor = blur_size, sigmaSpace=5.0)
                pmap = QPixmap.fromImage(cv2qt(blimg))
                self.scene.addPixmap(pmap)
                self.view.setScene(self.scene)


    #utility
def cv2qt(cv_img):
    height, width, depth = cv_img.shape
    imrgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    qt_img = QImage(imrgb.data, width, height, depth*width, QImage.Format.Format_RGB888)
    return qt_img
    
qApp = QApplication(sys.argv)
mainWindow = FilterApp()
mainWindow.show()
qApp.exec()
        
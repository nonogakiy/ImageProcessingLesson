import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
import cv2
import math

class FilterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        #
        # UI parts
        # Radio Button
        self.rbFilterGroup = QButtonGroup()
        rbvbox = QVBoxLayout()
        rbFilter = QGroupBox('Chose Filter')
        for fn in ['Blur', 'MedianBlur', 'Gaussian', 'Bilateral']:
            rbItem = QRadioButton(fn)
            rbvbox.addWidget(rbItem)
            self.rbFilterGroup.addButton(rbItem)
        self.rbFilterGroup.buttons()[0].setChecked(True)
        rbFilter.setLayout(rbvbox)
        # Slider
        self.sldFilterStrength = QSlider()
        self.sldFilterStrength.setOrientation(Qt.Orientation.Horizontal)
        self.sldFilterStrength.setRange(0, 255)
        self.sldFilterStrength.setValue(0)
        self.sldFilterStrength.valueChanged.connect(self.sldValueChanged)
        # View
        self.scene = QGraphicsScene()
        self.view = QGraphicsView()
        self.empire_cv = cv2.imread('./data/empire.jpg')
        empire_qt = cv2qt(self.empire_cv)
        pmap = QPixmap.fromImage(empire_qt)
        self.scene.addPixmap(pmap)
        self.view.setScene(self.scene)
        #
        # Layout
        #
        vbox = QVBoxLayout()
        vbox.addWidget(rbFilter)
        vbox.addWidget(self.sldFilterStrength)
        vbox.addStretch()
        hbox = QHBoxLayout()
        hbox.addWidget(self.view)
        hbox.addLayout(vbox)
        #
        MainContent = QWidget()
        MainContent.setLayout(hbox)
        self.setCentralWidget(MainContent)
        #
        # Menu Bar
        # File Menu
        self.topMenu = self.menuBar()
        menu_file = self.topMenu.addMenu('File')
        open_act = QAction('Open...', self)
        open_act.triggered.connect(self.openFile)
        save_act = QAction("Save...", self)
        quit_act = QAction("Quit", self)
        quit_act.triggered.connect(self.close)
        menu_file.addAction(open_act)
        menu_file.addAction(save_act)
        menu_file.addSeparator()
        menu_file.addAction(quit_act)
        # Edit Menu
        menu_edit = self.topMenu.addMenu('Edit')
        #
        #　Status Bar
        #
        self.sbMessage = self.statusBar()
        self.sbMessage.showMessage('Status: 初期状態')
        #
        #
        # Window Title
        self.setWindowTitle('Filter')
        #
    # Event
    def sldValueChanged(self, x):
        fn = self.rbFilterGroup.checkedButton().text()
        if fn == 'Blur':
            blur_size = int(math.floor(x / 8))
            if blur_size != 0:
                blimg = cv2.blur(self.empire_cv, (blur_size, blur_size))
                pmap = QPixmap.fromImage(cv2qt(blimg))
            else:
                pmap = QPixmap.fromImage(cv2qt(self.empire_cv))
        elif fn == 'MedianBlur':
            blur_size = int(math.floor(x / 16) * 2 + 1)
            if blur_size != 0:
                blimg = cv2.medianBlur(self.empire_cv, blur_size)
                pmap = QPixmap.fromImage(cv2qt(blimg))
            else:
                pmap = QPixmap.fromImage(cv2qt(self.empire_cv))
        elif fn == 'Gaussian':
            blur_size = x / 255 * 20.0
            if blur_size != 0.0:
                blimg = cv2.GaussianBlur(self.empire_cv, (31,31), blur_size)
                pmap = QPixmap.fromImage(cv2qt(blimg))
            else:
                pmap = QPixmap.fromImage(cv2qt(self.empire_cv))
        else:
            blur_size = x / 255 * 1000.0
            if blur_size != 0.0:
                blimg = cv2.bilateralFilter(self.empire_cv, d=5,sigmaColor = blur_size, sigmaSpace=200.0)
                pmap = QPixmap.fromImage(cv2qt(blimg))
            else:
                pmap = QPixmap.fromImage(cv2qt(self.empire_cv))                
        self.scene.clear()
        self.scene.addPixmap(pmap)
        self.view.setScene(self.scene)
        self.sbMessage.showMessage(f'Status: Blur ({blur_size})')
        #
    # Menu Action
    def openFile(self):
        self.filepath = QFileDialog.getOpenFileName(self, 'Open File Dialog')
        #
# utility
def cv2qt(cv_img):
    height, width, depth = cv_img.shape
    imrgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    qt_img = QImage(imrgb.data, width, height, depth*width, QImage.Format.Format_RGB888)
    return qt_img

# MainProgram
qApp = QApplication(sys.argv)
mainWindow = FilterApp()
mainWindow.show()
qApp.exec()
        
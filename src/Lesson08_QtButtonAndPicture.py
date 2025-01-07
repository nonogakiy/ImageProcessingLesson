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
        # ボタンを配置
        self.firstBtn = QPushButton('first')
        self.secondBtn = QPushButton('second')
        # ラジオボタンを配置
        self.rbButtons = QButtonGroup()
        rbvbox = QVBoxLayout()
        rbGroupBox = QGroupBox('選択肢')
        for item in ['Option1', 'Option2', 'Option3', 'Option4']:
            rbItem = QRadioButton(item)
            rbvbox.addWidget(rbItem)
            self.rbButtons.addButton(rbItem)
        rbGroupBox.setLayout(rbvbox)
        self.rbButtons.buttons()[0].setChecked(True) #Option1を選択しておく
        #addcomment
        # スライダーを配置
        self.sldValue = QSlider()
        self.sldValue.setOrientation(Qt.Orientation.Horizontal)
        self.sldValue.setRange(0, 255)
        self.sldValue.valueChanged.connect(self.sldValueChanged)
        # 画像を配置
        self.newimg_cv = cv2.imread('./data/empire.jpg')
        self.scene = QGraphicsScene()
        self.view = QGraphicsView()
        newimg_qt = cv2qt(self.newimg_cv)
        pmap = QPixmap.fromImage(newimg_qt)
        self.scene.addPixmap(pmap)
        self.view.setScene(self.scene)
        # レイアウト縦
        vbox = QVBoxLayout()
        vbox.addWidget(self.firstBtn)
        vbox.addWidget(self.secondBtn)
        vbox.addWidget(rbGroupBox)
        vbox.addWidget(self.sldValue)
        vbox.addStretch()
        # レイアウト横
        hbox = QHBoxLayout()
        hbox.addWidget(self.view)
        hbox.addLayout(vbox)
        # コンテンツの配置
        MainContents = QWidget()
        MainContents.setLayout(hbox)
        self.setCentralWidget(MainContents)
        # メニューバーの定義
        self.topMenu = self.menuBar()
        menu_file = self.topMenu.addMenu('File')
        open_act = QAction('Open...', self)
        open_act.triggered.connect(self.openFile)
        menu_file.addAction(open_act)
        quit_act = QAction('Quit', self)
        quit_act.triggered.connect(self.close)
        menu_file.addAction(quit_act)
        menu_edit = self.topMenu.addMenu('Edit')
        # ステータスバーの定義
        self.sbMessage = self.statusBar()
        self.sbMessage.showMessage('Status: 初期状態')
        # ウインドウタイトルの定義
        self.setWindowTitle('MyQtWindow')
    
    def openFile(self):
        self.filepath = QFileDialog.getOpenFileName(self, 'Open File Dialog')
        self.newimg_cv = cv2.imread(self.filepath[0])
        newimg_qt = cv2qt(self.newimg_cv)
        pmap = QPixmap.fromImage(newimg_qt)
        self.scene.clear()
        self.scene.addPixmap(pmap)
        self.view.setScene(self.scene)
        self.sbMessage.showMessage(self.filepath[0])

    def sldValueChanged(self, x):
        self.sbMessage.showMessage(str(x))

def cv2qt(cv_img):
    height, width, depth = cv_img.shape
    imrgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    qt_img = QImage(imrgb.data, width, height, depth*width, QImage.Format_RGB888)
    return qt_img

MyApp = QApplication(sys.argv)
mainWindow = MyMainWindow()
mainWindow.show()

MyApp.exec()
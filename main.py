import random
from json import load, dump

from PyQt6 import QtCore, QtGui, QtWidgets, QtMultimedia

import prizeshow
from mainwindow import Ui_MainForm
from photoshop import loadimages
from showprizes import Ui_Dialog


class MainWindow(QtWidgets.QMainWindow, Ui_MainForm):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.getconfig()
        self.prizes = self.configs.get('奖项')

        self.init_menus()
        self._height = 768
        self._width = 1366
        self.pixelratio = 1.0
        self.getscreensize()
        self.frameimage.setPixmap(QtGui.QPixmap('AE2.jpg'))
        self.frameimage.setText('')
        
        self.showFullScreen()
        self.configs = {}
        self.imagelist = loadimages()
        
        self._blockWidth = int(self._width / 15)
        self._blockHeight = int(self._height / 15)
        self.imagerowscount = len(self.imagelist) // 15 + int((len(self.imagelist) % 15) != 0)
        if (self._height - self.imagerowscount * self._blockHeight) < self._blockHeight:
            self.yoffset = 0
        else:
            self.yoffset = int((self._height - (self.imagerowscount * self._blockHeight)) / 2)
        self.imagedict = {}
        self.running = False
        self.init_ui()
        self.autotimer = QtCore.QTimer(self)
        self.autotimer.timeout.connect(self.setAnimation)
        self.autotimer.setInterval(20)
        self.prizeid = 0
        self.prizedialog = PrizeDilog(self._width, self._height, self)
        self.bgm = QtMultimedia.QSoundEffect()
        self.bgm.setSource(QtCore.QUrl.fromLocalFile('runing.wav'))

    def init_ui(self):
        self.CW.setGeometry(0, 0, self._width, self._height)
        self.frameimage.setGeometry(0, 0, self._width, self._height)
        print(self.imagelist)
        for i in range(len(self.imagelist)):
            photo = str(self.imagelist[i])

            lable = QtWidgets.QLabel(f'({photo})', self.frameimage)
            lable.setProperty('imagepath', f'({photo})')
            lable.setGeometry(QtCore.QRect((i % 15) * self._blockWidth, self.yoffset + (i // 15) * self._blockHeight,
                            self._blockWidth, self._blockHeight))
            lable.setProperty('order', i)
            lable.setProperty('type', 'image')
            lable.setObjectName(f'image{i}')
            lable.setVisible(False)
            lable.setPixmap(QtGui.QPixmap(photo))
            lable.setScaledContents(True)
            lable.setProperty('sizemode', 'init')
            lable.setVisible(True)
            lable.setStyleSheet(
                'border-width:1px;border-style:solid;border-color: rgb(self._blockWidth,self._blockWidth,'
                'self._blockWidth)')


    def init_menus(self):
        i = 0
        for prize in self.prizes:
            action = QtWidgets.QWidgetAction(self.menu_prizes)
            action.setProperty('prizeid',0)
            i += 1
            action.setObjectName(prize['name'])
            if prize['count'] <=0:
                action.setEnabled(False)
            action.setText(prize['name'])
            action.setCheckable(True)
            action.setShortcut(QtCore.QCoreApplication.translate("MainForm", f"F{i + 1}"))
            action.toggled.connect(self.prizemenuchange)
            self.menu_prizes.addAction(action)
            action.setChecked(True)
        self.menuBar().setVisible(False)


    def prizemenuchange(self):
        if self.sender().isChecked():
            self.menu_prizes.setProperty('prize', self.sender().text())
            self.setWindowTitle(f'AE二部抽奖程序[正在抽取{self.sender().text()}]')
            self.prize = self.sender().text()
        for at in self.menu_prizes.actions():
            if at.objectName() != self.menu_prizes.property('prize'):
                at.setChecked(False)
            else:
                self.prizeidx = at.property('prizeid')
                self.prize = self.configs['奖项'][self.prizeidx]

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        self.getconfig()
        """
        根据按下的按键响应不同事件:
            空格:开始/结束滚动
            F11: 全屏/最大化
            F12:显示快捷键列表
            F10:随机滚动/顺序滚动
            F9:显示获奖者列表
            F8:随机调整图片顺序
            F5:切换为四等奖
            F4:切换为三等奖
            F3:切换为二等奖
            F2:切换为一等奖
            F1:切换为特等奖
        """

        if a0.key() == QtCore.Qt.Key.Key_Space:
            self.runorstop()
        if not self.running:
            if a0.key() == QtCore.Qt.Key.Key_Escape:
                self.close()
            elif a0.key() == QtCore.Qt.Key.Key_Delete:
                self.clearconfigs()
            elif a0.key() == QtCore.Qt.Key.Key_F11:
                self.fullscreen()
            elif a0.key() == QtCore.Qt.Key.Key_F12:
                self.prizedialog.showMessage()
            elif a0.key() == QtCore.Qt.Key.Key_F10:
                self.actionrandom.setChecked(not self.actionrandom.isChecked())
            elif a0.key() == QtCore.Qt.Key.Key_F9:
                self.showallprizes(self.configs["奖项"][self.prizeidx])
            elif a0.key() == QtCore.Qt.Key.Key_F8:
                self.loadImage()
            elif a0.key() == QtCore.Qt.Key.Key_F5:
                self.menu_prizes.actions()[4].setChecked(True)
                self.prizedialog.showMessage(f'切换为{"四等奖"}', 1)
                self.prizeidx = 4
            elif a0.key() == QtCore.Qt.Key.Key_F4:
                self.menu_prizes.actions()[3].setChecked(True)
                self.prizedialog.showMessage(f'切换为{"三等奖"}', 1)
                self.prizeidx = 3
            elif a0.key() == QtCore.Qt.Key.Key_F3:
                self.menu_prizes.actions()[2].setChecked(True)
                self.prizedialog.showMessage(f'切换为{"二等奖"}', 1)
                self.prizeidx = 2
            elif a0.key() == QtCore.Qt.Key.Key_F2:
                self.menu_prizes.actions()[1].setChecked(True)
                self.prizedialog.showMessage(f'切换为{"一等奖"}', 1)
                self.prizeidx = 1
            elif a0.key() == QtCore.Qt.Key.Key_F1:
                self.menu_prizes.actions()[0].setChecked(True)
                self.prizedialog.showMessage(f'切换为{"特等奖"}', 1)
                self.prizeidx = 0

    def clearconfigs(self):
        self.configs = {
            "奖项": [
                {
                    "name": "特等奖",
                    "count": 1,
                    "persions": [
                    ]
                },
                {
                    "name": "一等奖",
                    "count": 2,
                    "persions": [
                    ]
                },
                {
                    "name": "二等奖",
                    "count": 4,
                    "persions": [
                    ]
                },
                {
                    "name": "三等奖",
                    "count": 6,
                    "persions": [
                    ]
                },
                {
                    "name": "四等奖",
                    "count": 10,
                    "persions": [
                    ]
                }
            ],
            "中獎人員名單": [
            ]
        }
        self.setconfig()
        self.getconfig()

    def setconfig(self):
        with open('config.json', 'w', encoding='utf-8') as f:
            dump(self.configs, f, ensure_ascii=False, indent=4)

    def hiddenimage(self):
        self.frameimage.setPixmap(QtGui.QPixmap('AE2.jpg'))
        for child in self.frameimage.children():
            if child.property('type') == 'image':
                child.setVisible(False)

    def showimage(self):
        for child in self.frameimage.children():
            if child.property('type') == 'image':
                child.setVisible(True)

    def fullscreen(self):
        print('触发全屏')
        if self.isFullScreen():
            # self.prizedialog.showMessage(message='退出全屏', Duration=1)
            self.showMaximized()
            self.menuBar().setVisible(True)
            self.CW.setGeometry(0, 0, self._width, self._height)
            self.frameimage.setGeometry(0, 0, self._width, self._height)
            self.frameimage.setScaledContents(True)
        else:
            # self.prizedialog.showMessage(message='开启全屏', Duration=1)
            self.menuBar().setVisible(False)
            self.showFullScreen()
            self.CW.setGeometry(0, 0, self._width, self._height)
            self.frameimage.setGeometry(0, 0, self._width, self._height)
            self.frameimage.setScaledContents(True)

    def runorstop(self) -> None:
        self.getconfig()

        self.prize = self.configs["奖项"][self.prizeidx]
        if self.prize['count'] <= 0:
            self.prizedialog.showMessage(f'{self.prize["name"]}已将抽完,请选择其他',1)
            return
        self.showimage()
        if self.autotimer.isActive():
            # self.bgm.stop()
            self.autotimer.stop()
            self.running = False
            self.prizedialog.showPrize(self.prize, self.prizefilename, self.frameimage.pixmap())
        else:
            if not self.isFullScreen():
                self.fullscreen()
            self.autotimer.start()
            self.running = True
            # self.bgm.play()

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.CW.resize(a0.size())
        self.frameimage.resize(a0.size())
        if self.isFullScreen():
            self.CW.setGeometry(0, 0, self._width, self._height)
            self.frameimage.setGeometry(0, 0, self._width, self._height)

    def showprizes(self):
        self.getconfig()
        self.prizes = self.configs.get('奖项')
        print(self.prizes)

    def getconfig(self) -> dict:
        with open(r'config.json', 'r', encoding='utf-8') as f:
            self.configs = load(f)
        return self.configs

    def deleimage(self):
        self.loadImage()

    def showhelp(self):
        self.prizedialog.showMessage()

    def startAnimation2big(self, widget: QtWidgets.QWidget, ratio: float):
        # noinspection PyTypeChecker
        animation = QtCore.QPropertyAnimation(widget, b"geometry", self.CW)
        old_pose = widget.geometry()
        idx = widget.property('order')
        if idx // 15 == 0:
            new_y = self.yoffset
        elif idx // 15 == (len(self.imagelist) - 1) // 15:
            new_y = self._height - self.yoffset - int((ratio * 2 + 0.1) * self._blockHeight)
        else:
            new_y = self.yoffset + (idx // 15) * self._blockHeight - int(ratio * self._blockHeight)

        if idx % 15 == 0:
            new_pose = QtCore.QRect(0, new_y,
                                    self._blockWidth + int((ratio * 2) * self._blockWidth),
                                    self._blockHeight + int((ratio * 2) * self._blockHeight))
        elif idx % 15 == 14:
            new_pose = QtCore.QRect(self._width - (self._blockWidth + int((ratio * 2) * self._blockWidth)), new_y,
                                    self._blockWidth + int((ratio * 2) * self._blockWidth),
                                    self._blockHeight + int((ratio * 2) * self._blockHeight))
        else:
            new_pose = QtCore.QRect((idx % 15) * self._blockWidth - (int(ratio * self._blockWidth)), new_y,
                                    self._blockWidth + int((ratio * 2) * self._blockWidth),
                                    self._blockHeight + int((ratio * 2) * self._blockHeight))

        animation.setStartValue(old_pose)
        animation.setEndValue(new_pose)
        animation.setDuration(5)
        animation.start()
        widget.setProperty('sizemode', 'big')

    def startAnimation2small(self, widget: QtWidgets.QWidget):
        # noinspection PyTypeChecker
        animation = QtCore.QPropertyAnimation(widget, b"geometry", self.frameimage)
        old_pose = widget.geometry()
        idx = widget.property('order')
        new_pose = QtCore.QRect((idx % 15) * self._blockWidth + (int(0.05 * self._blockWidth)),
                                self.yoffset + (idx // 15) * self._blockHeight + int(0.5 * self._blockHeight),
                                self._blockWidth - int(0.1 * self._blockWidth),
                                self._blockHeight - int(0.1 * self._blockHeight))
        animation.setStartValue(old_pose)
        animation.setEndValue(new_pose)
        animation.setDuration(5)
        animation.start()
        widget.setProperty('sizemode', 'small')

    def startAnimationReset(self, widget: QtWidgets.QWidget):
        # noinspection PyTypeChecker
        animation = QtCore.QPropertyAnimation(widget, b"geometry", self.CW)
        old_pose = widget.geometry()
        idx = widget.property('order')
        new_pose = QtCore.QRect((idx % 15) * self._blockWidth, self.yoffset + (idx // 15) * self._blockHeight,
                                self._blockWidth, self._blockHeight)
        animation.setStartValue(old_pose)
        animation.setEndValue(new_pose)
        animation.setDuration(5)
        animation.start()
        widget.setProperty('sizemode', 'init')

    def setAnimation(self):
        # print(datetime.datetime.now())
        if self.actionrandom.isChecked():
            self.prizeid = random.randint(0, len(self.imagelist) - 1)
        else:
            if self.prizeid >= len(self.imagelist) - 1:
                self.prizeid = 0
            else:
                self.prizeid += 1
        self.prizefilename = self.imagelist[self.prizeid]
        self.frameimage.setPixmap(QtGui.QPixmap(self.prizefilename))
        for child in self.frameimage.children():
            currfilename = child.property('imagepath')
            if not currfilename:
                continue

            if self.prizefilename not in child.property('imagepath'):
                try:
                    self.startAnimation2small(child)
                    child.setStyleSheet(
                        'border-width:1px;border-style:solid;border-color: rgb(self._blockWidth,self._blockWidth,'
                        'self._blockWidth)')
                except Exception as e:
                    print(repr(e))
            else:
                child.raise_()


                try:
                    self.startAnimation2big(child, 0.6)
                    child.setStyleSheet('border-width:5px;border-style:solid;border-color: rgb(0,0,255)')
                except Exception as e:
                    print(repr(e))

    def loadImage(self):
        print('导入图片')
        self.imagelist = loadimages()
        print(self.imagelist)
        for child in self.frameimage.children():
            if child.property('type') == 'image':
                print(child.property('imagepath')[1:-1])
                currfilename = child.property('imagepath')[1:-1]
                if currfilename:
                    if currfilename in self.imagelist:
                        child.setProperty('order', self.imagelist.index(currfilename))
                        self.startAnimationReset(child)
                    else:
                        child.deleteLater()

    def showallprizes(self,prize:dict):
        self.hiddenimage()
        PrizeForm(self._width, self._height, prize, self)

    def getscreensize(self):
        screen = QtGui.QGuiApplication.primaryScreen().geometry()
        self._width = screen.width()
        self._height = screen.height()
        self.pixelratio = QtGui.QGuiApplication.primaryScreen().devicePixelRatio()


class PrizeDilog(Ui_Dialog, QtWidgets.QDialog):
    def __init__(self, screen_width, screen_height, parent=None):
        super(PrizeDilog, self).__init__(parent)
        print(self.parent().objectName())
        self.picturename = ''
        self.setupUi(self)
        self.getconfig()
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.Autoclose)
        self._height = screen_height
        self._width = screen_width
        self.setGeometry(int(self._width * 0.2), int(self._height * 0.15), int(self._width * 0.6),
                         int((self._width * 0.6) * (9 / 16) + self._height * 0.1))
        self.contentbox.setGeometry(0, 0, int(self._width * 0.6),
                                    int((self._width * 0.6) * (9 / 16)))
        self.buttonBox.setGeometry(0, int((self._width * 0.6) * (9 / 16)), int(self._width * 0.6),
                                   int(self._height * 0.1))

    def showMessage(self, message: str = '', Duration: int = 3):
        self.setVisible(True)
        if Duration <= 0:
            Duration = 3
        self.setWindowTitle('提示框')
        if message == '':
            message = ('''
            快捷鍵列表:
                空格:开始/结束滚动
                F11: 全屏/最大化
                F12:显示快捷键列表
                F10:随机滚动/顺序滚动
                F9:显示获奖者列表
                F8:随机调整图片顺序
                F5:切换为四等奖
                F4:切换为三等奖
                F3:切换为二等奖
                F2:切换为一等奖
                F1:切换为特等奖
            ''')
        self.contentbox.setText(message)
        self.picturename = ''
        self.prize = ''
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Close)
        self.buttonBox.setGeometry(0, int((self._width * 0.6) * (9 / 16)), int(self._width * 0.6),
                                   int(self._height * 0.1))
        self.buttonBox.buttons()[0].setText(f'{Duration}秒后自動關閉')
        self.comboBox.setVisible(False)
        self.show()
        self.loopcount = Duration
        self.timer.start()

    def showPrize(self, prize: dict, picturepath: str, picture: QtGui.QPixmap):
        self.getconfig()
        self.setVisible(True)
        self.prize = prize
        self.setWindowTitle(f'第{len(prize["persions"])+1}名{prize["name"]}中獎確認')
        self.picturename = picturepath
        self.contentbox.setPixmap(picture)
        self.contentbox.setScaledContents(True)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        self.buttonBox.buttons()[0].setText('確認')
        self.buttonBox.buttons()[1].setText('忽略')
        self.buttonBox.setGeometry(0, int((self._width * 0.6) * (9 / 16)), int(self._width * 0.6),
                                   int(self._height * 0.1))
        self.comboBox.setGeometry(0, int((self._width * 0.6) * (9 / 16)), int(self._width * 0.3),
                                  int(self._height * 0.1))
        self.comboBox.setVisible(False)
        self.show()
    def accept(self):
        self.setVisible(False)
        self.configs['中獎人員名單'].append(self.picturename)
        for idx,_ in enumerate(self.configs['奖项']):
            if _['name'] == self.prize['name']:
                _['persions'].append(self.picturename)
                _['count'] = _['count']-1
                self.prizecount = _['count']
                self.prizeindex = idx
                break
        self.setconfig()
        self.getconfig()
        self.parent().deleimage()
        self.parent().showallprizes(self.configs['奖项'][self.prizeindex])
        if self.prizecount <= 0:
            super(PrizeDilog, self).accept()

    def getconfig(self) -> dict:
        with open(r'config.json', 'r', encoding='utf-8') as f:
            self.configs = load(f)
        return self.configs

    def setconfig(self):
        with open('config.json', 'w', encoding='utf-8') as f:
            dump(self.configs, f, ensure_ascii=False, indent=4)

    def Autoclose(self):
        self.loopcount -= 1
        self.buttonBox.buttons()[0].setText(f'{self.loopcount}秒后自動關閉')
        if self.loopcount <= 0:
            self.timer.stop()
            self.close()


class PrizeForm(prizeshow.Ui_Dialog,QtWidgets.QDialog):
    def __init__(self, screen_width, screen_height, prizeinfo:dict,parent=None):
        super(PrizeForm, self).__init__(parent)
        self.setupUi(self)
        self.bgm = QtMultimedia.QSoundEffect()
        self.bgm.setSource(QtCore.QUrl.fromLocalFile('runing.wav'))
        op = QtWidgets.QGraphicsOpacityEffect()
        op.setOpacity(0.5)


        self.background.setGeometry(0, 0, screen_width, screen_height)
        self.background.setPixmap(QtGui.QPixmap('AE6.JPG'))
        self.background.setScaledContents(True)
        self.prizetitle.setGeometry(int(screen_width * 0.1), 0, int(screen_width * 0.8), int(screen_height * 0.1))
        self.prizetitle.setText(f'{prizeinfo["name"]}获奖人员展示')
        self.prizetitle.setStyleSheet('color:#000000;background-color:rgb(128,128,128)')
        self.prizetitle.setGraphicsEffect(op)
        persions = prizeinfo["persions"]
        prizetype = prizeinfo['name']
        if prizetype == '四等奖':
            imagewidth = int(screen_width / 4)
            imageheight = int(imagewidth * (9 / 16))
            for idx, imagepath in enumerate(persions):
                lable = QtWidgets.QLabel(self)

                if idx == 5 or idx == 6:
                    lable.setGeometry(int(imagewidth * 0.01 + ((5 + idx) % 4) * (imagewidth * 1.005))
                                      , int(screen_height * 0.15 + ((5 + idx) // 4) * (imageheight * 1.01)), imagewidth,
                                      imageheight)
                elif idx == 4:
                    lable.setGeometry(int(imagewidth * 1.05 + (idx % 4) * (imagewidth * 1.01)),
                                      int(screen_height * 0.15 + (idx // 4) * (imageheight * 1.01)),
                                      imagewidth, imageheight)
                elif idx == 7:
                    lable.setGeometry(int(imagewidth * -1.01 + (idx % 4) * (imagewidth * 1.01)),
                                      int(screen_height * 0.15 + (idx // 4) * (imageheight * 1.01)),
                                      imagewidth, imageheight)
                else:
                    lable.setGeometry(int(imagewidth * 0.01 + (idx % 4) * (imagewidth * 1.005)),
                                      int(screen_height * 0.15 + (idx // 4) * (imageheight * 1.01)),
                                      imagewidth, imageheight)
                lable.setPixmap(QtGui.QPixmap(imagepath))
                lable.setScaledContents(True)
        elif prizetype == '三等奖':
            imagewidth = int(screen_width / 3)
            imageheight = int(imagewidth * (9 / 16))
            for idx, imagepath in enumerate(persions):
                lable = QtWidgets.QLabel(self)
                lable.setGeometry(int(imagewidth * 0.01 + (idx % 3) * (imagewidth * 1.01)),
                                  int(screen_height * 0.15 + (idx // 3) * (imageheight * 1.01)),
                                  imagewidth, imageheight)
                lable.setPixmap(QtGui.QPixmap(imagepath))
                lable.setScaledContents(True)
        elif prizetype == '二等奖':
            imagewidth = int(screen_width / 2.5)
            imageheight = int(imagewidth * (9 / 16))
            for idx, imagepath in enumerate(persions):
                lable = QtWidgets.QLabel(self)
                lable.setGeometry(int(imagewidth * 0.20 + (idx % 2) * (imagewidth * 1.01)),
                                  int(screen_height * 0.15 + (idx // 2) * (imageheight * 1.01)),
                                  imagewidth, imageheight)
                lable.setPixmap(QtGui.QPixmap(imagepath))
                lable.setScaledContents(True)
        elif prizetype == '一等奖':
            imagewidth = int(screen_width / 2.1)
            imageheight = int(imagewidth * (9 / 16))
            for idx, imagepath in enumerate(persions):
                lable = QtWidgets.QLabel(self)
                lable.setGeometry(int(imagewidth * 0.04 + (idx % 2) * (imagewidth * 1.01)),
                                  int(screen_height * 0.15 + (idx // 2) * (imageheight * 1.01)),
                                  imagewidth, imageheight)
                lable.setPixmap(QtGui.QPixmap(imagepath))
                lable.setScaledContents(True)
        elif prizetype == '特等奖':
            imagewidth = int(screen_width / 1.25)
            imageheight = int(imagewidth * (9 / 16))
            for idx, imagepath in enumerate(persions):
                lable = QtWidgets.QLabel(self)
                lable.setGeometry(int(imagewidth * 0.12) + (idx % 2) * imagewidth,
                                  int(screen_height * 0.15 + (idx // 2) * (imageheight * 1.05)),
                                  imagewidth, imageheight)
                lable.setPixmap(QtGui.QPixmap(imagepath))
                lable.setScaledContents(True)

        self.showFullScreen()
        # self.bgm.play()

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() == QtCore.Qt.Key.Key_Space:
            # self.bgm.stop()
            self.accept()


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    main_form = MainWindow()
    sys.exit(app.exec())
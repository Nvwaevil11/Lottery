# Form implementation generated from reading ui file 'prizeshow.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1264, 843)
        self.background = QtWidgets.QLabel(parent=Dialog)
        self.background.setGeometry(QtCore.QRect(0, 50, 1920, 1030))
        self.background.setObjectName("background")
        self.prizetitle = QtWidgets.QLabel(parent=Dialog)
        self.prizetitle.setGeometry(QtCore.QRect(0, 0, 1920, 50))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(48)
        font.setBold(True)
        font.setUnderline(False)
        self.prizetitle.setFont(font)
        self.prizetitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.prizetitle.setObjectName("prizetitle")
        
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.background.setText(_translate("Dialog", "TextLabel"))
        self.prizetitle.setText(_translate("Dialog",
                                           "<html><head/><body><p><span style=\" "
                                           "color:#000000;background-color:rgb(128,128,128)\">"
                                           "四等奖获奖名单</span></p></body></html>"))
# Form implementation generated from reading ui file 'prizesetting.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(504, 310)
        self.formLayoutWidget = QtWidgets.QWidget(parent=Form)
        self.formLayoutWidget.setGeometry(QtCore.QRect(20, 50, 471, 251))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(parent=self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label)
        self.line_edit_prize_name = QtWidgets.QLineEdit(parent=self.formLayoutWidget)
        self.line_edit_prize_name.setObjectName("line_edit_prize_name")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.line_edit_prize_name)
        self.label_2 = QtWidgets.QLabel(parent=self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_2)
        self.spin_box_prize_count = QtWidgets.QSpinBox(parent=self.formLayoutWidget)
        self.spin_box_prize_count.setObjectName("spin_box_prize_count")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.spin_box_prize_count)
        self.label_3 = QtWidgets.QLabel(parent=self.formLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(16)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_3)
        self.list_view_winners = QtWidgets.QListView(parent=self.formLayoutWidget)
        self.list_view_winners.setObjectName("list_view_winners")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.list_view_winners)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=self.formLayoutWidget)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.buttonBox)
        self.label_title = QtWidgets.QLabel(parent=Form)
        self.label_title.setGeometry(QtCore.QRect(150, 10, 181, 31))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(28)
        self.label_title.setFont(font)
        self.label_title.setObjectName("label_title")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "獎項名稱"))
        self.label_2.setText(_translate("Form", "獎項數量"))
        self.label_3.setText(_translate("Form", "中獎人員"))
        self.label_title.setText(_translate("Form", "設置獎項"))
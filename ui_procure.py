# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_procure.ui'
#
# Created: Fri Apr 25 13:43:41 2014
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Procure(object):
    def setupUi(self, Procure):
        Procure.setObjectName(_fromUtf8("Procure"))
        Procure.resize(379, 109)
        self.buttonBox = QtGui.QDialogButtonBox(Procure)
        self.buttonBox.setGeometry(QtCore.QRect(200, 60, 171, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.comboBox = QtGui.QComboBox(Procure)
        self.comboBox.setGeometry(QtCore.QRect(160, 20, 211, 21))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox_2 = QtGui.QComboBox(Procure)
        self.comboBox_2.setGeometry(QtCore.QRect(30, 20, 69, 22))
        self.comboBox_2.setObjectName(_fromUtf8("comboBox_2"))

        self.retranslateUi(Procure)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Procure.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Procure.reject)
        QtCore.QMetaObject.connectSlotsByName(Procure)

    def retranslateUi(self, Procure):
        Procure.setWindowTitle(_translate("Procure", "Procure", None))


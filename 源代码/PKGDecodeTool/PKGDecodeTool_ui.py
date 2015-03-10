# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PKGDecodeTool.ui'
#
# Created: Tue Jul 31 19:29:26 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmMain(object):
    def setupUi(self, frmMain):
        frmMain.setObjectName(_fromUtf8("frmMain"))
        frmMain.resize(534, 445)
        self.btnOpenFile = QtGui.QPushButton(frmMain)
        self.btnOpenFile.setGeometry(QtCore.QRect(440, 40, 75, 23))
        self.btnOpenFile.setObjectName(_fromUtf8("btnOpenFile"))
        self.label_2 = QtGui.QLabel(frmMain)
        self.label_2.setGeometry(QtCore.QRect(10, 12, 61, 20))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.btnSelDir = QtGui.QPushButton(frmMain)
        self.btnSelDir.setGeometry(QtCore.QRect(440, 10, 75, 23))
        self.btnSelDir.setObjectName(_fromUtf8("btnSelDir"))
        self.lstFileList = QtGui.QListWidget(frmMain)
        self.lstFileList.setGeometry(QtCore.QRect(10, 90, 511, 311))
        self.lstFileList.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.lstFileList.setObjectName(_fromUtf8("lstFileList"))
        self.btnDecode = QtGui.QPushButton(frmMain)
        self.btnDecode.setGeometry(QtCore.QRect(10, 410, 75, 23))
        self.btnDecode.setObjectName(_fromUtf8("btnDecode"))
        self.btnDecodeAll = QtGui.QPushButton(frmMain)
        self.btnDecodeAll.setGeometry(QtCore.QRect(100, 410, 75, 23))
        self.btnDecodeAll.setObjectName(_fromUtf8("btnDecodeAll"))
        self.btnExit = QtGui.QPushButton(frmMain)
        self.btnExit.setGeometry(QtCore.QRect(440, 410, 75, 23))
        self.btnExit.setObjectName(_fromUtf8("btnExit"))
        self.label_3 = QtGui.QLabel(frmMain)
        self.label_3.setGeometry(QtCore.QRect(10, 41, 61, 20))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(frmMain)
        self.label_4.setGeometry(QtCore.QRect(10, 70, 61, 20))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.txtSavePath = QtGui.QLineEdit(frmMain)
        self.txtSavePath.setGeometry(QtCore.QRect(80, 10, 351, 20))
        self.txtSavePath.setObjectName(_fromUtf8("txtSavePath"))
        self.txtSrcFile = QtGui.QLineEdit(frmMain)
        self.txtSrcFile.setGeometry(QtCore.QRect(80, 40, 351, 20))
        self.txtSrcFile.setObjectName(_fromUtf8("txtSrcFile"))

        self.retranslateUi(frmMain)
        QtCore.QObject.connect(self.btnExit, QtCore.SIGNAL(_fromUtf8("clicked()")), frmMain.close)
        QtCore.QMetaObject.connectSlotsByName(frmMain)

    def retranslateUi(self, frmMain):
        frmMain.setWindowTitle(QtGui.QApplication.translate("frmMain", "PKG资源包解密工具", None, QtGui.QApplication.UnicodeUTF8))
        self.btnOpenFile.setText(QtGui.QApplication.translate("frmMain", "打开文件", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("frmMain", "保存路径：", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSelDir.setText(QtGui.QApplication.translate("frmMain", "选择目录", None, QtGui.QApplication.UnicodeUTF8))
        self.btnDecode.setText(QtGui.QApplication.translate("frmMain", "解密", None, QtGui.QApplication.UnicodeUTF8))
        self.btnDecodeAll.setText(QtGui.QApplication.translate("frmMain", "全部解密", None, QtGui.QApplication.UnicodeUTF8))
        self.btnExit.setText(QtGui.QApplication.translate("frmMain", "退出", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("frmMain", "PKG资源包：", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("frmMain", "文件列表：", None, QtGui.QApplication.UnicodeUTF8))


# -*- coding: utf-8 -*-

import sys, os, codecs, struct, zlib
from PyQt4 import QtCore, QtGui

from PKGDecodeTool_ui import Ui_frmMain

class Worker(QtCore.QThread):   # 后台工作线程
    def __init__(self, parent = None):
        QtCore.QThread.__init__(self, parent)
        self.exiting = False
        self.savePath = u''
        self.pkgFileName = u''
        self.fileList = []
        self.index = []
        
    def __del__(self):
        self.exiting = True
        self.wait()

    def Decode(self, fileList, index):
        self.fileList = fileList
        self.index = index
        self.start()

    def mif2png(self, fileName):
        fileSize = os.path.getsize(fileName)
        if fileSize < 20:
            print fileName, u'是一个无效的MIF文件！'
            return
        
        f = open(fileName, 'rb')
        
        mifVersion = f.read(4)
        mifVersion, = struct.unpack('l', mifVersion)
        
        frameWidth = f.read(4)
        frameWidth, = struct.unpack('l', frameWidth)
        
        frameHeight = f.read(4)
        frameHeight, = struct.unpack('l', frameHeight)
        
        mifType = f.read(4)
        mifType, = struct.unpack('l', mifType)
        
        frameCount = f.read(4)
        frameCount, = struct.unpack('l', frameCount)
        
        imageWidth = frameWidth
        imageHeight = frameHeight * frameCount

        prefix = 0
        if mifType == 3:
            prefix = 20
        elif mifType == 7:
            prefix = 20 + 4 * frameCount
        else:
            print fileName, u'是一个无效的MIF文件！'
            return

        valid = True
        if mifVersion == 0:
            if prefix + imageWidth * imageHeight * 3 != fileSize:
                valid = False
        elif mifVersion == 1:
            if prefix + imageWidth * imageHeight * 3 > fileSize:
                valid = False

        if not valid:
            print fileName, u'是一个无效的MIF文件！'
            return

        img = QtGui.QImage(imageWidth, imageHeight, QtGui.QImage.Format_ARGB32)
        for currentFrame in range(0, frameCount):
            if mifType == 7:
                f.read(4)

            rgb16 = []
            for i in range(0, frameHeight * frameWidth):
                tmp = f.read(2)
                tmp, = struct.unpack('H', tmp)
                rgb16.append(tmp)
            
                    
            a8 = []
            for i in range(0, frameHeight * frameWidth):
                tmp = f.read(1)
                tmp, = struct.unpack('B', tmp)
                a8.append(tmp)
                
            for y in range(0, frameHeight):
                for x in range(0, frameWidth):
                    a = a8[x + y * frameWidth]
                    r = (rgb16[x + y * frameWidth] & 0xF800) >> 8  # 0xF800 = 1111100000000000
                    g = (rgb16[x + y * frameWidth] & 0x07E0) >> 3  # 0x07E0 = 0000011111100000
                    b = (rgb16[x + y * frameWidth] & 0x001F) << 3  # 0x001F = 0000000000011111
                    if a == 32:
                        a = 255
                    elif a > 0:
                        a <<= 3
                    img.setPixel(x, frameHeight * currentFrame + y, QtGui.qRgba(r, g, b, a))
                    
        outFileName = os.path.splitext(os.path.basename(fileName))[0] + u'.png'
        outFileName = os.path.join(os.path.dirname(fileName), outFileName)
        if os.path.isfile(outFileName):
            os.remove(outFileName)
            
        img.save(outFileName)
        
        f.close()
    
    def run(self):
        # 从pkg全路径中取不带扩展名的文件名，用做保存的文件夹名称
        folder = os.path.splitext(os.path.basename(self.pkgFileName))[0]
        # print folder
        
        for i in self.index:
            # 拼接用做保存的全路径文件名
            fileName = os.path.join(self.savePath, folder, self.fileList[i][0])
            print fileName

            pathName = os.path.dirname(fileName)        # 获得目录名
            if not os.path.exists(pathName):            # 判断目录是否存在
                os.makedirs(pathName)                   # 创建多级目录
                
            f = open(self.pkgFileName, 'rb')            # 获取压缩数据
            f.seek(self.fileList[i][1])
            fileData = f.read(self.fileList[i][3])
            f.close()
                
            fileData = zlib.decompress(fileData)        # 解压缩并保存到文件
            f = open(fileName, 'wb')
            f.write(fileData)
            f.close()

            self.mif2png(fileName)                      # 将mif文件转换为png文件

            ####################调用mif2png.exe将mif文件转换为png文件####################
            #import subprocess
            
            #outFileName = os.path.splitext(os.path.basename(fileName))[0] + u'.png'
            #outFileName = os.path.join(os.path.dirname(fileName), outFileName)
            #if os.path.isfile(outFileName):
            #    os.remove(outFileName)
    
            #cmd = '\"' + os.path.join(unicode(QtCore.QDir.currentPath()), u'mif2png.exe') + u'\" \"' + fileName + u'\"'
            #st = subprocess.STARTUPINFO
            #st.dwFlags = subprocess.STARTF_USESHOWWINDOW
            #st.wShowWindow = subprocess.SW_HIDE
            #subprocess.Popen(cmd.encode('gbk'), startupinfo = st)
            ####################调用mif2png.exe将mif文件转换为png文件####################
        
        self.emit(QtCore.SIGNAL('WorkerDone(int)'), 0)

class MainForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_frmMain()
        self.ui.setupUi(self)

        QtCore.QObject.connect(self.ui.btnSelDir, QtCore.SIGNAL("clicked()"),
                               self.SelDir_Btn_Clicked)
        QtCore.QObject.connect(self.ui.btnOpenFile, QtCore.SIGNAL("clicked()"),
                               self.OpenFile_Btn_Clicked)
        QtCore.QObject.connect(self.ui.btnDecode, QtCore.SIGNAL("clicked()"),
                               self.Decode_Btn_Clicked)
        QtCore.QObject.connect(self.ui.btnDecodeAll, QtCore.SIGNAL("clicked()"),
                               self.DecodeAll_Btn_Clicked)
        
        self.ui.txtSavePath.setText(QtCore.QDir.currentPath())

        self.fileList = []
        self.thread = Worker()

        self.connect(self.thread, QtCore.SIGNAL('WorkerDone(int)'), self.WorkerDone)
        self.connect(self.thread, QtCore.SIGNAL('started()'), self.WorkerStarted)
        self.connect(self.thread, QtCore.SIGNAL('finished()'), self.WorkerFinished)
        self.connect(self.thread, QtCore.SIGNAL("terminated()"), self.WorkerFinished)

    def WorkerDone(self, n):
        self.MsgBox(u'提示', u'解密成功!')
        self.ui.btnDecode.setEnabled(True)
        self.ui.btnDecodeAll.setEnabled(True)

    def WorkerStarted(self):
        print u'后台线程开始运行'
        
    def WorkerFinished(self):
        print u'后台线程运行结束！'
    
    # “选择目录”按钮单击
    def SelDir_Btn_Clicked(self):
        fileDlg = QtGui.QFileDialog(self, u'选择目录', QtCore.QDir.currentPath())
        savePath = fileDlg.getExistingDirectory()
        savePath = unicode(savePath)
        if os.path.isdir(savePath):
            self.ui.txtSavePath.setText(savePath)
        
    # “打开文件”按钮单击    
    def OpenFile_Btn_Clicked(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self, u'打开文件', 
                QtCore.QDir.currentPath(), u'PKG资源包(*.pkg);;所有文件(*.*)')
        fileName = unicode(fileName)
        if os.path.isfile(fileName):
            self.ui.txtSrcFile.setText(fileName)
            self.ReadPkgFile(fileName)
            self.ShowFileList()

    # 读取Pkg资源包内的文件列表
    def ReadPkgFile(self, fileName):
        self.fileList = []
        
        f = open(fileName, 'rb')
        
        self.pkgFileHeader = f.read(4)  # 文件标识(64 00 00 00)
        self.pkgFileHeader, = struct.unpack('l', self.pkgFileHeader)
        if self.pkgFileHeader == 0x64:
            print '\"', fileName, '\"', ' is pkg file!'
        else:
            print '\"', fileName, '\"', ' is not pkg file!'
            f.close()
            return

        self.fileCount = f.read(4)
        self.fileCount, = struct.unpack('l', self.fileCount)
        print u'文件总数：', self.fileCount

        self.fileListPos = f.read(4)
        self.fileListPos, = struct.unpack('l', self.fileListPos)
        print u'文件列表区的偏移地址：', self.fileListPos

        self.fileListSize = f.read(4)
        self.fileListSize, = struct.unpack('l', self.fileListSize)
        print u'文件列表区的大小：', self.fileListSize

        f.seek(self.fileListPos)
        
        for i in range(0, self.fileCount):
            self.fileList.append([])
            
            self.tmpFileNameLen = f.read(2)  # 文件名称字符串长度
            self.tmpFileNameLen, = struct.unpack('H', self.tmpFileNameLen)

            self.tmpFileName = f.read(self.tmpFileNameLen)  # 带相对路径的文件名称
            self.fileList[i].append(self.tmpFileName)

            f.read(4)    # 识别标志(00 00 00 00)

            self.tmpFileStartOffset = f.read(4)    # 文件起始偏移地址
            self.tmpFileStartOffset, = struct.unpack('l', self.tmpFileStartOffset)
            self.fileList[i].append(self.tmpFileStartOffset)
        
            self.tmpFileOriginSize = f.read(4)    # 原始文件大小
            self.tmpFileOriginSize, = struct.unpack('l', self.tmpFileOriginSize)
            self.fileList[i].append(self.tmpFileOriginSize)
            
            self.tmpFileSize = f.read(4)    # 文件大小
            self.tmpFileSize, = struct.unpack('l', self.tmpFileSize)
            self.fileList[i].append(self.tmpFileSize)
        
        f.close()

    # 显示文件列表
    def ShowFileList(self):
        self.ui.lstFileList.clear()
        
        if len(self.fileList) <= 0:
            return
        
        for item in self.fileList:
            self.ui.lstFileList.addItem(item[0])
    
    # “解密”按钮单击
    def Decode_Btn_Clicked(self):
        if self.ui.lstFileList.count() <= 0:
            self.MsgBox(u'提示', u'文件列表为空！')
            return
        
        if len(self.ui.lstFileList.selectedItems()) <= 0:
            self.MsgBox(u'提示', u'未选中文件！')
            return
        
        savePath = unicode(self.ui.txtSavePath.text())
        pkgFileName = unicode(self.ui.txtSrcFile.text())

        if not os.path.isfile(pkgFileName):
            self.MsgBox(u'提示', u'PKG资源包不存在！')
            return

        self.ui.btnDecode.setEnabled(False)
        self.ui.btnDecodeAll.setEnabled(False)

        index = []
        for i in range(0, self.ui.lstFileList.count()):
            if self.ui.lstFileList.isItemSelected(self.ui.lstFileList.item(i)):
                index.append(i)

        self.thread.savePath = savePath
        self.thread.pkgFileName = pkgFileName
        self.thread.Decode(self.fileList, index)
                
    # “全部解密”按钮单击
    def DecodeAll_Btn_Clicked(self):
        if self.ui.lstFileList.count() <= 0:
            self.MsgBox(u'提示', u'文件列表为空！')
            return
        
        savePath = unicode(self.ui.txtSavePath.text())
        pkgFileName = unicode(self.ui.txtSrcFile.text())

        if not os.path.isfile(pkgFileName):
            self.MsgBox(u'提示', u'PKG资源包不存在！')
            return

        self.ui.btnDecode.setEnabled(False)
        self.ui.btnDecodeAll.setEnabled(False)

        index = []
        for i in range(0, self.ui.lstFileList.count()):
            index.append(i)

        self.thread.savePath = savePath
        self.thread.pkgFileName = pkgFileName
        self.thread.Decode(self.fileList, index)

    # 自定义消息框
    def MsgBox(self, title, msg):
        msgbox = QtGui.QMessageBox(self)
        msgbox.setFont(QtGui.QFont('Tahoma', 9))
        msgbox.setWindowTitle(title)
        msgbox.setText(msg)
        msgbox.setIcon(QtGui.QMessageBox.Information)
        msgbox.addButton(u'确定', QtGui.QMessageBox.AcceptRole)
        msgbox.exec_()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mainForm = MainForm()
    mainForm.show()
    sys.exit(app.exec_())

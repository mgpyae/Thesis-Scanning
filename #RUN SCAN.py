import sys
import os
import subprocess
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication
import scanning
from PyQt5.QtCore import *
import time
import globals

class Worker(QRunnable):

    @pyqtSlot()
    def run(self):
        '''
        Your code goes in this function
        '''
        #scanning.scan()
        scanning.scan()

    def stop_scan(self):
        scanning.scan()
        #pass

    def quit_me(self):
        print("EXITING...")
        sys.exit()
        #main.close()
        #sys.exit(app.exec_())

# Streaming printed message on text box
class MyStream(QtCore.QObject):
    message = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(MyStream, self).__init__(parent)

    def write(self, message):
        self.message.emit(str(message))

class MyWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        self.pushButtonPrint = QtWidgets.QPushButton(self)
        self.pushButtonPrint.setText("Start Scan!")

        self.pushButtonPrint_2 = QtWidgets.QPushButton(self)
        self.pushButtonPrint_2.setText("Stop Scan!")

        self.pushButtonPrint_3 = QtWidgets.QPushButton(self)
        self.pushButtonPrint_3.setText("Quit App!")

        self.combobox = QtWidgets.QComboBox(self)
        self.combobox.addItems(["White Piece", "Red Piece", "Wire"])
        #self.combobox.setGeometry(QRect(70, 65, 150, 30))

        self.showLabel = QtWidgets.QLabel(self)
        self.showLabel.setText("Choose Scan Option")
        self.showLabel.setAlignment(Qt.AlignCenter)

        self.showLabel2 = QtWidgets.QLabel(self)
        self.showLabel2.setText("")
        self.showLabel2.setAlignment(Qt.AlignCenter)

        self.pushButtonPrint.clicked.connect(self.on_pushButtonPrint_clicked)
        self.pushButtonPrint_2.clicked.connect(self.on_pushButtonPrint2_clicked)
        self.pushButtonPrint_3.clicked.connect(self.on_pushButtonPrint3_clicked)
        #self.combobox.currentTextChanged.connect(self.on_comboChanged)
        self.combobox.activated[str].connect(self.on_comboChanged)

        self.textEdit = QtWidgets.QTextEdit(self)

        self.layoutVertical = QtWidgets.QVBoxLayout(self)
        self.layoutVertical.addWidget(self.pushButtonPrint)
        self.layoutVertical.addWidget(self.showLabel)
        self.layoutVertical.addWidget(self.combobox)
        self.layoutVertical.addStretch(50)
        self.layoutVertical.addWidget(self.showLabel2)
        self.layoutVertical.addWidget(self.pushButtonPrint_2)
        self.layoutVertical.addWidget(self.pushButtonPrint_3)
        self.layoutVertical.addWidget(self.textEdit)

    @QtCore.pyqtSlot()
    def on_pushButtonPrint_clicked(self):
        #cmd = 'python scanning.py'                                  # +++ `python `
        #output = subprocess.check_output(cmd, shell=True)               # ---
       #output2 = subprocess.check_output(['pythoon','pytest01','-i', 'test.txt'],stderr= subprocess.STDOUT)
        #print (output)
        worker = Worker()
        self.threadpool.start(worker)
        self.pushButtonPrint.setEnabled(False)

    def on_pushButtonPrint2_clicked(self):
        # p = subprocess.Popen('python scanning.py')
        # poll = p.poll()
        # if poll is None:
        #     print("Not Active")

        # worker3 = Worker()
        # self.threadpool.start(worker3.stop_scan())
        globals.stopSign = "stop"
        self.pushButtonPrint.setEnabled(True)
        time.sleep(1)
        globals.stopSign = "run"

    @QtCore.pyqtSlot()
    def on_pushButtonPrint3_clicked(self):
        globals.stopSign = "stop"
        print("Scan Stopped")
        print("App Quitting")
        time.sleep(1)
        sys.exit()
        # worker2 = Worker()
        # self.threadpool.start(worker2.quit_me())

    #@QtCore.pyqtSlot()
    def on_comboChanged(self, value):
        print ("Scan Option Changed to "+ value)
        globals.scanPiece = value


    @QtCore.pyqtSlot(str)
    def on_myStream_message(self, message):
        self.textEdit.moveCursor(QtGui.QTextCursor.End)
        self.textEdit.insertPlainText(message)

if __name__ == "__main__":
    import sys
    globals.global_initialize()
    globals.stopSign = "run"

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('Scanning App')

    main = MyWindow()
    main.show()

    myStream = MyStream()
    myStream.message.connect(main.on_myStream_message)

    sys.stdout = myStream
    sys.exit(app.exec_())
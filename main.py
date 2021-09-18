from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox
from PyQt5 import uic

import sys


class Test(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('StatsView.ui', self)

        self.isSerialOpened = False

        self.serial = QSerialPort()
        self.serial.setBaudRate(9600)
        # self.serial.setPortName(QSerialPortInfo.availablePorts()[0].portName())

        self.avPortsList.addItems(map(lambda x: x.portName(), QSerialPortInfo.availablePorts()))

        self.butt_send.clicked.connect(self.serialPrint)
        self.butt_inter.clicked.connect(self.serialInteract)

        self.portBaudRate.activated.connect(self.setBaudRate)


    def serialInteract(self):
        if self.isSerialOpened:
            self.serialClose()
            self.isSerialOpened = False
            self.butt_inter.setText("Open")
        elif not self.isSerialOpened:
            self.serialOpen()
            self.butt_inter.setText("Close")
            self.isSerialOpened = True

    def serialOpen(self):
        self.serial.open(QIODevice.ReadWrite)

    def serialClose(self):
        self.serial.close()

    def serialPrint(self):
        self.serial.write(self.lineEdit.text().encode())

    def setBaudRate(self):
        self.serial.setBaudRate(int(self.portBaudRate.currentText()))


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Test()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())

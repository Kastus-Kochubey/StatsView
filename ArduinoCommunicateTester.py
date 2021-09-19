import PyQt5.QtGui
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice
from PyQt5.QtWidgets import QApplication, QWidget, QListWidgetItem
from PyQt5 import uic
from PyQt5.QtCore import Qt

from threading import Thread
import sys
import schedule
from json import dumps, loads

SETTINGS_FILE_NAME = 'data.json'
MAX_LEN_READ_LINE_DATA = 100

class TestWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('ACT.ui', self)

        self.loadSettings()
        self.setup()
        self.connections()

    def setup(self):
        self.serial = QSerialPort()
        self.setCurrBaudRate()
        # self.serial.setBaudRate(9600)

        ports_names = list(map(lambda x: x.portName(), QSerialPortInfo.availablePorts()))
        self.avPortsList.addItems(ports_names)
        if len(ports_names):
            self.setPortName()

        # TODO:
        def scheduleRun():
            schedule.every().second.do(self.acceptData)
            schedule.every().second.do(self.log)
            schedule.run_all()

        # scheduleThread = Thread(target=scheduleRun())
        scheduleRun()

    def connections(self):
        self.serial.readyRead.connect(self.acceptData)

        self.butt_send.clicked.connect(self.serialSend)
        self.butt_inter.clicked.connect(self.serialInteract)

        self.portBaudRate.activated.connect(self.setCurrBaudRate)
        self.avPortsList.activated.connect(self.setPortName)
        self.lineEdit.returnPressed.connect(self.serialSend)

    def loadSettings(self):
        with open(SETTINGS_FILE_NAME, mode='r') as file:
            data = loads(''.join(file.readlines()))
            print(f'data: {data}')
            self.portBaudRate.setCurrentIndex(self.portBaudRate.findText(data['baud_rate']))

    # def keyPressEvent(self, event):
    #     print(f'{event.key()} pressed  {Qt.Key_e}')
    #     if event.key() == Qt.Key_Enter:
    #         print('enter pressed')
    #         if self.lineEdit.hasFocus():
    #             self.serialSend()

    def log(self):
        self.logList.addItem(f'port: {self.serial.portName()} '
                             f'baudRate: {self.serial.baudRate()}')
        print(f'port: {self.serial.portName()}')

    # TODO:
    def acceptData(self):
        # TODO:
        # data = str(self.serial.readLineData(100))
        data = self.serial.readLineData(MAX_LEN_READ_LINE_DATA)
        if data != 'None' and data:
            self.listWidget.addItem(data.decode())

    def setPortName(self):
        self.serial.setPortName(self.avPortsList.currentText())

    def setCurrBaudRate(self):
        self.serial.setBaudRate(int(self.portBaudRate.currentText()))

    def serialInteract(self):
        def serialOpen():
            self.serial.open(QIODevice.ReadWrite)

        def serialClose():
            self.serial.close()

        if self.serial.isOpen():
            serialClose()
            self.butt_inter.setText("Open")
        else:
            serialOpen()
            self.butt_inter.setText("Close")

    def serialSend(self):
        if self.serial.isOpen():
            print('serialSend')
            text = self.lineEdit.text()
            self.serial.writeData(text.encode())
            item = QListWidgetItem(text)
            item.setTextAlignment(Qt.AlignRight)
            self.listWidget.addItem(item)
            self.lineEdit.clear()

    def closeEvent(self, event):
        QWidget.closeEvent(self, event)
        data = {}
        if self.serial.isOpen():
            print('Serial close')
            self.serial.close()

        data['baud_rate'] = self.portBaudRate.currentText()
        with open(SETTINGS_FILE_NAME, mode='w') as file:
            file.write(dumps(data))


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TestWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())

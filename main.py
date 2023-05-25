# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import imp
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from GUIalpha import Ui_MainWindow
from function import Function_UI
import serial, serial.tools.list_ports


class MainWindow():
    def __init__(self):
        self.main_win = QMainWindow()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self.main_win)

        self.serial = Function_UI()
        self.serialPort = serial.Serial()

        self.uic.baud_List.addItems(self.serial.baudList)
        self.uic.baud_List.setCurrentText('9600')
        self.update_ports()
        self.uic.connect_Button.clicked.connect(self.connect_serial)
        self.uic.send_Button.clicked.connect(self.send_data)
        self.uic.clear_Button.clicked.connect(self.clear)
        self.uic.update_Button.clicked.connect(self.update_ports)
        self.serial.data_available.connect(self.update_view)

    def update_view(self, data):
        self.uic.textBrowser.append(data)

    def connect_serial(self):
        if (self.uic.connect_Button.isChecked()):
            port = self.uic.port_List.currentText()
            baud = self.uic.baud_List.currentText()
            self.serial.serialPort.port = port
            self.serial.serialPort.baudrate = baud
            self.serial.connect_serial()
            if (self.serial.serialPort.is_open):
                self.uic.connect_Button.setText("Disconnect")
        else:
            self.serial.disconnect_serial()
            self.uic.connect_Button.setText("Connect")

    def send_data(self):
        data_send = self.uic.send_Text.toPlainText()
        self.serial.send_data(data_send)

    def update_ports(self):
        self.serial.update_port()
        self.uic.port_List.clear()
        self.uic.port_List.addItems(self.serial.portList)

    def clear(self):
        self.uic.textBrowser.clear()

    def show(self):
        # command to run
        self.main_win.show()


def sine_wave(self, period):
    t = np.arange(0.0, 2.0 * period, 0.01)
    sine = 1 + np.sine(2 * np.pi * t)
    fig, axs = plt.subplots()
    axs.plot(t, sine)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())

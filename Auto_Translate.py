import sys
import time
from os import listdir
from os.path import exists
import threading

import cv2
import imutils
import numpy as np
import pyautogui as auto
import pytesseract
from PIL import ImageGrab
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QMainWindow, QLabel, QComboBox, QSlider, QPushButton, QCheckBox, QApplication, QWidget, \
    QPlainTextEdit, QAction, QMessageBox
from googletrans import Translator

RUN = True  # The main bool, true for all the treads to run, false to close all threads

if not exists("C:\\Program Files\\Tesseract-OCR\\tesseract.exe"):
    auto.alert(
        "Tesseract is not installed\nPlease install tesseract https://github.com/tesseract-ocr/tesseract/releases/tag/5.0.0-alpha")
    sys.exit()

translator = Translator()
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# asm.traineddata
f = listdir("C:\\Program Files\\Tesseract-OCR\\tessdata")
languages = []
for file in f:
    sp = file.split(".")
    if len(sp) == 2 and sp[1] == "traineddata":
        languages.append(sp[0])

lang = "eng"
x0 = 100
y0 = 100
x1 = 500
y1 = 500
gray_cutoff = 150
rotation_angle_deg = 0
gauss_constant = 3
invert = False
do_gauss = False
auto_up = False
print_to_con = False
new_img = auto.screenshot()


def kill_program():
    sys.exit()


class Main(QWidget):
    update_qt = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def display_image(self):
        global x0, y0, x1, y1, new_img

        def process_img(original_image):
            gray = np.array(original_image.convert('L'))
            if do_gauss:
                if invert:
                    gray = cv2.bitwise_not(gray)
                threshed_image = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 7,
                                                       gauss_constant)
            else:
                if invert:
                    ret, threshed_image = cv2.threshold(gray, gray_cutoff, 255, cv2.THRESH_BINARY_INV)
                else:
                    ret, threshed_image = cv2.threshold(gray, gray_cutoff, 255, cv2.THRESH_BINARY)
            rotated_image = imutils.rotate(threshed_image, rotation_angle_deg)
            return rotated_image

        while RUN:
            if x0 >= x1 or y0 >= y1:
                x0 = 100
                y0 = 100
                x1 = 500
                y1 = 500
            img = ImageGrab.grab(bbox=(x0, y0, x1, y1))
            new_img = process_img(img)
            cv2.imshow('Window', new_img)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

    def run(self):
        while RUN:
            if auto_up:
                self.get_text()
            else:
                time.sleep(1)

    def get_text(self):
        try:
            text = pytesseract.image_to_string(new_img, lang)
        except SystemError:
            text = "Error"
        if lang != "eng" and lang != "equ" and lang != "osd" and text != "":
            result = translator.translate(text).text
        elif text != "":
            result = text
        else:
            result = "-Empty-"
        self.update_qt.emit(result)


class MainGUI(QMainWindow):

    def __init__(self):
        super().__init__()

        label0 = QLabel("Language:", self)
        label0.setGeometry(30, 10, 100, 20)

        self.lan = QComboBox(self)
        self.lan.addItems(languages)
        self.lan.setGeometry(130, 10, 100, 20)
        self.lan.setCurrentText("eng")
        self.lan.currentIndexChanged.connect(self.set_lang)

        label = QLabel("Grayscale Cutoff", self)
        label.setGeometry(30, 40, 200, 20)

        gslider = QSlider(Qt.Horizontal, self)
        gslider.setGeometry(30, 60, 200, 20)
        gslider.setMinimum(0)
        gslider.setMaximum(255)
        gslider.setSingleStep(1)
        gslider.setValue(150)
        gslider.valueChanged[int].connect(self.set_gray_cutoff)

        label2 = QLabel("Rotate", self)
        label2.setGeometry(30, 80, 200, 20)

        self.rslider = QSlider(Qt.Horizontal, self)
        self.rslider.setGeometry(30, 100, 200, 20)
        self.rslider.setMinimum(-90)
        self.rslider.setMaximum(90)
        self.rslider.setValue(0)
        self.rslider.valueChanged[int].connect(self.set_rotation)

        reset_button = QPushButton("Reset Rotation", self)
        reset_button.setGeometry(30, 125, 100, 30)
        reset_button.pressed.connect(self.reset)

        checkbox = QCheckBox("Invert", self)
        checkbox.setGeometry(140, 130, 100, 20)
        checkbox.stateChanged.connect(self.set_invert)

        gauss_check = QCheckBox("Gaussian", self)
        gauss_check.setGeometry(200, 130, 100, 20)
        gauss_check.stateChanged.connect(self.set_gauss)

        label3 = QLabel("Gaussian Constant", self)
        label3.setGeometry(30, 165, 200, 20)

        gaussslider = QSlider(Qt.Horizontal, self)
        gaussslider.setGeometry(30, 190, 200, 20)
        gaussslider.setMinimum(0)
        gaussslider.setMaximum(30)
        gaussslider.setSingleStep(1)
        gaussslider.setValue(3)
        gaussslider.valueChanged[int].connect(self.set_gauss_constant)

        bounds = QPushButton("Set Bounds", self)
        bounds.setGeometry(30, 230, 100, 30)
        bounds.pressed.connect(self.set_bounds)

        up = QPushButton("Get Text", self)
        up.setGeometry(150, 230, 100, 30)
        up.pressed.connect(self.calc)

        self.audit = QCheckBox("Auto Update", self)
        self.audit.setGeometry(330, 240, 100, 30)
        self.audit.stateChanged.connect(self.set_auto_up)

        label4 = QLabel("Out Text", self)
        label4.setGeometry(345, 10, 200, 30)

        # self.out = QLabel("Out:", self)
        self.out = QPlainTextEdit(self)
        self.out.setGeometry(270, 40, 200, 200)

        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)

        self.app = Main()
        self.app.update_qt.connect(self.set_out)
        self.clock = ClockTicker()
        self.clock.update_qt.connect(self.set_out)

        self.x = threading.Thread(target=self.app.display_image)
        self.x.start()
        self.y = threading.Thread(target=self.app.run)
        self.y.start()
        self.z = threading.Thread(target=self.clock.run)
        self.z.start()

        self.setGeometry(50, 100, 480, 280)
        self.setWindowTitle("Auto Translate")
        self.show()

    def set_lang(self):
        global lang
        lang = self.lan.currentText()

    def set_gray_cutoff(self, value):
        global gray_cutoff
        gray_cutoff = value

    def set_rotation(self, value):
        global rotation_angle_deg
        rotation_angle_deg = value

    def set_invert(self):
        global invert
        invert = not invert

    def reset(self):
        global rotation_angle_deg
        rotation_angle_deg = 0
        self.rslider.setValue(0)

    def set_gauss(self):
        global do_gauss
        do_gauss = not do_gauss

    def set_gauss_constant(self, value):
        global gauss_constant
        gauss_constant = value

    def set_bounds(self):
        self.audit.setChecked(False)
        self.out.clear()
        self.clock.do_run = True

    def calc(self):
        self.app.get_text()

    def set_auto_up(self):
        global auto_up
        auto_up = not auto_up

    def set_out(self, value):
        self.out.setPlainText(value)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Quit?',
                                     'Are you sure you want to quit?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            if not type(event) == bool:
                global RUN
                RUN = False
                event.accept()
            else:
                sys.exit()
        else:
            if not type(event) == bool:
                event.ignore()


class ClockTicker(QWidget):
    update_qt = QtCore.pyqtSignal(str)
    do_run = False

    def __init__(self):
        super().__init__()

    def run(self):
        global x1, y1, x0, y0
        while RUN:
            if self.do_run:
                self.update_qt.emit("Top Left...3")
                time.sleep(.25)
                self.update_qt.emit("Top Left...3.")
                time.sleep(.25)
                self.update_qt.emit("Top Left...3..")
                time.sleep(.25)
                self.update_qt.emit("Top Left...3...")
                time.sleep(.25)
                self.update_qt.emit("Top Left...3...2")
                time.sleep(.25)
                self.update_qt.emit("Top Left...3...2.")
                time.sleep(.25)
                self.update_qt.emit("Top Left...3...2..")
                time.sleep(.25)
                self.update_qt.emit("Top Left...3...2...")
                time.sleep(.25)
                self.update_qt.emit("Top Left...3...2...1")
                time.sleep(.25)
                self.update_qt.emit("Top Left...3...2...1.")
                time.sleep(.25)
                self.update_qt.emit("Top Left...3...2...1..")
                time.sleep(.25)
                self.update_qt.emit("Top Left...3...2...1...")
                time.sleep(.25)

                x0_temp = auto.position().x
                y0_temp = auto.position().y

                self.update_qt.emit("Bottom Right...3")
                time.sleep(.25)
                self.update_qt.emit("Bottom Right...3.")
                time.sleep(.25)
                self.update_qt.emit("Bottom Right...3..")
                time.sleep(.25)
                self.update_qt.emit("Bottom Right...3...")
                time.sleep(.25)
                self.update_qt.emit("Bottom Right...3...2")
                time.sleep(.25)
                self.update_qt.emit("Bottom Right...3...2.")
                time.sleep(.25)
                self.update_qt.emit("Bottom Right...3...2..")
                time.sleep(.25)
                self.update_qt.emit("Bottom Right...3...2...")
                time.sleep(.25)
                self.update_qt.emit("Bottom Right...3...2...1")
                time.sleep(.25)
                self.update_qt.emit("Bottom Right...3...2...1.")
                time.sleep(.25)
                self.update_qt.emit("Bottom Right...3...2...1..")
                time.sleep(.25)
                self.update_qt.emit("Bottom Right...3...2...1...")
                time.sleep(.25)

                x1 = auto.position().x
                y1 = auto.position().y
                x0 = x0_temp
                y0 = y0_temp
                self.update_qt.emit("")
                self.do_run = False
            else:
                time.sleep(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainGUI()
    sys.exit(app.exec_())

#QT4 to QT5
# QtGui.QImage , QtGui.Pixmap
# QtWidgets.QVBoxLayout().setContentsMargins(0,0,0,0)
# QtWidgets .QApplication,QWidget

#Tutorial https://stackoverflow.com/questions/41103148/capture-webcam-video-using-pyqt

import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
import cv2
import numpy as np
import dlib
from imutils import face_utils


class QtCapture(QtWidgets.QWidget):
    def __init__(self, *args):
        super(QtWidgets.QWidget, self).__init__()

        self.fps = 24
        self.cap = cv2.VideoCapture(*args)

        p = "/home/sxx/Downloads/AI/Blueprints/Weights&Models/shape_predictor_68_face_landmarks.dat"
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(p)

        self.video_frame = QtWidgets.QLabel()
        lay = QtWidgets.QVBoxLayout()
        lay.setContentsMargins(0,0,0,0)
        lay.addWidget(self.video_frame)
        self.setLayout(lay)

        # ------ Modification ------ #
        self.isCapturing = False
        self.ith_frame = 1
        # ------ Modification ------ #

    def setFPS(self, fps):
        self.fps = fps

    def nextFrameSlot(self):
        ret, frame = self.cap.read()

        # ------ Modification ------ #
        # Save images if isCapturing
        if self.isCapturing:
            cv2.imwrite('img_%05d.jpg'%self.ith_frame, frame)
            self.ith_frame += 1
        # ------ Modification ------ #

        # Open CV Face Detect:::
        # face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # faces = face_cascade.detectMultiScale(frame, 1.3, 5)
        # for x, y, width, height in faces:
        #     cv2.rectangle(frame, (x, y), (x + width, y + height), color=(255, 0, 0), thickness=2)

        # Dlib Face Detect
        #Some variables at start
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rects = self.detector(frame, 0)

        for (i, rect) in enumerate(rects):
            shape = self.predictor(frame, rect)
            shape = face_utils.shape_to_np(shape)
            for (x, y) in shape:
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)


        
        img = QtGui.QImage(frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap.fromImage(img)
        self.video_frame.setPixmap(pix)

    def start(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)
        self.timer.start(1000./self.fps)

    def stop(self):
        self.timer.stop()

    # ------ Modification ------ #
    def capture(self):
        if not self.isCapturing:
            self.isCapturing = True
        else:
            self.isCapturing = False
    # ------ Modification ------ #

    def deleteLater(self):
        self.cap.release()
        super(QtWidgets.QWidget, self).deleteLater()


class ControlWindow(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.capture = None

        self.start_button = QtWidgets.QPushButton('Start')
        self.start_button.clicked.connect(self.startCapture)
        self.quit_button = QtWidgets.QPushButton('End')
        self.quit_button.clicked.connect(self.endCapture)
        self.end_button = QtWidgets.QPushButton('Stop')

        # ------ Modification ------ #
        self.capture_button = QtWidgets.QPushButton('Capture')
        self.capture_button.clicked.connect(self.saveCapture)
        # ------ Modification ------ #

        vbox = QtWidgets.QVBoxLayout(self)
        vbox.addWidget(self.start_button)
        vbox.addWidget(self.end_button)
        vbox.addWidget(self.quit_button)

        # ------ Modification ------ #
        vbox.addWidget(self.capture_button)
        # ------ Modification ------ #

        self.setLayout(vbox)
        self.setWindowTitle('Control Panel')
        self.setGeometry(100,100,200,200)
        self.show()

    def startCapture(self):
        if not self.capture:
            self.capture = QtCapture(0)
            self.end_button.clicked.connect(self.capture.stop)
            # self.capture.setFPS(1)
            self.capture.setParent(self)
            self.capture.setWindowFlags(QtCore.Qt.Tool)
        self.capture.start()
        self.capture.show()

    def endCapture(self):
        self.capture.deleteLater()
        self.capture = None

    # ------ Modification ------ #
    def saveCapture(self):
        if self.capture:
            self.capture.capture()
    # ------ Modification ------ #



if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = ControlWindow()
    sys.exit(app.exec_())
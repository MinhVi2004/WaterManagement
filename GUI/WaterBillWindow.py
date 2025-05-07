from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PyQt6.QtCore import QLocale
from PyQt6 import uic
from PyQt6.QtGui import QPixmap
from BUS.TinhTienNuocBUS import TinhTienNuocBUS
import cv2
import datetime
import os
import shutil

class WaterBillWindow(QWidget):
    def __init__(self):
      super().__init__()
      uic.load_ui("GUI/UI/WaterBillWindow.ui", self)
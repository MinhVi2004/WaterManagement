from PyQt6.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QMessageBox, QTableWidget, QTableWidgetItem, QLineEdit
from PyQt6 import uic



class AdminGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('GUI/UI/Home.ui', self)
        self.btnNV.clicked.connect(self.openNV)
        self.btnHD.clicked.connect(self.openNV)
        self.btnKH.clicked.connect(self.openKH)
        self.btnHome.clicked.connect(self.openNV)
    
    def openNV(self):
        from GUI.QLNV import QuanLyNhanVien
        self.openNV = QuanLyNhanVien()
        self.openNV.show()
        self.close()
    def openKH(self):
        from GUI.QLKH import QuanLyKhachHang
        self.openKH = QuanLyKhachHang()
        self.openKH.show()
        self.close()
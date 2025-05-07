from PyQt6.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QMessageBox, QTableWidget, QTableWidgetItem, QLineEdit
from PyQt6 import uic



class AdminGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('GUI/UI/Home.ui', self)
        self.btnNV.clicked.connect(self.openNV)
        self.btnHD.clicked.connect(self.openHD)
        self.btnKH.clicked.connect(self.openKH)
        self.btnDHN.clicked.connect(self.openDHN)
        self.btnDangXuat.clicked.connect(self.dangXuat)
    
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
    def openHD(self):
        from GUI.QLHoaDon import QuanLyHoaDon
        self.openHD = QuanLyHoaDon()
        self.openHD.show()
        self.close()
    def openDHN(self):
        from GUI.QLDongHoNuoc import QuanLyDongHoNuoc
        self.dongHoNuocWindow = QuanLyDongHoNuoc()
        self.dongHoNuocWindow.show()
        self.close()
    def dangXuat(self):
        from GUI.Login import Login_w
        self.login = Login_w()
        self.login.show()
        self.close()
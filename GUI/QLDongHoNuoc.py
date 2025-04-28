from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from PyQt6.uic import loadUi
from PyQt6.QtCore import pyqtSlot
from BUS.DongHoNuocBUS import DongHoNuocBUS
from BUS.KhachHangBUS import KhachHangBUS

class QuanLyDongHoNuoc(QMainWindow):
      def __init__(self):
            super().__init__()
            loadUi("./GUI/UI/QuanLyDongHo.ui", self)
            self.khachHangBus = KhachHangBUS()
            self.dongHoNuocBus = DongHoNuocBUS()
            self.List.setSelectionBehavior(self.List.SelectionBehavior.SelectRows)
            self.List.setSelectionMode(self.List.SelectionMode.SingleSelection)
            self.btnHome.clicked.connect(self.openHome)
            self.btnKH_2.clicked.connect(self.openKH)
            self.btnNV_2.clicked.connect(self.openNV)
            self.btnHD_2.clicked.connect(self.openHD)
            self.btnDangXuat.clicked.connect(self.dangXuat)
            self.btnKhoa.setEnabled(False)
            self.btnTaiLai.clicked.connect(self.reload_fields)
            self.btnKhoa.clicked.connect(self.khoa_dong_ho)
            self.btnThem.clicked.connect(self.add_dong_ho_nuoc)

            
            self.update_table()
            self.List.itemSelectionChanged.connect(self.on_table_selection_changed)
            
      @pyqtSlot()
      def add_dong_ho_nuoc(self):
            from GUI.ThemDongHoNuoc import ThemDongHoNuoc
            self.themDongHoNuoc = ThemDongHoNuoc()
            self.themDongHoNuoc.show()
      @pyqtSlot()
      def khoa_dong_ho(self):
            selected_row = self.List.currentRow()
            if selected_row >= 0:
                  current_status = self.List.item(selected_row, 5).text()

                  if current_status == "Bình Thường":
                        reply = QMessageBox.question(
                        self,
                        "Xác nhận",
                        "Bạn có chắc chắn muốn vô hiệu hóa đồng hồ này không?",
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                        )

                        if reply == QMessageBox.StandardButton.Yes:
                              # Đổi thành Vô Hiệu Hóa trong table
                              self.List.setItem(selected_row, 5, QTableWidgetItem("Vô Hiệu Hóa"))

                              # Cập nhật database
                              dong_ho_id = int(self.List.item(selected_row, 0).text())
                              self.dongHoNuocBus.update_status(dong_ho_id, "Vô Hiệu Hóa")

                              # Cập nhật QLineEdit
                              self.txtTrangThai.setText("Vô Hiệu Hóa")

                              QMessageBox.information(self, "Thông báo", "Đã vô hiệu hóa đồng hồ thành công!")
                        else:
                              # Người dùng bấm No
                              pass
                  else:
                        QMessageBox.warning(self, "Thông báo", "Đồng hồ đã bị vô hiệu hóa trước đó!")
            else:
                  QMessageBox.warning(self, "Thông báo", "Vui lòng chọn một dòng trước khi thực hiện!")

      @pyqtSlot()
      def on_table_selection_changed(self):
            selected_row = self.List.currentRow()
            if selected_row >= 0:
                  self.txtMaDH.setText(self.List.item(selected_row, 0).text())
                  self.txtTenKH.setText(self.List.item(selected_row, 1).text())
                  self.txtSoNuocHienTai.setText(self.List.item(selected_row, 2).text())
                  self.txtDiaDiem.setText(self.List.item(selected_row, 3).text())
                  self.txtNgayLapDat.setText(self.List.item(selected_row, 4).text())
                  self.txtTrangThai.setText(self.List.item(selected_row, 5).text())
                  
                  
                  self.btnKhoa.setEnabled(True)
            else:
                  self.btnKhoa.setEnabled(False)
      @pyqtSlot()
      def reload_fields(self):
            # Bỏ chọn dòng trong QTableWidget
            self.List.clearSelection()
            # Xóa tất cả dữ liệu trong các QLineEdit
            self.txtMaDH.setText("")
            self.txtTenKH.setText("")
            self.txtSoNuocHienTai.setText("")
            self.txtDiaDiem.setText("")
            self.txtNgayLapDat.setText("")
            self.txtTrangThai.setText("")


      def update_table(self):
            dongHoNuocs = self.dongHoNuocBus.get_all_dong_ho_nuoc()
            self.List.setRowCount(0)

            for dongHoNuoc in dongHoNuocs:
                  row_position = self.List.rowCount()
                  self.List.insertRow(row_position)

                  self.List.setItem(row_position, 0, QTableWidgetItem(str(dongHoNuoc.id)))
                  self.List.setItem(row_position, 1, QTableWidgetItem(str(self.khachHangBus.get_user(dongHoNuoc.customer_id).name)))
                  self.List.setItem(row_position, 2, QTableWidgetItem(str(dongHoNuoc.meter_number)))
                  self.List.setItem(row_position, 3, QTableWidgetItem(str(dongHoNuoc.location)))
                  self.List.setItem(row_position, 4, QTableWidgetItem(str(dongHoNuoc.installed_at)))
                  self.List.setItem(row_position, 5, QTableWidgetItem(str(dongHoNuoc.status)))
      def openNV(self):
            from GUI.QLNV import QuanLyNhanVien
            self.employee_window = QuanLyNhanVien()
            self.employee_window.show()
            self.close()

      def openKH(self):
            from GUI.QLKH import QuanLyKhachHang
            self.customer_window = QuanLyKhachHang()
            self.customer_window.show()
            self.close()

      def openHome(self):
            from GUI.AdminGUI import AdminGUI
            self.home_window = AdminGUI()
            self.home_window.show()
            self.close()
      def openHD(self):
            from GUI.QLHoaDon import QuanLyHoaDon
            self.employee_window = QuanLyHoaDon()
            self.employee_window.show()
            self.close()
      def dangXuat(self):
            from GUI.Login import Login_w
            self.login = Login_w()
            self.login.show()
            self.close()
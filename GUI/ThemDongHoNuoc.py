from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QAbstractItemView, QHeaderView, QMessageBox
from PyQt6.QtCore import Qt
#? Load giao diện sử dụng uic
from PyQt6 import uic
from BUS.DongHoNuocBUS import DongHoNuocBUS
from BUS.KhachHangBUS import KhachHangBUS
class ThemDongHoNuoc(QMainWindow):
      def __init__(self):
            super().__init__()
            uic.loadUi("GUI/UI/ThemDongHoNuoc.ui", self)
            self.dongHoNuocBUS = DongHoNuocBUS()
            self.customerBUS = KhachHangBUS()
            self.loadData()
            self.btnXacNhan.clicked.connect(self.xacNhan)
            self.btnHuy.clicked.connect(self.huy)
            self.tbDanhSachKhachHang.itemSelectionChanged.connect(self.on_table_selection_changed)
            
      def on_table_selection_changed(self):
            selected_row = self.tbDanhSachKhachHang.currentRow()
            
            if selected_row >= 0:
                  self.txtMaKH.setText(self.tbDanhSachKhachHang.item(selected_row, 0).text())
                  self.txtTenKH.setText(self.tbDanhSachKhachHang.item(selected_row, 1).text())
                  self.txtSoDienThoai.setText(self.tbDanhSachKhachHang.item(selected_row, 2).text())
                  self.txtDiaChi.setText(self.tbDanhSachKhachHang.item(selected_row, 3).text())
                  self.txtEmail.setText(self.tbDanhSachKhachHang.item(selected_row, 4).text())
            
      
      def loadData(self):
            listCustomer = self.customerBUS.get_all()
            self.tbDanhSachKhachHang.setRowCount(len(listCustomer))
            self.tbDanhSachKhachHang.setColumnCount(5)
            self.tbDanhSachKhachHang.verticalHeader().setVisible(False)
            self.tbDanhSachKhachHang.setColumnWidth(0, 100)
            for col in range(1, 6):
                  self.tbDanhSachKhachHang.horizontalHeader().setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)

            # Chỉ cho phép chọn nguyên hàng
            self.tbDanhSachKhachHang.setSelectionBehavior(self.tbDanhSachKhachHang.SelectionBehavior.SelectRows)
            self.tbDanhSachKhachHang.setSelectionMode(self.tbDanhSachKhachHang.SelectionMode.SingleSelection)


            for row, customer in enumerate(listCustomer):
                  item_id = QTableWidgetItem(str(customer.id))
                  item_id.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                  self.tbDanhSachKhachHang.setItem(row, 0, item_id)
                  self.tbDanhSachKhachHang.setItem(row, 1, QTableWidgetItem(customer.name))
                  self.tbDanhSachKhachHang.setItem(row, 2, QTableWidgetItem(customer.phone))
                  self.tbDanhSachKhachHang.setItem(row, 3, QTableWidgetItem(customer.address))
                  self.tbDanhSachKhachHang.setItem(row, 4, QTableWidgetItem(customer.email))

      def huy(self):
            from GUI.QLDongHoNuoc import QuanLyDongHoNuoc
            self.dongHoNuocWindow = QuanLyDongHoNuoc()
            self.dongHoNuocWindow.show()
            self.close()
      def xacNhan(self):
            if(self.txtMaKH.text() == ""):
                  QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn thông tin khách hàng.")
                  return
            if(self.txtDiaDiem.text() == "" or len(self.txtDiaDiem.text()) < 5):
                  QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập địa điểm hợp lệ.")
                  return
            # Tạo hộp thoại xác nhận
            reply = QMessageBox.question(self, 'Xác Nhận', 'Bạn có chắc chắn muốn thêm đồng hồ nước ở địa điểm này?',
                                          QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                          QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                  if(self.dongHoNuocBUS.add_dong_ho_nuoc(self.txtMaKH.text(), self.txtDiaDiem.text())):
                        QMessageBox.information(self, "Thông báo", "Thêm đồng hồ nước thành công.")
                        from GUI.QLDongHoNuoc import QuanLyDongHoNuoc
                        self.dongHoNuocWindow = QuanLyDongHoNuoc()
                        self.dongHoNuocWindow.show()
                        self.close()
            return
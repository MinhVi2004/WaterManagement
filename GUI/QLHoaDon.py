from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from PyQt6.uic import loadUi
from PyQt6.QtCore import pyqtSlot
from BUS.HoaDonBUS import HoaDonBUS

class QuanLyHoaDon(QMainWindow):
     def __init__(self):
          super().__init__()
          loadUi("./GUI/UI/QuanLyHoaDon.ui", self)  # Load the UI from the .ui file
          self.hoaDonBus = HoaDonBUS()  # Initialize the business layer
          
          # Connect buttons to respective methods
          self.btnHome.clicked.connect(self.openHome)
          self.btnKH_2.clicked.connect(self.openKH)
          self.btnNV_2.clicked.connect(self.openNV)
          self.btnAdd.clicked.connect(self.add_hoa_don)
          self.btnEdit.clicked.connect(self.edit_hoa_don)
          self.btnDel.clicked.connect(self.delete_hoa_don)
          self.pushButton_6.clicked.connect(self.search_hoa_don)
          self.btnReset.clicked.connect(self.reset_fields)
          
          # Initialize table
          self.update_table()

     def update_table(self):
          # Fetch HoaDon data from BUS
          hoa_dons = self.hoaDonBus.get_all_bills()

          # Clear table before filling it with updated data
          self.List.setRowCount(0)

          for hoa_don in hoa_dons:
               row_position = self.List.rowCount()
               self.List.insertRow(row_position)

               # Insert data into table
               self.List.setItem(row_position, 0, QTableWidgetItem(hoa_don.ma_hoa_don))
               self.List.setItem(row_position, 1, QTableWidgetItem(hoa_don.ma_kh))
               self.List.setItem(row_position, 2, QTableWidgetItem(hoa_don.ma_mn))
               self.List.setItem(row_position, 3, QTableWidgetItem(hoa_don.ma_doc))
               self.List.setItem(row_position, 4, QTableWidgetItem(str(hoa_don.so_tien)))
               self.List.setItem(row_position, 5, QTableWidgetItem(str(hoa_don.thoi_han)))
               self.List.setItem(row_position, 6, QTableWidgetItem(hoa_don.trang_thai))
               self.List.setItem(row_position, 7, QTableWidgetItem(hoa_don.ngay_tao))
               self.List.setItem(row_position, 8, QTableWidgetItem(hoa_don.nguoi_tao))

     @pyqtSlot()
     def add_hoa_don(self):
          # Get data from the form fields
          ma_kh = self.maKH.text()
          ma_mn = self.maMN.text()
          ma_doc = self.MaD.text()
          so_tien = self.newMeter_2.text()
          thoi_han = self.newMeter_3.text()
          trang_thai = self.newMeter_4.text()
          ngay_tao = self.newMeter_3.text()
          nguoi_tao = self.newMeter_4.text()

          # Call the business layer to add HoaDon
          hoa_don = self.hoaDonBus.create_bill(ma_kh, ma_mn, ma_doc, so_tien, thoi_han, trang_thai, ngay_tao, nguoi_tao)

          # Display success message
          QMessageBox.information(self, "Thông báo", "Thêm hóa đơn thành công!")

          # Update table
          self.update_table()

     @pyqtSlot()
     def edit_hoa_don(self):
          # Get selected row
          selected_row = self.List.currentRow()
          if selected_row >= 0:
               # Extract the ID from the selected row
               ma_hoa_don = self.List.item(selected_row, 0).text()

               # Retrieve the HoaDon from BUS
               hoa_don = self.hoaDonBus.get_bill_by_id(ma_hoa_don)

               # Set the form fields with the data of the selected HoaDon
               self.MaHD.setText(hoa_don.ma_hoa_don)
               self.maKH.setText(hoa_don.ma_kh)
               self.maMN.setText(hoa_don.ma_mn)
               self.MaD.setText(hoa_don.ma_doc)
               self.newMeter_2.setText(str(hoa_don.so_tien))
               self.newMeter_3.setText(str(hoa_don.thoi_han))
               self.newMeter_4.setText(hoa_don.trang_thai)
          else:
               QMessageBox.warning(self, "Cảnh báo", "Chưa chọn hóa đơn để sửa!")

     @pyqtSlot()
     def delete_hoa_don(self):
          # Get selected row
          selected_row = self.List.currentRow()
          if selected_row >= 0:
               # Extract the ID from the selected row
               ma_hoa_don = self.List.item(selected_row, 0).text()

               # Call the business layer to delete the HoaDon
               self.hoaDonBus.delete_bill(ma_hoa_don)

               # Update table after deletion
               self.update_table()

               QMessageBox.information(self, "Thông báo", "Xóa hóa đơn thành công!")
          else:
               QMessageBox.warning(self, "Cảnh báo", "Chưa chọn hóa đơn để xóa!")

     @pyqtSlot()
     def search_hoa_don(self):
          search_term = self.search.text()
          results = self.hoaDonBus.search_bills(search_term)

          # Clear table before filling it with search results
          self.List.setRowCount(0)

          for hoa_don in results:
               row_position = self.List.rowCount()
               self.List.insertRow(row_position)

               # Insert data into table
               self.List.setItem(row_position, 0, QTableWidgetItem(hoa_don.ma_hoa_don))
               self.List.setItem(row_position, 1, QTableWidgetItem(hoa_don.ma_kh))
               self.List.setItem(row_position, 2, QTableWidgetItem(hoa_don.ma_mn))
               self.List.setItem(row_position, 3, QTableWidgetItem(hoa_don.ma_doc))
               self.List.setItem(row_position, 4, QTableWidgetItem(str(hoa_don.so_tien)))
               self.List.setItem(row_position, 5, QTableWidgetItem(str(hoa_don.thoi_han)))
               self.List.setItem(row_position, 6, QTableWidgetItem(hoa_don.trang_thai))
               self.List.setItem(row_position, 7, QTableWidgetItem(hoa_don.ngay_tao))
               self.List.setItem(row_position, 8, QTableWidgetItem(hoa_don.nguoi_tao))

     @pyqtSlot()
     def reset_fields(self):
          # Reset all input fields
          self.MaHD.clear()
          self.maKH.clear()
          self.maMN.clear()
          self.MaD.clear()
          self.newMeter_2.clear()
          self.newMeter_3.clear()
          self.newMeter_4.clear()

     def openNV(self):
          """Open the employee management window."""
          from GUI.QLNV import QuanLyNhanVien
          self.employee_window = QuanLyNhanVien()
          self.employee_window.show()
          self.close()

     def openKH(self):
          # TODO: CHANGE THESE NAME CORRESPOND TO THE REAL NAME OF THE FILES
          from GUI.QLKH import QuanLyKhachHang
          self.customer_window = QuanLyKhachHang()
          self.customer_window.show()
          self.close()

     def openHome(self):
          from GUI.AdminGUI import AdminGUI
          self.home_window = AdminGUI()
          self.home_window.show()
          self.close()

if __name__ == "__main__":
     app = QApplication([])
     window = QuanLyHoaDon()
     window.show()
     app.exec()

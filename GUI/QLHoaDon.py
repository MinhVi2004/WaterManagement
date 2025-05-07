from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from PyQt6.uic import loadUi
from PyQt6.QtCore import pyqtSlot
from BUS.HoaDonBUS import HoaDonBUS

class QuanLyHoaDon(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("./GUI/UI/QuanLyHoaDon.ui", self)
        self.hoaDonBus = HoaDonBUS()
        self.List.setSelectionBehavior(self.List.SelectionBehavior.SelectRows)  # Chọn theo hàng
        self.List.setSelectionMode(self.List.SelectionMode.SingleSelection)     # Chỉ được chọn 1 hàng
        self.List.cellClicked.connect(self.show_selected_row_data)
        self.txtSearch.textChanged.connect(self.search_hoa_don)
        self.btnKH_2.clicked.connect(self.openKH)
        self.btnNV_2.clicked.connect(self.openNV)
        self.btnDHN_2.clicked.connect(self.openDHN)
        self.btnDangXuat.clicked.connect(self.dangXuat)
        self.pushButton_6.clicked.connect(self.search_hoa_don)

        self.update_table()
    @pyqtSlot(int, int)
    def show_selected_row_data(self, row, column):
          self.MaHD.setText(self.List.item(row, 0).text())
          self.TenKH.setText(self.List.item(row, 1).text())
          self.TenNV.setText(self.List.item(row, 2).text())
          self.txtMaMN.setText(self.List.item(row, 3).text())
          self.txtAmount.setText(self.List.item(row, 4).text())
          self.txtTotalBill.setText(self.List.item(row, 5).text())
          self.txtStatus.setText(self.List.item(row, 6).text())
          self.txtNgayTao.setText(self.List.item(row, 7).text())

    def update_table(self):
        hoa_dons = self.hoaDonBus.get_all_bills()
        self.List.setRowCount(0)

        for hoa_don in hoa_dons:
            row_position = self.List.rowCount()
            self.List.insertRow(row_position)

            self.List.setItem(row_position, 0, QTableWidgetItem(str(hoa_don.id)))
            self.List.setItem(row_position, 1, QTableWidgetItem(str(self.hoaDonBus.get_customer_by_id(hoa_don.customer_id))))
            self.List.setItem(row_position, 2, QTableWidgetItem(str(self.hoaDonBus.get_employee_by_id(hoa_don.processed_by))))
            self.List.setItem(row_position, 3, QTableWidgetItem(str(hoa_don.meter_id)))
            self.List.setItem(row_position, 4, QTableWidgetItem(str(hoa_don.amount)))
            self.List.setItem(row_position, 5, QTableWidgetItem(str(hoa_don.totalBill)))  # Could be due date or amount
            self.List.setItem(row_position, 6, QTableWidgetItem(str(hoa_don.status)))
            self.List.setItem(row_position, 7, QTableWidgetItem(str(hoa_don.created_at)))

    @pyqtSlot()
    def add_hoa_don(self):
        customer_id = self.maKH.text()
        meter_id = self.maMN.text()
        reading_id = self.MaD.text()
        amount = self.newMeter_2.text()
        totalBill = int(amount) * 3000 if amount.isdigit() else 0
        created_at = self.newMeter_3.text()
        status = self.newMeter_4.text()
        processed_by = self.newMeter_4.text()

        self.hoaDonBus.create_bill(customer_id, meter_id, reading_id, amount, totalBill, status, created_at, processed_by)

        QMessageBox.information(self, "Thông báo", "Thêm hóa đơn thành công!")
        self.update_table()

    @pyqtSlot()
    def edit_hoa_don(self):
        selected_row = self.List.currentRow()
        if selected_row >= 0:
            bill_id = self.List.item(selected_row, 0).text()
            hoa_don = self.hoaDonBus.get_bill_by_id(bill_id)

            self.MaHD.setText(hoa_don.id)
            self.maKH.setText(hoa_don.customer_id)
            self.maMN.setText(hoa_don.meter_id)
            self.MaD.setText(hoa_don.reading_id)
            self.newMeter_2.setText(str(hoa_don.amount))
            self.newMeter_3.setText(hoa_don.created_at)
            self.newMeter_4.setText(hoa_don.status)
        else:
            QMessageBox.warning(self, "Cảnh báo", "Chưa chọn hóa đơn để sửa!")

    @pyqtSlot()
    def delete_hoa_don(self):
        selected_row = self.List.currentRow()
        if selected_row >= 0:
            bill_id = self.List.item(selected_row, 0).text()
            self.hoaDonBus.delete_bill(bill_id)
            self.update_table()
            QMessageBox.information(self, "Thông báo", "Xóa hóa đơn thành công!")
        else:
            QMessageBox.warning(self, "Cảnh báo", "Chưa chọn hóa đơn để xóa!")

    @pyqtSlot()
    def search_hoa_don(self):
        keyword = self.txtSearch.text().strip()
        typeSearch  = self.cbSearchType.currentText()
        results = self.hoaDonBus.search_bills(keyword, typeSearch)
        self.List.setRowCount(0)

        for hoa_don in results:
            row_position = self.List.rowCount()
            self.List.insertRow(row_position)

            self.List.setItem(row_position, 0, QTableWidgetItem(str(hoa_don.id)))
            self.List.setItem(row_position, 1, QTableWidgetItem(self.hoaDonBus.get_customer_by_id(hoa_don.customer_id)))
            self.List.setItem(row_position, 2, QTableWidgetItem(self.hoaDonBus.get_employee_by_id(hoa_don.processed_by)))
            self.List.setItem(row_position, 3, QTableWidgetItem(str(hoa_don.meter_id)))
            self.List.setItem(row_position, 4, QTableWidgetItem(str(hoa_don.amount)))  # Could be due date or amount
            self.List.setItem(row_position, 5, QTableWidgetItem(str(hoa_don.totalBill)))
            self.List.setItem(row_position, 6, QTableWidgetItem(str(hoa_don.status)))
            self.List.setItem(row_position, 7, QTableWidgetItem(str(hoa_don.created_at)))

    @pyqtSlot()
    def reset_fields(self):
        self.MaHD.clear()
        self.TenKH.clear()
        self.TenNV.clear()
        self.txtMaMN.clear()
        self.txtAmount.clear()
        self.txtTotalBill.clear()
        self.txtStatus.clear()
        self.txtNgayTao.clear()

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

if __name__ == "__main__":
    app = QApplication([])
    window = QuanLyHoaDon()
    window.show()
    app.exec()

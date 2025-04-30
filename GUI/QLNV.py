from BUS.NhanVienBUS import NhanVienBUS
from PyQt6.QtCore import QDate
from PyQt6 import uic
from datetime import datetime
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox

class QuanLyNhanVien(QMainWindow):
    def __init__(self):
        super().__init__()
        self.NhanVienBUS = NhanVienBUS()
        uic.loadUi("./GUI/UI/QuanLyNhanVien.ui", self)
        self.load_data()

        self.tableNV.cellClicked.connect(self.fill_fields)
        self.btnEdit.clicked.connect(self.update_employee)
        self.btnAdd.clicked.connect(self.add_employee)
        self.btnDel.clicked.connect(self.delete_employee)
        self.btnReset.clicked.connect(self.reset_employee)
        self.searchbutton.clicked.connect(self.search_employee)
        self.btnKH.clicked.connect(self.openKH)
        self.btnDHN.clicked.connect(self.openDHN)
        self.btnHD.clicked.connect(self.openHD)
        self.btnDangXuat.clicked.connect(self.dangXuat)

    def load_data(self):
        self.tableNV.setRowCount(0)
        employees = self.NhanVienBUS.get_all()
        for row_index, employee in enumerate(employees):
            self.tableNV.insertRow(row_index)
            self.tableNV.setItem(row_index, 0, QTableWidgetItem(str(employee.id)))
            self.tableNV.setItem(row_index, 1, QTableWidgetItem(employee.name))
            self.tableNV.setItem(row_index, 2, QTableWidgetItem(employee.phone))
            self.tableNV.setItem(row_index, 3, QTableWidgetItem(employee.email))
            self.tableNV.setItem(row_index, 4, QTableWidgetItem(employee.password))
            self.tableNV.setItem(row_index, 5, QTableWidgetItem(str(employee.role)))
            self.tableNV.setItem(row_index, 6, QTableWidgetItem(str(employee.created_at)))
            statusStr = "Hoạt Động" if employee.status == 1 else "Không hoạt động"  
            self.tableNV.setItem(row_index, 7, QTableWidgetItem(statusStr))
    def reset_employee(self):
        self.maNV.clear()
        self.tenNV.clear()
        self.email.clear()
        self.phone.clear()
        self.password.clear()
        self.dateDK.clear()
        self.checkBox.setChecked(False)

    def fill_fields(self, row):
        self.maNV.setText(self.tableNV.item(row, 0).text())
        self.tenNV.setText(self.tableNV.item(row, 1).text())
        self.phone.setText(self.tableNV.item(row, 2).text())
        self.email.setText(self.tableNV.item(row, 3).text())
        self.password.setText(self.tableNV.item(row, 4).text())
        self.role.setCurrentText(self.tableNV.item(row, 5).text())
        date_str = self.tableNV.item(row, 6).text()
        try:
            date_obj = QDate.fromString(date_str, "yyyy-MM-dd")
            if not date_obj.isValid():
                raise ValueError("Ngày không hợp lệ")
            self.dateDK.setDate(date_obj)
        except Exception:
            self.dateDK.clear()
        status = self.tableNV.item(row, 7).text()
        self.checkBox.setChecked(status == "Hoạt Động")

    def add_employee(self):
        name = self.tenNV.text().strip()
        email = self.email.text().strip()
        phone = self.phone.text().strip()
        password = self.password.text().strip()
        role = self.role.currentText().strip()
        status = 1 if self.checkBox.isChecked() else 0
        if not name or not email or not phone or not password or not role:
            QMessageBox.warning(self, "Lỗi", "Vui lòng điền đầy đủ thông tin nhân viên!")
            return

        try:
            new_id = self.NhanVienBUS.insert_user(name, email, phone, password, role, status)
            if new_id is False:
                raise ValueError("Không thể thêm nhân viên!")
            QMessageBox.information(self, "Thành công", f"Đã thêm nhân viên mới với ID: {new_id}")
            self.load_data()
            self.reset_employee()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"{str(e)}")

    def update_employee(self):
        maNV = self.maNV.text().strip()
        if not maNV:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn nhân viên cần sửa!")
            return

        name = self.tenNV.text().strip()
        email = self.email.text().strip()
        phone = self.phone.text().strip()
        password = self.password.text().strip()
        role = self.role.currentText().strip()
        dateDK = self.dateDK.date().toString('dd/MM/yyyy')
        status = 1 if self.checkBox.isChecked() else 0

        if not name or not email or not phone or not password or not role or not dateDK:
            QMessageBox.warning(self, "Lỗi", "Vui lòng điền đầy đủ thông tin nhân viên!")
            return

        confirm = QMessageBox.question(
            self, "Xác nhận", "Bạn có chắc chắn muốn sửa thông tin nhân viên này?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                self.NhanVienBUS.update_user(maNV, name, email, phone, password, role, dateDK, status)
                QMessageBox.information(self, "Thành công", "Thông tin nhân viên đã được cập nhật!")
                self.load_data()
                self.reset_employee()
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"{str(e)}")

    def delete_employee(self):
        maNV = self.maNV.text().strip()
        if not maNV:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn nhân viên cần xóa!")
            return

        confirm = QMessageBox.question(
            self, "Xác nhận", "Bạn có chắc muốn xóa nhân viên này?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                self.NhanVienBUS.delete_user(maNV)
                QMessageBox.information(self, "Thành công", "Nhân viên đã được xóa!")
                self.load_data()
                self.reset_employee()
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"{str(e)}")

    def search_employee(self):
        search_text = self.search.text().strip().lower()
        if not search_text:
            self.load_data()
            return
        employees = self.NhanVienBUS.get_all()
        filterList = []
        for e in employees:
            if search_text in e.name.lower() or search_text in e.phone.lower():
                filterList.append(e)

        self.tableNV.setRowCount(0)
        for row_index, employee in enumerate(filterList):
            self.tableNV.insertRow(row_index)
            self.tableNV.setItem(row_index, 0, QTableWidgetItem(str(employee.id)))
            self.tableNV.setItem(row_index, 1, QTableWidgetItem(employee.name))
            self.tableNV.setItem(row_index, 2, QTableWidgetItem(employee.email))
            self.tableNV.setItem(row_index, 3, QTableWidgetItem(employee.phone))
            self.tableNV.setItem(row_index, 4, QTableWidgetItem(employee.password))
            self.tableNV.setItem(row_index, 5, QTableWidgetItem(str(employee.role)))
            self.tableNV.setItem(row_index, 6, QTableWidgetItem(str(employee.created_at)))
            statusStr = "Hoạt Động" if employee.status == 1 else "Không hoạt động"  
            self.tableNV.setItem(row_index, 7, QTableWidgetItem(statusStr))

    def openKH(self):
        from GUI.QLKH import QuanLyKhachHang
        self.openKH = QuanLyKhachHang()
        self.openKH.show()
        self.close()

    def openHD(self):
        from GUI.QLHoaDon import QuanLyHoaDon
        self.employee_window = QuanLyHoaDon()
        self.employee_window.show()
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
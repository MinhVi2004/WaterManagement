from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QAbstractItemView, QHeaderView, QMessageBox
from PyQt6.QtCore import Qt
#? Load giao diện sử dụng uic
from PyQt6 import uic
from BUS.DongHoNuocBUS import DongHoNuocBUS
from BUS.KhachHangBUS import KhachHangBUS
from DTO.DongHoNuocDTO import DongHoNuocDTO
from GUI.TinhTienNuoc import TinhTienNuoc
from DTO.KhachHangDTO import KhachHangDTO 
class ChonKhachHang(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.employee = user
        uic.loadUi("GUI/UI/chonKhachHangUI.ui", self)
        self.customerBUS = KhachHangBUS()
        self.dongHoNuocBUS = DongHoNuocBUS()
        self.loadData()
        self.btnSubmit.clicked.connect(self.xacNhanKhachHang)
        self.btnClose.clicked.connect(self.dangXuat)
        self.txtSearch.textChanged.connect(self.timKiemKhachHang)
    def dangXuat(self):
            from GUI.Login import Login_w
            self.login = Login_w()
            self.login.show()
            self.close()      
    def loadData(self):
      listDHN = self.dongHoNuocBUS.get_all_dong_ho_nuoc()  # Lấy danh sách tất cả đồng hồ nước
      self.tbDanhSachKhachHang.setRowCount(len(listDHN))
      self.tbDanhSachKhachHang.setColumnCount(6)
      self.tbDanhSachKhachHang.setHorizontalHeaderLabels(["Mã Đồng Hồ", "Khách Hàng", "Số điện thoại", "Số Nước Hiện Tại", "Địa Điểm", "Trạng Thái"])
      self.tbDanhSachKhachHang.verticalHeader().setVisible(False)
      self.tbDanhSachKhachHang.setColumnWidth(0, 100)
      
      for col in range(1, 6):
            self.tbDanhSachKhachHang.horizontalHeader().setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)

      # Chỉ cho phép chọn nguyên hàng
      self.tbDanhSachKhachHang.setSelectionBehavior(self.tbDanhSachKhachHang.SelectionBehavior.SelectRows)
      self.tbDanhSachKhachHang.setSelectionMode(self.tbDanhSachKhachHang.SelectionMode.SingleSelection)

      # Đổ dữ liệu
      for row_idx, dong_ho_nuoc in enumerate(listDHN):
            # Lấy thông tin khách hàng theo đồng hồ nước
            customer = self.dongHoNuocBUS.get_customer_by_watermeter_id(dong_ho_nuoc.id)

            # Nếu có khách hàng thì hiển thị, không thì để trống
            customer_name = customer['name'] if customer else ''
            customer_phone = customer['phone'] if customer else ''

            self.tbDanhSachKhachHang.setItem(row_idx, 0, QTableWidgetItem(str(dong_ho_nuoc.id)))
            self.tbDanhSachKhachHang.setItem(row_idx, 1, QTableWidgetItem(customer_name))
            self.tbDanhSachKhachHang.setItem(row_idx, 2, QTableWidgetItem(customer_phone))
            self.tbDanhSachKhachHang.setItem(row_idx, 3, QTableWidgetItem(str(dong_ho_nuoc.meter_number)))  # ví dụ: chỉ số nước hiện tại
            self.tbDanhSachKhachHang.setItem(row_idx, 4, QTableWidgetItem(dong_ho_nuoc.location))
            self.tbDanhSachKhachHang.setItem(row_idx, 5, QTableWidgetItem(dong_ho_nuoc.status))


    def xacNhanKhachHang(self):
        selected_row = self.tbDanhSachKhachHang.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một khách hàng.")
            return  # Không chọn khách nào

        # Create a KhachHangDTO object instead of a dictionary
        watermeter_id = self.tbDanhSachKhachHang.item(selected_row, 0).text()

            # Gọi phương thức get_customer_by_watermeter_id với watermeter_id
        customer = self.dongHoNuocBUS.get_customer_by_watermeter_id(watermeter_id)
        customer_data = KhachHangDTO(customer['id'], customer['name'], customer['email'], customer['phone'], customer['address'], customer['created_at'])
        waterMeter_data = self.dongHoNuocBUS.get_dong_ho_nuoc_by_id(watermeter_id)
        self.tinhTienNuoc = TinhTienNuoc(self.employee, customer_data, waterMeter_data)
        self.tinhTienNuoc.show()
        self.close()
    def timKiemKhachHang(self):
            keyword = self.txtSearch.toPlainText().strip()
            search_type = self.cbTypeSearch.currentText()
            if(keyword == ""):
                  listDHN = self.dongHoNuocBUS.get_all_dong_ho_nuoc()
            else:
                  listDHN = self.dongHoNuocBUS.search_water_meters_by_customer(keyword, search_type)
            self.tbDanhSachKhachHang.setRowCount(len(listDHN))
            self.tbDanhSachKhachHang.setColumnCount(6)
            self.tbDanhSachKhachHang.setHorizontalHeaderLabels(["Mã Đồng Hồ", "Khách Hàng", "Số điện thoại", "Số Nước Hiện Tại", "Địa Điểm", "Trạng Thái"])
            self.tbDanhSachKhachHang.verticalHeader().setVisible(False)
            self.tbDanhSachKhachHang.setColumnWidth(0, 100)
            
            for col in range(1, 6):
                  self.tbDanhSachKhachHang.horizontalHeader().setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)

            # Chỉ cho phép chọn nguyên hàng
            self.tbDanhSachKhachHang.setSelectionBehavior(self.tbDanhSachKhachHang.SelectionBehavior.SelectRows)
            self.tbDanhSachKhachHang.setSelectionMode(self.tbDanhSachKhachHang.SelectionMode.SingleSelection)

            # Đổ dữ liệu
            for row_idx, dong_ho_nuoc in enumerate(listDHN):
                  # Lấy thông tin khách hàng theo đồng hồ nước
                  customer = self.dongHoNuocBUS.get_customer_by_watermeter_id(dong_ho_nuoc.id)

                  # Nếu có khách hàng thì hiển thị, không thì để trống
                  customer_name = customer['name'] if customer else ''
                  customer_phone = customer['phone'] if customer else ''

                  self.tbDanhSachKhachHang.setItem(row_idx, 0, QTableWidgetItem(str(dong_ho_nuoc.id)))
                  self.tbDanhSachKhachHang.setItem(row_idx, 1, QTableWidgetItem(customer_name))
                  self.tbDanhSachKhachHang.setItem(row_idx, 2, QTableWidgetItem(customer_phone))
                  self.tbDanhSachKhachHang.setItem(row_idx, 3, QTableWidgetItem(str(dong_ho_nuoc.meter_number)))  # ví dụ: chỉ số nước hiện tại
                  self.tbDanhSachKhachHang.setItem(row_idx, 4, QTableWidgetItem(dong_ho_nuoc.location))
                  self.tbDanhSachKhachHang.setItem(row_idx, 5, QTableWidgetItem(dong_ho_nuoc.status))
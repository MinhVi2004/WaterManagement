from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PyQt6.QtCore import QLocale
from PyQt6 import uic
from PyQt6.QtGui import QPixmap
from BUS.TinhTienNuocBUS import TinhTienNuocBUS
import cv2
import datetime
import os
import shutil
class TinhTienNuoc(QMainWindow):
    def __init__(self, employee, customer_data, waterMeter_data):
        super().__init__()
        self.image_url = None  # Biến để lưu đường dẫn ảnh đã chọn
        self.employee = employee  # Nhân viên hiện tại
        self.tinhTienNuocBUS = TinhTienNuocBUS()
        uic.loadUi("GUI/UI/tinhTienNuocUI.ui", self)
        
        
        self.txtMaKH.setText(str(customer_data.id))
        self.txtHoTen.setText(customer_data.name)
        self.txtSoDienThoai.setText(customer_data.phone)
        self.txtEmail.setText(customer_data.email)
        self.txtDiaChi.setText(customer_data.address)
        

        if waterMeter_data:
            self.txtMaDongHoNuoc.setText(str(waterMeter_data.id))
            self.txtSoNuocTruoc.setText(str(waterMeter_data.meter_number))
        self.txtSoNuocSau.returnPressed.connect(self.calculate_amount)
        # Gán sự kiện cho nút "Chụp Ảnh" và "Chọn Ảnh"
        self.btnCapture.clicked.connect(self.capture_image)
        self.btnChoose.clicked.connect(self.open_file_dialog)
        self.btnClose.clicked.connect(self.openChonKhachHang)
        self.btnSubmit.clicked.connect(self.submit_data)
    def display_image(self, file_path):
        """Hiển thị ảnh lên QLabel"""
        pixmap = QPixmap(file_path)
        self.hinhAnhDaChon.setPixmap(pixmap)
        self.hinhAnhDaChon.setScaledContents(True)  # Đảm bảo ảnh vừa với QLabel
    
    def capture_image(self):
        """Mở camera để chụp ảnh và hiển thị lên QLabel"""
        cap = cv2.VideoCapture(0)  # Mở camera mặc định
        if not cap.isOpened():
            print("Không thể mở camera")
            return

        while True:
            ret, frame = cap.read()
            if not ret or frame is None:
                print("Không thể đọc dữ liệu từ camera")
                break

            cv2.imshow("Chụp Ảnh - Nhấn SPACE để chụp, ESC để thoát", frame)

            key = cv2.waitKey(1)
            if key == 27:  # Nhấn ESC để thoát
                break
            elif key == 32:  # Nhấn SPACE để chụp
                maKH = self.txtMaKH.text().strip()
                maDHN = self.txtMaDongHoNuoc.text().strip()

                
                ngayChup = datetime.datetime.now().strftime("%d%m%Y")
                file_name = f"{maKH}_{maDHN}_{ngayChup}.jpg"
                save_dir = "Resource/CaptureIMG"
                os.makedirs(save_dir, exist_ok=True)

                file_path = os.path.join(save_dir, file_name)
                cv2.imwrite(file_path, frame)
                self.image_url = file_name
                print(f"Ảnh đã được lưu vào : {file_path}")
                self.display_image(file_path)  
                break

        cap.release()
        cv2.destroyAllWindows()
    
    def open_file_dialog(self):
        """Chọn ảnh từ máy tính"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn ảnh", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        
        if file_path:
            print(f"Ảnh đã chọn: {file_path}")

            maKH = self.txtMaKH.text().strip()
            maDHN = self.txtMaDongHoNuoc.text().strip()

            
            ngayChup = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
            file_name = f"{maKH}_{maDHN}_{ngayChup}.jpg"
            
            save_dir = "Resource/ChooseIMG"
            os.makedirs(save_dir, exist_ok=True)

            save_path = os.path.join(save_dir, file_name)
            shutil.copy(file_path, save_path)
            self.image_url = file_name  
            print(f"Ảnh đã được lưu vào: {save_path}")
            self.display_image(file_path)
        else:
            print("Không có ảnh nào được chọn.")
    def calculate_amount(self):
            giaTienNuoc = 3000
            """Tính toán số tiền dựa trên số nước đã sử dụng"""
            try:
               soNuocTruoc = float(self.txtSoNuocTruoc.text())
               soNuocSau = float(self.txtSoNuocSau.text())
               if soNuocSau < soNuocTruoc:
                     QMessageBox.warning(self, "Lỗi", "Số nước sau không được nhỏ hơn số nước trước!")
                     return
               soNuocDaSuDung = soNuocSau - soNuocTruoc
               self.txtTongTieuThu.setText(str(soNuocDaSuDung))
               tongTien = soNuocDaSuDung * giaTienNuoc
               # Định dạng tổng tiền theo kiểu tiền tệ
               locale = QLocale()  # Sử dụng locale mặc định
               formatted_tongTien = locale.toCurrencyString(tongTien)
               self.txtTongTien.setText(str(formatted_tongTien))
            except ValueError:
               self.txtSoTien.setText("")
            
    def openChonKhachHang(self):
        from GUI.ChonKhachHang import ChonKhachHang
        """Mở giao diện Chọn Khách Hàng"""
        self.chonKhachHang = ChonKhachHang(self.employee)
        self.chonKhachHang.show()
        self.close()
    def parse_money_to_int(self, value_str):
      # Bỏ ký hiệu tiền và khoảng trắng
      cleaned = value_str.replace("₫", "").strip()
      # Xoá dấu phân cách nghìn
      cleaned = cleaned.replace(".", "")
      # Thay dấu phẩy thành dấu chấm (nếu cần dùng float)
      cleaned = cleaned.replace(",", ".")
      # Ép sang float rồi lấy int (nếu muốn bỏ phần lẻ)
      return int(float(cleaned))
    def submit_data(self):
      if self.image_url is None:
         QMessageBox.warning(self, "Lỗi", "Vui lòng chọn ảnh trước khi gửi!")
         return
      self.calculate_amount()
      if self.txtSoNuocSau.text().strip() == "":
         QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
         return
      maKH = self.txtMaKH.text().strip()
      maDHN = self.txtMaDongHoNuoc.text().strip()
      tongTieuThu = self.txtTongTieuThu.text().strip()
      tongTien = self.parse_money_to_int(self.txtTongTien.text().strip())
      maNV = self.employee["id"]
      soNuocTruoc = self.txtSoNuocTruoc.text().strip()
      soNuocSau = self.txtSoNuocSau.text().strip()
      
      self.tinhTienNuocBUS.createWaterMeterReading(maKH, maDHN, soNuocTruoc, soNuocSau, self.image_url, maNV, tongTieuThu, tongTien)
      
      QMessageBox.information(self, "Thành công", "Đã tạo hóa đơn thành công!")
      self.openChonKhachHang()
      
      
      
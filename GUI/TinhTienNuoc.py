#? Phần train cắt số
import os
# Buộc segmentation_models dùng tf.keras
os.environ["SM_FRAMEWORK"] = "tf.keras"

import segmentation_models as sm
import tensorflow as tf
# Xác nhận framework
sm.set_framework("tf.keras")
from PIL import Image, ExifTags
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.ndimage import binary_fill_holes
from skimage.measure import label, regionprops

# Đơn giản hóa: chỉ phần segmentation

# Các đường dẫn
CSV_PATH = 'H:/My Drive/WaterMeters/data.csv'
IMAGES_FOLDER = 'H:/My Drive/WaterMeters/images'
MASKS_FOLDER = 'H:/My Drive/WaterMeters/masks'

# IMAGE_PATH = 'H:/My Drive/WaterMeters/images/id_1_value_13_116.jpg'
MODEL_PATH = 'H:/My Drive/WaterMeters/final_segmentation_model.h5'
# Load DataFrame và in thông tin
data = pd.read_csv(CSV_PATH)
print(f'Total images: {len(os.listdir(IMAGES_FOLDER))}')
print(f'Total masks: {len(os.listdir(MASKS_FOLDER))}')
print(f'Dataset length: {len(data)}')

# Load segmentation model (không compile tự động)
model = tf.keras.models.load_model(
    MODEL_PATH,
    custom_objects={
        'binary_crossentropy_plus_jaccard_loss': sm.losses.bce_jaccard_loss,
        'iou_score': sm.metrics.iou_score
    },
    compile=False
)
# Compile thủ công
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
    loss=sm.losses.bce_jaccard_loss,
    metrics=[sm.metrics.iou_score]
)

# Hàm dự đoán mask
def predict_mask(model, image, target_size=(224, 224)):
    img = cv2.resize(image, target_size) / 255.0
    img = np.expand_dims(img, axis=0)
    pred = model.predict(img)[0]
    mask = (pred > 0.5).astype(np.uint8)
    mask = cv2.resize(mask, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_NEAREST)
    return mask

# Hàm xử lý mask
def process_mask(mask):
    filled = binary_fill_holes(mask).astype(np.uint8)
    kernel = np.ones((3,3), np.uint8)
    cleaned = cv2.morphologyEx(filled, cv2.MORPH_OPEN, kernel, iterations=2)
    return cleaned

# Hàm crop region chứa số
def extract_digits_region(image, mask):
    labeled = label(mask)
    regions = regionprops(labeled)
    largest = max(regions, key=lambda r: r.area, default=None)
    if largest:
        minr, minc, maxr, maxc = largest.bbox
        return image[minr:maxr, minc:maxc]
    print("No valid region found.")
    return None

# Thực thi pipeline
# image = cv2.imread(IMAGE_PATH)
# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# mask = predict_mask(model, image)
# mask_cleaned = process_mask(mask)
# cropped = extract_digits_region(image, mask_cleaned)

# Hiển thị kết quả
def show_results(image_path):
      image = cv2.imread(image_path)
      image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      mask = predict_mask(model, image)
      mask_cleaned = process_mask(mask)
      cropped = extract_digits_region(image, mask_cleaned)
      
      # #ảnh gốc
      # plt.figure(figsize=(12, 4))
      # plt.subplot(1, 3, 1)
      # plt.imshow(image)
      # plt.title('Original')
      # plt.axis('off')


      # plt.subplot(1, 3, 3)
      # if cropped is not None:
      #       plt.imshow(cropped)
      #       plt.title('Cropped Digits')
      # else:
      #       plt.text(0.5, 0.5, 'No region to crop', ha='center')
      #       plt.title('Cropped Digits')
      # plt.axis('off')

      # plt.tight_layout()
      # plt.show()
      return cropped





# Phần code giao diện chức năng
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PyQt6.QtCore import QLocale
from PyQt6 import uic
from PyQt6.QtGui import QImage,QPixmap
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
    def numpy_to_qpixmap(self, image_np):
      """Chuyển ảnh NumPy RGB sang QPixmap"""
      if image_np is None:
            return None
      h, w, ch = image_np.shape
      bytes_per_line = ch * w
      image = QImage(image_np.tobytes(), w, h, bytes_per_line, QImage.Format.Format_RGB888)
      return QPixmap.fromImage(image)
     
    def display_image(self, file_path):
      """Hiển thị ảnh đã được xoay đúng chiều dựa trên Exif"""
      try:
            image = Image.open(file_path)

            # Xử lý xoay dựa trên EXIF
            for orientation in ExifTags.TAGS.keys():
                  if ExifTags.TAGS[orientation] == 'Orientation':
                        break
            exif = image._getexif()
            if exif is not None:
                  orientation_value = exif.get(orientation, None)
                  if orientation_value == 3:
                        image = image.rotate(180, expand=True)
                  elif orientation_value == 6:
                        image = image.rotate(270, expand=True)
                  elif orientation_value == 8:
                        image = image.rotate(90, expand=True)

            # Lưu ảnh tạm thời đã xoay
            corrected_path = os.path.join("Resource", "temp_corrected.jpg")
            image.save(corrected_path)

            pixmap = QPixmap(corrected_path)
      except Exception as e:
            print(f"Lỗi khi xử lý ảnh: {e}")
            pixmap = QPixmap(file_path)

      self.hinhAnhDaChon.setPixmap(pixmap)
      self.hinhAnhDaChon.setScaledContents(True)
    
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
            cropped = show_results(file_path)

            if cropped is not None:
                  cropped_pixmap = self.numpy_to_qpixmap(cropped)
                  if cropped_pixmap:
                        self.croppedImageLabel.setPixmap(cropped_pixmap)
                        self.croppedImageLabel.setScaledContents(True)
                        # === Lưu ảnh đã crop ===
                        cropped_dir = "Resource/CroppedDigit"
                        os.makedirs(cropped_dir, exist_ok=True)

                        # Lưu với cùng định dạng tên ảnh gốc
                        cropped_filename = f"{maKH}_{maDHN}_{ngayChup}_cropped.jpg"
                        cropped_save_path = os.path.join(cropped_dir, cropped_filename)

                        # Sử dụng OpenCV để lưu ảnh
                        cropped_bgr = cv2.cvtColor(cropped, cv2.COLOR_RGB2BGR)
                        cv2.imwrite(cropped_save_path, cropped_bgr)

                        print(f"Ảnh đã crop được lưu tại: {cropped_save_path}")
                  else:
                        print("Không thể chuyển ảnh crop sang QPixmap")
            else:
                  print("Không tìm thấy vùng chứa số để crop.")
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
      
      
      
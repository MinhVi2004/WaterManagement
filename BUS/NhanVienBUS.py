from datetime import datetime
from DAO.NhanVienDAO import NhanVienDAO
import re

class NhanVienBUS:
    def __init__(self):
        self.DAO = NhanVienDAO()

    def get_user(self, id): 
        return self.DAO.get_user(id)
    
    def get_all(self):
        return self.DAO.get_all()

    def check_user(self, name, email, phone, password, role, status):
        name = name.strip().title()
        if not name.replace(" ", "").isalpha():
            raise ValueError("Tên chỉ được chứa chữ cái và khoảng trắng!")

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Email không đúng định dạng!")

        if len(password) < 6:
            raise ValueError("Mật khẩu phải có ít nhất 6 ký tự!")

        if not phone.isdigit():
            raise ValueError("Số điện thoại chỉ được chứa số!")

        if not phone.startswith("0"):
            raise ValueError("Số điện thoại phải bắt đầu bằng số 0!")

        if len(phone) != 10:
            raise ValueError("Số điện thoại phải có 10 chữ số")
        return name, email, phone, password, role, status

    def insert_user(self, name, email, phone, password, role, status):
        name, email, phone, password, role, status = self.check_user(name, email, phone, password, role, status)
        if self.DAO.email_exists(email):
            raise ValueError("Email đã tồn tại!")
        return self.DAO.insert_user(name, phone, email, password, role, status)

    def update_user(self, id, name, email, phone, password, role, created_at, status):
        name, email, phone, password, role, status = self.check_user(name, email, phone, password, role, status)
        try:
            created_at = datetime.strptime(created_at, "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            raise ValueError("Ngày đăng ký không đúng định dạng 'DD/MM/YYYY'!")
        self.DAO.update_user(id, name, phone, email, password, role, created_at, status)
    
    def delete_user(self, maNV):
        return self.DAO.delete_user(maNV)

    def validate_login(self, email, password):
        return self.DAO.validate_login(email, password)

    def close(self):
        self.DAO.close()
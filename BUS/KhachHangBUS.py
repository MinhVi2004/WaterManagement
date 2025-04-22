#Business Logic Layer/Business Object check and apply bussiness rules to the passed data to check for any logic invalidation (i.e non existing email, password too short, etc.)
from DAO.KhachHangDAO import KhachHangDAO
import re
class KhachHangBUS:
    def __init__(self):
        self.DAO = KhachHangDAO()
    def get_user(self, id): 
        return self.DAO.get_user(id)
    def get_all(self):
        """Lấy danh sách khách hàng từ DAO"""
        return self.DAO.get_all()
    def search_Customer(self, keyword, search_type):
        """Tìm kiếm khách hàng"""
        if search_type:
            return self.DAO.search_Customer(keyword, search_type)
        raise ValueError("từ khóa không được bỏ trống!")
    def insert_user(self, name, email, phone, address):
        if not name or not email or not phone or not address:
            raise ValueError("Vui lòng điền đầy đủ thông tin khách hàng!")
        # Example validation: check if email is in valid format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email): #[^@]+ means "one or more characters that are not @(john,nguyen,gmail,com)" && \. means a literal dot. && @ means a literal @
            raise ValueError("email phải theo định dạng ___@__.___")
        # Additional validations can go here:
        # If validation passes, proceed to insert the user
        new_user_id = self.DAO.insert_user(name, email, phone, address)
        return new_user_id
    def update_user(self, id, name, email, phone, address, NgayDangKy):
        if not name or not email or not phone or not address:
            raise ValueError("Vui lòng điền đầy đủ thông tin khách hàng!")
        """Updates an existing customer."""
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email): #[^@]+ means "one or more characters that are not @(john,nguyen,gmail,com)" && \. means a literal dot. && @ means a literal @
            raise ValueError(f"email phải theo định dạng ___@__.___, định dạng được nhập vào: {email}")
        self.DAO.update_user(id, name, email, phone, address, NgayDangKy)

    def delete_user(self, id):
        """Deletes a customer from the database."""
        self.DAO.delete_user(id)
    def close(self):
        self.DAO.close()

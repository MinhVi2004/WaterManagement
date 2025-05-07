from Database.database import Database
from DTO.NhanVienDTO import NhanVienDTO
class LoginBUS:
    def __init__(self):
        self.db = Database()

    def check_login(self, email, password):
        query = "SELECT * FROM employees WHERE email = %s AND password = %s "
        params = (email, password)
        result = self.db.fetch_all(query, params)

        if result and len(result) > 0:
            return result[0]  # Trả về thông tin nhân viên đầu tiên tìm thấy
        return None

from DTO.NhanVienDTO import NhanVienDTO
from Database.database import Database
from datetime import datetime

class NhanVienDAO:
    def __init__(self):
        self.db = Database()

    def get_all(self):
        """Lấy tất cả nhân viên"""
        query = "SELECT * FROM employees"
        rows = self.db.fetch_all(query)
        listNV = []
        for row in rows:
            dto = NhanVienDTO(row['id'], row['name'], row['email'], row['password'], row['role'], row['created_at'])
            listNV.append(dto)
        return listNV

    def get_user(self, id):
        """Lấy thông tin user theo ID"""
        query = "SELECT * FROM employees WHERE id = %s"
        rows = self.db.fetch_all(query, (id,))
        if rows:
            row = rows[0]
            return NhanVienDTO(row['id'], row['name'], row['email'], row['password'], row['role'], row['created_at'])
        return None

    def insert_user(self, name, email, password, role):
        """Thêm user mới"""
        get_max_id = "SELECT MAX(id) as max_id FROM employees"
        result = self.db.fetch_all(get_max_id)
        max_id = result[0]['max_id'] if result else 0
        new_id = max_id + 1
        today = datetime.today().strftime('%Y-%m-%d')
        query = "INSERT INTO employees (id, name, email, password, role, created_at) VALUES (%s, %s, %s, %s, %s, %s)"
        params = (new_id, name, email, password, role, today)
        success = self.db.execute_query(query, params)
        return new_id if success else None

    def update_user(self, id, name, email, password, role, created_at):
        query = "UPDATE employees SET name=%s, email=%s, password=%s, role=%s, created_at=%s WHERE id=%s"
        params = (name, email, password, role, created_at, id)
        return self.db.execute_query(query, params)

    def delete_user(self, id):
        """Xoá nhân viên theo ID"""
        check_query = "SELECT * FROM employees WHERE id = %s"
        rows = self.db.fetch_all(check_query, (id,))
        if not rows:
            raise ValueError(f"Không tìm thấy nhân viên với ID: {id}")
        delete_query = "DELETE FROM employees WHERE id = %s"
        return self.db.execute_query(delete_query, (id,))

    def validate_login(self, email, password):
        """Xác thực đăng nhập"""
        query = "SELECT * FROM employees WHERE email = %s"
        rows = self.db.fetch_all(query, (email,))
        if not rows:
            return False, "Email không tồn tại", None

        row = rows[0]
        if row['password'] != password:
            return False, "Mật khẩu không đúng", None

        name = row['name']
        role = row['role']
        return True, f"Đăng nhập thành công, chào {name}", role

    def email_exists(self, email):
        query = "SELECT COUNT(*) as count FROM employees WHERE email = %s"
        result = self.db.fetch_all(query, (email,))
        return result[0]['count'] > 0 if result else False

    def close(self):
        self.db.close()

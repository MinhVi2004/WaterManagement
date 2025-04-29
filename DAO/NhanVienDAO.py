from DTO.NhanVienDTO import NhanVienDTO
from Database.database import Database
from datetime import datetime
from typing import Optional, Tuple

class NhanVienDAO:
    def __init__(self):
        self.db = Database()

    def get_all(self):
        sql = "SELECT * FROM employees"
        rows = self.db.fetch_all(sql)
        listNV = []
        for row in rows:
            nv = NhanVienDTO(
                row['id'], row['name'], row['phone'], row['email'], row['password'],
                row['role'], row['created_at'], row['status']
            )
            listNV.append(nv)
        return listNV

    def get_user(self, id):
        sql = "SELECT * FROM employees WHERE id = %s"
        rows = self.db.fetch_all(sql, (id,))
        if rows:
            row = rows[0]
            return NhanVienDTO(
                row['id'], row['name'], row['phone'], row['email'], row['password'],
                row['role'], row['created_at'], row['status']
            )
        return None

    def insert_user(self, name, phone, email, password, role, status=1):
        today = datetime.today().strftime('%Y-%m-%d')
        sql = """
            INSERT INTO employees (name, phone, email, password, role, created_at, status) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (name, phone, email, password, role, today, status)
        return self.db.execute_query(sql, params)

    def update_user(self, id, name, phone, email, password, role, created_at, status):
        sql = """
            UPDATE employees 
            SET name=%s, phone=%s, email=%s, password=%s, role=%s, created_at=%s, status=%s 
            WHERE id=%s
        """
        params = (name, phone, email, password, role, created_at, status, id)
        return self.db.execute_query(sql, params)

    def delete_user(self, id):
        check_sql = "SELECT * FROM employees WHERE id = %s"
        rows = self.db.fetch_all(check_sql, (id,))
        if not rows:
            raise ValueError(f"Không tìm thấy nhân viên với ID: {id}")
        delete_sql = "DELETE FROM employees WHERE id = %s"
        return self.db.execute_query(delete_sql, (id,))

    def validate_login(self, email, password):
        sql = "SELECT * FROM employees WHERE email = %s"
        rows = self.db.fetch_all(sql, (email,))
        if not rows:
            return False, "Email không tồn tại", None
        row = rows[0]
        if row['password'] != password:
            return False, "Mật khẩu không đúng", None
        name = row['name']
        role = row['role']
        return True, f"Đăng nhập thành công, chào {name}", role

    def email_exists(self, email):
        sql = "SELECT * FROM employees WHERE email = %s"
        result = self.db.fetch_all(sql, (email,))
        return len(result) > 0  

    def close(self):
        self.db.close()
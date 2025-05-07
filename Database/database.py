import mysql.connector
from mysql.connector import Error
from Database.config import DB_CONFIG

class Database:
    def __init__(self):
        """Khởi tạo kết nối database."""
        self.conn = None
        self.cursor = None
        try:
            self.conn = mysql.connector.connect(**DB_CONFIG)
            self.cursor = self.conn.cursor(dictionary=True)
            print("Kết nối MySQL thành công!")
        except Error as e:
            print(f"Lỗi kết nối MySQL: {e}")

    def fetch_all(self, query, params=None):
        """Lấy tất cả dữ liệu từ truy vấn."""
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except Error as e:
            print(f"Lỗi khi lấy dữ liệu: {e}")
            return []

    def execute_query(self, query, params=None):
        """Thực thi INSERT, UPDATE, DELETE"""
        try:
            self.cursor.execute(query, params or ())
            self.conn.commit()
            return True
        except Error as e:
            print(f"Lỗi khi thực thi query: {e}")
            return False

    def close(self):
        """Đóng kết nối database."""
        if self.conn:
            self.cursor.close()
            self.conn.close()
            print("🔴 Đã đóng kết nối MySQL!")

from Database.database import Database

from DTO.KhachHangDTO import KhachHangDTO  # Import lớp DTO
from datetime import datetime
class KhachHangDAO:
    def __init__(self): #establish connection to database
        db = Database()  # Tạo đối tượng Database
        self.conn = db.conn
        self.cursor = db.conn.cursor()

    def get_all(self):  # get all...
        listKH = []
        """Lấy thông tin user theo ID"""
        self.cursor.execute("SELECT * FROM customers")
        rows = self.cursor.fetchall()
        for row in rows:
            user_dto = KhachHangDTO(row[0], row[1], row[2], row[3], row[4],row[5])  # transform useless tuples into DTO
            listKH.append(user_dto)  # Thêm vào danh sách
        return listKH

    def get_user(self, id): # get user by id
        """Lấy thông tin user theo ID"""
        self.cursor.execute("SELECT * FROM customers WHERE id = %s", (id,))
        row = self.cursor.fetchone()
        if row:
            return KhachHangDTO(row[0], row[1], row[2], row[3], row[4], row[5])  # Trả về đối tượng DTO
        return None
    def search_Customer(self, keyword, search_type): # search customer by name, email, phone, address or id
        """Tìm kiếm khách hàng theo tên, email, số điện thoại hoặc địa chỉ"""
        if search_type == "Họ Tên":
            sql = "SELECT * FROM customers WHERE name LIKE %s"
        elif search_type == "Email":
            sql = "SELECT * FROM customers WHERE email LIKE %s"
        elif search_type == "Số Điện Thoại":
            sql = "SELECT * FROM customers WHERE phone LIKE %s"
        elif search_type == "Địa Chỉ":
            sql = "SELECT * FROM customers WHERE address LIKE %s"
        elif search_type == "Mã KH":
            sql = "SELECT * FROM customers WHERE id = %s"
        else:
            raise ValueError("Invalid search type")

        self.cursor.execute(sql, ('%' + keyword + '%',))
        rows = self.cursor.fetchall()
        listKH = []
        for row in rows:
            user_dto = KhachHangDTO(row[0], row[1], row[2], row[3], row[4],row[5])
            listKH.append(user_dto)
        return listKH
    def insert_user(self, name, email, phone, address): # insert user with the creation date of today
        """Thêm user mới"""
        self.cursor.execute("SELECT MAX(id) FROM customers")
        max_id = self.cursor.fetchone()[0]
        new_id = max_id + 1 if max_id is not None else 1
        today = datetime.today().strftime('%Y-%m-%d')
        sql = "INSERT INTO customers (id, name, email, phone, address, created_at) VALUES (%s, %s, %s, %s, %s, %s)"
        self.cursor.execute(sql, (new_id, name, email, phone, address, today))
        self.conn.commit()
        return new_id
    
    def delete_user(self, id): # delete user by id
        """Xóa user theo ID"""
        self.cursor.execute("DELETE FROM customers WHERE id = %s", (id,))
        self.conn.commit()
        
    def update_user(self, id, name, email, phone, address, created_at):
        """Updates a customer in the database."""
        sql = "UPDATE customers SET name=%s, email=%s, phone=%s, address=%s, created_at=%s WHERE id=%s"
        self.cursor.execute(sql, (name, email, phone, address, created_at, id))
        self.conn.commit()
    def close(self):
        self.conn.close()
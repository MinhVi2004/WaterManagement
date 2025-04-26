from Database.database import Database
from DTO.HoaDonDTO import HoaDonDTO
from datetime import datetime

class HoaDonDAO:
    def __init__(self):
        """Tạo kết nối đến cơ sở dữ liệu"""
        self.db = Database()  # Tạo đối tượng Database

    def get_all(self):
        """Lấy tất cả các hóa đơn"""
        query = "SELECT * FROM bills"
        rows = self.db.fetch_all(query)
        listHD = []
        for row in rows:
            hoa_don_dto = HoaDonDTO(row['id'], row['customer_id'], row['meter_id'], row['reading_id'], row['amount'], row['status'], row['created_at'], row['processed_by'])
            listHD.append(hoa_don_dto)
        return listHD

    def get_invoice(self, id):
        """Lấy thông tin hóa đơn theo ID"""
        query = "SELECT * FROM bills WHERE id = %s"
        row = self.db.fetch_all(query, (id,))
        if row:
            return HoaDonDTO(row[0]['id'], row[0]['customer_id'], row[0]['meter_id'], row[0]['reading_id'], row[0]['amount'], row[0]['status'], row[0]['created_at'], row[0]['processed_by'])
        return None

    def search_invoice(self, keyword, search_type):
        """Tìm kiếm hóa đơn theo ID, customer_id, hoặc meter_id"""
        if search_type == "Mã Hóa Đơn":
            query = "SELECT * FROM bills WHERE id = %s"
        elif search_type == "Mã Khách Hàng":
            query = "SELECT * FROM bills WHERE customer_id = %s"
        elif search_type == "Mã Đồng Hồ":
            query = "SELECT * FROM bills WHERE meter_id = %s"
        else:
            raise ValueError("Invalid search type")
        
        rows = self.db.fetch_all(query, (keyword,))
        listHD = []
        for row in rows:
            hoa_don_dto = HoaDonDTO(row['id'], row['customer_id'], row['meter_id'], row['reading_id'], row['amount'], row['status'], row['created_at'], row['processed_by'])
            listHD.append(hoa_don_dto)
        return listHD

    def insert_invoice(self, customer_id, meter_id, reading_id, amount, status, processed_by):
        """Thêm hóa đơn mới"""
        today = datetime.today().strftime('%Y-%m-%d')
        query = """
            INSERT INTO bills (customer_id, meter_id, reading_id, amount, status, created_at, processed_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        success = self.db.execute_query(query, (customer_id, meter_id, reading_id, amount, status, today, processed_by))
        
        if success:
            query = "SELECT MAX(id) FROM bills"
            result = self.db.fetch_all(query)
            return result[0]['MAX(id)'] if result else None
        return None

    def delete_invoice(self, id):
        """Xóa hóa đơn theo ID"""
        query = "DELETE FROM bills WHERE id = %s"
        return self.db.execute_query(query, (id,))

    def update_invoice(self, id, customer_id, meter_id, reading_id, amount, status, processed_by, created_at):
        """Cập nhật thông tin hóa đơn"""
        query = """
            UPDATE bills 
            SET customer_id=%s, meter_id=%s, reading_id=%s, amount=%s, status=%s, processed_by=%s, created_at=%s
            WHERE id=%s
        """
        return self.db.execute_query(query, (customer_id, meter_id, reading_id, amount, status, processed_by, created_at, id))

    def close(self):
        """Đóng kết nối"""
        self.db.close()

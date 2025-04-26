from DAO.HoaDonDAO import HoaDonDAO
from DTO.HoaDonDTO import HoaDonDTO

class HoaDonBUS:
    def __init__(self):
        """Khởi tạo đối tượng HoaDonDAO để thao tác với dữ liệu"""
        self.hoa_don_dao = HoaDonDAO()

    def get_all_bills(self):
        """Lấy tất cả hóa đơn"""
        return self.hoa_don_dao.get_all()

    def get_bill_by_id(self, id):
        """Lấy hóa đơn theo ID"""
        return self.hoa_don_dao.get_invoice(id)
    def get_customer_by_id(self, id):
          """Lấy hóa đơn theo ID"""
          return self.hoa_don_dao.get_customer_by_id(id)
    def get_employee_by_id(self, id):
          """Lấy hóa đơn theo ID"""
          return self.hoa_don_dao.get_employee_by_id(id)
    def search_bills(self, keyword, search_type):
        """Tìm kiếm hóa đơn theo các tiêu chí"""
        return self.hoa_don_dao.search_invoice(keyword, search_type)

    def create_bill(self, customer_id, meter_id, reading_id, amount, status, processed_by):
        """Thêm hóa đơn mới"""
        return self.hoa_don_dao.insert_invoice(customer_id, meter_id, reading_id, amount, status, processed_by)

    def delete_bill(self, id):
        """Xóa hóa đơn theo ID"""
        return self.hoa_don_dao.delete_invoice(id)

    def update_bill(self, id, customer_id, meter_id, reading_id, amount, status, processed_by, created_at):
        """Cập nhật thông tin hóa đơn"""
        return self.hoa_don_dao.update_invoice(id, customer_id, meter_id, reading_id, amount, status, processed_by, created_at)

    def close(self):
        """Đóng kết nối"""
        self.hoa_don_dao.close()

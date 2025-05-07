from Database.database import Database
from DTO.DongHoNuocDTO import DongHoNuocDTO

class DongHoNuocDAO:
    def __init__(self):
        self.db = Database()

    def get_all(self):
        query = "SELECT * FROM water_meters"
        results = self.db.fetch_all(query)
        return [DongHoNuocDTO(**row) for row in results]
    def search_water_meters_by_customer(self, keyword, search_type): # search customer by name, email, phone, address or id
        """Tìm kiếm khách hàng theo tên, email, số điện thoại hoặc địa chỉ"""
        if search_type == "Họ Tên":
            sql = "SELECT wm.* FROM water_meters wm, customers c WHERE wm.customer_id = c.id AND c.name LIKE %s"
        elif search_type == "Email":
            sql = "SELECT wm.* FROM water_meters wm, customers c WHERE wm.customer_id = c.id AND c.email LIKE %s"
        elif search_type == "Số Điện Thoại":
            sql = "SELECT wm.* FROM water_meters wm, customers c WHERE wm.customer_id = c.id AND c.phone LIKE %s"
        elif search_type == "Địa Chỉ":
            sql = "SELECT wm.* FROM water_meters wm, customers c WHERE wm.customer_id = c.id AND c.address LIKE %s"
        elif search_type == "Mã KH":
            sql = "SELECT wm.* FROM water_meters wm, customers c WHERE wm.customer_id = c.id AND c.id = %s"
        else:
            raise ValueError("Invalid search type")
        param = ('%' + keyword + '%',)
        results = self.db.fetch_all(sql, param)
        return [DongHoNuocDTO(**row) for row in results]

    def get_by_id(self, id):
        query = "SELECT * FROM water_meters WHERE id = %s"
        results = self.db.fetch_all(query, (id,))
        if results:
            return DongHoNuocDTO(**results[0])
        return None

    def insert(self, dong_ho_nuoc: DongHoNuocDTO):
        query = """
            INSERT INTO water_meters (customer_id, meter_number, location, installed_at, status)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (dong_ho_nuoc.customer_id, dong_ho_nuoc.meter_number, dong_ho_nuoc.location, dong_ho_nuoc.installed_at, dong_ho_nuoc.status)
        return self.db.execute_query(query, params)
    def insert(self, customer_id, location):
        query = """
            INSERT INTO water_meters (customer_id, location)
            VALUES (%s, %s)
        """
        params = (customer_id, location)
        return self.db.execute_query(query, params)
      

    def update(self, dong_ho_nuoc: DongHoNuocDTO):
        query = """
            UPDATE water_meters
            SET customer_id = %s, meter_number = %s, location = %s, installed_at = %s, status = %s
            WHERE id = %s
        """
        params = (dong_ho_nuoc.customer_id, dong_ho_nuoc.meter_number, dong_ho_nuoc.location, dong_ho_nuoc.installed_at, dong_ho_nuoc.status, dong_ho_nuoc.id)
        return self.db.execute_query(query, params)

    def delete(self, id):
        query = "DELETE FROM water_meters WHERE id = %s"
        return self.db.execute_query(query, (id,))
    def get_customer_by_watermeter_id(self, watermeter_id):
      query = """
            SELECT c.* 
            FROM customers c
            JOIN water_meters d ON c.id = d.customer_id
            WHERE d.id = %s
      """
      result = self.db.fetch_all(query, (watermeter_id,))
      return result[0] if result else None



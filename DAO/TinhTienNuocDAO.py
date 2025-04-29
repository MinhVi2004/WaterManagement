from Database.database import Database
from DTO.WaterMeterDTO import WaterMeterDTO # Import WaterMeterDTO class
from DAO.HoaDonDAO import HoaDonDAO
class TinhTienNuocDAO:
    def __init__(self):
        self.db = Database()
        self.HoaDonDAO = HoaDonDAO()

    def getWaterMeterById(self, meter_id):
        query = "SELECT * FROM water_meters WHERE id = %s"
        result = self.db.fetch_all(query, (meter_id,))
        
        if result:
            row = result[0]  # This is a dict, not a tuple
            return WaterMeterDTO(
                id=row["id"],
                customer_id=row["customer_id"],
                meter_number=row["meter_number"],
                location=row["location"],
                installed_at=row["installed_at"]
            )
        
        return None
    def updateWaterMeterNumber(self, meter_id, new_meter_number):
      query = "UPDATE water_meters SET meter_number = %s WHERE id = %s"
      self.db.execute_query(query, (new_meter_number, meter_id))

    def createWaterMeterReading(self, customer_id, meter_id, reading_before, reading_value, image_url, processed_by, tongTieuThu, tongTien):
      query = "INSERT INTO meter_readings (meter_id, reading_before, reading_value, image_url, created_at) VALUES (%s, %s, %s, %s, current_timestamp())"
      self.db.execute_query(query, (meter_id, reading_before, reading_value, image_url))
      
      self.updateWaterMeterNumber(meter_id, reading_value)
      
      id_meter_reading = self.HoaDonDAO.get_newest_id_meter_reading()
      self.HoaDonDAO.insert_invoice(
            customer_id, meter_id, id_meter_reading, tongTieuThu, tongTien,
            "Chờ Thanh Toán", processed_by
      )

    
    def close_connection(self):
        """Đóng kết nối database."""
        self.db.close()

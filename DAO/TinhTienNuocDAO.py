from Database.database import Database
from DTO.WaterMeterDTO import WaterMeterDTO # Import WaterMeterDTO class
class TinhTienNuocDAO:
    def __init__(self):
        self.db = Database()

    from DTO.WaterMeterDTO import WaterMeterDTO  # Make sure this import is correct

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


    def close_connection(self):
        """Đóng kết nối database."""
        self.db.close()

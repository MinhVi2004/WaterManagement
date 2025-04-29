from DAO.TinhTienNuocDAO import TinhTienNuocDAO
class TinhTienNuocBUS:
    def __init__(self):
        self.tinhTienNuocDAO = TinhTienNuocDAO()

    def getWaterMeterById(self, meter_id):
        return self.tinhTienNuocDAO.getWaterMeterById(meter_id)
    def updateWaterMeterNumber(self, meter_id, new_meter_number):
      return      self.tinhTienNuocDAO.updateWaterMeterNumber(meter_id, new_meter_number)
    def createWaterMeterReading(self, customer_id, meter_id,reading_before, reading_value,image_url, processed_by, tongTieuThu, tongTien):
      return   self.tinhTienNuocDAO.createWaterMeterReading(customer_id, meter_id,reading_before, reading_value, image_url, processed_by, tongTieuThu, tongTien)
    def close_connection(self):
        return self.tinhTienNuocDAO.close_connection()

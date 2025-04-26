from DAO.DongHoNuocDAO import DongHoNuocDAO
from DTO.DongHoNuocDTO import DongHoNuocDTO

class DongHoNuocBUS:
    def __init__(self):
        self.dao = DongHoNuocDAO()

    def get_all_dong_ho_nuoc(self):
        return self.dao.get_all()   
    def get_customer_by_watermeter_id(self, watermeter_id):
      return self.dao.get_customer_by_watermeter_id(watermeter_id)
    def get_dong_ho_nuoc_by_id(self, id):
        return self.dao.get_by_id(id)

    def add_dong_ho_nuoc(self, dong_ho_nuoc: DongHoNuocDTO):
        return self.dao.insert(dong_ho_nuoc)
    def add_dong_ho_nuoc(self, customer_id, location):
        return self.dao.insert(customer_id, location)

    def update_dong_ho_nuoc(self, dong_ho_nuoc: DongHoNuocDTO):
        return self.dao.update(dong_ho_nuoc)

    def delete_dong_ho_nuoc(self, id):
        return self.dao.delete(id)

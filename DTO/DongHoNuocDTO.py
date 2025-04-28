class DongHoNuocDTO:
    def __init__(self, id=None, customer_id=None, meter_number=None, location=None, installed_at=None, status=None):
        self.id = id  # (id): mã đồng hồ nước
        self.customer_id = customer_id  # (customer_id): mã khách hàng
        self.meter_number = meter_number  # (meter_number): số đồng hồ
        self.location = location  # (location): vị trí lắp đặt
        self.installed_at = installed_at  # (installed_at): ngày lắp đặt
        self.status = status  # (status): trạng thái (hoạt động, hỏng, thay thế...)

    def __str__(self):
        return f"DongHoNuocDTO(id={self.id}, customer_id={self.customer_id}, meter_number={self.meter_number}, location={self.location}, installed_at={self.installed_at}, status={self.status})"

class HoaDonDTO:
    def __init__(self, id, customer_id, meter_id, reading_id, amount, totalBill, status, created_at, processed_by):
        self.id = id
        self.customer_id = customer_id
        self.meter_id = meter_id
        self.reading_id = reading_id
        self.amount = amount
        self.totalBill = totalBill
        self.status = status
        self.created_at = created_at
        self.processed_by = processed_by

    def __str__(self):
        return f"HoaDon (id={self.id}, customer_id={self.customer_id}, meter_id={self.meter_id}, reading_id={self.reading_id}, amount={self.amount}, totalBill={self.totalBill} status={self.status}, created_at={self.cerated_at}, processed_by={self.processed_by})"

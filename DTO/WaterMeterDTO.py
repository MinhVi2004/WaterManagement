class WaterMeterDTO:
    def __init__(self, id, customer_id, meter_number, location, installed_at):
        self.id = id
        self.customer_id = customer_id
        self.meter_number = meter_number
        self.location = location
        self.installed_at = installed_at

    def __str__(self):
        return (f"WaterMeterDTO(id={self.id}, customer_id={self.customer_id}, "
                f"meter_number={self.meter_number}, location={self.location}, "
                f"installed_at={self.installed_at})")

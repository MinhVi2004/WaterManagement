
class NhanVienDTO:
    def __init__(self, id, name, phone, email, password, role, created_at, status):
        self.id = id
        self.name = name
        self.phone = phone  
        self.email = email
        self.password = password
        self.created_at = created_at
        self.role = role
        self.status = status
    def __str__(self):
        return (f"ID: {self.id} | Tên: {self.name} | SĐT: {self.phone} | "
                f"Email: {self.email} | Password: {self.password} | "
                f"Vai trò: {self.role.value} | Ngày tạo: {self.created_at} | Trạng thái: {self.status.value}")
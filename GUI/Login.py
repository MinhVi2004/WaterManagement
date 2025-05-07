from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.uic import loadUi
from BUS.LoginBUS import LoginBUS
from GUI.QLNV import QuanLyNhanVien 
from GUI.ChonKhachHang import ChonKhachHang

class Login_w(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('GUI/UI/login.ui', self) 

        self.login_bus = LoginBUS()  
        self.btnLogin.clicked.connect(self.handle_login)

    def handle_login(self):
        username = self.UserEmail.text()
        password = self.UserPassword.text()

        user = self.login_bus.check_login(username, password)

        if user :
            if user["status"] == 1:
                role = user['role']  
                QMessageBox.information(self, "Thành công", f"Đăng nhập thành công với vai trò: {role}!")

                if role == 'ADMIN':
                    print("Chuyển tới giao diện Admin")
                    self.OpenManagerForm()
                    
                if role == 'STAFF':
                    print("Chuyển tới giao diện Nhân viên")
                    self.openStaffForm(user)
            else:
                QMessageBox.warning(self,"Lỗi","Tài khoản đã bị khóa")
        else:
            QMessageBox.warning(self, "Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng!")
            
    def openStaffForm(self, user):
        self.staff_form = ChonKhachHang(user)
        self.staff_form.show()
        self.close()
    
    def OpenManagerForm(self):
        self.admin_form = QuanLyNhanVien()
        self.admin_form.show()
        self.close()

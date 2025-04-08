from PyQt6.QtWidgets import QApplication
from GUI.ChonKhachHang import ChonKhachHang

app = QApplication([])
window = ChonKhachHang()
window.show()
app.exec()

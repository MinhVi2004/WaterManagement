from PyQt6.QtWidgets import QApplication
from GUI.Login import Login_w

app = QApplication([])
window = Login_w()
window.show()
app.exec()

from Database.database import Database

class LoginBUS:
    def __init__(self):
        self.db = Database()

    def check_login(self, email, password):
        query = "SELECT * FROM employees WHERE email = %s AND password = %s"
        params = (email, password)
        result = self.db.fetch_all(query, params)

        if result and len(result) > 0:
            return result[0]  # Trả về user dạng dict
        return None

from flask_login import UserMixin

class User(UserMixin):

    def __init__(self, user_id, is_advisor, username, password):
        self.id = user_id
        self.is_advisor = is_advisor
        self.username = username
        self.password = password

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

from flask_login import UserMixin
from app import mysql, login_manager


@login_manager.user_loader
def load_user(username):
    return User.get(username)

class User(UserMixin):
    def __init__(self, username, password, status, fname, lname, usertype):
        self.username = username
        self.password = password
        self.usertype = usertype
        self.status = status
        self.fname = fname
        self.lname = lname

    def get_id(self):
        return self.username

    def set_type(self, t):
        self.usertype = t

    @staticmethod
    def get(username):
        #print("==================================")
        """try to return user_id corresponding User object.
        This method is used by load_user callback function
        """
        if not username:
            return None
        cur = mysql.connection.cursor()
        if cur.execute('SELECT * FROM user where Username = "%s"' % username) > 0:
            data = cur.fetchall()
            username, status, password, fname, lname = data[0]
            usertype = 'User'
            isAdmin, isManager, isCustomer = False, False, False
            if cur.execute('select * from admin where Username = "%s"' % username):
                isAdmin = True
            if cur.execute('select * from manager where Username = "%s"' % username):
                isManager = True
            if cur.execute('select * from customer where Username = "%s"' % username):
                isCustomer = True
            if isCustomer and isAdmin:
                usertype = 'CustomerAdmin'
            elif isCustomer and isManager:
                usertype = 'CustomerManager'
            elif isAdmin:
                usertype = 'Admin'
            elif isManager:
                usertype = 'Manager'
            elif isCustomer:
                usertype = 'Customer'
            return User(username, password, status, fname, lname, usertype)
        return None





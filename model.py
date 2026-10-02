from datetime import datetime
class Grocery:
    def __init__(self, _id=0, name='', price='', img=None, types='', quantity='', user_id=0):
        self.grocId = _id
        self.grocName = name
        self.grocPrice = price
        self.grocImg = img
        self.grocType = types
        self.grocQuantity = quantity
        self.user_id = user_id
    def __repr__(self):
        return f'Grocery[{self.grocId},{self.grocName},{self.grocPrice},{self.grocImg},{self.grocType},{self.grocQuantity}]'
class Order:
    def __init__(self, order_id=0, customer_name='', phone_number='', order_datetime=None, order_items='', total_price=0.0, user_id=0):
        self.order_id = order_id
        self.customer_name = customer_name
        self.phone_number = phone_number
        self.order_datetime = order_datetime if order_datetime else datetime.now()
        self.order_items = order_items
        self.total_price = total_price
        self.user_id = user_id  # Add user_id for foreign key reference
    def __repr__(self):
        return f'Order[{self.order_id},{self.customer_name},{self.phone_number},{self.order_datetime},{self.order_items},{self.total_price}]'
class User:
    def __init__(self, user_id=0, username='', password=''):
        self.user_id = user_id
        self.username = username
        self.password = password
    def __repr__(self):
        return f'User[{self.user_id},{self.username}]'
class LoginAttempt:
    def __init__(self, attempt_id=0, username='', attempt_time=None, success=False, user_id=None):
        self.attempt_id = attempt_id
        self.username = username
        self.attempt_time = attempt_time if attempt_time else datetime.now()
        self.success = success
        self.user_id = user_id
    def __repr__(self):
        return f'LoginAttempt[{self.attempt_id},{self.username},{self.attempt_time},{self.success}]'
class LoginSession:
    def __init__(self, session_id=0, user_id=0, login_time=None, logout_time=None):
        self.session_id = session_id
        self.user_id = user_id
        self.login_time = login_time if login_time else datetime.now()
        self.logout_time = logout_time
    def __repr__(self):
        return f'LoginSession[{self.session_id},{self.user_id},{self.login_time},{self.logout_time}]'
from datetime import datetime
class Grocery:
    def __init__(self, _id=0, name='', price='', img=None, types='', quantity='', user_id=0):
        self.grocId = _id
        self.grocName = name
        self.grocPrice = price
        self.grocImg = img
        self.grocType = types
        self.grocQuantity = quantity
        self.user_id = user_id
    def __repr__(self):
        return f'Grocery[{self.grocId},{self.grocName},{self.grocPrice},{self.grocImg},{self.grocType},{self.grocQuantity}]'
class Order:
    def __init__(self, order_id=0, customer_name='', phone_number='', order_datetime=None, order_items='', total_price=0.0, user_id=0):
        self.order_id = order_id
        self.customer_name = customer_name
        self.phone_number = phone_number
        self.order_datetime = order_datetime if order_datetime else datetime.now()
        self.order_items = order_items
        self.total_price = total_price
        self.user_id = user_id  # Add user_id for foreign key reference
    def __repr__(self):
        return f'Order[{self.order_id},{self.customer_name},{self.phone_number},{self.order_datetime},{self.order_items},{self.total_price}]'
class User:
    def __init__(self, user_id=0, username='', password=''):
        self.user_id = user_id
        self.username = username
        self.password = password
    def __repr__(self):
        return f'User[{self.user_id},{self.username}]'
class LoginAttempt:
    def __init__(self, attempt_id=0, username='', attempt_time=None, success=False, user_id=None):
        self.attempt_id = attempt_id
        self.username = username
        self.attempt_time = attempt_time if attempt_time else datetime.now()
        self.success = success
        self.user_id = user_id
    def __repr__(self):
        return f'LoginAttempt[{self.attempt_id},{self.username},{self.attempt_time},{self.success}]'
class LoginSession:
    def __init__(self, session_id=0, user_id=0, login_time=None, logout_time=None):
        self.session_id = session_id
        self.user_id = user_id
        self.login_time = login_time if login_time else datetime.now()
        self.logout_time = logout_time
    def __repr__(self):
        return f'LoginSession[{self.session_id},{self.user_id},{self.login_time},{self.logout_time}]'

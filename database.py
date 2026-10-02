import pymysql
from model import Grocery, Order, User, LoginAttempt, LoginSession
from datetime import datetime

con = pymysql.connect(host='localhost', user='root', password='rakshith', db='grocerydb')
print('Connected Successfully with Database...')
cursor = con.cursor()
def saveGroc(groc):
    try:
        sqlQuery = 'INSERT INTO grocery (grocName, grocPrice, grocImg, grocType, grocQuantity, user_id) VALUES (%s, %s, %s, %s, %s, %s)'
        cursor.execute(sqlQuery, (groc.grocName, groc.grocPrice, groc.grocImg, groc.grocType, groc.grocQuantity, groc.user_id))
        con.commit()
    except Exception as e:
        print("-" * 5, 'Error', "-" * 5)
        print(e)
def getGroclist(user_id=None):
    groclist = []
    try:
        if user_id:
            sqlQuery = 'SELECT * FROM grocery WHERE user_id = %s'
            cursor.execute(sqlQuery, (user_id,))
        else:
            sqlQuery = 'SELECT * FROM grocery'
            cursor.execute(sqlQuery)
        rows = cursor.fetchall()
        con.commit()
        for row in rows:
            groc = Grocery(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            groclist.append(groc)
        return groclist
    except Exception as e:
        print("-" * 5, 'Error', "-" * 5)
        print(e)
def getGrocById(_id):
    try:
        print(f"getGrocById called with _id: {_id}, type: {type(_id)}") #debug
        sqlQuery = 'SELECT * FROM grocery WHERE grocId = %s'
        cursor.execute(sqlQuery, (_id,))
        row = cursor.fetchone()
        if row:
            groc = Grocery(row[0], row[1], row[2], row[3], row[4], row[5])
            con.commit()
            return groc
        else:
            return None
    except Exception as e:
        print("-" * 5, 'Error', "-" * 5)
        print(e)
        return None
    

def deleteGroc(_id):
    try:
        sqlQuery = 'DELETE FROM grocery WHERE grocId = %s'
        cursor.execute(sqlQuery, (_id,))
        con.commit()
    except Exception as e:
        print("-" * 5, 'Error', "-" * 5)
        print(e)

def updateGroc(_id, groc):
    try:
        sqlQuery = 'UPDATE grocery SET grocName = %s, grocPrice = %s, grocImg = %s, grocType = %s, grocQuantity = %s WHERE grocId = %s'
        cursor.execute(sqlQuery, (groc.grocName, groc.grocPrice, groc.grocImg, groc.grocType, groc.grocQuantity, _id))
        con.commit()
    except Exception as e:
        print("-" * 5, 'Error', "-" * 5)
        print(e)
def saveOrder(order):
    try:
        # Ensure the user_id exists in the `users` table
        sqlCheckUser = 'SELECT COUNT(*) FROM users WHERE user_id = %s'
        cursor.execute(sqlCheckUser, (order.user_id,))
        user_exists = cursor.fetchone()[0]
        
        if not user_exists:
            raise ValueError(f"User with user_id {order.user_id} does not exist in the users table.")

        # Insert the order into the orders table
        if not order.order_datetime:
            order.order_datetime = datetime.now()
        sqlQuery = 'INSERT INTO orders (customer_name, phone_number, order_datetime, order_items, total_price, user_id) VALUES (%s, %s, %s, %s, %s, %s)'
        cursor.execute(sqlQuery, (order.customer_name, order.phone_number, order.order_datetime, order.order_items, order.total_price, order.user_id))
        con.commit()
    except pymysql.Error as e:
        print("-" * 5, 'Database Error', "-" * 5)
        print(f"MySQL Error [{e.args[0]}]: {e.args[1]}")
    except Exception as e:
        print("-" * 5, 'General Error', "-" * 5)
        print(f"An error occurred: {e}")
def getOrderlist(user_id=None):
    orderlist = []
    try:
        if user_id:
            sqlQuery = 'SELECT * FROM orders WHERE user_id = %s'
            cursor.execute(sqlQuery, (user_id,))
        else:
            sqlQuery = 'SELECT * FROM orders'
            cursor.execute(sqlQuery)
        rows = cursor.fetchall()
        con.commit()
        for row in rows:
            order = Order(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            orderlist.append(order)
        return orderlist
    except Exception as e:
        print("-" * 5, 'Error', "-" * 5)
        print(e)
def getOrderById(order_id):
    try:
        sqlQuery = 'SELECT * FROM orders WHERE order_id = %s'
        cursor.execute(sqlQuery, (order_id,))
        row = cursor.fetchone()
        if row:
            order = Order(row[0], row[1], row[2], row[3], row[4], row[5])
            con.commit()
            return order
        else:
            return None
    except Exception as e:
        print("-" * 5, 'Error', "-" * 5)
        print(e)
        return None

def get_user_by_username(username):
    try:
        sqlQuery = 'SELECT * FROM Users WHERE username = %s'
        cursor.execute(sqlQuery, (username,))
        row = cursor.fetchone()
        if row:
            return User(row[0], row[1], row[2])  # Assuming User model takes id, username, password
        else:
            return None
    except Exception as e:
        print("-" * 5, 'Error', "-" * 5)
        print(e)
        return None

def save_user(user):
    try:
        sqlQuery = 'INSERT INTO Users (username, password) VALUES (%s, %s)'
        cursor.execute(sqlQuery, (user.username, user.password))
        con.commit()
    except Exception as e:
        print("-" * 5, 'Error', "-" * 5)
        print(e)

def save_login_attempt(attempt):
    try:
        user = get_user_by_username(attempt.username)
        user_id = user.user_id if user else None  # If user exists, get `user_id`, else `None`
        sqlQuery = 'INSERT INTO LoginAttempts (username, attempt_time, success, user_id) VALUES (%s, %s, %s, %s)'
        cursor.execute(sqlQuery, (attempt.username, attempt.attempt_time, attempt.success, user_id))
        con.commit()
    except Exception as e:
        print("-" * 5, 'Error', "-" * 5)
        print(e)
def save_login_session(session):
    try:
        sqlQuery = 'INSERT INTO LoginSessions (user_id, login_time) VALUES (%s, %s)'
        cursor.execute(sqlQuery, (session.user_id, session.login_time))
        con.commit()
    except Exception as e:
        print("-" * 5, 'Error', "-" * 5)
        print(e)

def get_latest_login_session(user_id):
    try:
        sqlQuery = 'SELECT * FROM LoginSessions WHERE user_id = %s ORDER BY login_time DESC LIMIT 1'
        cursor.execute(sqlQuery, (user_id,))
        row = cursor.fetchone()
        if row:
            return LoginSession(row[0], row[1], row[2], row[3]) # Assuming LoginSession model takes session_id, user_id, login_time, logout_time
        else:
            return None
    except Exception as e:
        print("-" * 5, 'Error', "-" * 5)
        print(e)
        return None

def update_login_session(session_id, logout_time):
    try:
        sqlQuery = 'UPDATE LoginSessions SET logout_time = %s WHERE session_id = %s'
        cursor.execute(sqlQuery, (logout_time, session_id))
        con.commit()
    except Exception as e:
        print("-" * 5, 'Error', "-" * 5)
        print(e)
def get_daily_sales_summary(date):
    try:
        sqlQuery = '''SELECT SUM(total_price) FROM orders WHERE DATE(order_datetime) = %s'''
        cursor.execute(sqlQuery, (date,))
        result = cursor.fetchone()
        
        if result and result[0]:
            return result[0]  # Return the total sales for the day
        else:
            return 0  # No sales on this day
    except Exception as e:
        print("-" * 5, 'Error', "-" * 5)
        print(e)
        return 0
# Fetch sales summary for all days
def get_all_sales_summary():
    try:
        # Get all sales grouped by day
        sqlQuery = '''SELECT DATE(order_datetime) AS sale_date, SUM(total_price) AS total_sales
                      FROM orders
                      GROUP BY DATE(order_datetime)
                      ORDER BY sale_date DESC'''
        cursor.execute(sqlQuery)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print("-" * 5, 'Error', "-" * 5)
        print(e)
        return []
def closeconnection():
    con.close()

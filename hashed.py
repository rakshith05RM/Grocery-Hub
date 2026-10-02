import bcrypt
import pymysql

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


con = pymysql.connect(host='localhost', user='root', passwd='rakshith', db='grocerydb')
print('Connected Successfully with Database...')
cursor = con.cursor()
username = input("Enter the username: ")
password = input("Enter the password: ")
hashed_password = hash_password(password)
print(f"Hashed password: {hashed_password.decode('utf-8')}")

# Insert into database
connection = pymysql.connect(
        user='root',
        password='rakshith',
        database='grocerydb',
        host='localhost'
    )

cursor = connection.cursor()
cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password.decode('utf-8')))
connection.commit()
cursor.close()
connection.close()
print("User created successfully")
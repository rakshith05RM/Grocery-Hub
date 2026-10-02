import pymysql
import base64
from PIL import Image
from io import BytesIO
def get_image_from_db(grocId):
    con = pymysql.connect(host='localhost', user='root', passwd='rakshith', db='grocerydb')
    cursor = con.cursor()
    sqlQuery = 'SELECT grocImg FROM grocery WHERE grocId = %s'
    cursor.execute(sqlQuery, (grocId,))
    row = cursor.fetchone()
    con.close()
    if row:
        print(f"Fetched row for grocId {grocId}: {row}")
    else:
        print(f"No row found for grocId {grocId}")
    return row[0] if row else None
def display_image(image_data):
    image = Image.open(BytesIO(image_data))
    image.show()

def save_image_to_file(image_data, file_name):
    with open(file_name, "wb") as file:
        file.write(image_data)
grocId =9 
image_data = get_image_from_db(grocId)
if image_data:
    display_image(image_data)
    save_image_to_file(image_data, "output_image.jpg")
else:
    print("No image found for the specified grocId.")
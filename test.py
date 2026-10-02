import database as db
print("Grocery List:")
for item in db.getGroclist():
    print(item)
deleteitem= input("Delete item ID (or Enter to skip): ")
if deleteitem:
    db.deleteGroc(int(deleteitem))
    print("Item deleted.")
else:
     print("Invalid ID.")
db.closeconnection()
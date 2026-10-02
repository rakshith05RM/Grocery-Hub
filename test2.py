import database as db
from model import Order, Grocery
from datetime import datetime
import json
def view_orders():
    orderlist = db.getOrderlist()
    if not orderlist:
        print("No orders found.")
        return
    print("-" * 20, "Order List", "-" * 20)
    for order in orderlist:
        print(f"Order ID: {order.order_id}")
        print(f"Customer Name: {order.customer_name}")
        print(f"Phone Number: {order.phone_number}")
        print(f"Order Datetime: {order.order_datetime}")
        print("Order Items:")
        order_items = json.loads(order.order_items)
        for item in order_items:
            print(f"  - {item['name']} - ${item['price']}")
        print(f"Total Price: ₹{order.total_price}")
        print("-" * 40)
def insert_order():
    customer_name = input("Enter customer name: ")
    phone_number = input("Enter phone number: ")
    groclist = db.getGroclist()
    if not groclist: 
        print("No groceries available to order.")
        return
    print("Available Groceries:")
    for i, groc in enumerate(groclist):
        print(f"{i+1}. {groc.grocName} - ${groc.grocPrice} (ID: {groc.grocId})")
    selected_items = input("Enter grocery IDs and quantities (ID:quantity,ID:quantity,...): ")
    selected_pairs = [item.strip() for item in selected_items.split(",")]
    order_details = []
    total_price = 0.0
    for pair in selected_pairs:
        try:
            item_id, quantity = map(int, pair.split(":"))
            groc = db.getGrocById(item_id)
            if groc:
                item_price = groc.grocPrice * quantity
                order_details.append({"name": groc.grocName, "price": groc.grocPrice, "quantity": quantity})
                total_price += item_price
            else:
                print(f"Grocery ID {item_id} not found.")
        except ValueError:
            print(f"Invalid input: {pair}. Please use ID:quantity format.")
    groclist = db.getGroclist()
    if not groclist:
        print("No groceries available to order.")
        return
    order_items_str = json.dumps(order_details)
    order = Order(
        customer_name=customer_name,
        phone_number=phone_number,
        order_items=order_items_str,
        total_price=total_price,
    )
    db.saveOrder(order)
    print("Order saved successfully.")
def main():
    while True:
        print("\n--- Order Test Menu ---")
        print("1. View Orders")
        print("2. Insert Order")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            view_orders()
        elif choice == "2":
            insert_order()
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
main()
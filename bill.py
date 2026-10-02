import json
import os
import datetime
import database as db
# Create directory if not exists
if not os.path.exists("CustomerBills"):
    os.makedirs("CustomerBills")
def generate_bill_file(order_id):
    order = db.getOrderById(order_id)  
    if not order:
        return None 
    order_items = json.loads(order.order_items)  
    bill_file_path = os.path.join("CustomerBills", f"Customer_{order_id}.txt")
    # Bill content starts here
    bill_content = [
        "**** Thank You for Your Purchase! ****\n",
        f"Customer Name : {order.customer_name} \t\t\tOrder Date: {order.order_datetime}",
        f"Phone Number  : {order.phone_number}",
       
        f"{'Product':<25}{'Price':<15}{'Quantity':<15}{'Total Price':<10}",
        "-" * 70
    ]
    total_amount = 0 
    for item in order_items:
        item_total = item['quantity'] * item['price']
        total_amount += item_total
        bill_content.append(f"{item['name']:<25}{item['price']:<15}{item['quantity']:<15}{'₹' + format(item_total, '.2f')}")
    bill_content.append("-" * 70)
    bill_content.append(f"{'Grand Total:':<15}{'₹' + format(total_amount, '.2f')}")
    bill_content.append("\n**** Thank you for shopping with us, We hope to see you again soon! ****")   
    # Write to file
    try:
        with open(bill_file_path, 'w', encoding='utf-8') as bill_file:
            bill_file.write("\n".join(bill_content))
    except Exception as e:
        print(f"Error writing to file: {e}")
        return None
    return bill_file_path
# Example usage
o = generate_bill_file(25)
print(o)
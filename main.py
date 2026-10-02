from flask import Flask, render_template, redirect, request, url_for, session, send_file
import database as db
from model import Grocery, Order, User, LoginAttempt, LoginSession
from datetime import datetime
import json
import base64
import bcrypt
from bill import generate_bill_file
app = Flask(__name__)
app.secret_key = "rm" 
@app.before_request
def before_request():
    if request.endpoint not in ['index', 'log_in', 'welcome', 'static'] and 'user_id' not in session:
        return redirect(url_for('log_in'))
@app.route("/")
def index():
    return redirect(url_for('welcome'))
@app.route('/welcome')
def welcome():
    return render_template('index.html')
@app.route('/login', methods=['GET', 'POST'])
def log_in():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.get_user_by_username(username)
        if user:
            hashed_password = user.password.encode('utf-8')  # Encode stored hash
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password): #encode password
                session['user_id'] = user.user_id
                session['login_time'] = datetime.now()
                db.save_login_session(LoginSession(user_id=user.user_id, login_time=session['login_time']))
                return redirect(url_for('home'))
            else:
                error = 'Invalid Credentials. Please try again.'
                db.save_login_attempt(LoginAttempt(username=username, attempt_time=datetime.now(), success=False))
        else:
            error = 'Invalid Credentials. Please try again.'
            db.save_login_attempt(LoginAttempt(username=username, attempt_time=datetime.now(), success=False))

    return render_template('login.html', error=error)
@app.route('/logout')
def logout():
    print("Logout route called!")
    try:
        if 'user_id' in session:
            logout_time = datetime.now()
            login_session = db.get_latest_login_session(session['user_id'])
            if login_session:
                db.update_login_session(login_session.session_id, logout_time)
            session.pop('user_id', None)
            session.pop('login_time', None)
            print("Session cleared.")
        else:
            print("user_id not in session")
        print("Rendering logout.html")
        return render_template('logout.html')
    except Exception as e:
        print(f"Error during logout: {e}")
        return "An error occurred during logout."
@app.route('/home')
def home():
    all_sales_raw = db.get_all_sales_summary()
    all_sales = [{'sale_date': row[0], 'total_sales': row[1]} for row in all_sales_raw]
    return render_template('home.html', all_sales=all_sales)
@app.route('/addgroc')
def addgroc():
    groc = Grocery()
    return render_template('addgroc.html', groc=groc, action='Add')
@app.route('/deletegroc/<int:grocId>')
def deletegroc(grocId):
    db.deleteGroc(grocId)
    return redirect('/groclist')
@app.route('/groclist')
def showgrocs():
    groclist = db.getGroclist()
    for groc in groclist:
        if groc.grocImg:
            groc.grocImg = base64.b64encode(groc.grocImg).decode('utf-8')
    return render_template('groclist.html', groclist=groclist)
@app.route('/editgroc/<int:grocId>')
def editgroc(grocId):
    groc = db.getGrocById(grocId)
    if groc.grocImg:
        groc.grocImg = base64.b64encode(groc.grocImg).decode('utf-8')
    return render_template('addgroc.html', groc=groc, action='Edit')
@app.route('/updategroc', methods=['POST'])
def updatename():
    _id = request.form['grocId']
    name = request.form['grocName']
    price = request.form['grocPrice']
    imgfile = request.files['grocImg']
    types = request.form['grocType']
    quantity = request.form['grocQuantity']
    existing_groc = db.getGrocById(_id)   
    if imgfile and imgfile.filename:  
        imgdata = imgfile.read()
    else:  
        imgdata = existing_groc.grocImg 
    groc = Grocery(_id, name, price, imgdata, types, quantity)
    db.updateGroc(_id, groc)
    return redirect(url_for('showgrocs'))
@app.route('/savegroc', methods=['POST'])
def savegroc():
    if 'user_id' not in session:
        return redirect(url_for('log_in'))
    user_id = session['user_id']
    name = request.form['grocName']
    price = request.form['grocPrice']
    types = request.form['grocType']
    quantity = request.form['grocQuantity']
    imgfile = request.files['grocImg']
    imgdata = imgfile.read()
    groc = Grocery(name=name, price=price, img=imgdata, types=types, quantity=quantity, user_id=user_id)
    db.saveGroc(groc)
    return redirect(url_for('showgrocs'))
@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        if 'user_id' not in session:
            return redirect(url_for('log_in'))  # Ensure the user is logged in
        # Retrieve user_id from session
        user_id = session['user_id']
        customer_name = request.form['customer_name']
        phone_number = request.form['phone_number']
        order_items = request.form.getlist('order_items[]')
        quantities = request.form.getlist('quantity[]')
        total_price = 0.0
        order_details = []
        for item_id, quantity in zip(order_items, quantities):
            try:
                item_id = int(item_id)
                quantity = int(quantity)
                groc = db.getGrocById(item_id)
                if groc:
                    item_price = groc.grocPrice * quantity
                    total_price += item_price
                    order_details.append({
                        "name": groc.grocName,
                        "price": float(groc.grocPrice),
                        "quantity": quantity
                    })
                else:
                    print(f"Grocery ID {item_id} not found.")
            except ValueError:
                print("Error: Invalid quantity or item ID.")
        order_items_str = json.dumps(order_details)
        if order_details:
            order = Order(
                customer_name=customer_name,
                phone_number=phone_number,
                order_items=order_items_str,
                total_price=total_price,
                order_datetime=datetime.now(),
                user_id=user_id  # Pass user_id to the Order object
            )
            db.saveOrder(order)
            return redirect(url_for('view_orders'))
        else:
            print("No valid order details found. Order not saved.")
    groclist = db.getGroclist()
    return render_template('order.html', groclist=groclist)
@app.route('/view_orders')
def view_orders():
    try:
        orderlist = db.getOrderlist()
        for order in orderlist:
            try:
                order.order_items = json.loads(order.order_items)
            except json.JSONDecodeError:
                print(f"Error decoding JSON for order {order.order_id}")
                order.order_items = []
        return render_template('view_orders.html', orderlist=orderlist)
    except Exception as e:
        print(f"Error fetching orders: {e}")
        return "An error occurred while fetching orders."
@app.route('/view_bill/<int:order_id>')
def bill_page(order_id):
    order = db.getOrderById(order_id)
    if not order:
        return "Order not found", 404
    try:
        order_items = json.loads(order.order_items)
    except json.JSONDecodeError:
        order_items = []
    return render_template('viewbill.html', order=order, order_items=order_items)
@app.route('/bill/<int:order_id>', methods=['GET'])
def generate_bill(order_id):
    bill_file = generate_bill_file(order_id)  # Use the imported function
    if bill_file:
        return send_file(bill_file, as_attachment=True)
    else:
        return "Order not found", 404   
if __name__ == '__main__':
    app.run(debug=True)
    db.closeconnection()
from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import MySQLdb.cursors
import mysql.connector
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Charanelangovan333@'
app.config['MYSQL_DB'] = 'inventory_management'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

# # Add Product
# @app.route('/add_product', methods=['GET', 'POST'])
# def add_product():
#     if request.method == 'POST':
#         product_name = request.form['product_name']
#         cursor = mysql.connection.cursor()
#         cursor.execute("INSERT INTO Product (product_name) VALUES (%s)", [product_name])
#         mysql.connection.commit()
#         return redirect('/')
#     return render_template('add_product.html')

# Add Location
@app.route('/add_location', methods=['GET', 'POST'])
def add_location():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Handle the addition of a new location
    if request.method == 'POST':
        location_name = request.form['location_name']
        cursor.execute("INSERT INTO Location (location_name) VALUES (%s)", [location_name])
        mysql.connection.commit()
        return redirect('/add_location')  # Redirect to the same page to see the updated list

    # Retrieve all locations to display
    cursor.execute("SELECT * FROM Location")
    locations = cursor.fetchall()
    
    return render_template('add_location.html', locations=locations)

@app.route('/add_movement', methods=['GET', 'POST'])
def add_movement():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Handle the addition of a new movement
    if request.method == 'POST':
        from_location = request.form['from_location']
        to_location = request.form['to_location']
        product_id = request.form['product_id']
        qty = request.form['qty']
        
        cursor.execute("""
            INSERT INTO ProductMovement (from_location, to_location, product_id, qty) 
            VALUES (%s, %s, %s, %s)
        """, (from_location, to_location, product_id, qty))
        mysql.connection.commit()
        return redirect('/add_movement')  # Redirect to the same page to see the updated list

    # Retrieve all movements to display
    cursor.execute("""
        SELECT * FROM ProductMovement
        JOIN Product ON ProductMovement.product_id = Product.product_id
        JOIN Location l1 ON ProductMovement.from_location = l1.location_id
        JOIN Location l2 ON ProductMovement.to_location = l2.location_id
    """)
    movements = cursor.fetchall()
    
    return render_template('add_movement.html', movements=movements)


@app.route('/balance')
def balance():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = '''
    SELECT 
        Product.product_name, 
        Location.location_name, 
        SUM(ProductMovement.qty) AS qty
    FROM ProductMovement
    JOIN Product ON ProductMovement.product_id = Product.product_id
    JOIN Location ON ProductMovement.to_location = Location.location_id
    GROUP BY Product.product_name, Location.location_name
    '''
    cursor.execute(query)
    movements = cursor.fetchall()
    
    return render_template('balance.html', movements=movements)

@app.route('/add_product', methods=['GET', 'POST'])
def products():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Handle the addition of a new product
    if request.method == 'POST':
        product_name = request.form['product_name']
        cursor.execute("INSERT INTO Product (product_name) VALUES (%s)", [product_name])
        mysql.connection.commit()
        return redirect('/add_product')  # Redirect to the same page to see the updated list

    # Retrieve all products to display
    cursor.execute("SELECT * FROM Product")
    products = cursor.fetchall()
    
    return render_template('add_product.html', products=products)
@app.route('/view_product/<int:product_id>')
def view_product(product_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    print("==>", product_id)
    # Fetch the product details by its ID
    cursor.execute("SELECT * FROM Product WHERE product_id = %s", (product_id,))
    product = cursor.fetchone()
    
    if not product:
        return "Product not found", 404
    
    return render_template('view_product.html', product=product)

@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # If the form is submitted, update the product
    if request.method == 'POST':
        product_name = request.form['product_name']
        
        # Update the product in the database
        cursor.execute("UPDATE Product SET product_name = %s WHERE product_id = %s", (product_name, product_id))
        mysql.connection.commit()
        return redirect('/add_product')
    
    # Fetch the existing product details
    cursor.execute("SELECT * FROM Product WHERE product_id = %s", (product_id,))
    product = cursor.fetchone()
    
    if not product:
        return "Product not found", 404
    
    return render_template('edit_product.html', product=product)

@app.route('/view_location/<int:location_id>')
def view_location(location_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #print("==>", location_id)
    # Fetch the product details by its ID
    cursor.execute("SELECT * FROM location WHERE location_id = %s", (location_id,))
    location = cursor.fetchone()
    
    if not location:
        return "location not found", 404
    
    return render_template('view_location.html', location=location)
if __name__ == '__main__':
    app.run(debug=True)

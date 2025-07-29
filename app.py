from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import sqlite3
import subprocess
import hashlib
import os

app = Flask('Harry Potter')
app.secret_key = 'your-secret-key'  # Replace with a secure key in production

def get_db():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # always points to perfume-ecommerce/
    db_path = os.path.join(BASE_DIR, 'database.db')         # forces use of correct database
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products')
def products_page():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM categories')
    categories = c.fetchall()
    c.execute('SELECT p.*, c.name AS category_name FROM products p JOIN categories c ON p.category_id = c.id')
    products = c.fetchall()
    conn.close()
    return render_template('products.html', categories=categories, products=products)

@app.route('/products/search')
def search_products():
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    conn = get_db()
    c = conn.cursor()
    sql = 'SELECT p.*, c.name AS category_name FROM products p JOIN categories c ON p.category_id = c.id WHERE 1=1'
    params = []
    if query:
        sql += ' AND p.name LIKE ?'
        params.append(f'%{query}%')
    if category:
        sql += ' AND c.id = ?'
        params.append(category)
    c.execute(sql, params)
    products = c.fetchall()
    conn.close()
    return jsonify([dict(row) for row in products])

@app.route('/cart')
def cart_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('cart.html')

@app.route('/checkout')
def checkout_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('checkout.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()
        conn = get_db()
        c = conn.cursor()
        try:
            c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            conn.close()
            return render_template('register.html', error='Username already exists')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/api/confirm-order', methods=['POST'])
def confirm_order():
    try:
        cart = request.json.get('cart', [])
        conn = get_db()
        c = conn.cursor()
        order_details = []
        for item in cart:
            c.execute('SELECT name, price FROM products WHERE id = ?', (item['id'],))
            product = c.fetchone()
            if product:
                order_details.append(f"{product['name']} (x{item['quantity']}): ${product['price'] * item['quantity']:.2f}")
        conn.close()
        order_summary = "\n".join(order_details)
        result = subprocess.run(
            ['java', '-cp', 'src', 'OrderConfirmation', order_summary],
            capture_output=True, text=True
        )
        return jsonify({'message': result.stdout.strip()})
    except Exception as e:
        return jsonify({'message': 'Order confirmed (mock)', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

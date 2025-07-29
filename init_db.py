import sqlite3
import os

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Full path to the database file
db_path = os.path.join(BASE_DIR, 'database.db')

# Connect to the correct database location
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Create tables
c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)''')

c.execute('''CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)''')

c.execute('''CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    image TEXT,
    category_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES categories(id)
)''')

# Insert sample data
c.execute("INSERT OR IGNORE INTO categories (name) VALUES ('Floral'), ('Fresh'), ('Woody')")

c.execute('''INSERT OR IGNORE INTO products (name, description, price, image, category_id) VALUES
    ('Elegant Rose', 'A floral fragrance with notes of rose and jasmine.', 49.99, 'images/perfume1.jpg', 1),
    ('Ocean Breeze', 'A fresh scent with hints of sea salt and citrus.', 59.99, 'images/perfume2.jpg', 2),
    ('Midnight Oud', 'A rich blend of oud and amber for a bold aroma.', 79.99, 'images/perfume3.jpg', 3)
''')

c.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ('admin', '123456'))

conn.commit()
conn.close()

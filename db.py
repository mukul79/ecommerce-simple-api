import sqlite3
conn = sqlite3.connect('products.db')
c = conn.cursor()
c.execute('''CREATE TABLE products
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL,
              category TEXT NOT NULL,
              brand TEXT NOT NULL,
              images TEXT NOT NULL)''')
conn.commit()

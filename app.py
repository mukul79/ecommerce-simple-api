from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)


@app.route("/")
def hello():
    return jsonify({"message": "Welcome to the API"})


@app.route("/insert", methods=["POST"])
def insert():
    data = request.get_json(force=True)
    name = data["name"]
    category = data["category"]
    brand = data["brand"]
    images = data["images"]
    conn = sqlite3.connect("products.db")
    c = conn.cursor()
    c.execute(
        f"INSERT INTO products(name,category,brand,images) values(?,?,?,?)", (name, category, brand, str(images))
    )
    conn.commit()
    return jsonify({"message": "Insertion done"})


@app.route("/update", methods=["POST"])
def update():
    data = request.get_json(force=True)
    id = data["id"]
    name = data["name"]
    category = data["category"]
    brand = data["brand"]
    images = data["images"]
    conn = sqlite3.connect("products.db")
    c = conn.cursor()
    c.execute(
        """UPDATE products 
        SET name = ?,brand = ?,  category = ?, images = ? 
        WHERE id = ?""",
        (name, brand, category, str(images), id),
    )
    conn.commit()
    return jsonify({"message": "Update done"})


@app.route("/delete/<id>", methods=["DELETE"])
def delete(id):
    data = request.get_json(force=True)
    # id = data['id']
    conn = sqlite3.connect("products.db")
    c = conn.cursor()
    c.execute(f"DELETE from products WHERE id = {id}")
    conn.commit()
    return jsonify({"message": f"Deletion done for id = {id}"})


@app.route("/listall", methods=["GET"])
def list_all():
    conn = sqlite3.connect("products.db")
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    rows = c.fetchall()
    conn.close()
    result = []
    for row in rows:
        result.append(
            {
                "name": row[0],
                "category": row[1],
                "brand": row[2],
                "images": row[3],
            }
        )
    return jsonify({"result": result})


@app.route("/filter", methods=["POST"])
def filter():
    data = request.get_json(force=True)
    # print(data)
    id = data.get("id", None)
    name = data.get("name", None)
    category = data.get("category", None)
    brand = data.get("brand", None)
    conn = sqlite3.connect("products.db")
    c = conn.cursor()
    c.execute("SELECT * FROM products")

    if id:
        c.execute(f"SELECT * FROM products where id = {id}")

    elif name and not category and not brand:
        c.execute("SELECT * FROM products WHERE name = ?", (name,))

    elif not name and category and not brand:
        c.execute("SELECT * FROM products WHERE category = ?", (category,))

    elif not name and not category and brand:
        c.execute("SELECT * FROM products WHERE brand = ?", (brand,))

    elif name and category and not brand:
        c.execute("SELECT * FROM products WHERE name = ? AND category", (name, category))

    elif name and not category and brand:
        c.execute("SELECT * FROM products WHERE name = ? AND brand = ?", (name, brand))

    elif not name and category and brand:
        c.execute("SELECT * FROM products WHERE category = ? AND brand = ?", (name, brand))

    elif name and category and brand:
        c.execute("SELECT * FROM products WHERE name = ? AND category = ? AND brand = ?", (name, category, brand))

    rows = c.fetchall()
    conn.close()

    result = []
    for row in rows:
        result.append(
            {
                "name": row[0],
                "category": row[1],
                "brand": row[2],
                "images": row[3],
            }
        )

    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(debug=True)

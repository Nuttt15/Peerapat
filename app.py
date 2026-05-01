from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# connect database
def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# หน้าแรก (แสดงเค้ก + category)
@app.route('/')
def index():
    conn = get_db()
    cakes = conn.execute('''
        SELECT cakes.*, categories.name as category_name
        FROM cakes
        LEFT JOIN categories ON cakes.category_id = categories.id
    ''').fetchall()
    conn.close()
    return render_template('cakemenu.html', cakes=cakes)

# เพิ่มสินค้า
@app.route('/add', methods=['GET', 'POST'])
def add():
    conn = get_db()
    categories = conn.execute('SELECT * FROM categories').fetchall()

    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        image = request.form['image']
        stock = request.form['stock']
        category_id = request.form['category_id']

        conn.execute('''
            INSERT INTO cakes (name, price, image, stock, category_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, price, image, stock, category_id))

        conn.commit()
        conn.close()
        return redirect('/')

    return render_template('add.html', categories=categories)

# แก้ไขสินค้า
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db()
    cake = conn.execute('SELECT * FROM cakes WHERE id = ?', (id,)).fetchone()
    categories = conn.execute('SELECT * FROM categories').fetchall()

    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        image = request.form['image']
        stock = request.form['stock']
        category_id = request.form['category_id']

        conn.execute('''
            UPDATE cakes
            SET name=?, price=?, image=?, stock=?, category_id=?
            WHERE id=?
        ''', (name, price, image, stock, category_id, id))

        conn.commit()
        conn.close()
        return redirect('/')

    return render_template('edit.html', cake=cake, categories=categories)

# ลบสินค้า
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db()
    conn.execute('DELETE FROM cakes WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

# run app
if __name__ == '__main__':
    app.run(debug=True)
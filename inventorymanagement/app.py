from flask import Flask, render_template, request, redirect
import sqlite3



app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('inventory.db')
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_db_connection()
    conn.execute(
        'CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, quantity INTEGER NOT NULL)'
    )
    conn.commit()
    conn.close()

@app.route('/')
def home():
        conn = get_db_connection()
        items = conn.execute('SELECT * FROM items').fetchall()
        conn.close()
        return render_template('index.html', items=items)


@app.route('/add', methods=['POST'])
def add_item():
    name = request.form['name']
    quantity = request.form['quantity']
    conn = get_db_connection()
    conn.execute('INSERT INTO items (name, quantity) VALUES (?, ?)', (name, quantity))
    conn.commit()
    conn.close()
    return redirect('/')


@app.route('/delete/<int:id>')
def delete_item(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM items WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')


if __name__ == '__app__':
    create_table()
    app.run(debug=True)







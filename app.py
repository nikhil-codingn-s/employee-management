from flask import Flask, render_template, request, redirect, url_for
from flask import g
import sqlite3

app = Flask(__name__)
DATABASE = "employees.db"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''CREATE TABLE IF NOT EXISTS employee (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT NOT NULL,
                      email TEXT,
                      role TEXT)''')
        db.commit()

@app.route('/')
def index():
    db = get_db()
    cur = db.execute("SELECT id, name, email, role FROM employee")
    employees = cur.fetchall()
    return render_template('index.html', employees=employees)

@app.route('/add', methods=['GET','POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        role = request.form['role']
        db = get_db()
        db.execute("INSERT INTO employee (name,email,role) VALUES (?,?,?)", (name, email, role))
        db.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)


from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ✅ Update this connection string according to your MySQL container setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@db/employee_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ✅ Employee model (matching your form)
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

# ✅ Home page
@app.route('/')
def index():
    employees = Employee.query.all()
    return render_template('index.html', employees=employees)

# ✅ Add employee page
@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        department = request.form.get('department')
        role = request.form.get('role')

        # Validation
        if not name or not email or not department or not role:
            flash("All fields are required!")
            return redirect(url_for('add_employee'))

        new_employee = Employee(name=name, email=email, department=department, role=role)
        db.session.add(new_employee)
        db.session.commit()
        flash("Employee added successfully!")
        return redirect(url_for('index'))

    return render_template('add.html')

# ✅ Delete employee
@app.route('/delete/<int:id>')
def delete_employee(id):
    employee = Employee.query.get(id)
    if employee:
        db.session.delete(employee)
        db.session.commit()
        flash("Employee deleted successfully!")
    else:
        flash("Employee not found!")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


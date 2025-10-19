from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ✅ Database connection (update password if needed)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Nikhil@em-mysql/employees'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ✅ Define Employee Model
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# ✅ Create tables automatically
with app.app_context():
    db.create_all()

# ✅ Home page (list employees)
@app.route('/')
def index():
    employees = Employee.query.all()
    return render_template('index.html', employees=employees)

# ✅ Add employee
@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form.get('name')
        role = request.form.get('role')
        salary = request.form.get('salary')
        email = request.form.get('email')

        # Check if all fields are filled
        if not (name and role and salary and email):
            return "All fields are required!", 400

        new_employee = Employee(name=name, role=role, salary=float(salary), email=email)
        db.session.add(new_employee)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add.html')

# ✅ Delete employee
@app.route('/delete/<int:id>')
def delete_employee(id):
    employee = Employee.query.get(id)
    if employee:
        db.session.delete(employee)
        db.session.commit()
    return redirect(url_for('index'))

# ✅ Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


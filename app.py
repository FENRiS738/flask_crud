from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "myraid@738#"

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:root@127.0.0.1:3306/flask"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Data Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

# Apis

@app.route('/')
def index():
    all_data = User.query.all()
    return render_template('home.html', users=all_data)


@app.route('/addUser', methods=['POST'])
def addUser():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        data = User(name, email, phone)
        db.session.add(data)
        db.session.commit()

        flash("User added successfully!")
        
        return redirect(url_for('index'))


@app.route('/updateUser',methods=['GET','POST'])
def updateUser():
    if request.method == "POST":
        data = User.query.get(request.form.get('id'))

        data.name = request.form['name']
        data.email = request.form['email']
        data.phone = request.form['phone']

        db.session.commit()

        flash("User updated successfully!")
        return redirect(url_for('index'))
    

@app.route('/deleteUser/<id>', methods=['GET','POST'])
def deleteUser(id: int):
    data = User.query.get(id)
    
    db.session.delete(data)
    db.session.commit()

    flash('User deleted successfully!')

    return redirect(url_for('index'))

from flask import render_template, redirect, session,request
from flask_app.models.user import User
from flask import flash
from flask_app import app
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return redirect('/user/LoginRegister')

@app.route('/user/LoginRegister')
def creation():
    return render_template("LoginAndRegister.html")

@app.route('/user/login', methods=['POST'])
def loging():
    if not User.validate_login(request.form):
        return redirect('/user/LoginRegister')
    session["user_id"]=User.find_by_email(request.form).id
    return redirect('/car/dashboard')
    
@app.route('/user/register', methods=['POST'])
def registering():
    if not User.validate_register(request.form):
        return redirect('/user/LoginRegister')
    data= {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    session["user_id"]=User.create_account(data)
    return redirect('/car/dashboard')
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/user/LoginRegister')
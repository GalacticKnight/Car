from flask import render_template, redirect, session, request
from flask_app import app 
from flask_app.models.user import User
from flask_app.models.car import Car
from flask import flash

@app.route('/car/dashboard')
def dashboard():
    data=User.find_by_id({"id":session["user_id"]})
    retreiving_all_cars =Car.get_all()
    return render_template('dashboard.html',user=data, cars =retreiving_all_cars)

@app.route('/cars/create')
def add_car():
    return render_template("add_car.html")


@app.route('/cars/add_car',methods=["POST"])
def adding_car():
    if not Car.validate_car(request.form):
        return redirect('/cars/create')
    Car.save(request.form)
    return redirect("/car/dashboard")


@app.route('/cars/view_car/<int:id>')
def view_car(id):
    car_info= Car.find_by_id({"id":id})
    you = User.find_by_id({"id":session["user_id"]})
    return render_template("view_car.html",cars=car_info, users=you)


@app.route('/cars/edit_car/<int:id>')
def edit_car(id):
    car_info= Car.find_by_id({"id":id})
    you = User.find_by_id({"id":session["user_id"]})
    return render_template("edit_car.html",cars=car_info, users=you)


@app.route('/cars/editing_car',methods=["POST"])
def editing_car():
    print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",request.form)
    if not Car.validate_car(request.form):
        return redirect(f'/cars/edit_car/{request.form["id"]}')
    Car.update(request.form)

    return redirect("/car/dashboard")


@app.route('/cars/delete/<int:id>')
def delete_car(id):
    
    Car.delete({"id":id})
    return redirect("/car/dashboard")
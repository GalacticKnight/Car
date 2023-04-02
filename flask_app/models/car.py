from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
from flask_app.models.user import User
import re

class Car:
    database="carstest_db"
    def __init__(self, data):
        self.id = data['id']
        self.price = data['price']
        self.model = data['model']
        self.make = data['make']
        self.year = data['year']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']#!!!!!!!!!!!!very important
        self.creator = None

    @staticmethod
    def validate_car(data):#apparently if this doesnt work, just restart the entire system and try again, if it still doesnt work, i can demonstrate.
        is_valid = True 
        if int(data['price']) == 0:#the only reason why its 0 is because i set it so that you cannot have less than 0
            flash("You giving a car for fee or for free?")
            is_valid = False
        if len(data['model']) < 3:
            flash("At least 3 characters.")
            is_data = False
        if len(data['make']) < 3:
            flash("At least 3 characters.")
            is_valid = False
        if int(data['year']) == 0:#the only reason why its 0 is because i set it so that you cannot have less than 0
            flash("I don't think cars were made back then.")
            is_valid = False
        if len(data['description']) < 3:
            flash("Please elaborate more")
            is_valid = False
        return is_valid

    
    @classmethod
    def save(cls,data):#you need user_id!!!!!!
        query = '''INSERT INTO cars 
        (price, model, make, year, description, users_id) 
        VALUES 
        (%(price)s, %(model)s, %(make)s,%(year)s,%(description)s, %(users_id)s);'''
        print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
        #you cannot assume, you HAVE TO HAVE AN ID TO LOCATIE WHERE YOU WANT TO PUT IN THE TABLE
        return connectToMySQL(cls.database).query_db(query,data)

    @classmethod
    def update(cls,data):#you need user_id!!!!!!
        query = '''UPDATE cars SET 
        id =(%(id)s),
        price = (%(price)s),
        model = (%(model)s),
        make = (%(make)s),
        year = (%(year)s),
        description = (%(description)s)
        where id= %(id)s;'''
        return connectToMySQL(cls.database).query_db(query,data)


    @classmethod
    def delete(cls,data):
        query = '''DELETE FROM cars WHERE ID = %(id)s;'''#??????????????????????
        results = connectToMySQL(cls.database).query_db(query,data)


    @classmethod
    def find_by_id(cls, data):
        query='''SELECT * FROM cars LEFT JOIN users on users.id = cars.users_id WHERE cars.id= %(id)s'''#!!!!!!!!!!!
        results = connectToMySQL(cls.database).query_db(query,data)
        print(results)
        r = cls(results[0])
        u = {
            "id": results[0]["users.id"],
            "first_name":results[0]["first_name"],
            "last_name":results[0]["last_name"],
            "email":results[0]["email"],
            "password":results[0]["password"],
            "created_at":results[0]["users.created_at"],
            "updated_at":results[0]["users.updated_at"]
        }
        print(results)
        r.creator=User(u)#
        return r

    @classmethod
    def get_all(cls):#the goal of this
        query = '''SELECT * FROM cars
        LEFT JOIN users on users.id = cars.users_id;'''
        results = connectToMySQL(cls.database).query_db(query)
        print(results)
        lst =[]
        for i in results:
            r = cls(i)
            u = {
                "id": i["users.id"],
                "first_name":i["first_name"],
                "last_name":i["last_name"],
                "email":i["email"],
                "password":i["password"],
                "created_at":i["users.created_at"],
                "updated_at":i["users.updated_at"]
            }
            r.creator=User(u)#
            lst.append(r)
        print("lst",lst)
        return lst

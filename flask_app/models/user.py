from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash#incorperates the idea of an error alert when there is a mistake like catch and exception
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
from flask_app import app
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

class User:
    database="carstest_db"#this is the schema!!!!!!
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email= data['email']
        self.password= data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_account(cls,data):
        query='''INSERT into users (first_name, last_name,email, password)
        VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);'''
        results = connectToMySQL(cls.database).query_db(query,data)
        return results

    #come back here
    @classmethod
    def find_by_id(cls, data):
        query='''SELECT * FROM users WHERE id= %(id)s'''
        results = connectToMySQL(cls.database).query_db(query,data)
        print(results)
        return cls(results[0])

    @classmethod
    def find_by_email(cls, data):
        query='''SELECT * FROM users WHERE email= %(email)s'''
        results = connectToMySQL(cls.database).query_db(query,data)
        print(results)
        return cls(results[0])

    @staticmethod
    def validate_register(data):#done
        is_valid = True 
        query='''SELECT * FROM users WHERE email= %(email)s'''
        results = connectToMySQL(User.database).query_db(query,data)
        if len(results) >= 1:
            flash("this email is already taken","register")
            is_valid = False
        if len(data['first_name']) < 3:
            flash("At least 3 characters.","register")
            is_valid = False
        if len(data['last_name']) < 3:
            flash("At least 3 characters.","register")
            is_data = False
        if not EMAIL_REGEX.match(data['email']):#this is important!!!!!!!!
            flash("invalid email","register")
            is_data = False
        if len(data['password']) < 8:
            flash("Must have more than 8 characters.","register")
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash("Must confirm your password correctly.","register")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(data):#done
        is_valid = True 
        query='''SELECT * FROM users WHERE email= %(email)s'''
        results = connectToMySQL(User.database).query_db(query,data)
        if results:
            found= User(results[0])
            if not bcrypt.check_password_hash(found.password, data['password']):
                flash("hash password does not match")
                is_valid=False
        else:
            flash("we havent found a match","login")
            is_valid = False
        return is_valid

    @classmethod
    def get_all(cls):#done
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.database).query_db(query)
        results = []
        for i in results:
            users.append(cls(i))
        return users
import sqlite3
from flask import request
from flask_restful import Resource
from models.user import UserModel

class UserRegister(Resource):   
    def post(self):
        login_data = request.get_json()

        if UserModel.get_user_by_username(login_data['username']):
            return {'message': 'A user with username ' + login_data['username'] + ' already exists'}
        
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "INSERT INTO users VALUES(NULL,?,?)"
        cursor.execute(query,(login_data['username'],login_data['password']))
        
        connection.commit()

        query = "SELECT * FROM users WHERE username=?"
        cursor.execute(query,(login_data['username'],))

        row = cursor.fetchone()
        if row:
            return {'message': 'username' + row[1]}
        else:
            None
        
        connection.close()


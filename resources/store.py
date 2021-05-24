import sqlite3
from flask import Flask, request
from flask_restful import Resource
from flask_jwt import jwt_required
from models.store import StoreModel


class Store(Resource):
    @jwt_required()
    def get(self,name):
        store =  StoreModel.find_store_by_name(name)
        if store:
            return store.json()
        else:
            return {'message': 'store not found'}, 404
    
    @jwt_required()       
    def post(self,name):
        if StoreModel.find_store_by_name(name):
            return {'message': 'Store already present'}

        #store_data = request.get_json()
        
        store = StoreModel(name)
        
        store.save_to_db()
        return {'message': 'item added successfully'}

    def delete(self,name):
        store = StoreModel.find_store_by_name(name)
        if store:
            store.delete_from_db()
            return {'message': 'store deleted successful'}
        else:
            return {'message': 'store not found'}
        
            
class StoreList(Resource):
    def get(self):
        store_list = StoreModel.query.all()
        return {'store': [each_store.json() for each_store in store_list]}
                

import sqlite3
from flask import Flask, request
from flask_restful import Resource
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    @jwt_required()
    def get(self,name):
        item =  ItemModel.find_item_by_name(name)
        if item:
            return item.json()
        else:
            return {'message': 'item not found'}, 404
    
    @jwt_required()       
    def post(self,name):
        if ItemModel.find_item_by_name(name):
            return {'message': 'item already present'}

        item_data = request.get_json()
        
        item = ItemModel(name, item_data['price'], item_data['store_id'])
        
        item.save_to_db()
        return {'message': 'item added successfully'}

    def delete(self,name):
        item = ItemModel.find_item_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'item deleted successful'}
        else:
            return {'message': 'item not found'}
        
    def put(self,name):
        item_data = request.get_json()
    
        item = ItemModel.find_item_by_name(name)

        if item:
            item.price = item_data['price']
            item.store_id = item_data['store_id']
        else:
            item = ItemModel(name, item_data['price'], item_data['store_id'])

        item.save_to_db()
        return {'message': 'changes saved successfully'}
        
            
class ItemList(Resource):
    def get(self):
        item_list = ItemModel.query.all()
        return {'item': [each_item.json() for each_item in item_list]}
                

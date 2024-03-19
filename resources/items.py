import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

from models  import ItemModel
from schemas import ItemScheme, ItemUpdateScheme

#Creo un blueprint
blp = Blueprint('Items', __name__, description='Operations on items')


#Cada decorador es una ruta
#Ruta items
@blp.route("/items")
class Items(MethodView):
    @blp.response(201, ItemScheme(many=True))
    def get(self):
        items = ItemModel.query.all()
        return items

    @jwt_required()
    @blp.arguments(ItemScheme)
    @blp.response(200, ItemScheme)
    def post(self, item_data):
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:

            abort(500, message="An error ocurred inserting the item")

        return item


#Ruta items lista
@blp.route("/items/<string:item_id>")
class ItemsList(MethodView):
    @blp.response(201, ItemScheme)
    def get(self, item_id):
        item = ItemModel.query.get(item_id)
        return item

    @blp.arguments(ItemUpdateScheme)
    @blp.response(201, ItemScheme)
    def put(self, item_data, item_id):
        item = ItemModel.query.get_or_404(item_id)

        if item:
            item.price = item_data['price']
            item.name = item_data['name']
        else:
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()

        return item
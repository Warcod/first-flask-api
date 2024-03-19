import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreScheme, StoreupdateScheme
from db import db
from models import StoresModel, ItemModel, TagModel, items_tags
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


blp = Blueprint('Stores', __name__, description='Operations on stores')


@blp.route("/store")
class Stores(MethodView):
    @blp.response(201, StoreScheme(many=True))
    def get(self):
        stores = StoresModel.query.all()
        return stores

    @blp.arguments(StoreScheme)
    @blp.response(201, StoreScheme)
    def post(self, store_data):
        store = StoresModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        
        except IntegrityError:
            abort(400, message="A store whit that name already exist")

        except SQLAlchemyError:

            abort(500, message="An error ocurred inserting the store")

        return store


@blp.route("/store/<string:store_id>")
class Storeslist(MethodView):
    @blp.response(201, StoreScheme)
    def get(self, store_id):
        store = StoresModel.query.get_or_404(store_id)
        return store
    
    @blp.arguments(StoreupdateScheme)
    @blp.response(201, StoreScheme)
    def put(self, store_data ,store_id):
        store = StoresModel.query.get(store_id)

        if store:
            store.name = store_data['name']
        else:
            store = StoresModel(id=store_id, **store_data)

        db.session.add(store)
        db.session.commit()

        return store

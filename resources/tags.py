from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from db import db
from models import TagModel, StoresModel, ItemModel
from schemas import TagScheme, ItemTagScheme


blp = Blueprint("Tags", "tags", description="Operations on tags")


@blp.route("/store/<string:store_id>/tags")
class Tag(MethodView):
    
    @blp.response(200, TagScheme(many=True))
    def get(self, store_id):
        store = StoresModel.query.get_or_404(store_id)
        return store.tags.all()
    
    @blp.arguments(TagScheme)
    @blp.response(201, TagScheme)
    def post(self, tag_data, store_id):

        tag = TagModel(**tag_data, store_id = store_id)

        try:
            db.session.add(tag)
            db.session.commit()

        except IntegrityError:
            abort(400, message="A tag whit that name already exist")

        except SQLAlchemyError:
            abort(500, message="An error ocurred inserting the tag")

        return tag


@blp.route("/tag/<string:tag_id>")
class Taglist(MethodView):  
    @blp.response(200, TagScheme(many=True))
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    

@blp.route("/item/<string:item_id>/tags/<string:tag_id>")
class LinkTagToItem(MethodView):

    @blp.response(200, TagScheme)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.append(tag)
        try:
            db.session.add(item)
            db.session.commit()

        except SQLAlchemyError:
            abort(500, message="An error ocurred while inserting the tag.")
    
        return tag

    
    @blp.response(200, ItemTagScheme)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)
        try:
            db.session.add(item)
            db.session.commit()

        except SQLAlchemyError:
            abort(500, message="An error ocurred while unlinking the tag.")

        return {"message": "Item removed from tag", "item" : item, "tag": tag}
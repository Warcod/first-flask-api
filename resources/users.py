from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token

from db import db
from models import UserModel
from schemas import UserScheme


blp = Blueprint("Users", __name__, description="Endpoint to interact whit creation and login users")


@blp.route("/users/<int:user_id>")
class Users(MethodView):

    @blp.response(200, UserScheme)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user
    
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)

        db.session.delete(user)
        db.session.commit()
        
        return {"message" : "The users has been deleted"}

@blp.route("/register")
class UserRegister(MethodView):

    @blp.arguments(UserScheme)
    @blp.response(200, UserScheme)
    def post(self, user_info):
        user = UserModel(
            username = user_info["username"],
            password= pbkdf2_sha256.hash(user_info["password"])
        )
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:

            abort(400, message="A user whit that username already exist")

        except SQLAlchemyError:

            abort(500, message="An error ocurred registering the user")

        return user
    

@blp.route("/login")
class UserLogin(MethodView):
        
    @blp.arguments(UserScheme)
    def post(self, login_info):
        user = UserModel.query.filter(
            UserModel.username == login_info['username']
        ).first()

        if user and pbkdf2_sha256.verify(login_info["password"], user.password):
            acces_token = create_access_token(identity=user.id)

            return {"acces_token": acces_token}
        
        abort(401, message="Credentials are invalid")
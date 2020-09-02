from flask import make_response, jsonify, request
from flask_restful import Resource
from application.api.users.User import User


class UserController(Resource):
    def get(self):
        # users = User.query.all()
        users = [
            {
                "username": "ncthanh",
                "email": "ncthanh@gmail.com"
            }
        ]
        return make_response(
            jsonify(users), 200
        )

    def post(self):
        new_user = User(
            username=request.json["username"],
            email=request.json["email"],
            password=request.json["password"]
        )
        User.save(new_user)


#!/usr/bin/python3
""" USERS Module """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_users():
    """ Function that retrieves all users objects """
    return jsonify(
        [item.to_dict() for item in storage.all(User).values()]
    )


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    """ Function that retrieves a specific user object """
    user = storage.get(User, user_id)
    return jsonify(user.to_dict()) if user is not None else abort(404)


@app_views.route(
    "/users/<user_id>", methods=["DELETE"], strict_slashes=False
)
def delete_user(user_id):
    """ Function that deletes a instance of a user object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """ Function that creates a user """
    kwargs = request.get_json()
    if kwargs is None:
        abort(400, "Not a JSON")
    if "email" not in kwargs:
        abort(400, "Missing email")
    if "password" not in kwargs:
        abort(400, "Missing password")
    new_user = User(**kwargs)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """ Function that updates a specific user object """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    kwargs = request.get_json()
    if kwargs is None:
        abort(400, "Not a JSON")
    for key, value in kwargs.items():
        if key not in ["id", "created_at", "updated_at", "email"]:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200

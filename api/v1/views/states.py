#!/usr/bin/python3
""" States Module """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states():
    """ Function that retrieves all states objects """
    return jsonify(
        [item.to_dict() for item in storage.all().values()]
    )


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state(state_id):
    """ Function that retrieves a specific state object """
    state = storage.get(State, state_id)
    return jsonify(state.to_dict()) if state is not None else abort(404)


@app_views.route(
    "/states/<state_id>", methods=["DELETE"], strict_slashes=False
)
def delete_state(state_id):
    """ Function that deletes a instance of a state object """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """ Function that creates a state """
    kwargs = request.get_json()
    if kwargs is None:
        abort(400, "Not a JSON")
    if "name" not in kwargs:
        abort(400, "Missing name")
    new_state = State(**kwargs)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """ Function that updates a specific state object """
    state = storage.get(State, state_id)
    if state_id is None:
        abort(404)
    kwargs = request.get_json()
    if kwargs is None:
        abort(400, "Not a JSON")
    for key, value in kwargs.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200

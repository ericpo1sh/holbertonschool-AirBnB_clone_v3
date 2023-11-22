#!/usr/bin/python3
""" Calls States API module"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=["GET"], strict_slashes=False)
def state_getter():
    """ List all of objects in the class State """
    list_states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(list_states)


@app_views.route('/states/<id>', methods=["GET"], strict_slashes=False)
def specific_state_getter(id):
    """ Gets the data of a specific state from the ID Given """
    specific_state = storage.get(State, id)
    if specific_state is None:
        abort(404)
    return jsonify(specific_state.to_dict())


@app_views.route('/states/<id>', methods=["DELETE"], strict_slashes=False)
def delete_state(id):
    """ Destroys a specific State object with the ID given, returns 404 error
    if id does not exist, else return 200 """
    specific_state = storage.get(State, id)
    if specific_state is None:
        abort(404)
    storage.delete(specific_state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/', methods=["POST"], strict_slashes=False)
def create_state():
    """ Create a new state via post using a JSON input, 400 error if not json
     or if dictionary does not contain name """
    get_dict = request.get_json(silent=True)
    if get_dict is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in get_dict.keys() or get_dict["name"] is None:
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_state = State(**get_dict)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route("states/<id>", methods=["PUT"], strict_slashes=False)
def update_state(id):
    """ Updates a specific State object """
    get_dict = request.get_json(silent=True)
    if get_dict is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    specific_state = storage.get(State, id)
    if specific_state is None:
        abort(404)
    ignore_list = ["id", "created_at", "updated_at"]
    for key, value in get_dict.items():
        if key in ignore_list:
            continue
        setattr(specific_state, key, value)
    storage.save()
    return make_response(jsonify(specific_state.to_dict()), 200)

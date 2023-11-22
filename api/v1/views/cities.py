#!/usr/bin/python3
""" City API Calls module"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def get_state_cities(state_id):
    """ Gets all City objects from a given state of id <state_id>: returns
    as a json. 404 Error if incorrect state """
    specific_state = storage.get(State, state_id)
    if specific_state is None:
        abort(404)
    list_cities = [city.to_dict() for city in storage.all(
        City).values() if city.state_id == state_id]
    return jsonify(list_cities)


@app_views.route("/cities/<city_id>", methods=["GET"],
                 strict_slashes=False)
def get_specific_city(city_id):
    """ Takes a specific city id and returns the json information of that city
    object. 404 Error if not found """
    specific_city = storage.get(City, city_id)
    if specific_city is None:
        abort(404)
    return jsonify(specific_city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_specific_city(city_id):
    """Deletes a City object if a correct ID is given,
    404 error if not. """
    specific_city = storage.get(City, city_id)
    if specific_city is None:
        abort(404)
    storage.delete(specific_city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states/<state_id>/cities",
                 methods=["Post"], strict_slashes=False)
def create_city(state_id):
    """ Create city using a JSON input """
    get_dict = request.get_json(silent=True)
    if get_dict is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in get_dict.keys() or get_dict["name"] is None:
        return make_response(jsonify({"error": "Missing name"}), 400)
    specific_state = storage.get(State, state_id)
    if specific_state is None:
        abort(404)
    get_dict["state_id"] = state_id
    new_city = City(**get_dict)
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """ Update the City object """
    get_dict = request.get_json(silent=True)
    if get_dict is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    specific_city = storage.get(City, city_id)
    if specific_city is None:
        abort(404)
    ignore_list = ["id", "state_id", "updated_at", "created_at"]
    for key, value in get_dict.items():
        if key in ignore_list:
            continue
        setattr(specific_city, key, value)
    storage.save()
    return make_response(jsonify(specific_city.to_dict()), 200)

#!/usr/bin/python3
""" Cities Module """
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models import storage
from models.city import City
from models.state import State


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city(city_id):
    """ Function that retrieves a specific state object """
    city = storage.get(City, city_id)
    return jsonify(city.to_dict()) if city is not None else abort(404)


@app_views.route("/states/<state_id>/cities",
                 methods=["GET"],
                 strict_slashes=False)
def get_state_cities(state_id):
    """ Function that returns all cities in a specific state object """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    list_cities = [city.to_dict() for city in storage.all(
        City).values() if city.state_id == state_id]
    return jsonify(list_cities)


@app_views.route(
    "/cities/<city_id>", methods=["DELETE"], strict_slashes=False
)
def delete_city(city_id):
    """ Function that deletes a instance of a city object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities",
                 methods=["Post"], strict_slashes=False)
def create_city(state_id):
    """ Create city using a JSON input"""
    get_dict = request.get_json(silent=True)
    if get_dict is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in get_dict.keys() or get_dict["name"] is None:
        return make_response(jsonify({"error": "Missing name"}), 400)
    specific_state = storage.get(State, state_id)
    if specific_state is None:
        abort(404)
    get_dict[state_id] = state_id
    new_city = City(**get_dict)
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """ Function that updates a specific city object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    kwargs = request.get_json()
    if kwargs is None:
        abort(400, "Not a JSON")
    for key, value in kwargs.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200

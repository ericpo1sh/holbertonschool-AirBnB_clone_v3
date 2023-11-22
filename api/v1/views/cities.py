#!/usr/bin/python3
""" Cities Module """
from api.v1.views import app_views
from flask import abort, jsonify, request
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
                 methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """ Function that creates a city """
    kwargs = request.get_json()
    if kwargs is None:
        abort(400, "Not a JSON")
    if "name" not in kwargs.keys():
        abort(400, "Missing name")
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    kwargs[state_id] = state_id
    new_city = City(**kwargs)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


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

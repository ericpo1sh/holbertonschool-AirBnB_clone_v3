#!/usr/bin/python3
""" Cities Module """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route(
        "/states/<state_id>/cities",
        methods=["GET"],
        strict_slashes=False
)
def get_cities(state_id):
    """ Function that retrieves all city objects linked to state_id """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        return jsonify([city.to_dict() for city in state.cities])


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city(city_id):
    """ Function that retrieves a specific city object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        return jsonify(city.to_dict())


@app_views.route(
    "/cities/<city_id>", methods=["DELETE"], strict_slashes=False
)
def delete_city(city_id):
    """ Function that deletes a instance of a city object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route(
        "/states/<state_id>/cities", methods=["POST"], strict_slashes=False
)
def create_city(state_id):
    """ Function that creates a new city """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    kwargs = request.get_json(silent=True)
    if kwargs is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in kwargs:
        return make_response(jsonify({"error": "Missing name"}), 400)
    else:
        new_city = City(**kwargs)
        new_city.state_id = state_id
        new_city.save()
        return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """ Function that updates a specific state object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    kwargs = request.get_json()
    if kwargs is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    else:
        for key, value in kwargs.items():
            if key not in ["id", "created_at", "updated_at", "state_id"]:
                setattr(city, key, value)
        storage.save()
        return make_response(jsonify(city.to_dict()), 200)

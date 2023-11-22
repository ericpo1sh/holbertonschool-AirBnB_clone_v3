#!/usr/bin/python3tate
""" Places Module """
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("/cities/<city_id>/places",
                 methods=["GET"],
                 strict_slashes=False)
def get_place_by_city(city_id):
    """ Function that retrieves a specific place object by city_id """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route("/places/<place_id>",
                 methods=["GET"],
                 strict_slashes=False)
def get_place(place_id):
    """ Function that returns all cities in a specific place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route(
    "/places/<place_id>", methods=["DELETE"], strict_slashes=False
)
def delete_place(place_id):
    """ Function that deletes a instance of a place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places",
                 methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    """ Function that creates a new place """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    kwargs = request.get_json()
    if kwargs is None:
        abort(400, "Not a JSON")
    if "user_id" not in kwargs:
        abort(400, "Missing user_id")
    if storage.get(User, kwargs["user_id"]) is None:
        abort(404)
    if "name" not in kwargs:
        abort(400, "Missing name")
    new_place = Place(**kwargs)
    new_place[city_id] = city_id
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """ Function that updates a specific place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    kwargs = request.get_json()
    if kwargs is None:
        abort(400, "Not a JSON")
    for key, value in kwargs.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200

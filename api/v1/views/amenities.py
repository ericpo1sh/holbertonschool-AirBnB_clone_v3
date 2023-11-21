#!/usr/bin/python3
""" Amenity Module """
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenities():
    """ Function that retrieves all amenitiy objects """
    return jsonify(
        [item.to_dict() for item in storage.all().values()]
    )


@app_views.route("/amenities/<amenity_id>",
                 methods=["GET"],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """ Function that retrieves a specific samenity object """
    amenity = storage.get(Amenity, amenity_id)
    return jsonify(amenity.to_dict()) if amenity is not None else abort(404)


@app_views.route(
    "/amenities/<amenity_id>", methods=["DELETE"], strict_slashes=False
)
def delete_amenity(amenity_id):
    """ Function that deletes a instance of a amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """ Function that creates a new amenity """
    kwargs = request.get_json()
    if kwargs is None:
        abort(400, "Not a JSON")
    if "name" not in kwargs:
        abort(400, "Missing name")
    new_amenity = Amenity(**kwargs)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>",
                 methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ Function that updates a specific amenity object """
    amenities = storage.get(Amenity, amenity_id)
    if amenities is None:
        abort(404)
    kwargs = request.get_json()
    if kwargs is None:
        abort(400, "Not a JSON")
    for key, value in kwargs.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenities, key, value)
    storage.save()
    return jsonify(amenities.to_dict()), 200

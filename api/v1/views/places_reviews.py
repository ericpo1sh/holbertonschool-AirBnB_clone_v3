#!/usr/bin/python3
""" Reviews Module """
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/places/<place_id>/reviews",
                 methods=["GET"],
                 strict_slashes=False)
def get_review_by_place(place_id):
    """ Function that retrieves a specific review object by place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route("/reviews/<review_id>",
                 methods=["GET"],
                 strict_slashes=False)
def get_review(review_id):
    """ Function that returns all cities in a specific review object """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route(
    "/reviews/<review_id>", methods=["DELETE"], strict_slashes=False
)
def delete_review(review_id):
    """ Function that deletes a instance of a review object """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews",
                 methods=["POST"],
                 strict_slashes=False)
def create_review(place_id):
    """ Function that creates a new review """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    kwargs = request.get_json()
    if kwargs is None:
        abort(400, "Not a JSON")
    if "user_id" not in kwargs:
        abort(400, "Missing user_id")
    if storage.get(User, kwargs["user_id"]) is None:
        abort(404)
    if "text" not in kwargs:
        abort(400, "Missing text")
    kwargs["place_id"] = place_id
    new_review = Review(**kwargs)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """ Function that updates a specific review object """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    kwargs = request.get_json()
    if kwargs is None:
        abort(400, "Not a JSON")
    for key, value in kwargs.items():
        if key not in ["id",
                       "user_id",
                       "place_id",
                       "created_at",
                       "updated_at"]:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200

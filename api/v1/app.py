#!/usr/bin/python3
""" Flask App Module for Web """
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify
from os import environ
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def handle_404(e):
    """ Function that handles error 404 """
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown(exc):
    """ Function that removes the current SQLAlchemy session """
    storage.close()


if __name__ == "__main__":
    app.run(
        host=environ.get("HBNB_API_HOST", "0.0.0.0"),
        port=environ.get("HBNB_API_PORT", "5000"),
        threaded=True
    )

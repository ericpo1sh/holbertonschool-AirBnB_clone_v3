#!/usr/bin/python3
""" Init module """
from flask import Blueprint
from api.v1.views.index import * # NOQA
from api.v1.views.states import * # NOQA
from api.v1.views.cities import * # NOQA


app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

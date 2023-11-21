#!/usr/bin/python3
""" Init modules """
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.views.cities import * # NOQA
from api.v1.views.index import * # NOQA
from api.v1.views.states import * # NOQA
from api.v1.views.amenities import * # NOQA
from api.v1.views.users import * # NOQA
from api.v1.views.places import * # NOQA

from flask import Blueprint

recognition = Blueprint('recognition', __name__)

from . import views

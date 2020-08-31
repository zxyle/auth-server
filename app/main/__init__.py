from flask import Blueprint

main_blue = Blueprint('main', __name__)

from . import views, errors

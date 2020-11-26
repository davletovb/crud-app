from flask import Blueprint

stix = Blueprint('stix', __name__)

from . import views
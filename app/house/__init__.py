from flask import Blueprint
house = Blueprint('house', __name__)
from . import views,errors,forms


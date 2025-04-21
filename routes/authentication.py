from flask import Blueprint
from models import Users, Profile

auth = Blueprint('auth', __name__)

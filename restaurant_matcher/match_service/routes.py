'''
Registers url endpoints and maps it to classes in controllers
'''

from flask import Blueprint
from flask_restful import Api
from .controllers import Skeleton

match_service_blueprint = Blueprint('match_service', __name__, url_prefix='/match_service')
match_service_api = Api(match_service_blueprint)

match_service_api.add_resource(Skeleton, '/',endpoint="match_service")

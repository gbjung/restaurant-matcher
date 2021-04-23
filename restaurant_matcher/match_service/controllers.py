'''
Holds the main data logic for the match restaurant match api.
'''

from flask_restful import Resource, request
from .validators import MatchServiceSchema
from restaurant_matcher.data_management.data_manager import DataManager

class Skeleton(Resource):
    def __init__(self):
        self.schema = MatchServiceSchema()
        self.DataManager = DataManager('fixtures/cuisines.csv', 'fixtures/restaurants.csv')

    def get(self):
        errors = self.schema.validate(request.args)
        if errors:
            return errors

        return {'task': 'Say "Hello, World!"'}

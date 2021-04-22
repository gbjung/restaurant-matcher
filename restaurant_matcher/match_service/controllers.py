'''
Holds the main data logic for the match restaurant match api.
'''

from flask_restful import Resource, request
from .validators import MatchServiceSchema

class Skeleton(Resource):
    def __init__(self):
        self.schema = MatchServiceSchema()

    def get(self):
        print([a for a in request.args.keys()])
        errors = self.schema.validate(request.args)
        if errors:
            return errors

        return {'task': 'Say "Hello, World!"'}

'''
Holds the main data logic for the match restaurant match api.
'''

from flask_restful import Resource

class Skeleton(Resource):
    def get(self, id):
        return {'task': 'Say "Hello, World!"'}

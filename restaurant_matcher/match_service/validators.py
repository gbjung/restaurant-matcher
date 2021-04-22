'''
URL parameter validators
'''
from marshmallow import Schema, fields, validate

class MatchServiceSchema(Schema):
    '''
    Validates search parameters provided by the url parameters
    '''
    name = fields.Str(required=False)
    rating = fields.Int(required=False, validate=validate.Range(min=1, max=5))
    distance = fields.Int(required=False, validate=validate.Range(min=1, max=10))
    price = fields.Int(required=False, validate=validate.Range(min=10, max=50))
    cuisine = fields.Str(required=False)

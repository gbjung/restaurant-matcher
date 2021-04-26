'''
Holds the main data logic for the match restaurant match api.
'''

from flask_restful import Resource, request
from .validators import MatchServiceSchema
from restaurant_matcher.data_management.data_manager import DataManager

class Skeleton(Resource):
    def __init__(self):
        self.schema = MatchServiceSchema()
        self.data_manager = DataManager('fixtures/cuisines.csv', 'fixtures/restaurants.csv')

    def get(self):
        errors = self.schema.validate(request.args)

        if errors:
            return errors

        request_params = request.args.to_dict()
        matching_restaurants = self.return_relevant_restaurants(request_params)

        return matching_restaurants

    def return_relevant_restaurants(self, supplied_filters):
        '''
        Takes the given filter keys & values and applies them to return
        a list of relevant restaurants
        args:
            supplied_filters: dict, key val of api request params
        '''
        relevant_restaurants_ids = self.data_manager.return_filtered_results(supplied_filters)
        restaurants_data = self.data_manager.return_restaurant_information(relevant_restaurants_ids)

        return restaurants_data

'''
Acts as a querier to make sense of the csv data
'''
import json
from csv import DictReader

from .data_storage import DataStorage

class DataManager:

    def __init__(self, cuisine_csv_path, restaurant_csv_path):
        self.data_storage = DataStorage()
        # Setup data
        self.data_storage.ingest(cuisine_csv_path, restaurant_csv_path)

        self.param_key_to_store_map = {
            "rating": self.return_filtered_ratings,
            "distance": self.return_filtered_distances,
            "price": self.return_filtered_prices,
        }
        # ranking of importance of criterias
        self.match_importance = ["distance", "rating", "price"]

    def return_filtered_ratings(self, restaurant_ids=[], rating='1'):
        '''
        Returns the restaurant ids that match the given rating.
        Ordered from highest rating to lowest
        ie: rating = 3, order will be 5 -> 4 -> 3
        args:
            rating: str, rating value to match
            restaurant_ids: optional list[str], additional match param
        output:
            matching_restaurants: list[list], array of arrays of perserve hierarchy
        '''
        matching_restaurants = []
        max_rating = 5

        for rate in range(max_rating, int(rating)-1, -1):
            matched_restaurants = self.data_storage.ratings.get(str(rate))
            if matched_restaurants:
                if restaurant_ids:
                    filtered_ids = [id for id in matched_restaurants if id in restaurant_ids]
                    if filtered_ids:
                        matching_restaurants.append(filtered_ids)
                else:
                    matching_restaurants.append(matched_restaurants)

        return matching_restaurants

    def return_filtered_distances(self, restaurant_ids=[], distance='10'):
        '''
        Returns the restaurant ids that match the given distance.
        Ordered from most exact to additionally encompassing
        ie: distance = 2, order will be 2 -> 3 -> 4...
        args:
            distance: str, distance value to match
            restaurant_ids: optional list[str], additional match param
        output:
            matching_restaurants: list[list], array of arrays of perserve hierarchy
        '''
        matching_restaurants = []
        min_distance = 1

        for mile in range(min_distance, int(distance)+1):
            matched_restaurants = self.data_storage.distances.get(str(mile))
            if matched_restaurants:
                if restaurant_ids:
                    filtered_ids = [id for id in matched_restaurants if id in restaurant_ids]
                    if filtered_ids:
                        matching_restaurants.append(filtered_ids)
                else:
                    matching_restaurants.append(matched_restaurants)

        return matching_restaurants

    def return_filtered_prices(self, restaurant_ids=[], price='50'):
        '''
        Returns the restaurant ids that match the given price.
        Ordered from cheapest
        ie: price = 20, order will be 10 -> 15 -> 20
        args:
            price: str, price value to match
            restaurant_ids: optional list[str], additional match param
        output:
            matching_restaurants: list[list], array of arrays of perserve hierarchy
        '''
        matching_restaurants = []
        min_price = 10
        price_increase = 5

        for price in range(min_price, int(price)+1, price_increase):
            matched_restaurants = self.data_storage.prices.get(str(price))
            if matched_restaurants:
                if restaurant_ids:
                    filtered_ids = [id for id in matched_restaurants if id in restaurant_ids]
                    if filtered_ids:
                        matching_restaurants.append(filtered_ids)
                else:
                    matching_restaurants.append(matched_restaurants)

        return matching_restaurants

    def return_filtered_cuisine(self, cuisine):
        '''
        Returns the restaurant ids that match the given cuisine type.
        args:
            cuisine: str, cuisine name to match
        output:
            matching_restaurants: list[int], array of restaurant ids
        '''
        matching_restaurants = []
        cuisine_names = self.data_storage.cuisines.keys()
        matching_cuisines = [name for name in cuisine_names if cuisine.lower() in name.lower()]
        if matching_cuisines:
            for matched_cuisine in matching_cuisines:
                cuisine_restaurant_ids = self.data_storage.cuisines.get(matched_cuisine)
                matching_restaurants.extend(cuisine_restaurant_ids)

        return matching_restaurants

    def return_filtered_restaurant_names(self, name, restaurant_ids=[]):
        '''
        Returns the restaurant ids whose restaurants names are substrings of given name
        args:
            name: str, restaurant name to match
            restaurant_ids: optional list[str], additional match param
        return:
            list[int], array of restaurant ids
        '''
        if restaurant_ids:
            restaurants = [(id, self.data_storage.names.get(id)) for id in restaurant_ids]
        else:
            restaurants = self.data_storage.names.items()

        return [restaurant[0] for restaurant in restaurants if name in restaurant[1].lower()]

    def order_results(self, unique_restaurant_ids, ranked_results, existing_sort_params):
        '''
        Takes previously filtered information and sorts it to order the results to fit the business logic required
        args:
            unique_restaurant_ids: set, previously filtered restaurant_ids left to sort
            ranked_results: dict, key/val of previously filtered parameters and the parameter specific filtered restaurant_ids
            existing_sort_params: list[str], ordered array of sort hierarchy
        '''
        if not existing_sort_params:
            return list(unique_restaurant_ids)

        relevance_order = []

        # Sort in order of importance: distance -> rating -> price
        while unique_restaurant_ids and existing_sort_params:
            key = existing_sort_params.pop(0)
            criteria_filtered_ids = ranked_results[key]
            # loop through each depth to determine order
            # depth ie: [[1,2,3], [8,4,5], [12], [44]]
            for depth in criteria_filtered_ids:
                found_in_level = unique_restaurant_ids & set(depth)
                unique_restaurant_ids = unique_restaurant_ids - found_in_level
                # if tied relevancy sort via next order criteria
                if len(found_in_level) > 1:
                    found_in_level = self.order_results(set(found_in_level), ranked_results, existing_sort_params)

                relevance_order = relevance_order + list(found_in_level)

        return relevance_order

    def return_filtered_results(self, params):
        '''
        Provides logical filtering and sorting based on provided parameters
        args:
            params: dict, hashed version of request args
        returns:
            list[int], an ordered array of restaurant ids
        '''
        unique_restaurant_ids = []
        ranked_results = {}
        # cuisine as a top level filter if valid
        if "cuisine" in params:
            unique_restaurant_ids = self.return_filtered_cuisine(params["cuisine"])

        # subsequent filters will create "AND queries
        for key in self.match_importance:
            filter_method = self.param_key_to_store_map.get(key)

            if key in params:
                restaurant_ids = filter_method(unique_restaurant_ids, params[key].lower())
            else:
                restaurant_ids = filter_method(unique_restaurant_ids)

            if not restaurant_ids:
                return None

            ranked_results[key] = restaurant_ids
            unique_restaurant_ids = [id for sublist in restaurant_ids for id in sublist]

        if "name" in params:
            unique_restaurant_ids = self.return_filtered_restaurant_names(params["name"], unique_restaurant_ids)

        return self.order_results(set(unique_restaurant_ids), ranked_results, self.match_importance)

    def return_restaurant_information(self, restaurant_ids):
        '''
        Returns all available information about specified restaurants
        args:
            restaurant_ids: list[int], restaurants ids
        return:
            restaurants: list[dict], array of hashes of all requested restaurants' properties
        '''
        restaurants = []
        for id in restaurant_ids:
            restaurants_data = self.data_storage.restaurant_details[id]

            whole_restaurant_info = {
                "name": self.data_storage.names[id],
                "cuisine": self.data_storage.cuisine_ids[restaurants_data["cuisine_id"]],
                "rating": restaurants_data["rating"],
                "distance": restaurants_data["distance"],
                "price": restaurants_data["price"]
            }

            restaurants.append(whole_restaurant_info)

        return restaurants

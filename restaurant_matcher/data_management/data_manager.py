'''
Parses csv files into memory. Acts as a database stand in.
'''
import json
from csv import DictReader

class DataManager:
    def __init__(self, cuisine_csv_path, restaurant_csv_path):
        self.cuisines = {} # cuisines to restaurants
        self.cuisine_ids = {} # cuisine id to cuisine names
        self.ratings = {} # restaurant ids to their ratings
        self.distances = {} # restaurant ids to their distances
        self.prices = {} # restaurant ids to their prices
        self.names = {} # restaurant id to their real name
        self.restaurant_count = 0
        self.parse_cuisines_from_csv(cuisine_csv_path)
        self.parse_restaurants_from_csv(restaurant_csv_path)

    def parse_cuisines_from_csv(self, cuisine_csv_path):
        '''
        Transforms the cuisines.csv data into readable dicts
        input:
            cuisine_csv_path: str, file path
        '''
        with open(cuisine_csv_path, 'r') as read_obj:
            csv_dict_reader = DictReader(read_obj)
            for row in csv_dict_reader:
                self.cuisines[row['name']] = []
                self.cuisine_ids[row['id']] = row['name']

    def parse_restaurants_from_csv(self, restaurant_csv_path):
        '''
        Transforms the restaurants.csv data into readable dicts
        input:
            restaurant_csv_path: str, file path
        '''
        with open(restaurant_csv_path, 'r') as read_obj:
            csv_dict_reader = DictReader(read_obj)
            for row in csv_dict_reader:
                current_restaurant_id = self.set_ids_to_restaurants(row['name'])
                self.match_restaurant_to_cuisine(current_restaurant_id, row['cuisine_id'])
                self.match_restaurant_to_rating(current_restaurant_id, row['customer_rating'])
                self.match_restaurant_to_distances(current_restaurant_id, row['distance'])
                self.match_restaurant_to_prices(current_restaurant_id, row['price'])

    def set_ids_to_restaurants(self, restaurant_name):
        '''
        Populates self.names with restaurant names to a generated id
        input:
            restaurant_name: str, name of a restaurant
        return:
            curr_count: int, inputed restaurant's corresponding id value
        '''
        curr_count = self.restaurant_count
        self.names[curr_count] = restaurant_name
        self.restaurant_count += 1
        return str(curr_count)

    def match_restaurant_to_cuisine(self, current_restaurant_id, cuisine_id):
        '''
        Populates self.cuisines with restaurant names of those under its jurisdiction
        input:
            cuisine_id: int, key value for self.cuisine_ids
            current_restaurant_id: int, restaurant's corresponding id value
        '''
        cuisine_name = self.cuisine_ids[cuisine_id]
        self.cuisines[cuisine_name].append(current_restaurant_id)

    def match_restaurant_to_rating(self, current_restaurant_id, customer_rating):
        '''
        Populates self.ratings with restaurant names of those under its jurisdiction
        input:
            customer_rating: int, range(1, 5), rating number
            current_restaurant_id: int, restaurant's corresponding id value
        '''
        if customer_rating in self.ratings:
            self.ratings[customer_rating].append(current_restaurant_id)
        else:
            self.ratings[customer_rating] = [current_restaurant_id]

    def match_restaurant_to_distances(self, current_restaurant_id, distance):
        '''
        Populates self.distances with restaurant names of those under its jurisdiction
        input:
            row: int, range(1, 10), distance value away from user
            current_restaurant_id: int, restaurant's corresponding id value
        '''
        if distance in self.distances:
            self.distances[distance].append(current_restaurant_id)
        else:
            self.distances[distance] = [current_restaurant_id]

    def match_restaurant_to_prices(self, current_restaurant_id, price):
        '''
        Populates self.prices with restaurant names of those under its jurisdiction
        input:
            row: int, range(10, 50), $price amount for restaurant
            current_restaurant_id: int, restaurant's corresponding id value
        '''
        if price in self.prices:
            self.prices[price].append(current_restaurant_id)
        else:
            self.prices[price] = [current_restaurant_id]

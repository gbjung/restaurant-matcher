import pytest
from restaurant_matcher.data_management.data_manager import DataManager

@pytest.fixture
def return_data_manager():
    return DataManager('tests/fixtures/test_cuisines.csv', 'tests/fixtures/test_restaurants.csv')

def test_return_filtered_ratings(return_data_manager):
    '''
    Tests return_filtered_ratings method to return in ranked order
    '''
    # With given restaurant_ids
    filtered_answer = return_data_manager.return_filtered_ratings([0,3,7,2,6])
    assert filtered_answer == [[3, 7], [2, 6], [0]]
    # With given rating
    filtered_answer = return_data_manager.return_filtered_ratings([0,3,7,2,6], '3')
    assert filtered_answer == [[3, 7], [2, 6]]

def test_return_filtered_distances(return_data_manager):
    '''
    Tests return_filtered_distances method to return in closest distance order
    '''
    # With given restaurant_ids
    filtered_answer = return_data_manager.return_filtered_distances([0,3,4,7,2,6])
    assert filtered_answer == [[0], [2], [3], [4, 7], [6]]
    # With given distance val
    filtered_answer = return_data_manager.return_filtered_distances([0,3,4,7,2,6], '5')
    assert filtered_answer == [[0], [2], [3], [4, 7]]

def test_return_filtered_prices(return_data_manager):
    '''
    Tests return_filtered_prices method to return in cheapest price order
    '''
    # With given restaurant_ids
    filtered_answer = return_data_manager.return_filtered_prices([0,3,4,7,2,6])
    assert filtered_answer == [[0], [2], [3], [6, 7], [4]]
    # With given rating
    filtered_answer = return_data_manager.return_filtered_prices([0,3,4,7,2,6], '35')
    assert filtered_answer == [[0], [2]]

def test_return_filtered_cuisine(return_data_manager):
    '''
    Tests return_filtered_cuisine method to return in matching cuisines
    '''
    # With full name
    filtered_answer = return_data_manager.return_filtered_cuisine("Chinese")
    assert filtered_answer == [4, 6]

    # With partial name
    filtered_answer = return_data_manager.return_filtered_cuisine("chine")
    assert filtered_answer == [4, 6]

    # With multiple partial matches name
    filtered_answer = return_data_manager.return_filtered_cuisine("i")
    assert filtered_answer == [0, 1, 2, 3, 4, 6, 5, 7]

def test_return_filtered_restaurant_names(return_data_manager):
    '''
    Tests return_filtered_restaurant_names method to return in matching cuisines
    '''
    # With full name
    filtered_answer = return_data_manager.return_filtered_restaurant_names("applebees1")
    assert filtered_answer == [0]

    # With partial name
    filtered_answer = return_data_manager.return_filtered_restaurant_names("applebees")
    assert filtered_answer == [0, 1, 2, 3, 4, 5, 7]

    # With additional id filter
    filtered_answer = return_data_manager.return_filtered_restaurant_names("applebees", [1,2,3])
    assert filtered_answer == [1, 2, 3]

def test_order_results(return_data_manager):
    '''
    Tests order_results method to return restaurant_ids in order based on applied business logic
    '''
    ranked_results = {'distance': [[0], [1], [2], [3], [4, 7], [5], [6]],
                      'rating': [[4], [3, 7], [2, 6], [1], [0, 5]],
                      'price': [[0], [1], [2], [5], [3], [6, 7], [4]]}

    ordered_ids = return_data_manager.order_results(set([0, 1, 2, 3, 4, 7, 5]), ranked_results, ["distance", "rating", "price"])
    assert ordered_ids == [0, 1, 2, 3, 4, 7, 5]

def test_return_filtered_results(return_data_manager):
    '''
    Tests return_filtered_results method to return filtered in-order restaurant_ids
    '''
    # single filter
    filtered_results = return_data_manager.return_filtered_results({'name': 'applebees'})
    assert filtered_results == [0, 1, 2, 3, 4, 7, 5]
    # multiple filters
    filtered_results = return_data_manager.return_filtered_results({'name': 'applebees', 'rating': '2'})
    assert filtered_results == [1, 2, 3, 4, 7]
    # all filters
    filtered_results = return_data_manager.return_filtered_results({'name': 'applebees', 'rating': '2',
                                                                    'distance': '10', 'price': '35',
                                                                    'cuisine': 'american'})
    assert filtered_results == [1, 2]
    # no results
    filtered_results = return_data_manager.return_filtered_results({'name': 'toronto'})
    assert filtered_results == []

def test_return_restaurant_information(return_data_manager):
    '''
    Tests return_restaurant_information method to return restaurant info for given restaurant ids
    '''
    restaurants = return_data_manager.return_restaurant_information([0, 1, 2, 3])
    assert restaurants == [{'name': 'applebees1', 'cuisine': 'American', 'rating': '1', 'distance': '1', 'price': '10'},
                           {'name': 'applebees2', 'cuisine': 'American', 'rating': '2', 'distance': '2', 'price': '20'},
                           {'name': 'applebees3', 'cuisine': 'American', 'rating': '3', 'distance': '3', 'price': '30'},
                           {'name': 'applebees4', 'cuisine': 'American', 'rating': '4', 'distance': '4', 'price': '40'}]

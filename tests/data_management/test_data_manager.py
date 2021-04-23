import pytest
from restaurant_matcher.data_management.data_manager import DataManager

@pytest.fixture
def return_data_manager():
    return DataManager('tests/fixtures/test_cuisines.csv', 'tests/fixtures/test_restaurants.csv')

def test_data_ingestion(return_data_manager):
    '''
    Happy case if all optional parameters are provided, no error logs
    '''
    assert return_data_manager.cuisine_ids == {'1': 'American', '2': 'Chinese', '3': 'Thai'}
    assert return_data_manager.ratings == {'1': [0, 5], '2': [1], '3': [2, 6], '4': [3, 7], '5': [4]}
    assert return_data_manager.distances == {'1': [0], '2': [1], '3': [2], '4': [3], '5': [4, 7], '6': [5], '7': [6]}
    assert return_data_manager.prices == {'10': [0], '20': [1], '30': [2], '40': [3], '50': [4], '35': [5], '45': [6, 7]}
    assert return_data_manager.cuisines == {'American': [0, 1, 2, 3], 'Chinese': [4, 6], 'Thai': [5, 7]}
    assert return_data_manager.names == {0: 'applebees1', 1: 'applebees2', 2: 'applebees3', 3: 'applebees4',
                                         4: 'applebees5', 5: 'applebees6', 6: 'red lobster', 7: 'applebees red lobster'}

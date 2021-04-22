import pytest
from restaurant_matcher.match_service.validators import MatchServiceSchema

@pytest.fixture
def return_match_service_schema():
    return MatchServiceSchema()

def test_all_valid_parameters(return_match_service_schema):
    '''
    Happy case if all optional parameters are provided, no error logs
    '''
    params = {'name': 'test', 'rating': 1, 'distance': 1, 'price': 10, 'cuisine': 'test'}
    assert return_match_service_schema.validate(params) == {}

def test_optional_valid_parameters(return_match_service_schema):
    '''
    Happy case if some optional parameters are provided, no error logs
    '''
    params = [
                {'rating': 1, 'distance': 1, 'price': 10, 'cuisine': 'test'},
                {'name': 'test','price': 10, 'cuisine': 'test'},
                {'name': 'test', 'rating': 1, 'cuisine': 'test'},
                {'name': 'test', 'rating': 1, 'distance': 1, 'price': 10},
                {'name': 'test', 'rating': 1}
            ]
    for param in params:
        assert return_match_service_schema.validate(param) == {}

def test_invalid_parameter(return_match_service_schema):
    '''
    For multi-param requests, capture failure if one optional param is invalid
    '''
    params = [
                # name not string
                {'name': 1, 'rating': 1, 'distance': 1, 'price': 10, 'cuisine': 'test'},
                # rating out of range
                {'name': 'test', 'rating': 0, 'distance': 1, 'price': 10, 'cuisine': 'test'},
                {'name': 'test', 'rating': 6, 'distance': 1, 'price': 10, 'cuisine': 'test'},
                # rating not int
                {'name': 'test', 'rating': 'good', 'distance': 1, 'price': 10, 'cuisine': 'test'},
                # distance out of range
                {'name': 'test', 'rating': 1, 'distance': 0, 'price': 10, 'cuisine': 'test'},
                {'name': 'test', 'rating': 1, 'distance': 11, 'price': 10, 'cuisine': 'test'},
                # distance not int
                {'name': 'test', 'rating': 1, 'distance': 'close', 'price': 10, 'cuisine': 'test'},
                # price out of range
                {'name': 'test', 'rating': 1, 'distance': 1, 'price': 0, 'cuisine': 'test'},
                {'name': 'test', 'rating': 1, 'distance': 1, 'price': 100, 'cuisine': 'test'},
                # price not int
                {'name': 'test', 'rating': 1, 'distance': 1, 'price': 'affordable', 'cuisine': 'test'},
                # cuisine type not string
                {'name': 'test', 'rating': 1, 'distance': 1, 'price': 10, 'cuisine': 1}
            ]

    for param in params:
        # should return one error message for each failure
        assert len(return_match_service_schema.validate(param).keys()) == 1

def test_invalid_parameters(return_match_service_schema):
    '''
    For multi-param requests, capture all failures for multiple invalid params
    '''
    params = {'name': 1, 'rating': 111, 'distance': 12, 'price': 10, 'cuisine': 'test'}
    number_of_errors = 3
    assert len(return_match_service_schema.validate(params).keys()) == number_of_errors

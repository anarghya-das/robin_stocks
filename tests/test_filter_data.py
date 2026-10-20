"""Offline tests for the fork filtering extensions."""

import unittest
from calcap_robin_stocks.robinhood.helper import filter_data


class TestHelperFunctions(unittest.TestCase):
    """Unit tests for helper functions - no login required"""

    def test_filter_data_single_key_from_list(self):
        """Test extracting a single key from a list of dicts"""

        data = [
            {'symbol': 'AAPL', 'price': 150},
            {'symbol': 'GOOGL', 'price': 2800},
            {'symbol': 'MSFT', 'price': 380}
        ]
        result = filter_data(data, 'symbol')
        assert result == ['AAPL', 'GOOGL', 'MSFT']

    def test_filter_data_single_key_from_dict(self):
        """Test extracting a single key from a dict"""

        data = {'symbol': 'AAPL', 'price': 150, 'quantity': 10}
        result = filter_data(data, 'price')
        assert result == 150

    def test_filter_data_multiple_keys_from_list(self):
        """Test extracting multiple keys from a list of dicts"""

        data = [
            {'symbol': 'AAPL', 'price': 150, 'quantity': 10},
            {'symbol': 'GOOGL', 'price': 2800, 'quantity': 5}
        ]
        result = filter_data(data, ['symbol', 'price'])
        assert result == [
            {'symbol': 'AAPL', 'price': 150},
            {'symbol': 'GOOGL', 'price': 2800}
        ]

    def test_filter_data_multiple_keys_from_dict(self):
        """Test extracting multiple keys from a dict"""

        data = {'symbol': 'AAPL', 'price': 150, 'quantity': 10, 'side': 'buy'}
        result = filter_data(data, ['symbol', 'quantity'])
        assert result == {'symbol': 'AAPL', 'quantity': 10}

    def test_filter_data_where_single_condition(self):
        """Test filtering with a single where condition"""

        data = [
            {'symbol': 'AAPL', 'price': 150, 'side': 'buy'},
            {'symbol': 'GOOGL', 'price': 2800, 'side': 'buy'},
            {'symbol': 'AAPL', 'price': 155, 'side': 'sell'}
        ]
        result = filter_data(data, None, where={'symbol': 'AAPL'})
        assert len(result) == 2
        assert all(item['symbol'] == 'AAPL' for item in result)

    def test_filter_data_where_multiple_conditions(self):
        """Test filtering with multiple where conditions (AND logic)"""

        data = [
            {'symbol': 'AAPL', 'price': 150, 'side': 'buy'},
            {'symbol': 'GOOGL', 'price': 2800, 'side': 'buy'},
            {'symbol': 'AAPL', 'price': 155, 'side': 'sell'}
        ]
        result = filter_data(data, None, where={
                             'symbol': 'AAPL', 'side': 'buy'})
        assert len(result) == 1
        assert result[0] == {'symbol': 'AAPL', 'price': 150, 'side': 'buy'}

    def test_filter_data_where_plus_single_key(self):
        """Test filtering with where condition and extracting a single key"""

        data = [
            {'symbol': 'AAPL', 'price': 150, 'side': 'buy'},
            {'symbol': 'AAPL', 'price': 155, 'side': 'sell'},
            {'symbol': 'GOOGL', 'price': 2800, 'side': 'buy'}
        ]
        result = filter_data(data, 'price', where={'symbol': 'AAPL'})
        assert result == [150, 155]

    def test_filter_data_where_plus_multiple_keys(self):
        """Test filtering with where condition and extracting multiple keys"""

        data = [
            {'symbol': 'AAPL', 'price': 150, 'quantity': 10, 'side': 'buy'},
            {'symbol': 'GOOGL', 'price': 2800, 'quantity': 5, 'side': 'buy'},
            {'symbol': 'MSFT', 'price': 380, 'quantity': 20, 'side': 'sell'}
        ]
        result = filter_data(data, ['symbol', 'price'], where={'side': 'buy'})
        assert len(result) == 2
        assert result == [
            {'symbol': 'AAPL', 'price': 150},
            {'symbol': 'GOOGL', 'price': 2800}
        ]

    def test_filter_data_where_no_matches(self):
        """Test filtering when no items match the where condition"""

        data = [
            {'symbol': 'AAPL', 'price': 150},
            {'symbol': 'GOOGL', 'price': 2800}
        ]
        result = filter_data(data, None, where={'symbol': 'TSLA'})
        assert result == []

    def test_filter_data_where_on_single_dict_match(self):
        """Test filtering a single dict with matching condition"""

        data = {'symbol': 'AAPL', 'price': 150, 'side': 'buy'}
        result = filter_data(data, None, where={'symbol': 'AAPL'})
        assert result == data

    def test_filter_data_where_on_single_dict_no_match(self):
        """Test filtering a single dict with non-matching condition"""

        data = {'symbol': 'AAPL', 'price': 150, 'side': 'buy'}
        result = filter_data(data, None, where={'symbol': 'GOOGL'})
        assert result == None

    def test_filter_data_none_input(self):
        """Test that None input returns None"""

        result = filter_data(None, 'symbol')
        assert result == None

    def test_filter_data_empty_list(self):
        """Test that empty list returns empty list"""

        result = filter_data([], 'symbol')
        assert result == []

    def test_filter_data_backwards_compatibility(self):
        """Test that all old functionality still works (backwards compatibility)"""

        # Old usage: single key extraction from list
        data = [{'name': 'Apple'}, {'name': 'Google'}]
        result = filter_data(data, 'name')
        assert result == ['Apple', 'Google']

        # Old usage: single key extraction from dict
        data = {'name': 'Apple', 'ticker': 'AAPL'}
        result = filter_data(data, 'ticker')
        assert result == 'AAPL'

        # Old usage: None info parameter returns original data
        data = [{'a': 1}, {'b': 2}]
        result = filter_data(data, None)
        assert result == data

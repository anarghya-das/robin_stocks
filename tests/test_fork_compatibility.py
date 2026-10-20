"""Offline checks for fork behavior required by Calcap."""

import unittest
from unittest.mock import patch

from robin_stocks.robinhood import account
from robin_stocks.robinhood.helper import filter_data


class TestForkCompatibility(unittest.TestCase):
    def setUp(self):
        self.rows = [
            {'account_number': 'one', 'brokerage_account_type': 'individual',
             'details': {'status': 'active'}},
            {'account_number': 'two', 'brokerage_account_type': 'joint',
             'details': {'status': 'inactive'}},
        ]

    def test_calcap_account_projection(self):
        self.assertEqual(
            filter_data(self.rows, ['account_number', 'brokerage_account_type']),
            [{'account_number': 'one', 'brokerage_account_type': 'individual'},
             {'account_number': 'two', 'brokerage_account_type': 'joint'}],
        )

    def test_tuple_projection_on_dictionary(self):
        self.assertEqual(filter_data(self.rows[0], ('account_number',)),
                         {'account_number': 'one'})

    def test_nested_projection_and_where_conditions(self):
        self.assertEqual(
            filter_data(self.rows, ['account_number', 'details.status'],
                        where={'details.status': 'active',
                               'brokerage_account_type': 'individual'}),
            [{'account_number': 'one', 'details.status': 'active'}],
        )

    def test_single_key_and_empty_results(self):
        self.assertEqual(filter_data(self.rows, 'account_number'), ['one', 'two'])
        self.assertEqual(filter_data(self.rows, 'details.status'),
                         ['active', 'inactive'])
        self.assertEqual(filter_data(self.rows, None,
                                     where={'account_number': 'missing'}), [])
        self.assertIsNone(filter_data(None, 'account_number'))
        self.assertEqual(filter_data([], 'account_number'), [])

    def test_unified_transfers_requests_all_pages(self):
        transfers = [{'id': 'first'}, {'id': 'second'}]
        with patch('robin_stocks.robinhood.helper.LOGGED_IN', True), \
                patch.object(account, 'request_get', return_value=transfers) as get:
            self.assertEqual(account.get_unified_transfers(), transfers)
            get.assert_called_once_with(account.unifiedtransfers_url(), 'pagination')


if __name__ == '__main__':
    unittest.main()

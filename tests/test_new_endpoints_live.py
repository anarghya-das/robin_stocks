"""Live tests for the endpoints added after the 2026-10 web-app audit.

These hit the real Robinhood API and need the same credentials as ``test_robinhood.py``
(``robin_username``, ``robin_password`` and, for MFA accounts, ``robin_mfa`` in the
environment / ``.env``). When those are absent the whole class is skipped, so the
offline suite still runs clean in CI without secrets.

Assertions check shape only (keys / types), matching what was observed against a live
signed-in session, so they stay robust regardless of the account's holdings.
"""

import os
import unittest

import calcap_robin_stocks.robinhood as r

try:
    import pyotp
except ImportError:  # pragma: no cover - pyotp is a test dependency
    pyotp = None


class TestNewEndpointsLive(unittest.TestCase):

    @classmethod
    def setup_class(cls):
        if not os.environ.get('robin_username') or not os.environ.get('robin_password'):
            raise unittest.SkipTest('live Robinhood credentials not configured')
        mfa = os.environ.get('robin_mfa')
        totp = pyotp.TOTP(mfa).now() if (mfa and pyotp) else None
        r.login(os.environ['robin_username'], os.environ['robin_password'], mfa_code=totp)

    @classmethod
    def teardown_class(cls):
        try:
            r.logout()
        except Exception:
            pass

    def test_load_unified_accounts(self):
        data = r.load_unified_accounts()
        self.assertIsInstance(data, list)
        self.assertTrue(data, 'expected at least one account')
        self.assertIn('account_number', data[0])
        self.assertIn('account_buying_power', data[0])

    def test_get_interest_rate(self):
        data = r.get_interest_rate()
        self.assertIsInstance(data, dict)
        self.assertIn('interest_rate', data)

    def test_get_acats_transfers(self):
        # May legitimately be empty; just has to be a well-formed list.
        self.assertIsInstance(r.get_acats_transfers(), list)

    def test_get_portfolio_performance(self):
        data = r.get_portfolio_performance()
        self.assertIsInstance(data, dict)
        self.assertIn('id', data)

    def test_get_marketdata_fundamentals(self):
        data = r.get_marketdata_fundamentals('AAPL')
        self.assertIsInstance(data, list)
        self.assertTrue(data)
        self.assertEqual(data[0]['symbol'], 'AAPL')
        self.assertIn('market_cap', data[0])

    # --- Tier 1 + Tier 2 ---

    def test_get_crypto_transfers(self):
        self.assertIsInstance(r.get_crypto_transfers(), list)

    def test_get_asset_transfers(self):
        data = r.get_asset_transfers()
        self.assertIsInstance(data, dict)
        self.assertIn('assetTransferRecord', data)

    def test_get_split_payments(self):
        self.assertIsInstance(r.get_split_payments(), list)

    def test_get_adr_fees(self):
        self.assertIsInstance(r.get_adr_fees(), list)

    def test_get_drip_enrollment(self):
        data = r.get_drip_enrollment()
        self.assertIsInstance(data, dict)
        self.assertIn('drip_enrolled', data)

    def test_get_retirement_history(self):
        self.assertIsInstance(r.get_retirement_history(), list)

    def test_get_rhy_accounts(self):
        self.assertIsInstance(r.get_rhy_accounts(), list)

    def test_get_combo_orders(self):
        self.assertIsInstance(r.get_combo_orders(), list)

    def test_get_advanced_orders(self):
        self.assertIsInstance(r.get_advanced_orders(), list)


if __name__ == '__main__':
    unittest.main()

import unittest
from decimal import Decimal
from unittest.mock import AsyncMock

from starter import recommend_price


class RecommendPriceTests(unittest.IsolatedAsyncioTestCase):
    async def test_applies_discount_to_cheapest_eligible_offer(self):
        fetch_offers = AsyncMock(return_value={
            "status": "success",
            "offers": [
                {"seller": "mYsHoP", "price": Decimal("40.00"), "delivery_days": 2},
                {"seller": "UNKNOWN", "price": Decimal("45.00"), "delivery_days": None},
                {"seller": "SLOW", "price": Decimal("50.00"), "delivery_days": 7},
                {"seller": "PARTS", "price": Decimal("99.99"), "delivery_days": 6},
                {"seller": "FAST", "price": Decimal("105.00"), "delivery_days": 0},
            ],
        })

        result = await recommend_price(fetch_offers, Decimal("100.00"), Decimal("90.00"))

        self.assertEqual(result["price"], Decimal("98.49"))
        self.assertEqual(result["decision"], "APPLY")
        self.assertTrue(result["reason"])

    async def test_holds_current_price_on_partial_result(self):
        fetch_offers = AsyncMock(return_value={
            "status": "partial",
            "offers": [
                {"seller": "PARTS", "price": Decimal("120.00"), "delivery_days": 2},
            ],
        })

        result = await recommend_price(fetch_offers, Decimal("100.00"), Decimal("110.00"))

        self.assertEqual(result["price"], Decimal("100.00"))
        self.assertEqual(result["decision"], "HOLD")
        self.assertTrue(result["reason"])

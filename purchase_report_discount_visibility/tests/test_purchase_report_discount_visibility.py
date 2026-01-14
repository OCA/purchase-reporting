# Copyright 2026 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.fields import Command

from odoo.addons.base.tests.common import BaseCommon


class TestPurchaseReportDiscountVisibility(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.vendor = cls.env["res.partner"].create({"name": "Test Vendor"})
        cls.product = cls.env["product.product"].create({"name": "Test Product"})

    def _create_po(self, discounts):
        return self.env["purchase.order"].create(
            {
                "partner_id": self.vendor.id,
                "order_line": [
                    Command.create(
                        {
                            "name": self.product.name,
                            "product_id": self.product.id,
                            "product_qty": 1.0,
                            "price_unit": 100.0,
                            "discount": d,
                        }
                    )
                    for d in discounts
                ],
            }
        )

    def test_display_discount(self):
        po = self._create_po([0.0, 0.0, 0.0])
        self.assertFalse(po._display_discount())
        po = self._create_po([0.0, 10.0, 0.0])
        self.assertTrue(po._display_discount())

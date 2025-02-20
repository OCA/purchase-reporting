# Copyright 2023 Moduon Team S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo import Command

from odoo.addons.base.tests.common import BaseCommon


class TestPurchaseReport(BaseCommon):
    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.partner = self.env["res.partner"].create({"name": "Test Vendor"})
        self.product = self.env["product.product"].create(
            {
                "name": "Test Product",
                "type": "consu",
            }
        )
        self.packaging = self.env["product.packaging"].create(
            {
                "name": "Box",
                "product_id": self.product.id,
                "qty": 5,  # Packaging contains 5 units
            }
        )
        self.purchase_order = self.env["purchase.order"].create(
            {
                "partner_id": self.partner.id,
                "order_line": [
                    Command.create(
                        {
                            "product_id": self.product.id,
                            "product_qty": 10,
                            "product_packaging_id": self.packaging.id,
                            "product_packaging_qty": 10,
                        }
                    )
                ],
            }
        )

    def test_purchase_report_with_packaging(self):
        """Test that purchase.report includes packaging data"""
        self.purchase_order.button_confirm()

        purchase_report = self.env["purchase.report"].search(
            [("product_id", "=", self.product.id)]
        )

        self.assertTrue(purchase_report, "Purchase report entry was not created")
        self.assertEqual(
            purchase_report[0].product_packaging_id,
            self.packaging,
            "Product packaging ID is incorrect in the report",
        )
        self.assertEqual(
            purchase_report[0].product_packaging_qty,
            10,
            "Product packaging quantity is incorrect in the report",
        )

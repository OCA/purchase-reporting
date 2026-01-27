# Copyright 2026 Quartile (https://www.quartile.co)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo.fields import Command

from odoo.addons.base.tests.common import BaseCommon


class TestPurchaseOrderReportHideTax(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.vendor = cls.env["res.partner"].create({"name": "Test Vendor"})
        cls.product = cls.env["product.product"].create({"name": "Test Product"})
        cls.tax_group_10 = cls.env["account.tax.group"].create({"name": "Tax 10%"})
        cls.tax_group_15 = cls.env["account.tax.group"].create({"name": "Tax 15%"})
        cls.tax_10 = cls.env["account.tax"].create(
            {
                "name": "TEST 10%",
                "type_tax_use": "purchase",
                "amount_type": "percent",
                "amount": 10.00,
                "tax_group_id": cls.tax_group_10.id,
            }
        )
        cls.tax_15 = cls.env["account.tax"].create(
            {
                "name": "TEST 15%",
                "type_tax_use": "purchase",
                "amount_type": "percent",
                "amount": 15.00,
                "tax_group_id": cls.tax_group_15.id,
            }
        )

    def _create_po(self, taxes_per_line):
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
                            "taxes_id": [Command.link(taxes.id)],
                        }
                    )
                    for taxes in taxes_per_line
                ],
            }
        )

    def test_show_tax_column_in_report(self):
        po = self._create_po([self.tax_10, self.tax_10])
        po._compute_show_tax_column_in_report()
        self.assertFalse(po.show_tax_column_in_report)
        # Mixed tax groups (10% + 15%) -> should show it (True)
        po = self._create_po([self.tax_10, self.tax_15])
        po._compute_show_tax_column_in_report()
        self.assertTrue(po.show_tax_column_in_report)

    def test_show_tax_column_in_report_by_tax_group_setting(self):
        self.tax_group_10.show_tax_column_in_purchase_report = True
        po = self._create_po([self.tax_10, self.tax_10])
        po._compute_show_tax_column_in_report()
        self.assertTrue(po.show_tax_column_in_report)

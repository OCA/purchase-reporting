# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestPurchaseReportHideLine(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company_id = cls.env.ref("base.main_company")
        cls.partner_id = cls.env["res.partner"].create({"name": "Test partner"})
        cls.product_id = cls.env["product.product"].create({"name": "Test product"})
        cls.purchase_id = cls.env["purchase.order"].create(
            {"partner_id": cls.partner_id.id}
        )

    def _purchase_add_line(self, purchase, quantity, price_unit):
        purchase.write(
            {
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product_id.id,
                            "product_uom": self.product_id.uom_id.id,
                            "name": self.product_id.name,
                            "price_unit": price_unit,
                            "product_qty": quantity,
                        },
                    )
                ],
            }
        )

    def test_default_hide_quantity(self):
        self.company_id.purchase_hide_in_report_default = "quantity"
        self._purchase_add_line(self.purchase_id, 0, 100)
        self.assertTrue(self.purchase_id.order_line[0].hide_in_report)

        self._purchase_add_line(self.purchase_id, 1, 0)
        self.assertFalse(self.purchase_id.order_line[1].hide_in_report)

    def test_default_hide_price(self):
        self.company_id.purchase_hide_in_report_default = "price"
        self._purchase_add_line(self.purchase_id, 1, 0)
        self.assertTrue(self.purchase_id.order_line[0].hide_in_report)

        self._purchase_add_line(self.purchase_id, 1, 100)
        self.assertFalse(self.purchase_id.order_line[1].hide_in_report)

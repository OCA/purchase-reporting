# Copyright 2024 Tecnativa - Pilar Vargas
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests import Form, tagged

from odoo.addons.base.tests.common import BaseCommon

REPORT_NAME = (
    "purchase_order_report_grouped_by_vendor.report_purchase_order_grouped_by_vendor"
)


# Rendering the report needs a fully loaded registry, as modules loaded after
# this one (purchase_stock, ...) extend the records involved in it.
@tagged("post_install", "-at_install")
class TestPurchaseOrderReportGroupedByVendor(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner1 = cls.env["res.partner"].create({"name": "Test Partner One"})
        cls.partner2 = cls.env["res.partner"].create({"name": "Test Partner Two"})
        cls.product1 = cls.env["product.product"].create({"name": "Test product 1"})
        cls.product2 = cls.env["product.product"].create({"name": "Test product 2"})

    def _create_purchase_order(self, partner):
        po_form = Form(self.env["purchase.order"])
        po_form.partner_id = partner
        with po_form.order_line.new() as po_line_form:
            po_line_form.product_id = self.product1
            po_line_form.product_qty = 2
            po_line_form.price_unit = 15.0
        with po_form.order_line.new() as po_line_form:
            po_line_form.product_id = self.product2
            po_line_form.product_qty = 1
            po_line_form.price_unit = 20.0
        return po_form.save()

    def test_01_report_grouped_by_vendor(self):
        po1_partner1 = self._create_purchase_order(self.partner1)
        po1_partner1.button_confirm()
        po2_partner1 = self._create_purchase_order(self.partner1)
        po2_partner1.button_confirm()
        po1_partner2 = self._create_purchase_order(self.partner2)
        po1_partner2.button_confirm()
        purchase_orders = po1_partner1 + po2_partner1 + po1_partner2
        # Only two groups, one per vendor
        groups = purchase_orders.get_grouped_data()
        self.assertEqual(
            [group["partner"] for group in groups], [self.partner1, self.partner2]
        )
        self.assertEqual(groups[0]["order_ids"], po1_partner1 + po2_partner1)
        self.assertEqual(groups[1]["order_ids"], po1_partner2)
        html = str(
            self.env["ir.actions.report"]._render_qweb_html(
                REPORT_NAME, purchase_orders.ids
            )[0]
        )
        # Both vendors must be in the report
        self.assertIn('<span itemprop="name">Test Partner One</span>', html)
        self.assertIn('<span itemprop="name">Test Partner Two</span>', html)
        # Purchase orders are grouped by vendor with Order Ref in lines.
        self.assertEqual(html.count(f"Order: {po1_partner1.name}"), 1)
        self.assertEqual(html.count(f"Order: {po2_partner1.name}"), 1)
        self.assertEqual(html.count(f"Order: {po1_partner2.name}"), 1)
        self.assertEqual(html.count(self.product1.name), 3)
        self.assertEqual(html.count(self.product2.name), 3)

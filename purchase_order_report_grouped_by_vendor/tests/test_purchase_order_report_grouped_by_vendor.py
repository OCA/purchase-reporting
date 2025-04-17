# Copyright 2024 Tecnativa - Pilar Vargas
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests.common import Form, TransactionCase


class TestPurchaseOrderReportGroupedByVendor(TransactionCase):
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
        purchase_order_ids = [
            po1_partner1.id,
            po2_partner1.id,
            po1_partner2.id,
        ]
        IrActionsReport = self.env["ir.actions.report"]
        res = IrActionsReport._render_qweb_html(
            IrActionsReport._get_report_from_name(
                "purchase_order_report_grouped_by_vendor"
                ".report_purchase_order_grouped_by_vendor"
            ),
            purchase_order_ids,
        )
        # Both vendors must be in the report
        self.assertRegex(str(res[0]), '<span itemprop="name">Test Partner One</span>')
        self.assertRegex(str(res[0]), '<span itemprop="name">Test Partner Two</span>')
        # Purchase orders are grouped by vendor with Order Ref in lines.
        self.assertEqual(str(res[0]).count(f"Order: {po1_partner1.name}"), 1)
        self.assertEqual(str(res[0]).count(f"Order: {po2_partner1.name}"), 1)
        self.assertEqual(str(res[0]).count(f"Order: {po1_partner2.name}"), 1)
        self.assertEqual(str(res[0]).count(self.product1.name), 3)
        self.assertEqual(str(res[0]).count(self.product2.name), 3)

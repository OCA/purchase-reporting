# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestPurchaseOrderReport(TransactionCase):
    def setUp(self):
        super(TestPurchaseOrderReport, self).setUp()
        self.base_comment_model = self.env["base.comment.template"]
        self.before_comment = self._create_comment("before_lines")
        self.after_comment = self._create_comment("after_lines")
        self.partner_id = self.env["res.partner"].create({"name": "Partner Test"})
        self.purchase_order = self.env.ref("purchase.purchase_order_4")
        self.purchase_order.update(
            {
                "comment_template1_id": self.before_comment.id,
                "comment_template2_id": self.after_comment.id,
            }
        )
        self.purchase_order._set_note1()
        self.purchase_order._set_note2()

    def _create_comment(self, position):
        return self.base_comment_model.create(
            {
                "name": "Comment " + position,
                "position": position,
                "text": "Text " + position,
            }
        )

    def test_comments_in_purchase_order(self):
        res = (
            self.env["ir.actions.report"]
            ._get_report_from_name("purchase.report_purchaseorder")
            .render_qweb_html(self.purchase_order.ids)
        )
        self.assertRegexpMatches(str(res[0]), self.before_comment.text)
        self.assertRegexpMatches(str(res[0]), self.after_comment.text)

    def test_onchange_partner_id(self):
        self.partner_id.property_comment_template_id = self.after_comment.id
        vals = {
            "partner_id": self.partner_id.id,
        }
        new_purchase = self.env["purchase.order"].new(vals)
        new_purchase.onchange_partner_id_purchase_comment()
        purchase_dict = new_purchase._convert_to_write(new_purchase._cache)
        new_purchase = self.env["purchase.order"].create(purchase_dict)
        self.assertEqual(new_purchase.comment_template2_id, self.after_comment)
        self.partner_id.property_comment_template_id = self.before_comment.id
        new_purchase = self.env["purchase.order"].new(vals)
        new_purchase.onchange_partner_id_purchase_comment()
        purchase_dict = new_purchase._convert_to_write(new_purchase._cache)
        new_purchase = self.env["purchase.order"].create(purchase_dict)
        self.assertEqual(new_purchase.comment_template1_id, self.before_comment)

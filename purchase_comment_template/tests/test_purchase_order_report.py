# Copyright 2018 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import Form, TransactionCase


class TestPurchaseOrderReport(TransactionCase):
    def setUp(self):
        super().setUp()
        self.company = self.env.ref("base.main_company")
        self.base_comment_model = self.env["base.comment.template"]
        self.before_comment = self._create_comment("purchase.order", "before_lines")
        self.after_comment = self._create_comment("purchase.order", "after_lines")
        self.partner = self.env["res.partner"].create({"name": "Partner Test"})
        self.partner.base_comment_template_ids = [
            (4, self.before_comment.id),
            (4, self.after_comment.id),
        ]
        self.purchase_order = self.env.ref("purchase.purchase_order_4")
        self.purchase_order.update(
            {
                "comment_template_ids": [
                    (4, self.before_comment.id),
                    (4, self.after_comment.id),
                ],
            }
        )

    def _create_comment(self, models, position):
        return self.base_comment_model.create(
            {
                "name": "Comment " + position,
                "company_id": self.company.id,
                "position": position,
                "text": "Text " + position,
                "models": models,
            }
        )

    def test_comments_in_purchase_order(self):
        res = (
            self.env["ir.actions.report"]
            ._get_report_from_name("purchase.report_purchaseorder")
            ._render_qweb_html(self.purchase_order.ids)
        )
        self.assertRegex(str(res[0]), self.before_comment.text)
        self.assertRegex(str(res[0]), self.after_comment.text)

    def test_onchange_partner_id(self):
        with Form(self.env["purchase.order"]) as new_purchase:
            new_purchase.partner_id = self.partner
            self.assertEqual(len(new_purchase.comment_template_ids), 2)

# Copyright 2021 Jarsa
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo.tests.common import TransactionCase


class TestPurchaseRequisitionReport(TransactionCase):
    def setUp(self):
        super(TestPurchaseRequisitionReport, self).setUp()
        self.base_comment_model = self.env["base.comment.template"]
        self.before_comment = self._create_comment("before_lines")
        self.after_comment = self._create_comment("after_lines")
        self.vendor_id = self.env["res.partner"].create({"name": "Partner Test"})
        self.purchase_requisition = self.env.ref("purchase_requisition.requisition1")
        self.purchase_requisition.update(
            {
                "comment_template1_id": self.before_comment.id,
                "comment_template2_id": self.after_comment.id,
            }
        )
        self.purchase_requisition._set_note1()
        self.purchase_requisition._set_note2()

    def _create_comment(self, position):
        return self.base_comment_model.create(
            {
                "name": "Comment " + position,
                "position": position,
                "text": "Text " + position,
            }
        )

    def test_comments_in_purchase_requisition(self):
        res = (
            self.env["ir.actions.report"]
            ._get_report_from_name("purchase_requisition.report_purchaserequisitions")
            ._render_qweb_html(self.purchase_requisition.ids)
        )
        self.assertRegex(str(res[0]), self.before_comment.text)
        self.assertRegex(str(res[0]), self.after_comment.text)

    def test_onchange_vendor_id(self):
        self.vendor_id.property_comment_template_id = self.after_comment.id
        vals = {
            "vendor_id": self.vendor_id.id,
        }
        new_purchase = self.env["purchase.requisition"].new(vals)
        new_purchase.onchange_vendor_id_purchase_comment()
        purchase_dict = new_purchase._convert_to_write(new_purchase._cache)
        new_purchase = self.env["purchase.requisition"].create(purchase_dict)
        self.assertEqual(new_purchase.comment_template2_id, self.after_comment)
        self.vendor_id.property_comment_template_id = self.before_comment.id
        new_purchase = self.env["purchase.requisition"].new(vals)
        new_purchase.onchange_vendor_id_purchase_comment()
        purchase_dict = new_purchase._convert_to_write(new_purchase._cache)
        new_purchase = self.env["purchase.requisition"].create(purchase_dict)
        self.assertEqual(new_purchase.comment_template1_id, self.before_comment)

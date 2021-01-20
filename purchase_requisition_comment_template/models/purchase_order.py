# Copyright 2021 Jarsa
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, models


class PurchaseOrder(models.Model):

    _inherit = "purchase.order"

    @api.onchange("requisition_id")
    def onchange_requisition_id_purchase_comment(self):
        if self.requisition_id:
            if self.requisition_id.comment_template1_id:
                self.comment_template1_id = self.requisition_id.comment_template1_id
            elif self.requisition_id.note1:
                self.note1 = self.requisition_id.note1
            if self.requisition_id.comment_template2_id:
                self.comment_template2_id = self.requisition_id.comment_template2_id
            elif self.requisition_id.note2:
                self.note2 = self.requisition_id.note2

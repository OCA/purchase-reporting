# -*- coding: utf-8 -*-
# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class PurchaseOrder(models.Model):
    """Add text comment"""

    _inherit = "purchase.order"

    comment_template1_id = fields.Many2one('base.comment.template',
                                           string='Top Comment Template')
    comment_template2_id = fields.Many2one('base.comment.template',
                                           string='Bottom Comment Template')
    note1 = fields.Html('Top Comment')
    note2 = fields.Html('Bottom Comment')

    @api.onchange('comment_template1_id')
    def _set_note1(self):
        comment = self.comment_template1_id
        if comment:
            self.note1 = comment.get_value(self.partner_id.id)

    @api.onchange('comment_template2_id')
    def _set_note2(self):
        comment = self.comment_template2_id
        if comment:
            self.note2 = comment.get_value(self.partner_id.id)

    @api.onchange('partner_id')
    def onchange_partner_id_purchase_comment(self):
        if self.partner_id:
            comment_template = self.partner_id.property_comment_template_id
            if comment_template.position == 'before_lines':
                self.comment_template1_id = comment_template
            elif comment_template.position == 'after_lines':
                self.comment_template2_id = comment_template


class PurchaseOrderLine(models.Model):
    """Add text comment"""

    _inherit = "purchase.order.line"

    formatted_note = fields.Html('Formatted Note')

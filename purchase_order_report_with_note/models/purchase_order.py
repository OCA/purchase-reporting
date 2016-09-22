# -*- coding: utf-8 -*-
#   Copyright (c) 2013 Camptocamp SA (http://www.camptocamp.com)
#   @author Vincent Renaville
# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class PurchaseConditionText(models.Model):

    """ Purchase order Textual information """

    _name = "purchase.condition_text"
    _description = "purchase conditions"

    name = fields.Char('Condition summary', required=True, size=128)
    type = fields.Selection([('header', 'Top condition'),
                             ('footer', 'Bottom condition')],
                            'type', required=True)
    text = fields.Html('Condition', translate=True, required=True)


class PurchaseOrder(models.Model):

    """ Adds condition to Po """

    _inherit = "purchase.order"
    _description = 'Purchase Order'

    text_condition1 = fields.Many2one('purchase.condition_text', 'Header',
                                      domain=[('type', '=', 'header')])
    text_condition2 = fields.Many2one('purchase.condition_text', 'Footer',
                                      domain=[('type', '=', 'footer')])
    note1 = fields.Html('Header')
    note2 = fields.Html('Footer')

    @api.onchange('text_condition1')
    def set_header(self):
        if self.text_condition1:
            self.note1 = self.text_condition1.text

    @api.onchange('text_condition2')
    def set_footer(self):
        if self.text_condition2:
            self.note2 = self.text_condition2.text

    @api.multi
    def print_quotation(self):
        self.write({'state': "sent"})
        xml = 'purchase_order_report_with_note.report_purchasequotation_qweb'
        return self.env['report'].get_action(self, xml)

    @api.multi
    def print_purchase(self):
        """
        This function prints the purchase order (already sent)
        """
        xml = 'purchase_order_report_with_note.report_purchaseorder_qweb'
        return self.env['report'].get_action(self, xml)

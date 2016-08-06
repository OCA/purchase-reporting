# -*- coding: utf-8 -*-
##############################################################################
#
#   Copyright (c) 2013 Camptocamp SA (http://www.camptocamp.com)
#   @author Vincent Renaville
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import api, fields, models,  _


class PurchaseConditionText(models.Model):
    """ Purchase order Textual information """
    _name = "purchase.condition_text"
    _description = "purchase conditions"

    name = fields.Char('Condition summary', required=True)
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
        '''
        This function prints the request for quotation and mark it as sent,
        so that we can see more easily the next step of the workflow
        '''
        assert len(self.ids) == 1, '''This option should only be used
        for a single id at a time'''
        self.signal_workflow('send_rfq')
        xml = 'purchase_order_webkit_with_notes.report_purchasequotation_qweb'
        return self.env['report'].get_action(self, xml)

    @api.multi
    def print_purchase(self):
        """
        This function prints the purchase order (already sent)
        """
        xml = 'purchase_order_webkit_with_notes.report_purchaseorder_qweb'
        return self.env['report'].get_action(self, xml)

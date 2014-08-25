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
from openerp.osv import orm, fields
from openerp import netsvc


class PurchaseConditionText(orm.Model):
    """ Purchase order Textual information """
    _name = "purchase.condition_text"
    _description = "purchase conditions"

    _columns = {
        'name': fields.char('Condition summary', required=True, size=128),
        'type': fields.selection([('header', 'Top condition'),
                                  ('footer', 'Bottom condition')],
                                 'type', required=True),
        'text': fields.html('Condition', translate=True, required=True),
    }


class PurchaseOrder(orm.Model):
    """ Adds condition to Po """

    _inherit = "purchase.order"
    _description = 'Purchase Order'

    _columns = {
        'text_condition1': fields.many2one('purchase.condition_text',
                                           'Header',
                                           domain=[('type', '=', 'header')]),
        'text_condition2': fields.many2one('purchase.condition_text',
                                           'Footer',
                                           domain=[('type', '=', 'footer')]),
        'note1': fields.html('Header'),
        'note2': fields.html('Footer')
    }

    def _set_condition(self, cr, uid, inv_id, commentid, key):
        """ Set the text of the notes in purchases """
        if not commentid:
            return {}
        try:
            lang = self.browse(cr, uid, inv_id)[0].partner_id.lang
        except Exception:
            lang = 'en_US'
        cond = self.pool.get('purchase.condition_text').browse(cr, uid,
                                                               commentid,
                                                               {'lang': lang})
        return {'value': {key: cond.text}}

    def set_header(self, cr, uid, inv_id, commentid):
        return self._set_condition(cr, uid, inv_id, commentid, 'note1')

    def set_footer(self, cr, uid, inv_id, commentid):
        return self._set_condition(cr, uid, inv_id, commentid, 'note2')

    def print_quotation(self, cr, uid, ids, context=None):
        """
        This function prints the purchase order and mark it as sent,
        so that we can see more easily the next step of the workflow
        """
        assert len(ids) == 1, \
            "This option should only be used for a single id at a time"
        wf_service = netsvc.LocalService("workflow")
        wf_service.trg_validate(uid, 'purchase.order',
                                ids[0], 'send_rfq', cr)
        datas = {'model': 'purchase.order',
                 'ids': ids,
                 'form': self.read(cr, uid, ids[0], context=context),
                 }
        return {'type': 'ir.actions.report.xml',
                'report_name': 'purchase.quotation.webkit',
                'datas': datas,
                'nodestroy': True}

    def print_purchase(self, cr, uid, ids, context=None):
        """
        This function prints the purchase order (already sent)
        """
        datas = {'model': 'purchase.order',
                 'ids': ids,
                 'form': self.read(cr, uid, ids[0], context=context),
                 }
        return {'type': 'ir.actions.report.xml',
                'report_name': 'purchase.order.webkit',
                'datas': datas,
                'nodestroy': True}

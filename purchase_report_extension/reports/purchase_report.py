# Copyright 2021 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class PurchaseReport(models.Model):
    _inherit = "purchase.report"

    order_id = fields.Many2one(
        comodel_name="purchase.order",
        string="Order",
        readonly=True,
    )
    qty_ordered = fields.Float(string="Qty Ordered", readonly=True)
    qty_received = fields.Float(string="Qty Received", readonly=True)
    qty_billed = fields.Float(string="Qty Billed", readonly=True)
    qty_to_be_billed = fields.Float(string="Qty to be Billed", readonly=True)

    def _select(self):
        return super()._select() + """,
        s.id as order_id,
        sum(l.product_qty / u.factor * u2.factor) as qty_ordered,
        sum(l.qty_received / u.factor * u2.factor) as qty_received,
        sum(l.qty_invoiced / u.factor * u2.factor) as qty_billed,
        case when t.purchase_method = 'purchase'
            then
                sum(l.product_qty / u.factor * u2.factor)
                - sum(l.qty_invoiced / u.factor * u2.factor)
            else
                sum(l.qty_received / u.factor * u2.factor)
                - sum(l.qty_invoiced / u.factor * u2.factor)
        end as qty_to_be_billed
        """

    def _group_by(self):
        return super()._group_by() + ", t.purchase_method, s.id"

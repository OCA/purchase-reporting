# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    hide_in_report = fields.Boolean(
        compute="_compute_hide_in_report", store=True, readonly=False
    )

    @api.depends("company_id", "product_qty", "price_unit")
    def _compute_hide_in_report(self):
        for rec in self:
            if rec.company_id.purchase_hide_in_report_default != "none":
                field = (
                    "product_qty"
                    if rec.company_id.purchase_hide_in_report_default == "quantity"
                    else "price_subtotal"
                )
                rec.hide_in_report = not rec[field]
            else:
                rec.hide_in_report = False

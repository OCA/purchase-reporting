# Copyright 2024 Tecnativa - Pilar Vargas
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from collections import defaultdict

from odoo import models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def get_grouped_data(self):
        grouped_data = defaultdict(lambda: {"partner": None, "order_ids": []})
        for order in self:
            partner = order.partner_id
            grouped_data[partner]["partner"] = partner
            grouped_data[partner]["order_ids"].append(order)
        consolidated_data = []
        for partner, data in grouped_data.items():
            consolidated_data.append(
                {
                    "partner": partner,
                    "order_ids": data["order_ids"],
                }
            )
        return consolidated_data

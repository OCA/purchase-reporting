# Copyright 2024 Tecnativa - Pilar Vargas
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def get_grouped_data(self):
        """Return the recordset grouped by vendor, sorted by vendor name.

        Each item is a dict with the vendor (``partner``) and its orders
        (``order_ids``), which is what the grouped report template renders.
        """
        groups = self.grouped("partner_id")
        return [
            {"partner": partner, "order_ids": orders}
            for partner, orders in sorted(
                groups.items(), key=lambda item: item[0].display_name or ""
            )
        ]

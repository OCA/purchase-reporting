# Copyright 2023 Moduon Team S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)


from odoo import fields, models
from odoo.tools import SQL


class PurchaseReport(models.Model):
    _inherit = "purchase.report"

    product_packaging_id = fields.Many2one(
        "product.packaging",
        string="Packaging",
        readonly=True,
    )
    product_packaging_qty = fields.Float(
        string="Packaging Qty",
        readonly=True,
    )

    def _select(self):
        return SQL(
            """
            %s,
            l.product_packaging_id AS product_packaging_id,
            SUM(l.product_packaging_qty) AS product_packaging_qty
        """,
            super()._select(),
        )

    def _from(self):
        return SQL(
            """
            %s
            LEFT JOIN product_packaging ON l.product_packaging_id = product_packaging.id
        """,
            super()._from(),
        )

    def _group_by(self):
        return SQL(
            """
            %s,
            l.product_packaging_id
        """,
            super()._group_by(),
        )

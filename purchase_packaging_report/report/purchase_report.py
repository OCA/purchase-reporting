# Copyright 2023 Moduon Team S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)


from odoo import fields, models


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
        result = super()._select()
        return f"""
            {result},
            l.product_packaging_id AS product_packaging_id,
            SUM(l.product_packaging_qty) AS product_packaging_qty
        """

    def _from(self):
        result = super()._from()
        return f"""
            {result}
            LEFT JOIN product_packaging ON l.product_packaging_id = product_packaging.id
        """

    def _group_by(self):
        result = super()._group_by()
        return f"{result}, l.product_packaging_id"

# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    purchase_hide_in_report_default = fields.Selection(
        selection=[
            ("none", "None"),
            ("quantity", "Quantity equal to 0"),
            ("price", "Price equal to 0"),
        ],
        required=True,
        default="none",
    )

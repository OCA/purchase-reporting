# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    purchase_hide_in_report_default = fields.Selection(
        related="company_id.purchase_hide_in_report_default",
        readonly=False,
        required=True,
    )

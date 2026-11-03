# Copyright 2026 Quartile (https://www.quartile.co)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo import fields, models


class AccountTaxGroup(models.Model):
    _inherit = "account.tax.group"

    show_tax_column_in_purchase_report = fields.Boolean(
        help="If enabled, always show the Taxes column on the Purchase Order report "
        "for this tax group even when all lines in the order share the same taxes."
    )

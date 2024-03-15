# Copyright 2018 ForgeFlow S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class PurchaseOrder(models.Model):

    _name = "purchase.order"
    _inherit = ["purchase.order", "comment.template"]

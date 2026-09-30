# 2026 Copyright ForgeFlow(https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, models

from odoo.addons.report_xlsx_helper.report.report_xlsx_abstract import (
    ReportXlsxAbstract,
)
from odoo.addons.report_xlsx_helper.report.report_xlsx_format import FORMATS

_render = ReportXlsxAbstract._render


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.model
    def _report_xlsx_fields(self):
        return [
            "order_ref",
            "vendor",
            "date_order",
            "date_planned",
            "product",
            "description",
            "qty",
            "uom",
            "price_unit",
            "discount",
            "taxes",
            "price_subtotal",
        ]

    @api.model
    def _report_xlsx_template(self):
        return {
            "order_ref": {
                "header": {"value": self.env._("Order Reference")},
                "data": {"value": _render("order_line.order_id.name")},
                "width": 20,
            },
            "vendor": {
                "header": {"value": self.env._("Vendor")},
                "data": {"value": _render("order_line.partner_id.name or ''")},
                "width": 30,
            },
            "date_order": {
                "header": {"value": self.env._("Order Date")},
                "data": {
                    "value": _render("order_line.order_id.date_order"),
                    "format": FORMATS["format_tcell_date_left"],
                },
                "width": 15,
            },
            "date_planned": {
                "header": {"value": self.env._("Expected Date")},
                "data": {
                    "value": _render("order_line.date_planned"),
                    "format": FORMATS["format_tcell_date_left"],
                },
                "width": 15,
            },
            "product": {
                "header": {"value": self.env._("Product")},
                "data": {"value": _render("order_line.product_id.name or ''")},
                "width": 30,
            },
            "description": {
                "header": {"value": self.env._("Description")},
                "data": {"value": _render("order_line.name or ''")},
                "width": 40,
            },
            "qty": {
                "header": {
                    "value": self.env._("Qty"),
                    "format": FORMATS["format_theader_yellow_right"],
                },
                "data": {
                    "value": _render("order_line.product_qty"),
                    "format": FORMATS["format_tcell_amount_right"],
                },
                "width": 10,
            },
            "uom": {
                "header": {"value": self.env._("UoM")},
                "data": {"value": _render("order_line.product_uom_id.name or ''")},
                "width": 10,
            },
            "price_unit": {
                "header": {
                    "value": self.env._("Unit Price"),
                    "format": FORMATS["format_theader_yellow_right"],
                },
                "data": {
                    "value": _render("order_line.price_unit"),
                    "format": FORMATS["format_tcell_amount_right"],
                },
                "width": 15,
            },
            "discount": {
                "header": {
                    "value": self.env._("Discount (%)"),
                    "format": FORMATS["format_theader_yellow_right"],
                },
                "data": {
                    "value": _render("order_line.discount"),
                    "format": FORMATS["format_tcell_percent_right"],
                },
                "width": 12,
            },
            "taxes": {
                "header": {"value": self.env._("Taxes")},
                "data": {
                    "value": _render("', '.join(order_line.tax_ids.mapped('name'))"),
                },
                "width": 20,
            },
            "price_subtotal": {
                "header": {
                    "value": self.env._("Subtotal"),
                    "format": FORMATS["format_theader_yellow_right"],
                },
                "data": {
                    "value": _render("order_line.price_subtotal"),
                    "format": FORMATS["format_tcell_amount_right"],
                },
                "width": 15,
            },
        }

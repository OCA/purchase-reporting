# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Purchase Report Shipping Address",
    "version": "16.0.1.0.0",
    "category": "Reporting",
    "website": "https://github.com/OCA/purchase-reporting",
    "license": "AGPL-3",
    "author": "Quartile Limited, Odoo Community Association (OCA)",
    "depends": ["purchase_stock"],
    "data": [
        "views/stock_warehouse_views.xml",
        "reports/purchase_order_templates.xml",
        "reports/purchase_quotation_templates.xml",
    ],
    "installable": True,
}

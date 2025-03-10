# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Purchase Report Hide Line",
    "summary": "Hide purchase order lines from the Purchase Report",
    "version": "17.0.1.0.0",
    "category": "Purchase",
    "website": "https://github.com/OCA/purchase-reporting",
    "author": "Sygel, Odoo Community Association (OCA)",
    "maintainers": ["tisho99"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "purchase",
    ],
    "data": [
        "views/report_purchase.xml",
        "views/purchase_order_views.xml",
        "views/res_config_settings.xml",
    ],
}

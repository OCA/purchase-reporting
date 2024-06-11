# Copyright 2024 Moduon Team S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

{
    "name": "Purchase Packaging Report",
    "summary": "Packaging data in purchase reports",
    "version": "16.0.1.0.1",
    "development_status": "Alpha",
    "category": "Inventory/Purchase",
    "website": "https://github.com/OCA/purchase-reporting",
    "author": "Moduon, Odoo Community Association (OCA)",
    "maintainers": ["Shide"],
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "purchase",
    ],
    "data": [
        "report/purchase_report_views.xml",
        "report/purchase_order_templates.xml",
        "report/purchase_quotation_templates.xml",
    ],
}

# Copyright 2025 Moduon Team S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)
{
    "name": "Purchase order line hide tax in report",
    "summary": "Hide taxes column when they don't add value",
    "version": "18.0.1.0.1",
    "development_status": "Alpha",
    "category": "Purchases",
    "website": "https://github.com/OCA/purchase-reporting",
    "author": "Moduon, Odoo Community Association (OCA)",
    "maintainers": ["chienandalu", "rafaelbn"],
    "license": "LGPL-3",
    "depends": ["purchase"],
    "data": [
        "reports/purchase_order_report_template.xml",
        "views/account_tax_group_views.xml",
    ],
}

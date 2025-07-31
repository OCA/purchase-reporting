# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
{
    "name": "Purchase Order Report Without Tax Column",
    "summary": """
        Hides taxes data in purchase order report
    """,
    "license": "AGPL-3",
    "version": "18.0.1.0.0",
    "author": "Solvos, Odoo Community Association (OCA)",
    "category": "Purchase",
    "website": "https://github.com/OCA/purchase-reporting",
    "depends": ["purchase"],
    "data": [
        "security/purchase_order_security.xml",
        "reports/purchase_order_report.xml",
        "views/res_config_settings.xml",
    ],
    "installable": True,
}

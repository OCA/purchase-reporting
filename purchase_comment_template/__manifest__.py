# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Purchase Comments",
    "summary": "Comments texts templates on Purchase documents",
    "version": "14.0.1.0.0",
    "category": "Purchase",
    "website": "https://github.com/OCA/purchase-reporting",
    "author": "Eficent, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "purchase",
        "base_comment_template",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/purchase_order_view.xml",
        "views/base_comment_template_view.xml",
        "views/report_purchaseorder.xml",
        "views/report_quotation.xml",
    ],
    "installable": True,
}

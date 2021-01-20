# Copyright 2021 Jarsa
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    "name": "Purchase Requisition Comments",
    "summary": "Comments texts templates on Purchase requisition documents",
    "version": "14.0.1.0.0",
    "category": "Purchase",
    "website": "https://github.com/OCA/purchase-reporting",
    "author": "Jarsa, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "depends": [
        "purchase_comment_template",
        "purchase_requisition",
    ],
    "data": [
        "views/purchase_requisition_view.xml",
        "views/report_purchase_requisition.xml",
    ],
    "installable": True,
}

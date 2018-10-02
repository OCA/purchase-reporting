# -*- coding: utf-8 -*-
#   Copyright 2017 Camptocamp SA (http://www.camptocamp.com)
#   @author Vincent Renaville
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Purchase Order Report With Note',
    'version': '10.0.1.0.0',
    'category': 'Reports/Qweb',
    'license': 'AGPL-3',
    "author": "Camptocamp SA,"
              "Eficent, "
              "Serpent CS,"
              "Odoo Community Association (OCA)",
    'website': "https://odoo-community.org/",
    'depends': ['purchase'],
    'data': [
        'security/ir.model.access.csv',
        'report/purchase_report.xml',
        'views/purchase_view.xml',
        'views/report_purchasequotation_qweb.xml',
        'views/report_purchaseorder_qweb.xml',
    ],
    'installable': True,
}

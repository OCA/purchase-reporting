# -*- coding: utf-8 -*-
# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase
from odoo import report


class TestPurchaseOrderReport(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestPurchaseOrderReport, self).setUp()
        self.base_comment_model = self.env['base.comment.template']
        self.before_comment = self._create_comment('before_lines')
        self.after_comment = self._create_comment('after_lines')

        self.purchase_order = self.env.ref('purchase.purchase_order_4')
        self.purchase_order.update({
            'comment_template1_id': self.before_comment.id,
            'comment_template2_id': self.after_comment.id
        })
        self.purchase_order._set_note1()
        self.purchase_order._set_note2()

    def _create_comment(self, position):
        return self.base_comment_model.create({
            'name': 'Comment ' + position,
            'position': position,
            'text': 'Text ' + position
        })

    def test_comments_in_purchase_order(self):
        (res, _) = report. \
            render_report(self.env.cr, self.env.uid, [self.purchase_order.id],
                          'purchase.report_purchaseorder', {})
        self.assertRegexpMatches(res, self.before_comment.text)
        self.assertRegexpMatches(res, self.after_comment.text)

# Copyright 2018 ForgeFlow S.L.
# Copyright 2024 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from ast import literal_eval

from odoo.tests.common import Form, TransactionCase

from odoo.addons.mail.tests.common import mail_new_test_user


class TestPurchaseOrderReport(TransactionCase):
    def setUp(self):
        super().setUp()
        self.company = self.env.ref("base.main_company")
        self.base_comment_model = self.env["base.comment.template"]
        self.before_comment = self._create_comment("purchase.order", "before_lines")
        self.after_comment = self._create_comment("purchase.order", "after_lines")
        self.partner = self.env["res.partner"].create({"name": "Partner Test"})
        self.partner.base_comment_template_ids = [
            (4, self.before_comment.id),
            (4, self.after_comment.id),
        ]
        self.purchase_order = self.env.ref("purchase.purchase_order_4")
        self.purchase_order.update(
            {
                "comment_template_ids": [
                    (4, self.before_comment.id),
                    (4, self.after_comment.id),
                ],
            }
        )

    def _create_comment(self, models, position):
        return self.base_comment_model.create(
            {
                "name": "Comment " + position,
                "company_id": self.company.id,
                "position": position,
                "text": "Text " + position,
                "models": models,
            }
        )

    def test_comments_in_purchase_order(self):
        res = self.env["ir.actions.report"]._render_qweb_html(
            "purchase.report_purchaseorder", self.purchase_order.ids
        )
        self.assertRegex(str(res[0]), self.before_comment.text)
        self.assertRegex(str(res[0]), self.after_comment.text)

    def test_onchange_partner_id(self):
        with Form(self.env["purchase.order"]) as new_purchase:
            new_purchase.partner_id = self.partner
            self.assertEqual(len(new_purchase.comment_template_ids), 2)

    def test_open_comments_menu(self):
        """The Purchase Manager (without Access Rights) can open the comments menu."""
        # Arrange
        purchase_manager = mail_new_test_user(
            self.env,
            login="purchase_manager",
            groups="purchase.group_purchase_manager",
        )
        comments_menu = self.env.ref(
            "purchase_comment_template.menu_base_comment_template_purchase"
        )
        comments_action = comments_menu.action
        comments_action_domain = literal_eval(comments_action.domain)
        comments_model = self.env[comments_action.res_model]
        # pre-condition
        self.assertNotIn(
            self.env.ref("base.group_erp_manager"), purchase_manager.groups_id
        )

        # Act
        comments = comments_model.with_user(purchase_manager).search(
            comments_action_domain
        )

        # Assert
        self.assertTrue(comments)

    def test_comments_menu_multi_model(self):
        """Comments for multiple model can be found in the comments menu."""
        # Arrange
        comments_menu = self.env.ref(
            "purchase_comment_template.menu_base_comment_template_purchase"
        )
        comments_action = comments_menu.action
        comments_action_domain = literal_eval(comments_action.domain)
        comments_model = self.env[comments_action.res_model]
        user_ir_model = self.env.ref("base.model_res_users")
        user_ir_model.is_comment_template = True
        multi_model_comment = self._create_comment(
            ",".join(
                [
                    self.purchase_order._name,
                    user_ir_model.model,
                ]
            ),
            "before_lines",
        )
        # pre-condition
        self.assertGreater(len(multi_model_comment.model_ids), 1)

        # Act
        comments = comments_model.search(comments_action_domain)

        # Assert
        self.assertIn(multi_model_comment, comments)

    def test_create_from_comments_menu(self):
        """Comments created from the purchase comments menu
        are purchase order comments by default."""
        # Arrange
        comments_menu = self.env.ref(
            "purchase_comment_template.menu_base_comment_template_purchase"
        )
        comments_action = comments_menu.action
        comments_action_context = literal_eval(comments_action.context)
        comments_model = self.env[comments_action.res_model].with_context(
            **comments_action_context
        )

        # Act
        comment_form = Form(comments_model)
        comment_form.name = "Test purchase comment"
        comment_form.text = "Test text"
        comment = comment_form.save()

        # Assert
        self.assertEqual(comment.model_ids.model, self.purchase_order._name)

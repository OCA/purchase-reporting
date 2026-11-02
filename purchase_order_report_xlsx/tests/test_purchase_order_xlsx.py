# 2026 Copyright ForgeFlow(https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo.fields import Command

from odoo.addons.base.tests.common import BaseCommon


class TestPurchaseOrderXlsx(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env["product.product"].create({"name": "Test Product"})
        cls.po = cls.env["purchase.order"].create(
            {
                "partner_id": cls.partner.id,
                "order_line": [
                    Command.create(
                        {
                            "name": cls.product.name,
                            "product_id": cls.product.id,
                            "product_qty": 2.0,
                            "price_unit": 50.0,
                        }
                    )
                ],
            }
        )
        ctx = {
            "report_name": "purchase_order_report_xlsx.purchase_order_xlsx",
            "active_model": "purchase.order",
            "active_ids": cls.po.ids,
        }
        cls.report = cls.env["ir.actions.report"].with_context(**ctx)

    def test_report_renders(self):
        result = self.report._render_xlsx(None, None, None)
        self.assertEqual(result[1], "xlsx")

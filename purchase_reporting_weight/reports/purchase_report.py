# Copyright 2017 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# Copyright 2018 David Vidal <david.vidal@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, tools


class PurchaseReport(models.Model):
    _inherit = "purchase.report"

    def _select(self):
        return """
            , CASE
                WHEN u.category_id = imd.res_id
                THEN SUM(l.product_qty / u.factor * u2.factor)
                ELSE SUM(p.weight * l.product_qty / u.factor * u2.factor)
            END AS weight
            """

    def _from(self):
        return """
            JOIN ir_model_data imd
                ON (imd.module = 'product' AND
                    imd.name = 'product_uom_categ_kgm')
            """

    def _group_by(self):
        return ", p.weight, u.category_id, imd.res_id"

    @api.model_cr
    def init(self):
        """Inject parts in the query with this hack, fetching the query and
        recreating it. Query is returned all in upper case and with final ';'.
        """
        super(PurchaseReport, self).init()
        self._cr.execute("SELECT pg_get_viewdef(%s, true)", (self._table,))
        view_def = self._cr.fetchone()[0]
        view_def = view_def.replace(
            "sum(p.weight * l.product_qty/u.factor*u2.factor) as weight,",
            "{}".format(self._select()),
        )
        view_def = view_def.replace(
            "GROUP BY", " {} GROUP BY".format(self._from()),
        )
        if view_def[-1] == ';':
            view_def = view_def[:-1]
        view_def += self._group_by()
        # Re-create view
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("create or replace view {} as ({})".format(
            self._table, view_def,
        ))

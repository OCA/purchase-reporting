# -*- coding: utf-8 -*-
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#    Copyright 2015 Camptocamp SA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from openerp import tools, models, fields


class PurchaseStockAnalysis(models.Model):
    _name = "purchase.stock.analysis"
    _description = "Purchases Stock Analysis"
    _auto = False

    date_order = fields.Datetime(
        readonly=True,
        help="Date on which this document has been created")
    state = fields.Selection(
        [('draft', 'Request for Quotation'),
         ('confirmed', 'Waiting Supplier Ack'),
         ('approved', 'Approved'),
         ('except_picking', 'Shipping Exception'),
         ('except_invoice', 'Invoice Exception'),
         ('done', 'Done'),
         ('cancel', 'Cancelled')], readonly=True)
    product_id = fields.Many2one('product.product', readonly=True)
    picking_type_id = fields.Many2one('stock.warehouse', readonly=True)
    location_id = fields.Many2one('stock.location', 'Destination',
                                  readonly=True)
    partner_id = fields.Many2one('res.partner', 'Supplier', readonly=True)
    pricelist_id = fields.Many2one('product.pricelist', 'Pricelist',
                                   readonly=True)
    date_approve = fields.Date('Date Approved', readonly=True)
    expected_date = fields.Date('Expected Date', readonly=True)
    validator = fields.Many2one('res.users', 'Validated By', readonly=True)
    product_uom = fields.Many2one('product.uom', 'Reference Unit of Measure',
                                  required=True)
    company_id = fields.Many2one('res.company', 'Company', readonly=True)
    user_id = fields.Many2one('res.users', 'Responsible', readonly=True)

    delay = fields.Float(
        'Days to Validate', digits=(16, 2), readonly=True,
        help='Days between the Order Date and the Date Approval')

    # was delay_pass in purchase analysis
    days_to_deliver = fields.Float(
        digits=(16, 2), readonly=True,
        help='Days between the Order Date and the initial Scheduled Date')

    days_initial_to_updated_schedule = fields.Float(
        digits=(16, 2), readonly=True,
        help='Days from initial to updated Scheduled Date of Delivery')

    days_schedule_to_actual_delivery = fields.Float(
        digits=(16, 2), readonly=True,
        help='Days from the updated Scheduled Date of Delivery and the actual'
        'Delivery Date')

    unit_quantity = fields.Integer('Unit Quantity', readonly=True)
    price_total = fields.Float('Total Price', readonly=True)
    price_average = fields.Float('Average Price', readonly=True,
                                 group_operator="avg")
    negociation = fields.Float('Purchase-Standard Price', readonly=True,
                               group_operator="avg")
    price_standard = fields.Float(readonly=True, group_operator="sum")
    category_id = fields.Many2one('product.category', readonly=True)

    _order = 'date_order desc, price_total desc'

    def init(self, cr):
        tools.sql.drop_view_if_exists(cr, 'purchase_stock_analysis')
        cr.execute("""
            create or replace view purchase_stock_analysis as (
                {with_as}
                {select}
                {from_join}
                {group_by}
            );
        """.format(with_as=self._with_as(),
                   select=self._select(),
                   from_join=self._from_join(),
                   group_by=self._group_by(),
                   ))

    def _with_as(self):
        return """
            WITH currency_rate (currency_id, rate, date_start, date_end)
            AS (
                SELECT r.currency_id, r.rate, r.name AS date_start,
                    (SELECT name FROM res_currency_rate r2
                    WHERE r2.name > r.name AND
                        r2.currency_id = r.currency_id
                        ORDER BY r2.name ASC
                        LIMIT 1) AS date_end
                FROM res_currency_rate r
            )
            """

    def _select(self):
        return """
            SELECT
                MIN(l.id) as id,
                s.date_order as date_order,
                l.state,
                s.date_approve,
                s.minimum_planned_date as expected_date,
                s.dest_address_id,
                s.pricelist_id,
                s.validator,
                spt.warehouse_id as picking_type_id,
                s.partner_id as partner_id,
                s.create_uid as user_id,
                s.company_id as company_id,
                l.product_id,
                t.categ_id as category_id,
                t.uom_id as product_uom,
                s.location_id as location_id,
                sum(l.product_qty/u.factor*u2.factor) as unit_quantity,
                extract(epoch from age(s.date_approve,s.date_order)) /
                    (24*60*60)::decimal(16,2) as delay,

                extract(epoch from age(l.date_planned,s.date_order)) /
                (24*60*60)::decimal(16,2) as days_to_deliver,

                extract(epoch from move.date_expected - l.date_planned)
                        / (24*60*60)::decimal(16,2)
                        as days_initial_to_updated_schedule,
                extract(epoch from move.date - move.date_expected)
                        / (24*60*60)::decimal(16,2)
                        as days_schedule_to_actual_delivery,

                SUM(l.price_unit * cr.rate * l.product_qty)::decimal(16, 2)
                    as price_total,
                AVG(100.0 * (l.price_unit * cr.rate * l.product_qty) /
                    NULLIF(ip.value_float * l.product_qty / u.factor
                        * u2.factor, 0.0))::decimal(16,2) as negociation,
                SUM(ip.value_float * l.product_qty/u.factor
                    * u2.factor)::decimal(16,2) as price_standard,
                (SUM(l.product_qty*cr.rate*l.price_unit)/
                    NULLIF(sum(l.product_qty/u.factor*u2.factor),
                            0.0))::decimal(16,2) as price_average
        """

    def _from_join(self):
        return """
                FROM purchase_order_line l
                    JOIN purchase_order s on (l.order_id=s.id)
                        LEFT JOIN product_product p on (l.product_id=p.id)
                            LEFT JOIN product_template t
                                ON (p.product_tmpl_id=t.id)
                            LEFT JOIN ir_property ip ON
                                (ip.name='standard_price'
                                 AND ip.res_id=CONCAT('product.template,',t.id)
                                 AND ip.company_id=s.company_id)
                    LEFT JOIN product_uom u on (u.id=l.product_uom)
                    LEFT JOIN product_uom u2 on (u2.id=t.uom_id)
                    LEFT JOIN stock_picking_type spt
                        on (spt.id=s.picking_type_id)
                    JOIN currency_rate cr ON (cr.currency_id = s.currency_id
                        AND cr.date_start <= coalesce(s.date_order, now()) AND
                        (cr.date_end IS NULL
                         OR cr.date_end > COALESCE(s.date_order, now())))
                    LEFT JOIN stock_move move ON (move.purchase_line_id=l.id)
                    """

    def _group_by(self):
        return """
            GROUP BY
            s.company_id,
            s.create_uid,
            s.partner_id,
            u.factor,
            s.location_id,
            l.price_unit,
            s.date_approve,
            l.date_planned,
            l.product_uom,
            s.minimum_planned_date,
            s.pricelist_id,
            s.validator,
            s.dest_address_id,
            l.product_id,
            t.categ_id,
            s.date_order,
            l.state,
            spt.warehouse_id,
            u.uom_type,
            u.category_id,
            t.uom_id,
            u.id,
            u2.factor,
            move.date,
            move.date_expected
            """

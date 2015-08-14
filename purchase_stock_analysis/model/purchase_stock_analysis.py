# -*- coding: utf-8 -*-

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

    delay = fields.Float('Days to Validate', digits=(16, 2), readonly=True)
    delay_pass = fields.Float('Days to Deliver', digits=(16, 2), readonly=True)

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
                select
                    min(l.id) as id,
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
                        (24*60*60)::decimal(16,2) as delay_pass,
                    sum(l.price_unit * cr.rate * l.product_qty)::decimal(16, 2)
                        as price_total,
                    avg(100.0 * (l.price_unit * cr.rate * l.product_qty) /
                        NULLIF(ip.value_float * l.product_qty / u.factor
                            * u2.factor, 0.0))::decimal(16,2) as negociation,
                    sum(ip.value_float * l.product_qty/u.factor
                        * u2.factor)::decimal(16,2) as price_standard,
                    (sum(l.product_qty*cr.rate*l.price_unit)/
                        NULLIF(sum(l.product_qty/u.factor*u2.factor),
                               0.0))::decimal(16,2) as price_average
                from purchase_order_line l
                    join purchase_order s on (l.order_id=s.id)
                        left join product_product p on (l.product_id=p.id)
                            left join product_template t
                                on (p.product_tmpl_id=t.id)
                            LEFT JOIN ir_property ip ON
                                (ip.name='standard_price'
                                 AND ip.res_id=CONCAT('product.template,',t.id)
                                 AND ip.company_id=s.company_id)
                    left join product_uom u on (u.id=l.product_uom)
                    left join product_uom u2 on (u2.id=t.uom_id)
                    left join stock_picking_type spt
                        on (spt.id=s.picking_type_id)
                    join currency_rate cr on (cr.currency_id = s.currency_id
                        and cr.date_start <= coalesce(s.date_order, now()) and
                        (cr.date_end is null
                         or cr.date_end > coalesce(s.date_order, now())))
                    left join stock_move move on (move.purchase_line_id=l.id)
                group by
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
                    u2.factor
            )
        """)

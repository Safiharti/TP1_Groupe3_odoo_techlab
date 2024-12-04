from odoo import models, fields, api

class ProductPerformance(models.Model):
    _name = 'product.performance'
    _description = 'Product Performance'
    
    product_id = fields.Many2one('product.product', string="Product", required=True)
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    total_sales = fields.Float(string="Total Sales", compute='_compute_total_sales', store=True)

    @api.depends('product_id', 'start_date', 'end_date')
    def _compute_total_sales(self):
        for record in self:
            sales = self.env['sale.order.line'].search([
                ('product_id', '=', record.product_id.id),
                ('order_id.date_order', '>=', record.start_date),
                ('order_id.date_order', '<=', record.end_date)
            ])
            record.total_sales = sum(sale.price_total for sale in sales)

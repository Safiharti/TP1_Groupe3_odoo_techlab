from odoo import models, fields, api

class CustomerLoyalty(models.Model):
    _name = 'customer.loyalty'
    _description = 'Customer Loyalty'

    partner_id = fields.Many2one('res.partner', string="Customer", required=True)
    total_orders = fields.Integer(string="Total Orders", compute='_compute_total_orders', store=True)
    average_spent = fields.Float(string="Average Spent", compute='_compute_average_spent', store=True)

    @api.depends('partner_id.sale_order_ids')
    def _compute_total_orders(self):
        for customer in self:
            customer.total_orders = len(customer.partner_id.sale_order_ids)

    @api.depends('partner_id.sale_order_ids.amount_total')
    def _compute_average_spent(self):
        for customer in self:
            total_amount = sum(order.amount_total for order in customer.partner_id.sale_order_ids)
            customer.average_spent = total_amount / customer.total_orders if customer.total_orders > 0 else 0

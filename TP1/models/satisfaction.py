from odoo import models, fields

class Satisfaction(models.Model):
    _name = 'sale.satisfaction'
    _description = 'Employee-Customer Satisfaction'

    sale_id = fields.Many2one('sale.order', string="Sale Order")
    employee_id = fields.Many2one('hr.employee', string="Employee")
    customer_id = fields.Many2one('res.partner', string="Customer")
    satisfaction_level = fields.Selection([
        ('very_bad', 'Very Bad'),
        ('bad', 'Bad'),
        ('neutral', 'Neutral'),
        ('good', 'Good'),
        ('very_good', 'Very Good'),
    ], string="Satisfaction Level", required=True)

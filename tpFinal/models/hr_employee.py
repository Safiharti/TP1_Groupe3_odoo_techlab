from odoo import models, fields

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    max_orders = fields.Integer("Max Orders", default=5)

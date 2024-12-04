from odoo import models, fields, api

class EmployeePerformance(models.Model):
    _name = 'employee.performance'
    _description = 'Employee Performance'

    employee_id = fields.Many2one('hr.employee', string="Employee", required=True)
    product_performance_ids = fields.One2many('product.performance', 'employee_id', string="Product Performance")

from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    max_orders = fields.Integer(
        string="Commandes Max Simultanées",
        default=5,
        help="Nombre maximum de commandes qu'un employé peut gérer simultanément."
    )
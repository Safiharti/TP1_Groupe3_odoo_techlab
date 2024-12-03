from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    max_open_orders = fields.Integer(string='Max Open Orders', default=5)
    current_open_orders = fields.Integer(string='Current Open Orders', compute='_compute_current_open_orders')

    @api.depends('user_id')
    def _compute_current_open_orders(self):
        for employee in self:
            # Calculer le nombre de commandes ouvertes pour cet employé
            employee.current_open_orders = self.env['sale.order'].search_count([
                ('user_id', '=', employee.user_id.id),  # Vérifier l'utilisateur associé à l'employé
                ('state', '=', 'sale'),  # Commande confirmée
                ('invoice_status', '=', 'invoiced'),  # Commande n'ayant pas encore été totalement facturée
                ('invoice_ids.state', '=', 'posted')  # La facture doit être validée et prête à être payée
            ])

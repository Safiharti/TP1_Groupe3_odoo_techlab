from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, vals):
        employee = self.env['hr.employee'].browse(vals.get('user_id'))
        if employee:
            # Vérifier les commandes en cours de l'employé
            orders_in_progress = self.search_count([
                ('user_id', '=', employee.id),
                ('invoice_status', '!=', 'invoiced')  # Factures non payées
            ])
            if orders_in_progress >= employee.max_orders:
                raise ValidationError(
                    f"L'employé {employee.name} a atteint la limite de {employee.max_orders} commandes simultanées."
                )
        return super(SaleOrder, self).create(vals)

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    
    tax_id = fields.Many2many(
        'account.tax', 
        string='Taxes',
        domain=lambda self: self._get_tax_domain()
    )

    @api.model
    def _get_tax_domain(self):
        company_id = self.env.context.get('default_company_id') or self.env.company.id
        return ['|', ('company_id', '=', False), ('company_id', 'parent_of', company_id)]

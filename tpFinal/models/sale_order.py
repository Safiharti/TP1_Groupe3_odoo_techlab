from odoo import models, fields, api
from odoo.exceptions import ValidationError
from num2words import num2words

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Champ pour le montant en lettres
    amount_total_in_words = fields.Char(
        string="Montant total en lettres",
        compute="_compute_amount_total_in_words",
        store=True
    )

    @api.depends('amount_total')
    def _compute_amount_total_in_words(self):
        for order in self:
            order.amount_total_in_words = num2words(order.amount_total, lang='fr').capitalize()

    @api.model
    def create(self, vals):
        # Vérification que le champ partenaire (partner_id) est présent
        if not vals.get('partner_id'):
            raise ValidationError("Vous devez sélectionner un client pour cette commande.")

        # Vérifie si un utilisateur (user_id) est défini
        user_id = vals.get('user_id')
        if user_id:
            # Recherche de l'employé associé à cet utilisateur
            employee = self.env['hr.employee'].search([('user_id', '=', user_id)], limit=1)
            if employee:
                # Compte les commandes en cours pour cet employé
                orders_in_progress = self.search_count([
                    ('user_id', '=', user_id),
                    ('invoice_status', '!=', 'invoiced')
                ])
                if orders_in_progress >= employee.max_orders:
                    raise ValidationError(
                        f"L'employé {employee.name} a atteint la limite de {employee.max_orders} commandes simultanées."
                    )

        # Appel de la méthode de création parente
        return super(SaleOrder, self).create(vals)

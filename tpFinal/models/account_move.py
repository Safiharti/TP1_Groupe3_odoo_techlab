from odoo import models, fields, api
from odoo.addons.moduletmp import amount_to_text  # Assurez-vous que la fonction est disponible

class AccountMove(models.Model):
    _inherit = 'account.move'

    # Ajout du champ 'amount_total_in_words' pour stocker le montant en mots
    amount_total_in_words = fields.Char(
        string='Amount in Words',
        compute='_compute_amount_total_in_words',
        store=True,  # Champ maintenant stocké dans la base de données
    )

    @api.depends('amount_total')
    def _compute_amount_total_in_words(self):
        for record in self:
            # Utilisation de la fonction amount_to_text pour convertir le montant en mots
            record.amount_total_in_words = amount_to_text.amount_to_text(record.amount_total)

from odoo import models, fields, api
from num2words import num2words


class AccountMove(models.Model):
    _inherit = 'account.move'

    # Champ calculé pour afficher le montant total en lettres
    amount_total_in_words = fields.Char(
        string="Montant total en lettres",
        compute="_compute_amount_total_in_words",
        store=True
    )

    def action_open_cancel_reason_wizard(self):
        """Ouvre le wizard pour saisir la raison d'annulation."""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Raison d\'annulation',
            'res_model': 'cancel.reason.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_invoice_id': self.id},
        }

    def action_cancel_with_reason(self, reason):
        """Annule la facture avec une raison spécifiée."""
        self.write({'state': 'cancel'})  # Passe l'état de la facture à "annulée".
        self.message_post(body=f"Facture annulée avec la raison : {reason}")

    @api.depends('amount_total', 'currency_id')
    def _compute_amount_total_in_words(self):
        """Calcul du montant total en lettres avec la devise."""
        for move in self:
            if move.amount_total:
                try:
                    # Vérifiez que la devise existe
                    if not move.currency_id:
                        move.amount_total_in_words = "Devise non définie"
                        continue

                    # Convertir la partie entière en lettres
                    main_amount_in_words = num2words(int(move.amount_total), lang='fr')

                    # Convertir les centimes si existants
                    cents = int(round(move.amount_total % 1 * 100))
                    cents_in_words = num2words(cents, lang='fr') if cents > 0 else ""

                    # Récupérer le nom de la devise
                    currency_name = move.currency_id.currency_unit_label or move.currency_id.name

                    # Construire le texte final
                    if cents > 0:
                        move.amount_total_in_words = f"{main_amount_in_words.capitalize()} {currency_name} et {cents_in_words} centimes"
                    else:
                        move.amount_total_in_words = f"{main_amount_in_words.capitalize()} {currency_name}"

                except Exception as e:
                    move.amount_total_in_words = f"Erreur : {str(e)}"
            else:
                move.amount_total_in_words = ""

    # Forcer le calcul du montant en lettres après la confirmation
    def action_post(self):
        """Override the action_post method to recalculate the total amount in words."""
        res = super(AccountMove, self).action_post()  # Appeler la méthode originale
        for move in self:
            move._compute_amount_total_in_words()  # Recalculer le montant en lettres après confirmation
        return res

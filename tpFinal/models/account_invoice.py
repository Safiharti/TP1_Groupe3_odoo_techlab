from odoo import models, fields, api
from odoo.exceptions import UserError

class AccountInvoice(models.Model):
    _inherit = 'account.move'
    
    # Ajout d'un champ 'responsable de facture' (utilisateur)
    responsable_de_facture = fields.Many2one('res.users', string='Responsable de facture')

    # Champ d'état personnalisé pour l'étape "En attente de responsable"
    state = fields.Selection(
        [
            ('draft', 'Brouillon'),
            ('waiting_for_responsible', 'En attente de responsable de facture'),
            ('posted', 'Publié'),
            ('cancel', 'Annulé'),
        ],
         string='État'
    )

    seuil_montant = 10000  # Seuil de montant (exemple : 10 000)

    @api.model
    def create(self, vals):
        # Si la facture dépasse un certain montant, on la place en état "En attente de responsable de facture"
        if vals.get('amount_total', 0.0) > self.seuil_montant:
            vals['state'] = 'waiting_for_responsible'
        return super(AccountInvoice, self).create(vals)

    def action_post(self):
        # Vérification si le montant dépasse le seuil et qu'un responsable a été désigné
        for record in self:
            if record.amount_total > self.seuil_montant and not record.responsable_de_facture:
                raise UserError("La facture dépasse le seuil de montant et nécessite un responsable pour validation.")
        
        # Si tout est bon, on passe l'état à "validé" ou autre selon le processus
        return super(AccountInvoice, self).action_post()

    def action_validate_invoice(self):
        for record in self:
            if record.amount_total > self.seuil_montant and record.state != 'waiting_for_responsible':
                # Si la facture dépasse le seuil, elle doit être mise en attente d'approbation
                record.write({'state': 'waiting_for_responsible'})
                return True

            if record.responsable_de_facture and record.state == 'waiting_for_responsible':
                # Si la facture est en attente d'approbation et qu'un responsable a été désigné, elle peut être validée
                record.write({'state': 'posted'})
                return True

        raise UserError("Seul le responsable peut valider cette facture.")
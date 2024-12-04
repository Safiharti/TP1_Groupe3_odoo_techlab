from odoo import models, fields, api
from odoo.addons.moduletmp import amount_to_text  # Assurez-vous que la fonction est disponible
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'

    # Champ pour stocker la raison d'annulation
    cancel_reason = fields.Char(string="Raison d'annulation", help="Raison pour l'annulation de la facture")

    # Champ 'amount_total_in_words' pour stocker le montant en mots
    amount_total_in_words = fields.Char(
        string='Montant en mots',
        compute='_compute_amount_total_in_words',
        store=True,  # Champ maintenant stocké dans la base de données
    )


    @api.depends('amount_total')
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

    decoration_class = fields.Char('Decoration Class', compute='_compute_decoration_class')

    def action_cancel_invoice_with_reason(self):
            """
            Action pour annuler une facture avec une raison. Si aucune raison n'est fournie, 
            un wizard peut être déclenché pour la saisir.
            """
            for record in self:
                if record.state != 'draft':
                    raise UserError("Seules les factures en état 'Brouillon' peuvent être annulées.")
                # Exemple : Définir une raison par défaut ou ouvrir un wizard
                record.write({
                    'state': 'cancel',
                    'cancel_reason': 'Annulé directement depuis la vue liste.',
                })

    def confirm_cancel_reason(self):
        """
        Confirmation de l'annulation avec une raison fournie via le wizard.
        """
        for record in self:
            if not record.cancel_reason:
                raise UserError("Vous devez fournir une raison pour annuler la facture.")
            
            record.write({'state': 'cancel'})


    

    state = fields.Selection(
    [
        ('draft', 'Draft'),
        ('posted', 'Posted'),
        ('cancel', 'Cancelled'),
    ],
    string='Status',
    readonly=True,
    copy=False,
    index=True,
    tracking=True,
    )



    amount_total = fields.Monetary(string='Total Amount', compute='_compute_amount_total')

    def _compute_amount_total(self):
        for record in self:
            record.amount_total = sum(line.price_subtotal for line in record.invoice_line_ids)

        decoration_class = fields.Selection(
            selection=[('info', 'Info'), ('warning', 'Warning'), ('danger', 'Danger'), ('none', 'None')],
            compute='_compute_decoration_class',
            string="Decoration Class",
            store=False
        )

    @api.depends('amount_total')
    def _compute_decoration_class(self):
        """Détermine la classe CSS de décoration en fonction des paramètres configurés."""
        Param = self.env['ir.config_parameter']
        warning_threshold = float(Param.get_param('account_move.warning_threshold', default=40000))
        danger_threshold = float(Param.get_param('account_move.danger_threshold', default=40000))

        for move in self:
            if move.amount_total >= danger_threshold:
                move.decoration_class = 'danger'
            elif move.amount_total >= warning_threshold:
                move.decoration_class = 'warning'
            else:
                move.decoration_class = 'none'
    
    
    def action_post(self):
        """Override the action_post method to recalculate the total amount in words."""
        res = super(AccountMove, self).action_post()  # Appeler la méthode originale
        for move in self:
            move._compute_amount_total_in_words()  # Recalculer le montant en lettres après confirmation
        return res
                
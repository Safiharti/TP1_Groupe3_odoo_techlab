from odoo import models, fields,api

class PaymentMethodRule(models.Model):
    _name = 'payment.method.rule'
    _description = 'Règle de méthode de paiement'

    name = fields.Char(string="Nom de la règle", required=True)
    min_amount = fields.Float(string="Montant minimum", required=True)
    max_amount = fields.Float(string="Montant maximum", required=True)
    payment_method_id = fields.Many2one('account.payment.method', string="Méthode de paiement", required=True)

    @api.model
    def get_payment_method(self, amount):
        """
        Cette méthode retourne la méthode de paiement selon les règles définies
        en fonction du montant donné.
        """
        rules = self.search([('min_amount', '<=', amount), ('max_amount', '>=', amount)])
        if rules:
            return rules[0].payment_method_id
        return None
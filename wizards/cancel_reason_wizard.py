from odoo import models, fields


class CancelReasonWizard(models.TransientModel):
    _name = 'cancel.reason.wizard'
    _description = 'Popup pour saisir la raison d\'annulation'

    invoice_id = fields.Many2one('account.move', string='Facture', required=True)
    reason = fields.Text(string='Raison', required=True)

    def confirm_cancel(self):
        """Appelle la méthode pour annuler la facture avec la raison."""
        self.invoice_id.action_cancel_with_reason(self.reason)
        return {'type': 'ir.actions.act_window_close'}

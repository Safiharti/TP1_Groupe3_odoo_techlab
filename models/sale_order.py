from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_create_invoice(self):
        """
        Crée une facture à partir de la commande confirmée.
        """
        for order in self:
            if order.state != 'sale':
                raise UserError("Vous ne pouvez créer une facture que pour une commande confirmée.")

            # Vérifie si une facture est déjà liée
            if order.invoice_status == 'invoiced':
                raise UserError("Toutes les lignes de cette commande ont déjà été facturées.")

            # Création de la facture via le wizard de facturation
            invoice = self.env['account.move'].create({
                'move_type': 'out_invoice',  # Facture client
                'partner_id': order.partner_id.id,  # Client associé
                'invoice_origin': order.name,  # Référence à la commande
                'invoice_line_ids': [
                    (0, 0, {
                        'product_id': line.product_id.id,
                        'quantity': line.product_uom_qty,
                        'price_unit': line.price_unit,
                        'name': line.name,
                        'tax_ids': [(6, 0, line.tax_id.ids)]
                    }) for line in order.order_line
                ],
            })

            # Lien entre la commande et la facture
            order.write({'invoice_ids': [(4, invoice.id)]})

            # Mise à jour du statut de facturation
            order._compute_invoice_status()

        return True

    def action_confirm(self):
        for order in self:
            employee = self.env['hr.employee'].search([('user_id', '=', order.user_id.id)], limit=1)

            # Vérifier si l'employé a atteint sa limite de commandes ouvertes
            if employee and employee.max_open_orders > 0:
                open_orders = self.env['sale.order'].search_count([
                    ('user_id', '=', order.user_id.id),
                    ('state', '=', 'sale'),
                    ('invoice_status', '=', 'invoiced'),  # Commande à facturer
                    ('invoice_ids.state', '=', 'posted')  # Facture confirmée et prête à être payée
                ])
                if open_orders >= employee.max_open_orders:
                    raise ValidationError(
                        f"L'employé {employee.name} ne peut pas gérer plus de {employee.max_open_orders} commandes ouvertes. "
                        f"Nombre actuel de commandes ouvertes : {open_orders}."
                    )

        # Appel de la méthode d'origine pour confirmer la commande
        return super(SaleOrder, self).action_confirm()

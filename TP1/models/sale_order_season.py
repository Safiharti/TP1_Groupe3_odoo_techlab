from odoo import models, fields

# Ajout du champ 'season_id' au modèle existant 'sale.order'
class SaleOrder(models.Model):
    _inherit = 'sale.order'  # Héritage du modèle existant

    season_id = fields.Many2one('sale.season', string="Sales Season")

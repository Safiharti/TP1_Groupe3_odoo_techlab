from odoo import models, fields

class SaleSeason(models.Model):
    _name = 'sale.season'
    _description = 'Sales Season'

    name = fields.Char(string="Season Name", required=True)
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    sale_ids = fields.One2many('sale.order', 'season_id', string="Sales Orders")

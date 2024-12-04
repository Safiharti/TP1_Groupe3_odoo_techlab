from odoo import models, fields

class ProductRecommendation(models.Model):
    _name = 'product.recommendation'
    _description = 'Product Recommendation'

    customer_id = fields.Many2one('res.partner', string="Customer")
    recommended_product_ids = fields.Many2many('product.product', string="Recommended Products")

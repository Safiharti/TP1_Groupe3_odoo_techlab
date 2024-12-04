from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    account_move_warning_threshold = fields.Float(
        string="Warning Threshold",
        config_parameter='account_move.warning_threshold',
        default=40000
    )
    account_move_danger_threshold = fields.Float(
        string="Danger Threshold",
        config_parameter='account_move.danger_threshold',
        default=40000
    )

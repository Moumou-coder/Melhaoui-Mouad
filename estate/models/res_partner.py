from odoo import fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'
    limit_amount_sale_order = fields.Monetary(string='Limit Amount Training', currency_field='currency_id', digits=(12, 2))


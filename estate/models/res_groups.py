from odoo import fields, models

class ResGroups(models.Model):
    _inherit = 'res.groups'
    max_amount = fields.Float(string = "training max price (Approval)")
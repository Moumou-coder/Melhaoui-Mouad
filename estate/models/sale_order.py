from odoo import api, models, _, fields
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    def action_confirm(self):

        res = super().action_confirm()

        event = self.env['calendar.event'].create({
            'partner_id': self.partner_id.id,
            'name': self.name,
            'start': self.date_order,
            'stop': self.date_order,
            'allday': True,
        })
        
        return res

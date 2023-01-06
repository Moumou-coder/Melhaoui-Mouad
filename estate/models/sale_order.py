from odoo import api, models, _, fields
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    
    def action_confirm(self):
        
        res = super().action_confirm()

        order_line_id = self.order_line.id
        order_line = self.env['sale.order.line'].browse(order_line_id)
        training_date = order_line.training_date
        
        event = self.env['calendar.event'].create({
            'name': self.name,
            'start': self.training_date,
            'stop': self.training_date,
            'allday': True,
            'partner_id': self.partner_id.id,
        })
        
        return res

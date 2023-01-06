from odoo import api, models, _, fields
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    sale_order_line = self.env['sale.order.line']
    
    def action_confirm(self):

        res = super().action_confirm()
        sale_order_line_date = sale_order_line.training_date

        event = self.env['calendar.event'].create({
            'partner_id': self.partner_id,
            'name': self.name,
            'start': sale_order_line_date,
            #'stop': self.training_date,
            'allday': True,
        })
        
        return res

from odoo import api, models, _, fields
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    def action_confirm(self):

        res = super().action_confirm()

        sale_order_line = self.env['sale.order.line']
        sale_order_line_field = sale_order_line.read(['training_date'])
        sale_order_line_date = sale_order_line_field['training_date']

        event = self.env['calendar.event'].create({
            'name': self.name,
            'start': sale_order_line_date,
            #'stop': self.training_date,
            'allday': True,
            'partner_id': self.partner_id.id,
        })
        
        return res

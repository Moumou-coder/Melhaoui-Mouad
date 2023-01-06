from odoo import api, models, _, fields
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    def action_confirm(self):
        
        res = super(SaleOrder, self).action_confirm()
        order_line_id = self.order_line.id
        order_line = self.env['sale.order.line'].browse(order_line_id)
        training_date = order_line.training_date
        description = order_line.name
        employee_id = order_line.employee_id.user_id
        #employee_id = order_line.employee_id.id
        #employee_id = order_line.employee_id
        
        event = self.env['calendar.event'].create({
            'name': description,
            'start': training_date,
            'stop': training_date,
            'allday': True,
            'partner_ids': [(4, employee_id.id)],
        })
        
        return res

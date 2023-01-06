from odoo import api, models, _, fields
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    training_date = fields.Date(string="Training Date")
    employee = fields.Many2one('hr.employee', string='employee')
    
    
    def action_confirm(self):
        
        res = super().action_confirm()

        order_line_id = self.order_line.id
        order_line = self.env['sale.order.line'].browse(order_line_id)
        training_date = order_line.training_date
        
        event = self.env['calendar.event'].create({
            'name': self.name,
            'start': training_date,
            'stop': training_date,
            'allday': True,
            'partner_id': self.partner_id.id,
            'employee': self.employee.id,
        })
        
        return res

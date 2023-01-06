from odoo import api, models, _, fields
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    training_date = fields.Date(string="Training Date")
    employee = fields.Many2one("hr.employee", string="employee")
    #description = fields.Text(string='Description')
    
    def action_confirm(self):
        
        res = super().action_confirm()
        
        event = self.env['calendar.event'].create({
            'name': self.name,
            'start': self.training_date,
            'stop': self.training_date,
            'allday': True,
            'partner_id': self.partner_id.id,
            'employee_id': self.employee_id.id,
        })
        
        return res

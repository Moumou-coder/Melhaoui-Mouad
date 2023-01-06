from odoo import api, models, _, fields
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    #training_date = fields.Date(string="Training Date")
    
    def action_confirm(self):
        
        res = super(SaleOrder, self).action_confirm()
        # Create a new event for each sale order line
        for line in self.order_line:
            event = self.env['calendar.event'].create({
                'name': line.product_id.name,
                'start': self.training_date,
                'stop': self.training_date,
                'allday': True,
                'location': self.partner_id.name,
                'partner_ids': [(4, self.partner_id.id)],
            })
        # Return the original result
        return res


"""         order_line_id = self.order_line.id
        order_line = self.env['sale.order.line'].browse(order_line_id)
        training_date = order_line.training_date
        description = order_line.name
        #employee_id = order_line.employee_id.id

        #employee = order_line.employee
        #employee = self.env['hr.employee'].browse(employee)
        #employee_id = order_line.user_id.id
        
        
        event = self.env['calendar.event'].create({
            'name': description,
            'start': training_date,
            'stop': training_date,
            'allday': True,
            'partner_id': self.partner_id.name,
        })
        
        return res """

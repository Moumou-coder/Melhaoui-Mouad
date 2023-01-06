from odoo import fields, models, Command

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    training_date = fields.Date(string="Training Date")
    employee = fields.Many2one("hr.employee", string="employee")

    def action_confirm(self):
        res = super().action_confirm()

        event = self.env['calendar.event'].create({
            'name': self.name,
            'start': self.training_date,
            'stop': self.training_date,
            'allday': True,
            'partner_id': self.employee.id,
        })

        return res
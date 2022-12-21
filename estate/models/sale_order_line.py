from odoo import fields, models, Command

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    training_date = fields.Date(string="Training Date")
    training_employee = fields.Many2One("hr.employee", string="Employee")
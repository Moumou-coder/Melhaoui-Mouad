from odoo import api, models, _, fields
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    group_level_one = "level_one"
    groups_level_two = "level_two"
    manager_approval_level_one = false;
    manager_approval_level_two = false;
    
    def action_confirm(self):
        res = super().action_confirm()

        order_line_id = self.order_line.id
        order_line = self.env['sale.order.line'].browse(order_line_id)
        training_date_start = order_line.training_date_start
        training_date_end = order_line.training_date_end
        description = order_line.name
        price_unit = order_line.price_unit

        user_groups = self.env['res.users'].browse(self.user_id.id).groups_id
        group_names = user_groups.name_get()
        
        for t in group_names:
            if groups_level_two in t:
                manager_approval_level_two = true;
                break
            else:
                manager_approval_level_two = false;

        if(price_unit < 500) :
            event = self.env['calendar.event'].create({
                'name': description,
                'start': training_date_start,
                'stop': training_date_end,
                'allday': True,
                'partner_ids': [(4, self.partner_id.id)],
            })
        else :
            raise ValidationError(manager_approval_level_two)
        
        return res

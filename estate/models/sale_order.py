from odoo import api, models, _, fields
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    def action_confirm(self):
        res = super().action_confirm()

        order_line_id = self.order_line.id
        order_line = self.env['sale.order.line'].browse(order_line_id)
        training_date_start = order_line.training_date_start
        training_date_end = order_line.training_date_end
        description = order_line.name
        price_unit = order_line.price_unit
        
        
        group_level_one = "level_one"
        user_approval_level_one = False
        group_level_two = "level_two"
        user_approval_level_two = False
        
        user_groups = self.env['res.users'].browse(self.user_id.id).groups_id
        group_names = user_groups.name_get()
        for g in group_names:
            if group_level_two in g:
                user_approval_level_two = True;
                break;
            elif group_level_one in g: 
                user_approval_level_one = True;
                break;
            else:
                user_approval_level_two = False;
                user_approval_level_one = False;
                
        msg_not_approval = "Vous n'avez pas les droits d'accès pour confirmer cette vente !"
        msg_cannot_sale = "Ce genre de vente ne peut pas être établie pour le moment"

        if((price_unit < 500)
        or ((500 > price_unit <= 2000) and user_approval_level_one == True) 
        or ((2000 > price_unit <= 5000) and user_approval_level_two == True )):
            event = self.env['calendar.event'].create({
                'name': description,
                'start': training_date_start,
                'stop': training_date_end,
                'allday': True,
                'partner_ids': [(4, self.partner_id.id)],
            })
        elif((500 > price_unit <= 2000) and user_approval_level_one == False): 
            raise ValidationError(f"level-1 : {user_approval_level_one} =>  {msg_not_approval}")
        elif ((2000 > price_unit <= 5000) and user_approval_level_two == False ): 
            raise ValidationError(f"level-2 : {user_approval_level_two} =>  {msg_not_approval}")
        else:
            raise ValidationError(msg_cannot_sale)

        return res

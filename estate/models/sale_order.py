from odoo import api, models, _, fields
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    """ def request_approval(self):
        self.ensure_one()
        # Créer une activité pour un manager dans le chatter
        self.env['mail.activity'].create_activity(
            res_id=self.id,
            res_model=self._name,
            activity_type_id=self.env.ref('mail.mail_activity_data_todo').id,
            summary="Demande d'approbation de devis",
            note="Veuillez approuver ou refuser le devis ci-joint.",
            user_id=self.env.user.id,
            planned_date=fields.Datetime.now(),
        ) """

    # Nous avons pas réussi à notifier un gestionnaire cependant nous avons trouvé 2 moyens d'envoyer un message. 
    # Par contre, une erreur persiste à chque fois lors de l'appuie du bouton 
    
    def request_approval(self):
        # Messages 
        msg_no_manager : "Aucun manager disponible actuellement pour l'approbation..."

        # Récupérer le manager 
        manager = self.env['res.users'].search([], limit=1)

        if not manager:
            raise ValueError(msg_no_manager)
        else :
            # Créer une activité pour le manager dans le chat
            self.message(body=_('Demande approbation envoyée à %s') % manager.name, subtype='mail.mt_comment')

    def action_confirm(self):
        res = super().action_confirm()

        # Récupérer les données nécessaires de sale.order.line afin de créer l'event
        order_line_id = self.order_line.id
        order_line = self.env['sale.order.line'].browse(order_line_id)
        training_date_start = order_line.training_date_start
        training_date_end = order_line.training_date_end
        description = order_line.name
        price_unit = order_line.price_unit
        
        # Vérifier que l'utilisateur a bien les droits afin de valider la vente de formation
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

        # Messages d'erreur à afficher en cas de non-respect au niveau des conditions ex: ne pas avoir les droits pour la vente         
        msg_not_approval = "Vous n'avez pas les droits d'accès pour confirmer cette vente !"
        msg_cannot_sale = "Ce genre de vente ne peut pas être établie pour le moment..."
        msg_limit_amount =  "Ce partenaire n'est pas autorisé à avoir des ordres de vente dépassant un certain montant."

        # Bloc de vérification pour la vente de formation et l'ajout de l'event dans le calendrier
        if((price_unit < 500)
        or (price_unit >= 500 and price_unit <= 2000 and user_approval_level_one) 
        or (price_unit >= 500 and price_unit <= 5000 and user_approval_level_two)):
            # Vérifiez si le montant de la commande est supérieur à la limite autorisée pour le partenaire (ex:client douteux)
            # On suppose que si limit amount = 0, c'est que limite amount n'a pas été défini
            if (self.amount_total > self.partner_id.limit_amount_sale_order and self.partner_id.limit_amount_sale_order != 0):
                raise ValidationError(msg_limit_amount)
            else :
                event = self.env['calendar.event'].create({
                    'name': description,
                    'start': training_date_start,
                    'stop': training_date_end,
                    'allday': True,
                    'partner_ids': [(4, self.partner_id.id)],
                })
        elif(price_unit >= 500 and price_unit <= 2000 and not user_approval_level_one): 
            raise ValidationError(msg_not_approval)
        elif(price_unit >= 500 and price_unit <= 5000 and not user_approval_level_two): 
            raise ValidationError(msg_not_approval)
        else:
            raise ValidationError(msg_cannot_sale)

        return res

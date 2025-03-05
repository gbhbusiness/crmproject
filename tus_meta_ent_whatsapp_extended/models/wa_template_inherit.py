
from odoo import _, api, fields, models


class MailMessage(models.Model):
    _inherit = 'whatsapp.template'

    dynamic_model_id = fields.Many2one('ir.model', string='Applies to', ondelete='cascade')
    is_project_template = fields.Boolean("Project Template?")
    is_tower_template = fields.Boolean("Tower Template?")
    is_category_template = fields.Boolean("Category Template?")
    is_value_template = fields.Boolean("Value Template?")
    is_sub_cat_template = fields.Boolean("Sub Category Template")


class WhatsappChatbotScript(models.Model):
    _inherit = 'whatsapp.chatbot.script'

    dynamic_model_id = fields.Many2one(related='template_id.dynamic_model_id')
    receive_action_id = fields.Many2one(comodel_name="whatsapp.ir.actions", string="Received Actions")
    next_sq_number = fields.Integer(string='Next sequence Number', required=False)


class WhatsappChatbot(models.Model):
    _inherit = 'whatsapp.chatbot'

    end_template_id = fields.Many2one('whatsapp.template', 'End Message Template')





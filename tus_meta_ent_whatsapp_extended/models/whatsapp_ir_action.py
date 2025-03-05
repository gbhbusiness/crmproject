from odoo import models, fields, api, _
from odoo.exceptions import UserError


class WhatsAppIrActions(models.Model):
    _inherit = 'whatsapp.ir.actions'

    is_custom_action = fields.Boolean('is_custom_action')
    dynamic_model_id = fields.Many2one("ir.model", ondelete="cascade")
    dynamic_field_id = fields.Many2one("ir.model.fields", ondelete="cascade")
    dynamic_send_template_id = fields.Many2one("whatsapp.template", ondelete="cascade")
    dynamic_selection = fields.Selection(string='Dynamic Selection',
                                         selection=[('create', 'Create'), ('write', 'Write'),
                                                    ('search', 'Search'), ('browse', 'Browse'),
                                                    ('reschedule', 'Reschedule'), ('cancel', 'Cancel'),
                                                    ])
    dynamic_working_selection = fields.Selection(string='Dynamic Working Selection',
                                                 selection=[('send', 'Send'), ('receive', 'Receive'),
                                                            ('action', 'Action')])
    dynamic_template_list_title = fields.Char("Template List Title")
    reschedule_action = fields.Char("Reschedule Booking")
    cancel_action = fields.Char("Cancel Booking")
    dynamic_action_selection = fields.Selection(string='Dynamic Action Selection',
                                                selection=[('confirm', 'Confirm'), ('reschedule', 'Reschedule'),
                                                           ('cancel', 'Cancel')])

    dynamic_field_ids = fields.Many2many("ir.model.fields", string="Dynamic Fields")
    dynamic_is_chatbot_ended = fields.Boolean('Is Chatbot Ended')
    dynamic_message =  fields.Char(string="Dynamic Message")





from odoo import models, fields, api


class WATemplateButton(models.Model):
    _inherit = 'whatsapp.template.button'
    _description = 'Inherited whatsapp template button to add flow to the template'

    button_type = fields.Selection(selection_add=[('flow', 'Flow')], ondelete={'flow': 'cascade'})
    flow_id = fields.Char(string="Flow ID", related='wa_template_id.wa_flow_id.flow_id')
    screen_id = fields.Char(string="Screen ID")








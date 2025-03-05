from odoo import models, fields, api


class WAFlowTemplate(models.Model):
    _name = 'wa.flows'
    _description = 'Whatsapp flow template configurations'

    name = fields.Char('Template Name')
    flow_state = fields.Selection([
        ('draft', 'DRAFT'),
        ('created', 'CREATED'),
        ('published', 'PUBLISHED'),
        ('deprecated', 'DEPRECATED')
    ], string='FLow State', default='draft')
    wa_account_id = fields.Many2one('whatsapp.account', 'WhatsApp Account')
    flows_categories = fields.Selection([('sign_up', 'SIGN UP'),
                                         ('sign_in', 'SIGN IN'),
                                         ('appointment_booking', 'APPOINTMENT BOOKING'),
                                         ('lead_generation', 'LEAD GENERATION'),
                                         ('contact_us', 'CONTACT US'),
                                         ('customer_support', 'CUSTOMER SUPPORT'),
                                         ('survey', 'SURVEY'),
                                         ('other', 'OTHER')], string="Flow Categories")
    template_id = fields.Many2one('whatsapp.template', 'Templates')
    flow_id = fields.Char("Flow ID")
    flow_model_id = fields.Many2one('ir.model', string='Flow Model')
    create_model_id = fields.Many2one('ir.model', string='Targeted Model')
    resource_ref = fields.Reference(
        string='Record',
        compute='_compute_resource_ref',
        compute_sudo=False, readonly=False,
        selection='_selection_target_model',
        store=True
    )

    @api.depends('flow_model_id')
    def _compute_resource_ref(self):
        for preview in self:
            # mail_template = preview.mail_template_id.sudo()
            if preview.flow_model_id:
                model = preview.flow_model_id.sudo().model
                res = self.env[model].search([], limit=1)
                preview.resource_ref = f'{model},{res.id}' if res else False
            else:
                preview.resource_ref = False

    @api.model
    def _selection_target_model(self):
        return [(model.model, model.name) for model in self.env['ir.model'].sudo().search([])]

    field_mapping_ids = fields.One2many('field.mapping', 'flow_id', string="Mapped Flow Fields")

    def create_whatsapp_flow(self):
        if self.wa_account_id:
            answer = self.wa_account_id._create_whatsapp_flow(self.name, self.flows_categories)
            if answer and 'id' in answer:
                self.flow_id = answer.get('id')
                self.flow_state = 'created'

    def delete_whatsapp_flow(self):
        if self.wa_account_id:
            answer = self.wa_account_id._delete_whatsapp_flow(self.flow_id)
            if answer and 'success' in answer:
                self.flow_id = ''
                self.flow_state = 'draft'

    def publish_whatsapp_flow(self):
        if self.wa_account_id:
            answer = self.wa_account_id._publish_whatsapp_flow(self.flow_id)
            self.flow_state = 'published' if answer and 'success' in answer else self.flow_state

    def deprecate_whatsapp_flow(self):
        if self.wa_account_id:
            answer = self.wa_account_id._deprecate_whatsapp_flow(self.flow_id)
            self.flow_state = 'deprecated' if answer and 'success' in answer else self.flow_state


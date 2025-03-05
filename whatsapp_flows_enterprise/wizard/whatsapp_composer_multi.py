from odoo import models, fields, api


class WhatsappComposerMulti(models.Model):
    _name = 'whatsapp.composer.multi'
    _description = "Send whatsapp templates to multiple customers"

    def default_get(self, fields):
        result = super(WhatsappComposerMulti, self).default_get(fields)
        if self._context and self._context.get('active_model'):
            template_domain = [('status', '=', 'approved'), ('model_id.model', '=', self._context.get('active_model'))]
            wa_template_ids = self.wa_template_id.search(template_domain)
            result['domain_wa_template_ids'] = [(6, 0, wa_template_ids.ids)]
        return result

    partner_ids = fields.Many2many(comodel_name="res.partner")
    wa_template_id = fields.Many2one(comodel_name="whatsapp.template", string="Whatsapp Template")
    domain_wa_template_ids = fields.Many2many(comodel_name="whatsapp.template")
    body_html = fields.Html("Body")

    @api.onchange('wa_template_id')
    def onchange_template_wrapper(self):
        self.body_html = self.wa_template_id.body if self.wa_template_id and self.wa_template_id.body else ''

    def send_multi_whatsapp_message(self):
        if self.partner_ids:
            user_partner = self.wa_template_id.wa_account_id.notify_user_ids if len(self.wa_template_id.wa_account_id.notify_user_ids) == 1 else self.wa_template_id.wa_account_id.notify_user_ids[0]
            for partner in self.partner_ids:
                whatsapp_composer = self.env["whatsapp.composer"].with_user(user_partner.id).create({
                            "phone": partner.mobile,
                            "wa_template_id": self.wa_template_id.id,
                            "res_model": self.wa_template_id.model_id.model,
                        })
                whatsapp_composer._send_whatsapp_template()

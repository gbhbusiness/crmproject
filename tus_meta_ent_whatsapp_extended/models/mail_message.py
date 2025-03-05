from odoo import _, api, fields, models


class MailThreadInherit(models.AbstractModel):
    _inherit = 'mail.thread'


    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, **kwargs):
        parent_id = kwargs.get('parent_id')
        res  = super(MailThreadInherit,self).message_post(**kwargs)
        if parent_id:
            res.parent_id= parent_id
        return res


class MailMessage(models.Model):
    _inherit = 'mail.message'

    wa_template_id = fields.Many2one(comodel_name='whatsapp.template', string='Wa Template Id')

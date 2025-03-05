from odoo import api,models,fields,_,tools

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'


    attachment_ids = fields.Many2many('ir.attachment',string="Attachments")
    helpdesk_ticket_link = fields.Char(string="Helpdesk Link",compute = '_compute_helpdesk_url')

    def _compute_helpdesk_url(self):
        for rec in self:
            rec.helpdesk_ticket_link = rec._get_share_url()


from odoo import api, models, fields, _, tools


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    attachment_ids = fields.Many2many('ir.attachment', string="Attachments")
    helpdesk_ticket_link = fields.Char(string="Helpdesk Link", compute='_compute_helpdesk_url')
    response_data = fields.Text(string="Flow Data")

    def _compute_helpdesk_url(self):
        for rec in self:
            rec.helpdesk_ticket_link = rec._get_share_url()

    def action_confirm(self):
        for rec in self:
            stage = self.env['helpdesk.stage'].search([]).filtered(lambda x:x.is_progress)
            if stage:
                rec.stage_id = stage.id


    def action_cancel(self):
        for rec in self:
            stage = self.env['helpdesk.stage'].search([]).filtered(lambda x: x.is_cancel)
            if stage:
                rec.stage_id = stage.id


class HelpdeskStage(models.Model):
    _inherit = 'helpdesk.stage'

    is_progress = fields.Boolean(string = "Is Progress")
    is_cancel =  fields.Boolean(string = "Is Cancel")

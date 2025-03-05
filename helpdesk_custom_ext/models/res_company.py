from odoo import api,models,fields,tools,_

class ResCompany(models.Model):
    _inherit = 'res.company'

    team_id = fields.Many2one('helpdesk.team',string="Team")
    helpdesk_template_id = fields.Many2one(comodel_name="whatsapp.template",string=" Helpdesk Ticket Template")



class ResConfigSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    team_id =  fields.Many2one(related='company_id.team_id',readonly=False)
    helpdesk_template_id = fields.Many2one(related = 'company_id.helpdesk_template_id',readonly=False)
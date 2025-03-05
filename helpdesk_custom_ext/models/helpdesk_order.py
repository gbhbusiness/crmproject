from sympy.integrals.meijerint_doc import category

from odoo import api, models, fields, tools, _,SUPERUSER_ID


class HelpdeskOrder(models.Model):
    _name = 'helpdesk.order'
    _description = "HelpdeskOrder"

    partner_id = fields.Many2one('res.partner',string= "Customer")
    name =  fields.Char(string="Name")
    email = fields.Char(string="Email")
    categories = fields.Char(string='Categories')
    sub_categories = fields.Char(string='Subcategories')
    project = fields.Char(string='Project')
    tower = fields.Char(string='Tower')
    unit_number = fields.Char(string='Unit number')
    description = fields.Text(string='Description')
    user_id =  fields.Many2one('res.users',string= "User")
    company_id = fields.Many2one('res.company',string="Company",default=lambda self: self.env.company)
    state = fields.Selection(
        [('draft', 'New'),('confirm', 'Confirmed'),('cancel', 'Cancelled')],'Status',default='draft')
    attachment_ids =  fields.Many2many('ir.attachment',string="Attachment")
    # chatbot_id = fields.Many2one(comodel_name="whatsapp.chatbot", string="Chatbot")


    def action_confirm(self):
        self.state = 'confirm'
        category = self.env['helpdesk.ticket.type'].sudo().search([('name','=',self.categories)])
        sub_category = category.services_ids.filtered(lambda x:x.name ==self.sub_categories)
        project = self.env['helpdesk.project'].sudo().search([('name','=',self.project)])
        tower = (project.tower_ids.filtered(lambda x:x.name ==self.tower))

        helpdesk_ticket = self.env['helpdesk.ticket'].sudo().create({
            'name': self.partner_id.name,
            'user_id': SUPERUSER_ID,
            'team_id': self.company_id.team_id.id,
            'ticket_type_id':category.id,
            'services_ids':[(4, sub_category.id)],
            'partner_id':self.partner_id.id,
            'email_cc':self.email,
            'project_id':project.id,
            'tower_id':tower.id,
            'unit_no':self.unit_number,
            'description':self.description,
            'attachment_ids':[(6, 0, self.attachment_ids.ids)]
        })
        wizard_rec = self.env['whatsapp.composer'].sudo().with_context(active_model=helpdesk_ticket._name,
                                                                active_id=helpdesk_ticket.id).with_user(SUPERUSER_ID).create(
            {'phone': helpdesk_ticket.partner_id.mobile , "res_model": helpdesk_ticket._name,
             'wa_template_id':  helpdesk_ticket.company_id.helpdesk_template_id.id})
        wizard_rec._send_whatsapp_template()



    def action_cancel(self):
        self.state = 'cancel'






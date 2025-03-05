# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HelpdeskService(models.Model):
    _name = 'helpdesk.service'
    _description = 'Services'

    name = fields.Char(string="Service Name")


class ProjectTower(models.Model):
    _name = 'project.tower'
    _description = 'Tower'

    name = fields.Char(string="Tower No.")


class HelpdeskProject(models.Model):
    _name = 'helpdesk.project'
    _description = 'Project'

    name = fields.Char(string="Project Name")
    tower_ids = fields.Many2many('project.tower', string="Tower No.")


class HelpdeskTicketType(models.Model):
    _inherit = 'helpdesk.ticket.type'

    services_ids = fields.Many2many('helpdesk.service', string="Service Name")


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    @api.depends('ticket_type_id')
    def _compute_helpdesk_service(self):
        for rec in self:
            if rec.type_services_ids:
                rec.type_services_ids = []
            else:
                rec.type_services_ids = rec.ticket_type_id.services_ids.ids or []

    @api.depends('project_id')
    def _compute_helpdesk_project_tower(self):
        for rec in self:
            if rec.project_tower_ids:
                rec.project_tower_ids = []
            else:
                rec.project_tower_ids = rec.project_id.tower_ids.ids or []

    type_services_ids = fields.Many2many('helpdesk.service',
        'helpdesk.ticket_ticket_service_rel', 'helpdesk_id', 'service_id', compute='_compute_helpdesk_service')
    services_ids = fields.Many2many('helpdesk.service')
    # is_portal_ticket = fields.Boolean()

    project_id = fields.Many2one('helpdesk.project', string="Project Name")
    project_tower_ids = fields.Many2many('project.tower','ticket_project_tower_rel', 'helpdesk_id', 'project_tower_id',
        compute='_compute_helpdesk_project_tower')
    tower_id = fields.Many2one('project.tower', string="Tower No.")
    unit_no = fields.Char(string="Unit No.")


class HelpdeskTeam(models.Model):
    _inherit = "helpdesk.team"


    def _ensure_submit_form_view(self):
        teams = self.filtered('use_website_helpdesk_form')
        if not teams:
            return

        default_form = self.env.ref('website_helpdesk.ticket_submit_form')
        for team in teams:
            if not team.website_form_view_id:
                # xmlid = 'website_helpdesk.team_form_' + str(team.id)
                # form_template = self.env['ir.ui.view'].sudo().create({
                #     'type': 'qweb',
                #     'arch': default_form,
                #     'name': xmlid,
                #     'key': xmlid
                # })
                # self.env['ir.model.data'].sudo().create({
                #     'module': 'website_helpdesk',
                #     'name': xmlid.split('.')[1],
                #     'model': 'ir.ui.view',
                #     'res_id': form_template.id,
                #     'noupdate': True
                # })
                team.website_form_view_id = default_form.id

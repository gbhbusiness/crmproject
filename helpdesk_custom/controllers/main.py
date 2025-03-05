# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from werkzeug.exceptions import NotFound
from werkzeug.utils import redirect

from odoo import http, _
from odoo.http import request
from odoo.osv import expression

from odoo.addons.website_helpdesk.controllers import main

class WebsiteHelpdesk(http.Controller):

    @http.route(['/helpdesk/type_info/<model("helpdesk.ticket.type"):type>'], type='json', auth="public", methods=['POST'], website=True)
    def ticket_type_infos(self, **kw):
        ticket_type = kw.get('type')
        helpdeskType = request.env['helpdesk.ticket.type'].sudo().search([('id','=',ticket_type.id)])

        return dict(services=[[service.id, service.name] for service in helpdeskType.services_ids])

    @http.route(['/helpdesk/project/<model("helpdesk.project"):project>'], type='json', auth="public", methods=['POST'], website=True)
    def ticket_project_tower(self, **kw):
        project = kw.get('project')
        projects = request.env['helpdesk.project'].sudo().search([('id','=',project.id)])

        return dict(towers=[[tower.id, tower.name] for tower in projects.tower_ids])


class WebsiteHelpdesk(main.WebsiteHelpdesk):

    def get_helpdesk_team_data(self, team, search=None):
        types = request.env['helpdesk.ticket.type'].sudo().search([])
        projects = request.env['helpdesk.project'].sudo().search([])

        return {'team': team, 'types':types, 'projects':projects}

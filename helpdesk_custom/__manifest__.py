# -*- coding: utf-8 -*-

{
    'name': "Helpdesk Ticket Customisation",
    'version': '17.0.1.1.0',
    'summary': """Helpdesk Ticket Custom""",
    'description': """This module used to Helpdesk Ticket Custom""",
    'author': "",
    'maintainer': '',
    'category': 'Tools',
    'depends': ['base', 'helpdesk', 'website_helpdesk'],
    'license': '',
    'data': [
        'security/ir.model.access.csv',
        'data/website_helpdesk.xml',
        'views/helpdesk_ticket_views.xml',
        'views/helpdesk_ticket_template.xml',
    ],
    'installable': True,
    'auto_install': False,
    'assets': {
        'web.assets_frontend': [
            'helpdesk_custom/static/src/js/helpdesk_ticket.js',
        ]
    }
}

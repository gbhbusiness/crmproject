# -*- coding: utf-8 -*-

{
    'name': "Helpdesk Ticket Customisation Ext",
    'version': '17.0.1.1.0',
    'summary': """Helpdesk Ticket Custom""",
    'description': """This module used to Helpdesk Ticket Custom""",
    'category': 'Tools',
    'depends': ['helpdesk_custom', 'odoo_whatsapp_ent_chatbot'],
    'license': '',
    'data': [
         'security/ir.model.access.csv',
        'views/helpdesk_order_views.xml',
        'views/helpdesk_ticket_views.xml',
        'views/res_config_setting.xml',
    ],
    'installable': True,
    'auto_install': False,
   }

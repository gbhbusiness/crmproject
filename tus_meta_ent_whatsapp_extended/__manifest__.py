# -*- coding: utf-8 -*-
{
    'name': "Tus Meta Enterprise Whatsapp Extended",
    'version': '1.1',
    'summary': "Short (1 phrase/line) summary of the module's purpose",
    'description': """
    """,
    'category': 'Uncategorized',

    # any module necessary for this one to work correctly
    'depends': ['odoo_whatsapp_ent_chatbot'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'data/chatbot_whatsapp_template.xml',
        # 'data/chatbot_action.xml',
        # 'data/chatbot_script.xml',
        'views/whatsapp_template_view_inherit.xml',
        'views/whatsapp_ir_action_view_inherit.xml',
        'views/wa_chatbot_view_inherit.xml',
    ],
}


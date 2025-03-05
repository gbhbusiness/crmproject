{
    "name": "Whatsapp Extended  | Odoo Meta WhatsApp Graph API | Odoo V17 Enterprise Edition",
    "version": "17.2",
    "category": "Discuss",
    "summary": "Odoo Whatsapp Extended module is extended version of whatsapp enterprise",
    "description": """
        Whatsapp Extended,
        Interactive Templates,
        Odoo
        ERP
        Odoo ERP
        WhatsApp
        Whats-App
        Odoo V17 Enterprise Edition""",
    "depends": ["whatsapp", "base_automation"],
    "data": [
        "security/ir.model.access.csv",
        "views/interactive_buttons_views.xml",
        "views/interactive_list_views.xml",
        "views/interactive_product_list_views.xml",
        "views/whatsapp_interactive_template_views.xml",
        "views/whatsapp_template_inherit_views.xml",
        "views/res_partner_inherit_views.xml",
        "views/ir_actions.xml",
        "views/whatsapp_account_views.xml",
    ],
    'assets': {
        'web.assets_backend': [
            'whatsapp_extended/static/src/xml/message.xml',
            'whatsapp_extended/static/src/xml/AgentsList.xml',
            'whatsapp_extended/static/src/js/agents/**/*',
            'whatsapp_extended/static/src/scss/*.scss',
            'whatsapp_extended/static/src/js/templates/**/*',
        ],
    },
  
    "installable": True,
    "auto_install": False,
    "application": True,
    "images": ["static/description/main_screen.gif"],
}

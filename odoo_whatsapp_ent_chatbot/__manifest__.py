# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.
{
    "name": "Odoo WhatsApp Chatbot | Odoo V17 Enterprise Edition | WhatsApp Cloud API",
    "version": "17.2",
    "author": "",
    "category": "Discuss",
    "summary": "Odoo Whatsapp Chatbot Integration, Interactive Templates, Buttons send through odoo on WhatsApp and Message Automation",
    "description": """
        Odoo Whatsapp Chatbot Integration,
        Interactive Templates,
        Buttons send through odoo on WhatsApp and Message Automation
        Odoo Chatbot
        Chatbot
        Odoo
        ERP
        Odoo ERP
        WhatsApp
        Whats-App
        Discuss
        App
        Community
        Odoo Whatsapp Chatbot
        Whatsapp Chatbot
        Odoo V17 Enterprise Edition
    """,
    "depends": ["whatsapp_extended",'sale'],
    "data": [
        "security/ir.model.access.csv",
        "data/wa_template.xml",
        "data/whatsapp_chatbot.xml",
        "views/whatsapp_chatbot_script_views.xml",
        "views/discuss_channel_views.xml",
        "views/whatsapp_chatbot_views.xml",
        "views/whatsapp_ir_action_views.xml",
        "views/whatsapp_account_inherit_view.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "/odoo_whatsapp_ent_chatbot/static/src/scss/kanban_view.scss"
        ],
    },
    "images": ["static/description/main_screen.gif"],
    "installable": True,
    "auto_install": False,
    "application": True,
}

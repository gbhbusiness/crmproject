{
    'name': 'WhatsApp Flows Enterprise',
    'version': '17.2',
    'category': 'Base',
    'summary': """Whatsapp flows module
        Odoo WhatsApp Integration
        Flows
        Whatsapp FLows
        Odoo Meta WhatsApp Graph API
        Odoo V17 Enterprise Edition
        Odoo V17 Enterprise WhatsApp Integration
        V17 Enterprise WhatsApp
        Enterprise WhatsApp
        Enterprise
        WhatsApp Enterprise
        Odoo WhatsApp Enterprise
        Odoo WhatsApp Cloud API
        WhatsApp Cloud API
        WhatsApp Enterprise Edition
    """,
    'description': """
        Whatsapp flows module
        Whatsapp flows
        Odoo WhatsApp Integration
        Odoo Meta WhatsApp Graph API
        Odoo V17 Community Edition
        Odoo V17 Community WhatsApp Integration
        V17 Enterprise WhatsApp
        Enterprise WhatsApp
        Enterprise
        WhatsApp Enterprise
        Odoo WhatsApp Enterprise
        Odoo WhatsApp Cloud API
        WhatsApp Cloud API
        WhatsApp Enterprise Edition
    """,
    'depends': ['whatsapp_extended'],
    'data': ['security/ir.model.access.csv',
             'wizard/whatsapp_composer_multi_views.xml',
             'views/whatsapp_flows_views.xml',
             'views/whatsapp_account_flow_views_inherit.xml',
             'views/wa_flow_template_views_inherit.xml',
             'views/whatsapp_template_button_views_inherit.xml'
             ],
    'installable': True,
    'auto_install': False,

    # 'images': ['static/description/tus_banner.gif'],
}

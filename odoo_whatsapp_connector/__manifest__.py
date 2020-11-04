# See LICENSE file for full copyright and licensing details.

{
    'name': 'Odoo Whatsapp Integration',
    'summary': 'This module is used for Whatsapp Connection',
    'version': '13.0.1.0.0',
    'license': 'LGPL-3',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'maintainer': 'Serpent Consulting Services Pvt. Ltd.',
    'website': 'http://www.serpentcs.com',
    'sequence': 1,
    'category': 'Extra Tools',
    'depends': [
        'contacts'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/whatsapp_error_log_cron.xml',
        'views/res_company_view.xml',
        'views/res_partner_view.xml',
        'views/whatsapp_message_log_view.xml',
        'views/mail_template.xml',
        'wizard/whatsapp_message_view.xml',
    ],
    'images': ['static/description/odoo-whatsapp-main.gif'],
    'installable': True,
    'price': 79,
    'external_dependencies': {'python': ['phonenumbers']},
    'currency': 'EUR'
}

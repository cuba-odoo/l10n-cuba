# -*- coding: utf-8 -*-
{
    'name': "l10n_cu_website_sale",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'l10n_cu_address',
        'website_sale'
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/shop_address.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/l10n_cu_website_sale/static/src/lib/jquery.validate.min.js',
            '/l10n_cu_website_sale/static/src/js/checkout.js'
        ]
    }
}

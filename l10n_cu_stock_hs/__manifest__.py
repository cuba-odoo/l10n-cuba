# -*- coding: utf-8 -*-
{
    'name': "Cuba-Stock H.S code",

    'summary': """
        Cuba Stock HS Code""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Ing. Orlando Martinez Bao. Ing. José Andrés Hernández Bustio . Enrique ...",
    'website': "",
    'license': 'LGPL-3',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory/Inventory',
    'version': '15.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base','product','stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hs_code.xml',
        'views/product_category.xml',
        'views/product_template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

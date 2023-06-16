# -*- coding: utf-8 -*-
{
    'name': "Cuba-Stock",
    'license': 'LGPL-3',
    'summary': """
        Gestión de inventario para Cuba
    """,

    'description': """
        Establecer los elementos necesarios para el manejo de los inventarios en cuba.
    """,

    'author': "Ing. José Andrés Hernández Bustio, . Enrique ..., Ing. Orlando Martinez Bao (YYOGestiono)",
    'website': "",
    'category': 'Inventory/Inventory',
    'version': '15.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product','stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/product_brand.xml',
        'views/product_product_views.xml',
        'views/product_template_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

# -*- coding: utf-8 -*-
{
    'name': "Cuba - Documentacion",
    'summary': """
        Documentacion funcional de la Localizacion Cubana.""",
    'author': "Comunidad Cubana de Odoo",
    'category': 'Accounting',
    'version': '0.1',
    'depends': ['website'],
    'data': [
        'views/web_views.xml',
    ],
    'license': 'LGPL-3',
    'assets': {
        'web.assets_frontend': [
            'web_documentation/static/src/css/web.css',

        ],
    },
}

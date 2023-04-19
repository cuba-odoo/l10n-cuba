# -*- encoding: utf-8 -*-
##############################################################################
{
    'name': 'Arancel Management',
    'version': '1.0',
    'description': """
Management of Arancel

Gestión de Aranceles (Partidas y subpartida nacional)

    """,
    'author': 'TecKISA',
    'website': "http://teckisa.com",
    'category': "Warehouse",
    'license': 'AGPL-3',
    'depends': ['product', 'stock'],
    'data': [
            'views/product_view.xml',
            'security/ir.model.access.csv'
        ],
    'demo_xml': [],
    "update_xml": [],
    'installable': True,
    'auto_install': False
}

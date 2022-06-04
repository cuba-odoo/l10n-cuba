# -*- coding: utf-8 -*-
{
    'name': "VB - Importar extractos bancarios",
    'summary': """
        Importar extractos bancarios de BANDEC.""",
    'author': "Comunidad Cubana de Odoo",
    'category': 'Accounting',
    'version': '0.1',
    'depends': ['om_account_bank_statement_import'],
    'data': [
        'wizard/import_wizard.xml',
    ],
    'license': 'LGPL-3',
}

# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# List of contributors:
# Bernardo Yaser León Ávila <bernardo@idola.it>
# Yunior Rafael Hernández Cabrera <yunior@idola.it>
# Yeniel León Ferrer

{
    'name': 'Cuba - Banks',
    'version': '0.1',
    'author': 'Idola Odoo Team',
    'category': 'Cuba',
    'description': """
Cuban charts of accounts.
========================================

    * Define las sucursales bancarias del país incluida su dirección y teléfono
""",
    'depends': [
        'base',
        'address_cu',
    ],
    'data': [
        'data/res_bank_data.xml',
        'views/res_bank_views.xml',
    ],
}

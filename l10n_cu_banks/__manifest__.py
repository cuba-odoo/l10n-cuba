# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# List of contributors:
# Bernardo Yaser León Ávila <bernardo@idola.it>
# Yunior Rafael Hernández Cabrera <yunior@idola.it>
# Yeniel León Ferrer

{
    'name': 'Bancos Cubanos',
    'version': '14.0.1.0.0',
    'author': 'Idola Odoo Team, Comunidad cubana de Odoo',
    'category': 'Localization',
    'description': """
        * Define las sucursales bancarias del país incluida su dirección y teléfono
    """,
    'depends': [
        'l10n_cu',
        'l10n_cu_address',
    ],
    "license": "AGPL-3",
    'data': [
        'views/res_bank_view.xml',
        'data/res_bank_data.xml',
    ],
    "auto_install": True,
}

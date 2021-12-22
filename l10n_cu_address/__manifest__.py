# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# List of contributors:
# Bernardo Yaser León Ávila <bernardo@idola.it>
# Yunior Rafael Hernández Cabrera <yunior@idola.it>


{
    "name" : "Topónimos cubanos",
    "version" : "14.0.1.0.0",
    "author" : "Idola Odoo Team, Comunidad cubana de Odoo",
    "category": "Localization",
    "depends" : [
        "l10n_cu",
    ],
    "license": "AGPL-3",
    "data" : [
        'data/res_country_state_data.xml',
        'data/res_municipality_data.xml',
        'views/res_cu_municipality.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
    ],
    "auto_install": True,
}

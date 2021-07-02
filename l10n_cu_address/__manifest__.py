# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# List of contributors:
# Bernardo Yaser León Ávila <bernardo@idola.it>
# Yunior Rafael Hernández Cabrera <yunior@idola.it>

{
    "name" : "Cuba - Address",
    "version" : "0.1",
    "author" : "Idola Odoo Team",
    "category": "Cuba",
    "depends" : [
        "base",
    ],
    "data" : [
        'data/res_country_state_data.xml',
        'data/res_municipality_data.xml',
        'views/res_cu_municipality.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
    ],
}

# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# List of contributors:
# Bernardo Yaser León Ávila <bernardo@idola.it>
# Yunior Rafael Hernández Cabrera <yunior@idola.it>
# Yusnel Rojas Garcia
# Julio Smith
# Segu
# Javier Escobar

{
    'name': 'Cuba - Contabilidad',
    'version': '16.0',
    'author': 'Idola Odoo Team, Comunidad cubana de Odoo ',
    'category': 'Accounting/Localizations/Account Charts',
    'description': """
        Cuban charts of accounts.
            * Defines the following chart of account templates:
                * Cuban general chart of accounts by 494/2016 modified by 407/2019
                * Cuban general chart of accounts for Actividad Empresarial
                * Cuban general chart of accounts for Unidades Presupuestadas de Tratamiento Especial 
                * Cuban general chart of accounts for Sector Cooperativo Agropecuario y no Agropecuario"
    """,
    'depends': [
        'account',
    ],
    'data': [
        'data/account_chart_data.xml',        
        'data/account.account.template-common.csv',
        'data/account.account.template-tcp.csv',
        'data/account.account.template-private.csv',
        'data/account.account.template-public.csv',
        'data/account_chart_post_data.xml',
        'data/account_group_template_data.xml',
         # 'data/account_tax_template_data.xml',
        # 'data/account_fiscal_position_template_data.xml',
        # 'data/account_fiscal_position_tax_template_data.xml',
        # 'data/account_chart_template_data.xml',
        # 'data/res_cnae_data.xml',
        "views/account_views.xml",
        "views/res_company_views.xml",
        "views/expense_element_views.xml",
        "security/ir.model.access.csv"
    ],
    'license': 'LGPL-3',
}

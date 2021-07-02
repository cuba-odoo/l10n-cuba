# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# List of contributors:
# Bernardo Yaser León Ávila <bernardo@idola.it>
# Yunior Rafael Hernández Cabrera <yunior@idola.it>
# Yusnel Rojas Garcia
# Julio Smith

{
    'name': 'Cuba - Accounting',
    'version': '0.1',
    'author': 'Idola Odoo Team',
    'category': 'Accounting/Localizations/Account Charts/Cuba',
    'description': """
Cuban charts of accounts.
========================================

    * Defines the following chart of account templates:
        * Cuban general chart of accounts by 494/2016 modified by 407/2019: "Nomenclador de Cuentas para la Actividad Empresarial, Unidades Presupuestadas de Tratamiento Especial y el Sector Cooperativo Agropecuario y no Agropecuario"
        * Cuban general chart of accounts for freelance workers
""",
    'depends': [
        'account',
    ],
    'data': [
        'data/l10n_cu_chart_data.xml',
        #'data/account.account.template-tcp.csv',
        'data/account.account.template-company.csv',
        'data/account_chart_data.xml',
        'data/account_tax_group_data.xml',
        'data/account_tax_data.xml',
        'data/account_fiscal_position_template_data.xml',
        'data/account_chart_template_data.xml',
    ],
}

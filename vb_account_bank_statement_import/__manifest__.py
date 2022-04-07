# -*- coding: utf-8 -*-
{
    'name': "VB - Importar extractos bancarios",
    'summary': """
        Plantilla de contratos de trabajadores.""",
    'description': """
        Long description of module's purpose
    """,
    'author': "Segu",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '0.1',
    'depends': ['om_account_bank_statement_import'],
    'data': [
        # 'security/ir.model.access.csv',
        # 'reports/hr_contract_template_report.xml',
        # 'views/hr_contract_template_views.xml',
        # 'views/hr_contract_views.xml',
        'wizard/import_wizard.xml',
    ],
    'license': 'LGPL-3',
}

# -*- coding: utf-8 -*-
{
    'name': "Plantillas de contratos de trabajadores",
    'summary': """
        Plantilla de contratos de trabajadores.""",
    'description': """
        Long description of module's purpose
    """,
    'author': "Segu",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resources',
    'version': '0.1',
    'depends': ['l10n_cu_hr_payroll'],
    'data': [
        'data/hr_job_data.xml',
        'data/hr_contract_template_data.xml',
        'security/ir.model.access.csv',
        'reports/hr_contract_template_report.xml',
        'views/hr_contract_template_views.xml',
        'views/hr_contract_views.xml',
        'views/hr_contract_templates.xml',
    ],
}

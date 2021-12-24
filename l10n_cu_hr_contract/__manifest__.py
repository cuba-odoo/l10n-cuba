# List of contributors:
# Segu S.U.R.L

{
     'name': 'Cuba - HR Contratos',
     'version': '0.1',
     'category': 'Human Resources',
     'description': 'Contratos de trabajadores - Cuba.',
     'author': 'Comunidad Cubana de Odoo',
     'depends': ["hr_contract", "l10n_cu_hr_payroll"],
     'auto_install': True,
     'data': [          
          "views/hr_contract_views.xml",
          "views/hr_contract_template.xml",
          "reports/hr_contract_report.xml",
     ],
}

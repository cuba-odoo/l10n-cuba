{
     'name': 'Cuba - HR Contratos',
     'version': '0.1',
     'category': 'Human Resources',
     'description': 'Contratos de trabajadores para las MIPYME en Cuba.',
     'author': 'Segu',
     'depends': ["hr_contract", "l10n_cu_hr_payroll"],
     'auto_install': True,
     'data': [
          "reports/hr_contract_report.xml",
          "views/hr_contract_views.xml",
     ],
}

# List of contributors:
# Segu

{
     'name': 'Cuba - HR Contratos',
     'version': '15.0',
     'category': 'Human Resources',
     'summary': """
        Contratos de empleados, régimen de contribución.
     """,
     'description': 'Contratos de trabajadores - Cuba.',
     'author': 'Comunidad Cubana de Odoo',
     'depends': ["hr_contract", "l10n_cu_hr_payroll"],
     'auto_install': True,
     'data': [          
          "views/hr_contract_views.xml",
          "data/hr_contract_type_data.xml",
     ],
     'license': 'LGPL-3',
}

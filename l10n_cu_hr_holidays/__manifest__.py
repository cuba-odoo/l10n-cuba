# List of contributors:
# Segu

{
     'name': 'Cuba - HR Ausencias',
     'version': '20.0.1.0.0',
     'category': 'Human Resources',
     'description': 'Solicitudes de ausencias de los trabajadores - Cuba.',
     'author': 'Comunidad Cubana de Odoo',
     'depends': ['hr_holidays', 'l10n_cu_hr_payroll_enterprise'],
     'auto_install': True,
     'data': [
          'data/hr_holidays_data.xml',
          "views/hr_leave_type_views.xml",
          "views/hr_leave_views.xml"
     ],
     'license': 'LGPL-3',
}

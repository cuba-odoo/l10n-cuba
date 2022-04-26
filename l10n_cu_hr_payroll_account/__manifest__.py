# List of contributors:
# Segu

{
    'name': 'Cuba - Nóminas con contabilidad',
    'category': 'Accounting/Accounting',
    'version': '15.0',
    'description': """
Accounting Data for Cuba Payroll Rules.
==========================================
    """,
    'depends': ['om_hr_payroll_account', 'l10n_cu', 'l10n_cu_hr_payroll'],
    'author': 'Comunidad Cubana de Odoo',
    'data': [
        'data/hr_payroll_account_data.xml',
        'views/hr_payroll_account_views.xml',
        "wizard/hr_payroll_payslips_by_employees_wizard.xml",
    ],
    'license': 'LGPL-3',
}

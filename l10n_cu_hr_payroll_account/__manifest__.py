# List of contributors:
# Segu

{
    'name': 'Cuba - Nóminas con contabilidad',
    'category': 'Accounting/Accounting',    
    'description': """
Accounting Data for Cuba Payroll Rules.
==========================================
    """,
    'depends': ['l10n_cu', 'l10n_cu_hr_payroll', 'hr_payroll_account_community'],
    'author': 'Comunidad Cubana de Odoo',
    'data': [
        'data/hr_payroll_account_data.xml',
        'views/hr_payroll_account_views.xml',
        "wizard/hr_payroll_payslips_by_employees_wizard.xml",
    ],
}

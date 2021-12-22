# List of contributors:
# Segu S.U.R.L

{
    'name': 'Cuba - Nóminas con contabilidad',
    'category': 'Accounting/Accounting',    
    'description': """
Accounting Data for Cuba Payroll Rules.
==========================================
    """,
    'depends': ['hr_payroll_account_community', 'l10n_cu', 'l10n_cu_hr_payroll'],
    'author': 'Comunidad Cubana de Odoo',
    'data': [
        'data/hr_payroll_account_data.xml',
        'views/hr_payroll_account_views.xml',
    ],
}
